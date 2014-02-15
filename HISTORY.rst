.. :changelog:

History
-------

0.2.1 (2014-02-15)
++++++++++++++++++

* Fixed Python 3.3 test errors. Shouldn't have any functional effect on Python
  3.3 usage except for matching module paths of pygeocodio objects.

0.2.0 (2014-02-07)
++++++++++++++++++

* Added initial reverse geocoding functionality
* Swaps default coordinates order. This is a mostly backwards incompatible
  change to amend a silly design decision.

0.1.4 (2014-01-25)
++++++++++++++++++

* Handle error in which Geoco.io has returned empty result set

0.1.3 (2014-01-25)
++++++++++++++++++

* Packaging fix, thanks to @kyen99

0.1.2 (2014-01-23)
++++++++++++++++++

* Moves and enhances fixture data to JSON data based on linted server responses
* Adds Geocodio named errors
* Better handling of errors in individual locations from batch requests

0.1.1 (2014-01-22)
++++++++++++++++++

* Adds requests to install_requires in setup.py and drops minimum version to 1.0.0

0.1.0 (2014-01-21)
++++++++++++++++++

* First release on PyPI.
