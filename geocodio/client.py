#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import logging
import requests
from .data import Address, Location, LocationCollection
from .exceptions import (GeocodioAuthError, GeocodioDataError,
        GeocodioServerError, GeocodioError)


logger = logging.getLogger(__name__)

ALLOWED_FIELDS = ['cd', 'cd13', 'stateleg', 'school', 'timezone']


def protect_fields(f):
    def wrapper(*args, **kwargs):
        fields = kwargs.get('fields', [])
        for field in fields:
            if field not in ALLOWED_FIELDS:
                raise ValueError("'{0}' is not a valid field value".format(field))
        return f(*args, **kwargs)
    return wrapper


def error_response(response):
    """
    Raises errors matching the response code
    """
    if response.status_code >= 500:
        raise GeocodioServerError
    elif response.status_code == 403:
        raise GeocodioAuthError
    elif response.status_code == 422:
        raise GeocodioDataError(response.json()['error'])
    else:
        raise GeocodioError("Unknown service error (HTTP {0})".format(response.status_code))


def json_points(points):
    """
    Returns a list of points [(lat, lng)...] as a JSON formatted list of
    strings.

    >>> json_points([(1,2), (3,4)])
    '["1,2", "3,4"]'
    """
    return json.dumps(["{0},{1}".format(point[0], point[1]) for point in points])


class GeocodioClient(object):
    """
    Client connection for Geocod.io API
    """
    BASE_URL = "http://api.geocod.io/v1/{verb}"

    def __init__(self, key, order='lat'):
        """
        """
        self.API_KEY = key
        if order not in ('lat', 'lng'):
            raise ValueError("Order but be either `lat` or `lng`")
        self.order = order

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
        url = self.BASE_URL.format(verb="parse")
        response = requests.get(url, params={'q': address, 'api_key': self.API_KEY})
        if response.status_code != 200:
            return error_response(response)
        return Address(response.json())

    @protect_fields
    def batch_geocode(self, addresses, **kwargs):
        """
        Returns an Address dictionary with the components of the queried
        address.
        """
        fields = kwargs.pop('fields', [])
        url = self.BASE_URL.format(verb="geocode")

        response = requests.post(url, params={'api_key': self.API_KEY,
            'fields': fields},
                headers={'content-type': 'application/json'},
                data=json.dumps(addresses))
        if response.status_code != 200:
            return error_response(response)
        return LocationCollection(response.json()['results'])

    @protect_fields
    def geocode_address(self, address, **kwargs):
        """
        Returns a Location dictionary with the components of the queried
        address and the geocoded location.

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
        fields = kwargs.pop('fields', [])
        url = self.BASE_URL.format(verb="geocode")
        response = requests.get(url, params={'q': address, 'api_key':
            self.API_KEY, 'fields': fields})
        if response.status_code != 200:
            return error_response(response)
        return Location(response.json())

    @protect_fields
    def geocode(self, address_data, **kwargs):
        """
        Returns geocoding data for either a list of addresses or a single
        address represented as a string.

        Provides a single point of access for end users.
        """
        fields = kwargs.pop('fields', [])
        if isinstance(address_data, list):
            return self.batch_geocode(address_data, fields=fields)
        return self.geocode_address(address_data, fields=fields)

    @protect_fields
    def reverse_point(self, latitude, longitude, **kwargs):
        """
        Method for identifying an address from a geographic point
        """
        fields = kwargs.pop('fields', [])
        url = self.BASE_URL.format(verb="reverse")
        point_param = "{0},{1}".format(latitude, longitude)
        response = requests.get(url, params={'q': point_param,
            'api_key': self.API_KEY, 'fields': fields})
        if response.status_code != 200:
            return error_response(response)
        return Location(response.json())

    @protect_fields
    def batch_reverse(self, points, **kwargs):
        """
        Method for identifying the addresses from a list of lat/lng tuples
        """
        fields = kwargs.pop('fields', [])
        url = self.BASE_URL.format(verb="reverse")
        response = requests.post(url, params={'api_key': self.API_KEY, 'fields': fields},
                headers={'content-type': 'application/json'},
                data=json_points(points))
        if response.status_code != 200:
            return error_response(response)
        logger.debug(response)
        return LocationCollection(response.json()['results'])

    @protect_fields
    def reverse(self, points, **kwargs):
        """
        General method for reversing addresses, either a single address or
        multiple.

        *args should either be a longitude/latitude pair or a list of
        such pairs::

        >>> multiple_locations = reverse([(40, -19), (43, 112)])
        >>> single_location = reverse((40, -19))

        """
        if isinstance(points, list):
            return self.batch_reverse(points, **kwargs)
        if self.order == 'lat':
            x, y = points
        else:
            y, x = points
        return self.reverse_point(x, y, **kwargs)
