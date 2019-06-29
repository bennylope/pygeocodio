.. index:: data, types, Address, Location, LocationCollection

==========
Data types
==========

The client returns values represented by lightly-extended Python dictionaries
and lists. They have been extended to provide easier access to frequently
requested or primary data elements, and to make accessing data simple.

By adding only a few methods and data lookup elements the source data is
largely left as-is for developers to use as they see fit.

For example, if the data for a geocoded address returned by Geocodio includes
`accuracy_type`, then you access that by referencing the key, `'accuracy_type'`.::

    >>> geocoded_location = client.geocode("42370 Bob Hope Drive, Rancho Mirage CA")
    >>> geocoded_location.accuracy
    1
    >>> geocoded_location.accuracy_type
    Traceback (most recent call last)
        File "<stdin>", line 1, in <module>
    AttributeError: 'Location' object has no attribute 'accuracy_type'.
    
The `geocoded_location` is a `Location` instance, a wrapper around a dictionary,
and in the results may be several identified locations ordered by accuracy.
The `accuracy` and `coords` attributes referenced from the `Location` instance,
`geocoded_location`, access the first element, which is itself referenced as `best_match`.
Additional values can be pulled from it by iterating over the `results` in the
dictionary or using the `best_match` attribute which returns the dictionary
for the first geocoded match:
    
    >>> geocoded_location.best_match['accuracy_type']
    "rooftop"

.. currentmodule:: geocodio.data

Address
=======

An `Address` object is just a dictionary object that provides two access methods for
returning the accuracy value of the geocoded address as an attribute and the
coordinates of the address as an attribute.

.. method:: Address.__init__(results_list, order='lat')

    `results_list` is the raw data

    `order` allows you to change the default order of the
    coordinate points. Setting order to 'lng' or any value other
    than 'lat' will return the points in `(longitude, latitude)`
    order.

.. method:: Address.coords

    A property method that returns the coordinates of the address or `None` if
    they are not available (in the case of a parsed address).

.. method:: Address.accuracy

    A property method that returns the accuracy rating of the geocoded address.

When parsing an address, the result is returned as an `Address` for
consistency, but the result's usefullness will be limited to the dictionary
structure.

Location
========

A `Location` object is a dictionary object that provides the same access
methods as an `Address` object. Because a geocoded Location may have more than
one address returned, the methods refer to the coordinates and accuracy
respectively of the most most accurate geocoded address.

.. method:: Location.__init__(results_dict, order='lat')

    `results_dict` is the raw data

    `order` allows you to change the default order of the
    coordinate points. Setting order to 'lng' or any value other
    than 'lat' will return the points in `(longitude, latitude)`
    order.

.. method:: Location.coords

    A property method that returns the coordinates of the best
    matched address or `None` if they are not available.

.. method:: Location.accuracy

    A property method that returns the accuracy rating of the best
    matched address.

LocationCollection
==================

A `LocationCollection` object is a list of `Location` objects. It maintains an
internal dictionary of each geocoding or reverse geocoding query with reference
to the list index of the result. This allows the order of the list to be
preserved but for simple lookup of the values without needing to iterate over
the entire list.

.. note::
    This demands an OrderedDict! Unfortunately OrderedDict was only introduced
    in Python 2.7, and Python 2.6 is a targeted supported version of Python for
    this project. So, boo.

.. method:: LocationCollection.get(key)

    A method that returns a `Location` object from the list of locations by
    checking against the query input.

    The key can be the queried address as a string (geocoding) or the queried
    point (reverse geocoding) or a dictionary of queried address components.
    The point can be provided as a tuple of floats::

        (33.12, -78.123)

    a tuple of float-coerceable values (e.g. a float as a string)::

        ("33.12", "-78.123")

    or a string representing the query::

        "33.12, -78.123"

    This method is provided instead of overriding the `__getitem__` method as
    the latter allows index based access to the list.

.. method:: LocationCollection.coords

    A property method that returns a list of all of the coordinates
