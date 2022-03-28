.. :changelog:

History
-------

1.1.0 (2022-03-28)
+++++++++++++++++++

* Adds a timeout parameter for API requests (thanks aviv!)

1.0.1 (2021-07-18)
+++++++++++++++++++
* Fixes batched keyed address geocoding

1.0.0 (2020-06-18)
+++++++++++++++++++

* Adds support for keying batch geocode results (thanks liufran1 and Unix-Code!)
* Adds support for keying batch reverse geocode results (thanks liufran1 and Unix-Code!)

0.12.0 (2020-06-04)
+++++++++++++++++++

* Adds auto-loading of API version (thanks Unix-Code!)
* Default API calls to Version 1.6 (thanks MiniCodeMonkey!) 

0.11.1 (2019-11-07)
+++++++++++++++++++

* Default API calls to Version 1.4 (thanks cyranix!) 

0.11.0 (2019-10-19)
+++++++++++++++++++

* Search by address components (thanks Unix-Code!)

0.10.0 (2019-02-05)
+++++++++++++++++++

* Replaced http with https in clinet (thanks shea-parkes!)

0.9.0 (2019-01-15)
++++++++++++++++++

* Updates to use Geocodio API v 1.3 by default (thanks joshgeller!)
* The API version is now configurable for backwards and forward compatibility


0.8.0 (2018-12-30)
++++++++++++++++++

* Adds new US Census fields (thanks pedromachados!)

0.7.0 (2018-03-29)
++++++++++++++++++

* Added support for new Congressional districts for 2018 election (thanks nickcatal!)

0.6.0 (2018-02-16)
++++++++++++++++++

* Upgrade to Geocodio API version 1.2 (thanks MiniCodeMonkey!)
* Update allowed fields
* Update docs that Canada now included (thanks Goorzhel!)
* Miscellaneous fixes (thanks snake-plissken!)

0.5.0 (2016-05-16)
++++++++++++++++++

* Add additional allowed fields (census, cd114)

0.4.2 (2015-02-17)
++++++++++++++++++

* Bug fix the last bug fix

0.4.1 (2015-02-17)
++++++++++++++++++

* Bug fix to flatten 'fields' argument as a single query key

0.4.0 (2014-09-28)
++++++++++++++++++

* Bug fix for batch reverse geocoding
* Removes request handling from client methods

0.3.0 (2014-03-24)
++++++++++++++++++

* Adds support for additional data fields (e.g. Congressional districts, timezone)

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
