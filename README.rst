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

Features
--------

* Geocode an individual address
* Batch geocode up to 10,000 addresses at a time
* Parse an address into its identifiable components

Read the complete `Geocod.io documentation <http://geocod.io/docs/>`> for
service documentation.

Installation
------------

pygeocodio requires `requests` 2.0.0 or greater and will ensure requests is
installed::

    pip install pygeocodio

Using
-----

Import the API client and ensure you have a valid API key::

    >>> from geocodio import GeocodioClient
    >>> client = GeocodioClient(MY_KEY)
    >>> geocoded_location = client.geocode("42370 Bob Hope Drive, Rancho Mirage CA")

The result from the Geocod.io service is a dictionary including your query, its
components, and a list of matching results::

    >>> geocoded_location
    {
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

This returned several geolocation results in descending order of accuracy, so
the first and most accurate geocoded location latitude and longitude can be
accessed using the `coords` attribute::

    >>> geocoded_location.coords
    (-116.40833849559, 33.738987255507)

.. note::

    To make working with `other geographic data
    <http://postgis.net/docs/ST_Point.html>`_ formats easier the `coords`
    method returns a tuple in (longitude, latitude) format.

You can also geocode a list of addresses::

    >>> geocoded_addresses = geocodio.geocode(['1600 Pennsylvania Ave, Washington, DC',
            '3101 Patterson Ave, Richmond, VA, 23221'])

Return just the coordinates for the list of geocoded addresses::

    >>> geocoded_addresses.coords
    [(-116.40833849559, 33.738987255507), (-116.40833849559, 33.738987255507)]

Lookup an address by formatted address::

    >>> geocoded_addresses.addresses.get['1600 Pennsylvania Ave, Washington, DC'].coords
    (-116.40833849559, 33.738987255507)

Note that to perform the key based lookup you must use the `get` method. This
preserves the list's index based lookup.

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

The return value is simple enough to us as the returned dictionary.
