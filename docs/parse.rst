=========================
Address component parsing
=========================

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
