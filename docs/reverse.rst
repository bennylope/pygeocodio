=================
Reverse geocoding
=================

Reverse geocoding takes a point and returns a matching address.

Single point reverse-geocoding
==============================

Reverse geocoding::

    >>> client.reverse((33.738987, -116.4083))


Batch reverse-geocoding
=======================

You can also reverse geocode in batch::

    >>> client.reverse([(33.738987, -116.4083), (34.288, -112.12)])

As with geocoding, there is a limit of 10,000 points you can geocode at a time.
