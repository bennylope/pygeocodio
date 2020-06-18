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
            return self["location"][x], self["location"][y]
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
        super().__init__(result_dict)
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


class LocationCollectionUtils:
    @classmethod
    def extract_coords_key(cls, item):
        try:
            coord1, coord2 = float(item[0]), float(item[1])
        except IndexError:
            raise ValueError("Two values are required for a coordinate pair")
        except ValueError:
            raise ValueError("Only float or float-coercable values can be passed")

        return "{0},{1}".format(coord1, coord2)

    @classmethod
    def get_lookup_key(cls, item):
        if isinstance(item, tuple):
            key = cls.extract_coords_key(item)
        elif isinstance(item, dict):
            key = json.dumps(item)
        else:
            key = item
        return key


class LocationCollection(list):
    """
    A list of Location objects, with dictionary lookup by address.
    """

    def __init__(self, results_list, order="lat"):
        """
        Loads the individual responses into an internal list and uses the query
        values as lookup keys.
        """
        results = []
        lookups = {}
        for index, result in enumerate(results_list):
            results.append(Location(result["response"], order=order))
            orig_query = result["query"]
            lookup_key = json.dumps(orig_query) if isinstance(orig_query, dict) else orig_query
            lookups[lookup_key] = index

        super().__init__(results)
        self.order = order
        self.lookups = lookups

    def __getitem__(self, item):
        if isinstance(item, int):
            ind = item
        else:
            key = LocationCollectionUtils.get_lookup_key(item)
            try:
                ind = self.lookups[key]
            except KeyError as e:
                raise IndexError("Invalid Index From Lookup For Location Collection") from e
        return super().__getitem__(ind)

    def get(self, key, default=None):
        """
        Returns an individual Location by query lookup, e.g. address, components dict, or point.
        """
        key = LocationCollectionUtils.get_lookup_key(key)
        try:
            return self[self.lookups[key]]
        except KeyError:
            return default

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
        return [item.formatted_address for item in self]


class LocationCollectionDict(dict):
    """
    A dict of Location objects, with dictionary lookup by address.
    """

    def __init__(self, results_list, order="lat"):
        """
        Loads the individual responses into an internal list and uses the query
        values as lookup keys.
        """
        results = {}
        lookups = {}
        for key, result in results_list.items():
            results[key] = Location(result["response"], order=order)
            orig_query = result["query"]
            lookup_key = json.dumps(orig_query) if isinstance(orig_query, dict) else orig_query
            lookups[lookup_key] = key

        super().__init__(results)
        self.order = order
        self.lookups = lookups

    def __contains__(self, value):
        key = LocationCollectionUtils.get_lookup_key(value)
        return super().__contains__(key) or (key in self.lookups and super().__contains__(self.lookups[key]))

    def __getitem__(self, item):
        key = LocationCollectionUtils.get_lookup_key(item)
        if key in self.lookups:
            key = self.lookups[key]
        return super().__getitem__(key)

    def get(self, key, default=None):
        """
        Returns an individual Location by query lookup, e.g. address, components dict, or point.
        """
        key = LocationCollectionUtils.get_lookup_key(key)
        if key in self.lookups:
            key = self.lookups[key]
        return super().get(key, default)

    @property
    def coords(self):
        """
        Returns a dict of tuples for the best matched coordinates.
        """
        return {k: l.coords for k, l in self.items()}

    @property
    def formatted_addresses(self):
        """
        Returns a dict of formatted addresses from the Location list
        """
        return {k: l.formatted_address for k, l in self.items()}
