#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_geocodio
----------------------------------

Tests for `geocodio.data` module.
"""

import os
import json
import unittest
from geocodio.data import Address, Location, LocationCollection


class TestDataTypes(unittest.TestCase):

    def setUp(self):
        """
        Read the test data from JSON files which are modified from actual
        service response only for formatting. This makes this file much easier
        to read, the data easier to inspect, and ensures that the data matches
        what the service actually replies with.
        """
        fixtures = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'response/')
        with open(os.path.join(fixtures, 'single.json'), 'r') as single_json:
            self.single_response = json.loads(single_json.read())
        with open(os.path.join(fixtures, 'batch.json'), 'r') as batch_json:
            self.batch_response = json.loads(batch_json.read())
        with open(os.path.join(fixtures, 'address.json'), 'r') as address_json:
            self.address_response = json.loads(address_json.read())

    def test_address_coords(self):
        """Ensure Address.coords property returns None when no location"""
        x = Address(self.address_response)
        self.assertEqual(None, x.coords)

    def test_address_accuracy(self):
        """Ensure Address.accuracy property returns None when no location"""
        x = Address(self.address_response)
        self.assertEqual(None, x.accuracy)

    def test_location_coords(self):
        """Ensure Location.coords property returns a GIS suitable tuple"""
        x = Location(self.single_response)
        self.assertEqual(x.coords, (-77.457561054054, 37.554895702703))

    def test_collection(self):
        """Ensure that the LocationCollection stores as a list of Locations"""
        self.assertTrue(isinstance(self.batch_response, dict))
        locations = LocationCollection(self.batch_response)
        self.assertTrue(isinstance(locations[0], Location))

    def test_collection_coords(self):
        """Ensure the coords property returns a list of GIS suitable tuples"""
        locations = LocationCollection(self.batch_response)
        self.assertEqual(locations.coords, [(-77.477400571429, 37.560890255102),
                (-77.457561054054, 37.554895702703), None])

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
