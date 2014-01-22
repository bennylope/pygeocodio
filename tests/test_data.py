#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_geocodio
----------------------------------

Tests for `geocodio.data` module.
"""

import unittest
from geocodio.data import Location, LocationCollection


class TestDataTypes(unittest.TestCase):

    def setUp(self):
        self.result_dict = {
            "input": {
                "address_components": {
                    "number": "42370",
                    "street": "Bob Hope",
                    "suffix": "Dr",
                    "city": "Rancho Mirage",
                    "state": "CA"
                },
                "formatted_address": "42370 Bob Hope Dr, Rancho Mirage CA"
            },
            "results": [
                {
                    "address_components": {
                        "number": "42370",
                        "street": "Bob Hope",
                        "suffix": "Dr",
                        "city": "Rancho Mirage",
                        "state": "CA",
                        "zip": "92270"
                    },
                    "formatted_address": "42370 Bob Hope Dr, Rancho Mirage CA, 92270",
                    "location": {
                        "lat": 33.738987255507,
                        "lng": -116.40833849559
                    },
                    "accuracy": 1
                },
                {
                    "address_components": {
                        "number": "42370",
                        "street": "Bob Hope",
                        "suffix": "Dr",
                        "city": "Rancho Mirage",
                        "state": "CA",
                        "zip": "92270"
                    },
                    "formatted_address": "42370 Bob Hope Dr, Rancho Mirage CA, 92270",
                    "location": {
                        "lat": 33.738980796909,
                        "lng": -116.40833917329
                    },
                    "accuracy": 0.8
                }
            ]
        }
        self.batch_response = {
            "results": [
                {
                    "query": "3101 patterson ave, richmond, va",
                    "response": {
                        "input": {
                            "address_components": {
                                "city": "Richmond",
                                "number": "3101",
                                "state": "VA",
                                "street": "Patterson",
                                "suffix": "Ave"
                            },
                            "formatted_address": "3101 Patterson Ave, Richmond VA"
                        },
                        "results": [
                            {
                                "accuracy": 0.8,
                                "address_components": {
                                    "city": "Richmond",
                                    "number": "3101",
                                    "state": "VA",
                                    "street": "Patterson",
                                    "suffix": "Ave",
                                    "zip": "23221"
                                },
                                "formatted_address": "3101 Patterson Ave, Richmond VA, 23221",
                                "location": {
                                    "lat": 37.560890255102,
                                    "lng": -77.477400571429
                                }
                            }
                        ]
                    }
                },
                {
                    "query": "1657 W Broad St, Richmond, VA",
                    "response": {
                        "input": {
                            "address_components": {
                                "city": "Richmond",
                                "number": "1657",
                                "predirectional": "W",
                                "state": "VA",
                                "street": "Broad",
                                "suffix": "St"
                            },
                            "formatted_address": "1657 W Broad St, Richmond VA"
                        },
                        "results": [
                            {
                                "accuracy": 1,
                                "address_components": {
                                    "city": "Richmond",
                                    "number": "1657",
                                    "predirectional": "W",
                                    "state": "VA",
                                    "street": "Broad",
                                    "suffix": "St",
                                    "zip": "23220"
                                },
                                "formatted_address": "1657 W Broad St, Richmond VA, 23220",
                                "location": {
                                    "lat": 37.554895702703,
                                    "lng": -77.457561054054
                                }
                            },
                            {
                                "accuracy": 0.8,
                                "address_components": {
                                    "city": "Richmond",
                                    "number": "1657",
                                    "predirectional": "W",
                                    "state": "VA",
                                    "street": "Broad",
                                    "suffix": "St",
                                    "zip": "23220"
                                },
                                "formatted_address": "1657 W Broad St, Richmond VA, 23220",
                                "location": {
                                    "lat": 37.554919546875,
                                    "lng": -77.45760096875
                                }
                            }
                        ]
                    }
                }
            ]
        }

    def test_coords(self):
        """Ensure the coords property returns a GIS suitable tuple"""
        x = Location(self.result_dict)
        self.assertEqual(x.coords, (-116.40833849559, 33.738987255507))

    def test_collection(self):
        """Ensure that the LocationCollection stores as a list of Locations"""
        self.assertTrue(isinstance(self.batch_response, dict))
        locations = LocationCollection(self.batch_response)
        self.assertTrue(isinstance(locations[0], Location))

    def test_collection_coords(self):
        """Ensure the coords property returns a list of GIS suitable tuples"""
        locations = LocationCollection(self.batch_response)
        self.assertEqual(locations.coords,
                [(-77.477400571429, 37.560890255102), (-77.457561054054, 37.554895702703)])

    def test_collection_get(self):
        """Ensure 'get' performs a key based lookup"""
        locations = LocationCollection(self.batch_response)
        self.assertEqual(locations.get("3101 patterson ave, richmond, va").coords,
                (-77.477400571429, 37.560890255102))
        # Case sensitive on the specific query
        self.assertRaises(KeyError, locations.get,
                "3101 Patterson Ave, richmond, va")


if __name__ == '__main__':
    unittest.main()
