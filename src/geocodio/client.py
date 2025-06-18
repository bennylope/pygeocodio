import json
import logging
import re

import requests

from geocodio.data import Address, Location, LocationCollection, LocationCollectionDict
from geocodio import exceptions

logger = logging.getLogger(__name__)

DEFAULT_API_VERSION = "1.9"


def error_response(response):
    """
    Raises errors matching the response code
    """
    if response.status_code >= 500:
        raise exceptions.GeocodioServerError

    elif response.status_code == 403:
        raise exceptions.GeocodioAuthError

    elif response.status_code == 422:
        raise exceptions.GeocodioDataError(response.json()["error"])

    else:
        raise exceptions.GeocodioError(
            "Unknown service error (HTTP {0})".format(response.status_code)
        )


def json_points(points):
    """
    Returns a list of points [(lat, lng)...] / dict of points {key: (lat, lng), ...} as a JSON formatted list/dict of
    strings.

    >>> json_points([(1,2), (3,4)])
    '["1,2", "3,4"]'
    >>> json_points({"a": (1, 2), "b": (3, 4)})
    '{"a": "1,2", "b": "3,4"}'
    """

    def to_point_str(point):
        return "{0},{1}".format(point[0], point[1])

    if isinstance(points, list):
        point_strs = [to_point_str(point) for point in points]
    elif isinstance(points, dict):
        point_strs = {k: to_point_str(point) for k, point in points.items()}
    else:
        return None
    return json.dumps(point_strs)


class GeocodioClient(object):
    """
    Client connection for Geocod.io API
    """

    def __init__(
        self,
        key,
        order="lat",
        version=None,
        hipaa_enabled=False,
        auto_load_api_version=False,
        timeout=None,
        custom_base_domain=None,
    ):
        """Initialize and configure the client.

        Args:
            key: Geocodio API key
            order: one of `lat` or `lng` to determine the ordering
                    of latitude and longitude. The default is `lat`
                    (lat, lng); using `lng` (lng, lat) uses a PostGIS
                    compatible ordering
            version: the Geocodio API version
            hipaa_enabled: whether to use HIPAA API (if you don't know,
                    then you don't need it!)
            auto_load_api_version: whether to automatically select the
                    latest API version from the Geocodio API. This *may*
                    result in errors, i.e. during a new API version
                    rollout.
            timeout: request timeout
            custom_base_domain: custom API domain

        """
        if custom_base_domain is None:
            self.hipaa_enabled = hipaa_enabled
            self.BASE_DOMAIN = "https://api{hipaa_append}.geocod.io".format(
                hipaa_append=("-hipaa" if self.hipaa_enabled else "")
            )
        else:
            self.BASE_DOMAIN = custom_base_domain

        if version is None and auto_load_api_version:
            version = self._parse_curr_api_version(self.BASE_DOMAIN)
        # Fall back to manual default API version if couldn't be found or isn't overridden
        self.version = version or DEFAULT_API_VERSION

        self.BASE_URL = "{domain}/v{version}/{{verb}}".format(
            domain=self.BASE_DOMAIN, version=self.version
        )
        self.API_KEY = key
        if order not in ("lat", "lng"):
            raise ValueError("Order but be either `lat` or `lng`")
        self.order = order
        self.timeout = timeout

    @staticmethod
    def _parse_curr_api_version(api_url):
        try:
            resp = requests.get(api_url)
            result = resp.json()
            # Parses version from string: "... vX.Y.Z" -> "X.Y"
            match = re.search(r"(v\d+.\d+)", result["description"])
            return match and match.group()[1:]
        except Exception:
            return None

    def _req(self, method="get", verb=None, headers={}, params={}, data={}):
        """
        Method to wrap all request building

        :return: a Response object based on the specified method and request values.
        """
        url = self.BASE_URL.format(verb=verb)
        request_headers = {"content-type": "application/json"}
        request_params = {"api_key": self.API_KEY}
        request_headers.update(headers)
        request_params.update(params)
        return getattr(requests, method)(
            url,
            params=request_params,
            headers=request_headers,
            data=data,
            timeout=self.timeout,
        )

    def parse(self, address):
        """
        Returns an Address dictionary with the components of the queried
        address.

        >>> client = GeocodioClient('some_api_key')
        >>> client.parse("1600 Pennsylvania Ave, Washington DC")
        {
            "address_components": {
                "number": "1600",
                "street": "Pennsylvania",
                "suffix": "Ave",
                "city": "Washington",
                "state": "DC"
            },
            "formatted_address": "1600 Pennsylvania Ave, Washington DC"
        }
        """
        response = self._req(verb="parse", params={"q": address})
        if response.status_code != 200:
            return error_response(response)

        return Address(response.json())

    def batch_geocode(self, addresses, **kwargs):
        """
        Returns an Address dictionary with the components of the queried
        address. Accepts either a list or dictionary of addresses
        """
        fields = ",".join(kwargs.pop("fields", []))
        limit = kwargs.pop("limit", 0)
        response = self._req(
            "post",
            verb="geocode",
            params={"fields": fields, "limit": limit},
            data=json.dumps(addresses),
        )
        if response.status_code != 200:
            return error_response(response)

        results = response.json()["results"]
        if isinstance(results, list):
            return LocationCollection(results)
        elif isinstance(results, dict):
            return LocationCollectionDict(results)
        else:
            raise Exception("Error: Unknown API change")

    def geocode_address(self, address=None, components=None, **kwargs):
        """
        Returns a Location dictionary with the components of the queried
        address/components dictionary and the geocoded location.

        >>> client = GeocodioClient('some_api_key')
        >>> client.geocode("1600 Pennsylvania Ave, Washington DC")
        {
        "input": {
            "address_components": {
                "number": "1600",
                "street": "Pennsylvania",
                "suffix": "Ave",
                "city": "Washington",
                "state": "DC"
            },
            "formatted_address": "1600 Pennsylvania Ave, Washington DC"
        },
        "results": [
            {
                "address_components": {
                    "number": "1600",
                    "street": "Pennsylvania",
                    "suffix": "Ave",
                    "city": "Washington",
                    "state": "DC",
                    "zip": "20500"
                },
                "formatted_address": "1600 Pennsylvania Ave, Washington DC, 20500",
                "location": {
                    "lat": 38.897700000000,
                    "lng": -77.03650000000,
                },
                "accuracy": 1
            },
            {
                "address_components": {
                    "number": "1600",
                    "street": "Pennsylvania",
                    "suffix": "Ave",
                    "city": "Washington",
                    "state": "DC",
                    "zip": "20500"
                },
                "formatted_address": "1600 Pennsylvania Ave, Washington DC, 20500",
                "location": {
                    "lat": 38.897700000000,
                    "lng": -77.03650000000,
                },
                "accuracy": 0.8
                }
            ]
        }
        """
        fields = ",".join(kwargs.pop("fields", []))
        limit = kwargs.pop("limit", 0)
        params = {"fields": fields, "limit": limit}
        if address is not None:
            params["q"] = address
        else:
            params.update(components)
        response = self._req(verb="geocode", params=params)
        if response.status_code != 200:
            return error_response(response)

        return Location(response.json())

    def geocode(self, address_data=None, components_data=None, **kwargs):
        """
        Returns geocoding data for either a list of addresses/component dictionaries,
        a dictionary of addresses/component dictionaries with arbitrary keys,
        or a single address represented as a string/components dictionary.

        Provides a single point of access for end users.
        """
        if (address_data is not None) == (components_data is not None):
            return None

        use_components = components_data is not None and address_data is None
        param_data = components_data if use_components else address_data

        use_batch = (
            isinstance(param_data, list)
            or (not use_components and isinstance(param_data, dict))
            or (
                use_components
                and isinstance(param_data, dict)
                and all(isinstance(c, dict) for c in param_data.values())
            )
        )
        if use_batch:
            return self.batch_geocode(param_data, **kwargs)
        else:
            param_key = "components" if use_components else "address"
            kwargs.update({param_key: param_data})
            return self.geocode_address(**kwargs)

    def reverse_point(self, latitude, longitude, **kwargs):
        """
        Method for identifying an address from a geographic point
        """
        fields = ",".join(kwargs.pop("fields", []))
        point_param = "{0},{1}".format(latitude, longitude)
        response = self._req(
            verb="reverse", params={"q": point_param, "fields": fields}
        )
        if response.status_code != 200:
            return error_response(response)

        return Location(response.json())

    def batch_reverse(self, points, **kwargs):
        """
        Method for identifying the addresses from a list of lat/lng tuples
        or dict mapping of arbitrary keys to lat/lng tuples
        """
        fields = ",".join(kwargs.pop("fields", []))
        response = self._req(
            "post", verb="reverse", params={"fields": fields}, data=json_points(points)
        )
        if response.status_code != 200:
            return error_response(response)

        results = response.json()["results"]
        if isinstance(results, list):
            return LocationCollection(results)
        elif isinstance(results, dict):
            return LocationCollectionDict(results)
        else:
            raise Exception("Error: Unknown API change")

    def reverse(self, points, **kwargs):
        """
        General method for reversing addresses, either a single address or
        multiple.

        *args should either be a longitude/latitude pair, a list of
        such pairs, or dictionary (with arbitrary keys) with values of such pairs::

        >>> multiple_locations = reverse([(40, -19), (43, 112)])
        >>> keyed_multiple_locations = reverse({"a": (40, -19), "b": (43, 112)})
        >>> single_location = reverse((40, -19))

        """
        if isinstance(points, list) or isinstance(points, dict):
            return self.batch_reverse(points, **kwargs)

        if self.order == "lat":
            x, y = points
        else:
            y, x = points
        return self.reverse_point(x, y, **kwargs)
