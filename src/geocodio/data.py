#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json


class Address(dict):
    """
    Dictionary class that provides some convenience wrappers for accessing
    commonly used data elements on an Address.
    """

    def __init__(self, address_dict, order="lat"):
        super(Address, self).__init__(address_dict)
        self.order = order

    @property
    def coords(self):
        """
        Returns a tuple representing the location of the address in a
        GIS coords format, i.e. (longitude, latitude).
        """
        x, y = ("lat", "lng") if self.order == "lat" else ("lng", "lat")
        try:
            return (self["location"][x], self["location"][y])

        except KeyError:
            return None

    @property
    def accuracy(self):
        """
        Returns the accuracy integer or None of the geocoded address.
        """
        try:
            return self["accuracy"]

        except KeyError:
            return None

    @property
    def formatted_address(self):
        """
        Returns a list of formatted addresses from the Location list
        """
        return self.get("formatted_address", "")


class Location(dict):
    """
    Dictionary class that provides some convenience accessors to commonly used
    data elements.
    """

    def __init__(self, result_dict, order="lat"):
        super(Location, self).__init__(result_dict)
        try:
            self.best_match = Address(self["results"][0], order=order)
        # A KeyError would be raised if an address could not be parsed or
        # geocoded, i.e. from a batch address geocoding process. An index error
        # would be raised under similar circumstances, e.g. the 'results' key
        # just refers to an empty list.
        except (KeyError, IndexError):
            self.best_match = Address({})
        self.order = order

    @property
    def coords(self):
        """
        Returns a tuple representing the location of the first result in a
        GIS coords format, i.e. (longitude, latitude).
        """
        return self.best_match.coords

    @property
    def accuracy(self):
        """
        Returns the accuracy integer or None of the geocoded address.
        """
        return self.best_match.accuracy

    @property
    def formatted_address(self):
        """
        Returns a list of formatted addresses from the Location list
        """
        return self.best_match.formatted_address


class LocationCollection(list):
    """
    A list of Location objects, with dictionary lookup by address.
    """

    lookups = {}

    def __init__(self, results_list, order="lat"):
        """
        Loads the individual responses into an internal list and uses the query
        values as lookup keys.
        """
        results = []
        for index, result in enumerate(results_list):
            results.append(Location(result["response"], order=order))
            orig_query = result["query"]
            lookup_key = json.dumps(orig_query) if isinstance(orig_query, dict) else orig_query
            self.lookups[lookup_key] = index

        super(LocationCollection, self).__init__(results)
        self.order = order

    def get(self, key):
        """
        Returns an individual Location by query lookup, e.g. address, components dict, or point.
        """

        if isinstance(key, tuple):
            # TODO handle different ordering
            try:
                x, y = float(key[0]), float(key[1])
            except IndexError:
                raise ValueError("Two values are required for a coordinate pair")

            except ValueError:
                raise ValueError("Only float or float-coercable values can be passed")

            key = "{0},{1}".format(x, y)
        elif isinstance(key, dict):
            key = json.dumps(key)

        return self[self.lookups[key]]

    @property
    def coords(self):
        """
        Returns a list of tuples for the best matched coordinates.
        """
        return [item.coords for item in self]

    @property
    def formatted_addresses(self):
        """
        Returns a list of formatted addresses from the Location list
        """
        return [l.formatted_address for l in self]


class LocationCollectionDict(dict):
    """
    A dict of Location objects, with dictionary lookup by address.
    """

    lookups = {}

    def __init__(self, results_list, order="lat"):
        """
        Loads the individual responses into an internal list and uses the query
        values as lookup keys.
        """
        results = {}
        for key, result in results_list.items():
            results[key]=Location(result["response"], order=order)
            orig_query = result["query"]
            lookup_key = json.dumps(orig_query) if isinstance(orig_query, dict) else orig_query
            self.lookups[lookup_key] = key

        super(LocationCollectionDict, self).__init__(results)
        self.order = order

    def get(self, key):
        """
        Returns an individual Location by query lookup, e.g. address, components dict, or point.
        """

        if isinstance(key, tuple):
            # TODO handle different ordering
            try:
                x, y = float(key[0]), float(key[1])
            except IndexError:
                raise ValueError("Two values are required for a coordinate pair")

            except ValueError:
                raise ValueError("Only float or float-coercable values can be passed")

            key = "{0},{1}".format(x, y)
        elif isinstance(key, dict):
            key = json.dumps(key)

        return self[self.lookups[key]]

    @property
    def coords(self):
        """
        Returns a dict of tuples for the best matched coordinates.
        """
        return {k:l.coords for k,l in self.items()}

    @property
    def formatted_addresses(self):
        """
        Returns a dict of formatted addresses from the Location list
        """
        return {k:l.formatted_address for k,l in self.items()}
