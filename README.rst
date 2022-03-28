===========
Py-Geocodio
===========

.. image:: https://badge.fury.io/py/pygeocodio.svg
    :target: http://badge.fury.io/py/pygeocodio

.. image:: https://github.com/bennylope/pygeocodio/actions/workflows/tests.yml/badge.svg?branch=master
    :target: https://github.com/bennylope/pygeocodio/actions

.. image:: https://img.shields.io/pypi/dm/pygeocodio.svg
        :target: https://img.shields.io/pypi/dm/pygeocodio.svg


Python wrapper for `Geocodio geocoding API <http://geocod.io/docs/>`_.

Full documentation on `Read the Docs <http://pygeocodio.readthedocs.org/en/latest/>`_.

**If you are upgrading from a version prior to 0.2.0 please see the changelog
in HISTORY.rst. The default coordinate ordering has changed to something a bit
more sensible for most users.**

Geocodio API Features
=====================

* Geocode an individual address
* Batch geocode up to 10,000 addresses at a time
* Parse an address into its identifiable components
* Reverse geocode an individual geographic point
* Batch reverse geocode up to 10,000 points at a time
* Perform operations using the HIPAA API URL

The service is limited to U.S. and Canada addresses for the time being.

Read the complete `Geocodio documentation <http://geocod.io/docs/>`_ for
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

Note that you can pass in a timeout value in seconds (the default is no timeout)::

    >>> client = GeocodioClient(YOUR_API_KEY, timeout=15)

Geocoding
---------

Geocoding an individual address::

    >>> geocoded_location = client.geocode("42370 Bob Hope Drive, Rancho Mirage CA")
    >>> geocoded_location.coords
    (33.738987255507, -116.40833849559)


Geocode a set of address components::

    >>> geocoded_location = client.geocode(components_data={
      "postal_code": "02210",
      "country": "US"
    })
    >>> geocoded_location.coords
    (42.347547, -71.040645)

Batch geocoding
---------------

You can also geocode a list of addresses::

    >>> geocoded_addresses = client.geocode([
            '2 15th St NW, Washington, DC 20024',
            '3101 Patterson Ave, Richmond, VA, 23221'
        ])

Return a list of just the coordinates for the resultant geocoded addresses::

    >>> geocoded_addresses.coords
    [(38.890083, -76.983822), (37.560446, -77.476008)]
    >>> geocoded_addresses[0].coords
    (38.890083, -76.983822)

Lookup an address by the queried address::

    >>> geocoded_addresses.get('2 15th St NW, Washington, DC 20024').coords
    (38.879138, -76.981879))


You can also geocode a list of address component dictionaries::

    >>> geocoded_addresses = client.geocode(components_data=[{
            'street': '1109 N Highland St',
            'city': 'Arlington',
            'state': 'VA'
        }, {
            'city': 'Toronto',
            'country': 'CA'
        }])


And geocode a keyed mapping of address components::

    >>> gecoded_addresses = client.geocode(components_data={
            "1": {
                "street": "1109 N Highland St",
                "city": "Arlington",
                "state": "VA"
            },
            "2": {
                "city": "Toronto",
                "country": "CA"
            }})


And geocode even a keyed mapping of addresses::

    >>> geocoded_addresses = client.geocode({
            "1": "3101 patterson ave, richmond, va",
            "2": "1657 W Broad St, Richmond, VA"
        })

Return a list of just the coordinates for the resultant geocoded addresses::

    >>> geocoded_addresses.coords
    {'1': (37.560454, -77.47601), '2': (37.555176, -77.458273)}


Lookup an address by its key::

    >>> geocoded_addresses.get("1").coords
    (37.560454, -77.47601)


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
            (38.890083, -76.983822)
        ])

Return the list of formatted addresses::

    >>> locations.formatted_addresses
    ["42370 Bob Hope Dr, Rancho Mirage CA, 92270",  "42370 Bob Hope Dr, Rancho Mirage CA, 92270", "2 15th St NW, Washington, DC 20024"]

Access a specific address by the queried point tuple::

    >>> locations.get("38.890083,-76.983822").formatted_address
    "2 15th St NW, Washington, DC 20024"

Or by the more natural key of the queried point tuple::

    >>> locations.get((38.890083, -76.983822)).formatted_address
    "2 15th St NW, Washington, DC 20024"

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
