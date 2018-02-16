#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_geocodio
----------------------------------

Tests for `geocodio.data` module.
"""

import json
import os
import unittest

from geocodio.data import Address
from geocodio.data import Location
from geocodio.data import LocationCollection


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
        with open(os.path.join(fixtures, 'missing_results.json'), 'r') as missing_json:
            self.missing_results = json.loads(missing_json.read())
        with open(os.path.join(fixtures, 'batch_reverse.json'), 'r') as batch_reverse_json:
            self.batch_reverse_response = json.loads(batch_reverse_json.read())

    def test_address_coords(self):
        """Ensure Address.coords property returns None when no location"""
        x = Address(self.address_response)
        self.assertEqual(None, x.coords)

    def test_address_accuracy(self):
        """Ensure Address.accuracy property returns None when no location"""
        x = Address(self.address_response)
        self.assertEqual(None, x.accuracy)

    def test_location_coords(self):
        """Ensure Location.coords property returns a suitable tuple"""
        x = Location(self.single_response)
        self.assertEqual(x.coords, (37.554895702703, -77.457561054054))

        # Do the same with the order changed
        x = Location(self.single_response, order='lng')
        self.assertEqual(x.coords, (-77.457561054054, 37.554895702703))

    def test_location_results_missing(self):
        """Ensure empty results are processed as a missing address"""
        bad_results = Location(self.missing_results)
        self.assertEqual(bad_results.coords, None)

    def test_collection(self):
        """Ensure that the LocationCollection stores as a list of Locations"""
        self.assertTrue(isinstance(self.batch_response, dict))
        locations = LocationCollection(self.batch_response['results'])

        self.assertTrue(isinstance(locations[0], Location))

        locations = LocationCollection(self.batch_reverse_response['results'])
        self.assertTrue(isinstance(locations[0], Location))

    def test_collection_coords(self):
        """Ensure the coords property returns a list of suitable tuples"""
        locations = LocationCollection(self.batch_response['results'])
        self.assertEqual(locations.coords, [
                (37.560890255102, -77.477400571429),
                (37.554895702703, -77.457561054054),
                None,
        ])

        # Do the same with the order changed
        locations = LocationCollection(self.batch_response['results'], order='lng')
        self.assertEqual(locations.coords, [
                (-77.477400571429, 37.560890255102),
                (-77.457561054054, 37.554895702703),
                None,
        ])

    def test_collection_addresses(self):
        """Ensure that formatted addresses are returned"""
        locations = LocationCollection(self.batch_response['results'])
        self.assertEqual(locations.formatted_addresses, [
            "3101 Patterson Ave, Richmond VA, 23221",
            "1657 W Broad St, Richmond VA, 23220",
            ""
        ])

    def test_collection_get(self):
        """Ensure 'get' performs a key based lookup"""
        locations = LocationCollection(self.batch_response['results'])
        self.assertEqual(locations.get("3101 patterson ave, richmond, va").coords,
                (37.560890255102, -77.477400571429))

        # Case sensitive on the specific query
        self.assertRaises(KeyError, locations.get,
                "3101 Patterson Ave, richmond, va")

        locations = LocationCollection(self.batch_reverse_response['results'])

        # The rendred query string value is acceptable
        self.assertEqual(locations.get("37.538758,-77.433594").coords,
                (37.538758, -77.433594))
        # A tuple of floats is acceptable
        self.assertEqual(locations.get((37.538758, -77.433594)).coords,
                (37.538758, -77.433594))
        # If it can be coerced to a float it is acceptable
        self.assertEqual(locations.get(("37.538758", "-77.433594")).coords,
                (37.538758, -77.433594))

        # This is unacceptable
        self.assertRaises(ValueError, locations.get, ("37.538758 N", "-77.433594 W"))


if __name__ == '__main__':
    unittest.main()
