#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import requests
from data import Address, Location, LocationCollection
from exceptions import UnprocessableError


class GeocodioClient(object):
    """
    Client connection for Geocod.io API
    """
    BASE_URL = "http://api.geocod.io/v1/{verb}"

    def __init__(self, key):
        self.API_KEY = key

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
        return Address(response.json())

    def batch_geocode(self, addresses):
        """
        Returns an Address dictionary with the components of the queried
        address.
        """
        url = self.BASE_URL.format(verb="geocode")

        response = requests.post(url, params={'api_key': self.API_KEY},
                headers={'content-type': 'application/json'},
                data=json.dumps(addresses))
        if response.status_code == 422:
            raise UnprocessableError(response.json()['error'])
        return LocationCollection(response.json())

    def geocode_address(self, address):
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
        url = self.BASE_URL.format(verb="geocode")
        response = requests.get(url, params={'q': address, 'api_key': self.API_KEY})
        return Location(response.json())

    def geocode(self, address_data):
        """
        Returns geocoding data for either a list of addresses or a single
        address represented as a string.

        Provides a single point of access for end users.
        """
        if isinstance(address_data, list):
            return self.batch_geocode(address_data)
        return self.geocode_address(address_data)
