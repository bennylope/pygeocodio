============
Py-Geocod.io
============

.. image:: https://badge.fury.io/py/pygeocodio.png
    :target: http://badge.fury.io/py/pygeocodio

.. image:: https://travis-ci.org/bennylope/pygeocodio.png?branch=master
        :target: https://travis-ci.org/bennylope/pygeocodio

.. image:: https://pypip.in/d/pygeocodio/badge.png
        :target: https://crate.io/packages/pygeocodio?version=latest


Python wrapper for `Geocod.io geocoding API <http://geocod.io/docs/>`_.

Full documentation on `Read the Docs <http://pygeocodio.readthedocs.org/en/latest/>`_.

**If you are upgrading from a version prior to 0.2.0 please see the changelog
in HISTORY.rst. The default coordinate ordering has changed to something a bit
more sensible for most users.**

Geocod.io API Features
======================

* Geocode an individual address
* Batch geocode up to 10,000 addresses at a time
* Parse an address into its identifiable components
* Reverse geocode an individual geographic point
* Batch reverse geocode up to 10,000 points at a time

The service is limited to U.S. addresses for the time being.

Read the complete `Geocod.io documentation <http://geocod.io/docs/>`_ for
service documentation.

Installation
============

pygeocodio requires `requests` 1.0.0 or greater and will ensure requests is
installed::

    pip install pygeocodio

Basic usage
===========

Import the API client and ensure you have a valid API key::

    >>> from geocodio import GeocodioClient
    >>> client = GeocodioClient(YOUR_API_KEY)

Geocoding
---------

Geocoding an individual address::

    >>> geocoded_location = client.geocode("42370 Bob Hope Drive, Rancho Mirage CA")
    >>> geocoded_location.coords
    (33.738987255507, -116.40833849559)

Batch geocoding
---------------

You can also geocode a list of addresses::

    >>> geocoded_addresses = geocodio.geocode([
            '1600 Pennsylvania Ave, Washington, DC',
            '3101 Patterson Ave, Richmond, VA, 23221'
        ])

Return a list of just the coordinates for the resultant geocoded addresses::

    >>> geocoded_addresses.coords
    [(33.738987255507, -116.40833849559), (33.738987255507, -116.40833849559)]
    >>> geocoded_addresses[0].coords
    (33.738987255507, -116.40833849559)

Lookup an address by queried address::

    >>> geocoded_addresses.addresses.get['1600 Pennsylvania Ave, Washington, DC'].coords
    (33.738987255507, -116.40833849559)

Address parsing
---------------

And if you just want to parse an individual address into its components::

    >>> client.parse('1600 Pennsylvania Ave, Washington DC')
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

Reverse geocoding
-----------------

Reverse geocode a point to find a matching address::

    >>> location = client.reverse((33.738987, -116.4083))
    >>> location.formatted_address
    "42370 Bob Hope Dr, Rancho Mirage CA, 92270"

Batch reverse geocoding
-----------------------

And multiple points at a time::

    >>> locations = client.reverse([
            (33.738987, -116.4083),
            (33.738987, -116.4083),
            (33.738987, -116.4083)
        ])

Return the list of formatted addresses::

    >>> locations.formatted_addresses
    ["100 Main St, Springfield, USA", "100 Main St, Springfield, USA", "100 Main St, Springfield, USA"]

Access a specific address by queried point tuple::

    >>> locations.addresses.get("33.738987, -116.4083").formatted_address
    "1600 Pennsylvania Ave, Washington, DC"

Or by the more natural key of the queried point tuple::

    >>> locations.addresses.get((33.738987, -116.4083)).formatted_address
    "1600 Pennsylvania Ave, Washington, DC"

CLI usage
=========

In the works!

Documentation
=============

For complete documentation see `the docs
<http://pygeocodio.readthedocs.org/en/latest/>`_.

License
=======

BSD License
