"""
test_geocodio
----------------------------------

Tests for `geocodio.data` module.
"""

import json
import os
import unittest

from geocodio.data import (
    Address,
    LocationCollectionUtils,
    Location,
    LocationCollection,
    LocationCollectionDict,
)


class TestLocationCollectionUtils(unittest.TestCase):
    def test_extract_coords_key(self):
        self.assertEqual(
            LocationCollectionUtils.extract_coords_key((-5.0, 5.0)), "-5.0,5.0"
        )

        self.assertEqual(
            LocationCollectionUtils.extract_coords_key(("-5.0", "5.0")), "-5.0,5.0"
        )

        self.assertRaises(
            ValueError, LocationCollectionUtils.extract_coords_key, (5.0,)
        )

        self.assertRaises(
            ValueError, LocationCollectionUtils.extract_coords_key, ("abc", "5.0")
        )

    def test_get_lookup_key(self):
        self.assertEqual(
            LocationCollectionUtils.get_lookup_key((-5.0, 5.0)), "-5.0,5.0"
        )

        self.assertEqual(
            LocationCollectionUtils.get_lookup_key(("-5.0", "5.0")), "-5.0,5.0"
        )

        self.assertEqual(
            LocationCollectionUtils.get_lookup_key({"1": "2"}), '{"1": "2"}'
        )

        self.assertEqual(LocationCollectionUtils.get_lookup_key(None), None)

        self.assertEqual(LocationCollectionUtils.get_lookup_key("stuff"), "stuff")

        self.assertEqual(LocationCollectionUtils.get_lookup_key(5), 5)


class TestDataTypes(unittest.TestCase):
    def setUp(self):
        """
        Read the test data from JSON files which are modified from actual
        service response only for formatting. This makes this file much easier
        to read, the data easier to inspect, and ensures that the data matches
        what the service actually replies with.
        """
        fixtures = os.path.join(os.path.dirname(os.path.abspath(__file__)), "response/")
        with open(os.path.join(fixtures, "single.json"), "r") as single_json:
            self.single_response = json.loads(single_json.read())
        with open(os.path.join(fixtures, "batch.json"), "r") as batch_json:
            self.batch_response = json.loads(batch_json.read())
        with open(os.path.join(fixtures, "batch_dict.json"), "r") as batch_dict_json:
            self.batch_dict_response = json.loads(batch_dict_json.read())
        with open(
            os.path.join(fixtures, "batch_components.json"), "r"
        ) as batch_components_json:
            self.batch_components_response = json.loads(batch_components_json.read())
        with open(
            os.path.join(fixtures, "batch_dict_components.json"), "r"
        ) as batch_dict_components_json:
            self.batch_dict_components_response = json.loads(
                batch_dict_components_json.read()
            )
        with open(os.path.join(fixtures, "address.json"), "r") as address_json:
            self.address_response = json.loads(address_json.read())
        with open(os.path.join(fixtures, "missing_results.json"), "r") as missing_json:
            self.missing_results = json.loads(missing_json.read())
        with open(
            os.path.join(fixtures, "batch_reverse.json"), "r"
        ) as batch_reverse_json:
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
        x = Location(self.single_response, order="lng")
        self.assertEqual(x.coords, (-77.457561054054, 37.554895702703))

    def test_location_results_missing(self):
        """Ensure empty results are processed as a missing address"""
        bad_results = Location(self.missing_results)
        self.assertEqual(bad_results.coords, None)

    def test_collection(self):
        """Ensure that the LocationCollection stores as a list of Locations"""
        self.assertTrue(isinstance(self.batch_response, dict))
        locations = LocationCollection(self.batch_response["results"])

        self.assertTrue(isinstance(locations[0], Location))

        locations = LocationCollection(self.batch_reverse_response["results"])
        self.assertTrue(isinstance(locations[0], Location))

    def test_collection_coords(self):
        """Ensure the coords property returns a list of suitable tuples"""
        locations = LocationCollection(self.batch_response["results"])
        self.assertEqual(
            locations.coords,
            [
                (37.560890255102, -77.477400571429),
                (37.554895702703, -77.457561054054),
                None,
            ],
        )

        # Do the same with the order changed
        locations = LocationCollection(self.batch_response["results"], order="lng")
        self.assertEqual(
            locations.coords,
            [
                (-77.477400571429, 37.560890255102),
                (-77.457561054054, 37.554895702703),
                None,
            ],
        )

    def test_collection_addresses(self):
        """Ensure that formatted addresses are returned"""
        locations = LocationCollection(self.batch_response["results"])
        self.assertEqual(
            locations.formatted_addresses,
            [
                "3101 Patterson Ave, Richmond VA, 23221",
                "1657 W Broad St, Richmond VA, 23220",
                "",
            ],
        )

    def test_collection_get(self):
        """Ensure 'get' performs a key based lookup"""
        locations = LocationCollection(self.batch_response["results"])
        self.assertEqual(
            locations.get("3101 patterson ave, richmond, va").coords,
            (37.560890255102, -77.477400571429),
        )

        locations = LocationCollection(self.batch_components_response["results"])
        self.assertEqual(
            locations.get(
                {"street": "1109 N Highland St", "city": "Arlington", "state": "VA"}
            ).coords,
            (38.886672, -77.094735),
        )

        locations = LocationCollection(self.batch_reverse_response["results"])
        # The rendered query string value is acceptable
        self.assertEqual(
            locations.get("37.538758,-77.433594").coords, (37.538758, -77.433594)
        )
        # A tuple of floats is acceptable
        self.assertEqual(
            locations.get((37.538758, -77.433594)).coords, (37.538758, -77.433594)
        )
        # If it can be coerced to a float it is acceptable
        self.assertEqual(
            locations.get(("37.538758", "-77.433594")).coords, (37.538758, -77.433594)
        )

        # This is unacceptable
        self.assertRaises(ValueError, locations.get, ("37.538758 N", "-77.433594 W"))

    def test_collection_get_default(self):
        """Ensure 'get' returns default if key-based lookup fails without an error"""
        locations = LocationCollection(self.batch_response["results"])
        self.assertEqual(locations.get("wrong original query lookup"), None)

        locations = LocationCollection(self.batch_components_response["results"])
        self.assertEqual(
            locations.get(
                {"street": "wrong street", "city": "Arlington", "state": "VA"}, "test"
            ),
            "test",
        )

        locations = LocationCollection(self.batch_reverse_response["results"])

        self.assertEqual(locations.get((5, 5), None), None)
        # If it can be coerced to a float it is acceptable
        self.assertEqual(locations.get(("-4", "-5"), 5), 5)

        # This is still unacceptable
        self.assertRaises(ValueError, locations.get, ("37.538758 N", "-77.433594 W"))

    def test_collection_magic_get_item(self):
        """
        Ensure LocationCollection[key] performs a key based lookup for an index corresponding with key
        or performs an index lookup
        """
        locations = LocationCollection(self.batch_response["results"])
        # Works with normal list indexing
        self.assertEqual(locations[1].coords, (37.554895702703, -77.457561054054))
        self.assertRaises(IndexError, locations.__getitem__, len(locations))

        self.assertEqual(
            locations["3101 patterson ave, richmond, va"].coords,
            (37.560890255102, -77.477400571429),
        )

        # Case sensitive on the specific query
        self.assertRaises(
            IndexError, locations.__getitem__, "3101 Patterson Ave, richmond, va"
        )

        locations = LocationCollection(self.batch_components_response["results"])
        self.assertEqual(
            locations[
                {"street": "1109 N Highland St", "city": "Arlington", "state": "VA"}
            ].coords,
            (38.886672, -77.094735),
        )

        # Requires all fields used for lookup
        self.assertRaises(
            IndexError,
            locations.__getitem__,
            {"street": "1109 N Highland St", "city": "Arlington"},
        )

        locations = LocationCollection(self.batch_reverse_response["results"])
        # The rendered query string value is acceptable
        self.assertEqual(
            locations["37.538758,-77.433594"].coords, (37.538758, -77.433594)
        )
        # A tuple of floats is acceptable
        self.assertEqual(
            locations[(37.538758, -77.433594)].coords, (37.538758, -77.433594)
        )
        # If it can be coerced to a float it is acceptable
        self.assertEqual(
            locations[("37.538758", "-77.433594")].coords, (37.538758, -77.433594)
        )

        # This is unacceptable
        self.assertRaises(
            ValueError, locations.__getitem__, ("37.538758 N", "-77.433594 W")
        )

    def test_dict_collection(self):
        """Ensure that the LocationCollectionDict stores as a dict of Locations"""
        self.assertTrue(isinstance(self.batch_dict_response, dict))
        locations = LocationCollectionDict(self.batch_dict_response["results"])

        self.assertTrue(isinstance(locations["1"], Location))

    def test_dict_collection_coords(self):
        """Ensure the coords property returns a list of suitable tuples"""
        locations = LocationCollectionDict(self.batch_dict_response["results"])
        self.assertEqual(
            locations.coords,
            {
                "1": (37.560890255102, -77.477400571429),
                "2": (37.554895702703, -77.457561054054),
                "3": None,
            },
        )

        # Do the same with the order changed
        locations = LocationCollectionDict(
            self.batch_dict_response["results"], order="lng"
        )
        self.assertEqual(
            locations.coords,
            {
                "1": (-77.477400571429, 37.560890255102),
                "2": (-77.457561054054, 37.554895702703),
                "3": None,
            },
        )

    def test_dict_collection_addresses(self):
        """Ensure that formatted addresses are returned"""
        locations = LocationCollectionDict(self.batch_dict_response["results"])
        self.assertEqual(
            locations.formatted_addresses,
            {
                "1": "3101 Patterson Ave, Richmond VA, 23221",
                "2": "1657 W Broad St, Richmond VA, 23220",
                "3": "",
            },
        )

    def test_dict_collection_get(self):
        """Ensure 'get' performs a key based lookup"""
        locations = LocationCollectionDict(self.batch_dict_response["results"])
        self.assertEqual(
            locations.get("3101 patterson ave, richmond, va").coords,
            (37.560890255102, -77.477400571429),
        )

        # Ensure 'get' is able to look up by dictionary key
        self.assertEqual(
            locations.get("1").coords,
            (37.560890255102, -77.477400571429),
        )

        locations = LocationCollectionDict(
            self.batch_dict_components_response["results"]
        )
        self.assertEqual(
            locations.get(
                {"street": "1109 N Highland St", "city": "Arlington", "state": "VA"}
            ).coords,
            (38.886672, -77.094735),
        )

    def test_dict_collection_get_default(self):
        """Ensure 'get' returns default if key-based lookup fails without an error"""
        locations = LocationCollectionDict(self.batch_dict_response["results"])
        self.assertEqual(locations.get("wrong original query lookup"), None)

        self.assertEqual(locations.get("25"), None)

        locations = LocationCollectionDict(
            self.batch_dict_components_response["results"]
        )
        self.assertEqual(
            locations.get(
                {"street": "wrong street", "city": "Arlington", "state": "VA"}, "test"
            ),
            "test",
        )

    def test_dict_collection_magic_get_item(self):
        """Ensure LocationCollectionDict[key] performs a key-based lookup, raising a KeyError on any missing key"""
        locations = LocationCollectionDict(self.batch_dict_response["results"])
        self.assertEqual(
            locations["3101 patterson ave, richmond, va"].coords,
            (37.560890255102, -77.477400571429),
        )

        # Ensure 'get' is able to look up by dictionary key
        self.assertEqual(
            locations["1"].coords,
            (37.560890255102, -77.477400571429),
        )

        # Case sensitive on the specific query
        self.assertRaises(
            KeyError, locations.__getitem__, "3101 Patterson Ave, richmond, va"
        )

        locations = LocationCollectionDict(
            self.batch_dict_components_response["results"]
        )
        self.assertEqual(
            locations[
                {"street": "1109 N Highland St", "city": "Arlington", "state": "VA"}
            ].coords,
            (38.886672, -77.094735),
        )

        # Requires all fields used for lookup
        self.assertRaises(
            KeyError,
            locations.__getitem__,
            {"street": "1109 N Highland St", "city": "Arlington"},
        )

    def test_dict_collection_magic_contains(self):
        """Ensure "key in LocationDict(...)" checks if key would return a result with LocationDict(...)[key]"""
        locations = LocationCollectionDict(self.batch_dict_response["results"])
        self.assertTrue("3101 patterson ave, richmond, va" in locations)

        # Ensure it also works with look up by dictionary key
        self.assertTrue("1" in locations)

        # Case sensitive on the specific query
        self.assertFalse("3101 Patterson Ave, richmond, va" in locations)

        locations = LocationCollectionDict(
            self.batch_dict_components_response["results"]
        )
        self.assertTrue(
            {"street": "1109 N Highland St", "city": "Arlington", "state": "VA"}
            in locations
        )

        # Requires all fields used for lookup
        self.assertFalse(
            {"street": "1109 N Highland St", "city": "Arlington"} in locations
        )
