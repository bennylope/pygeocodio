#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_geocodio
----------------------------------

Tests for `geocodio.client` module.
"""

import os
import unittest

import httpretty

from geocodio import exceptions
from geocodio.client import GeocodioClient, DEFAULT_API_VERSION
from geocodio.client import json_points
from geocodio.data import Location
from geocodio.data import LocationCollection


class ClientFixtures(object):
    def setUp(self):
        self.TEST_API_KEY = "1010110101"
        self.parse_url = "https://api.geocod.io/v{api_version}/parse".format(api_version=DEFAULT_API_VERSION)
        self.geocode_url = "https://api.geocod.io/v{api_version}/geocode".format(api_version=DEFAULT_API_VERSION)
        self.reverse_url = "https://api.geocod.io/v{api_version}/reverse".format(api_version=DEFAULT_API_VERSION)
        # WARNING - Client will ignore auto-loading api version for all tests using the fixture
        self.client = GeocodioClient(self.TEST_API_KEY, auto_load_api_version=False)
        self.err = '{"error": "We are testing"}'


class TestClientInit(unittest.TestCase):
    def setUp(self):
        self.TEST_API_KEY = "1010110101"

    def test_hipaa_enabled(self):
        client = GeocodioClient(self.TEST_API_KEY, hipaa_enabled=True, auto_load_api_version=False)
        self.assertTrue(client.hipaa_enabled)
        self.assertTrue(client.BASE_URL.startswith("https://api-hipaa.geocod.io"))

    def test_hipaa_disabled(self):
        client = GeocodioClient(self.TEST_API_KEY, auto_load_api_version=False)
        self.assertFalse(client.hipaa_enabled)
        self.assertTrue(client.BASE_URL.startswith("https://api.geocod.io"))

    def test_diff_version(self):
        client = GeocodioClient(self.TEST_API_KEY, version="1.0")
        self.assertTrue(client.BASE_URL.startswith("https://api.geocod.io/v1.0"))
        self.assertEqual(client.version, "1.0")

    def test_default_version(self):
        client = GeocodioClient(self.TEST_API_KEY, auto_load_api_version=False)
        self.assertTrue(
            client.BASE_URL.startswith("https://api.geocod.io/v{version}".format(version=DEFAULT_API_VERSION)))
        self.assertEqual(client.version, DEFAULT_API_VERSION)


class TestClientInitAutoLoadApiVersion(unittest.TestCase):
    def setUp(self):
        self.TEST_API_KEY = "1010110101"
        self.base_domain = "https://api.geocod.io"
        self.base_hipaa_domain = "https://api-hipaa.geocod.io"
        fixtures = os.path.join(os.path.dirname(os.path.abspath(__file__)), "response/")
        with open(os.path.join(fixtures, "api_description.json"), "r") as api_description_json:
            self.api_description = api_description_json.read()

    @httpretty.activate
    def test_auto_load_api_version(self):
        httpretty.register_uri(
            httpretty.GET, self.base_domain, body=self.api_description, status=200
        )
        client = GeocodioClient(self.TEST_API_KEY)
        expected_version = "1.6"
        self.assertEqual(client.version, expected_version)
        self.assertTrue(client.BASE_URL.startswith("{domain}/v{version}".format(domain=self.base_domain,
                                                                                version=expected_version)))

    @httpretty.activate
    def test_auto_load_hipaa_api_version(self):
        httpretty.register_uri(
            httpretty.GET, self.base_hipaa_domain, body=self.api_description, status=200
        )
        client = GeocodioClient(self.TEST_API_KEY, hipaa_enabled=True)
        expected_version = "1.6"
        self.assertEqual(client.version, expected_version)
        self.assertTrue(
            client.BASE_URL.startswith(
                "{domain}/v{version}".format(domain=self.base_hipaa_domain, version=expected_version)))

    @httpretty.activate
    def test_auto_load_failure(self):
        httpretty.register_uri(
            httpretty.GET, self.base_domain, body="does not matter", status=500
        )
        client = GeocodioClient(self.TEST_API_KEY)
        expected_version = DEFAULT_API_VERSION
        self.assertEqual(client.version, expected_version)
        self.assertTrue(
            client.BASE_URL.startswith(
                "{domain}/v{version}".format(domain=self.base_domain, version=expected_version)))

    @httpretty.activate
    def test_skip_auto_load(self):
        httpretty.register_uri(
            httpretty.GET, self.base_domain, body=self.api_description, status=200
        )
        expected_version = "1.0"
        client = GeocodioClient(self.TEST_API_KEY, version=expected_version)
        self.assertEqual(client.version, expected_version)
        self.assertTrue(
            client.BASE_URL.startswith(
                "{domain}/v{version}".format(domain=self.base_domain, version=expected_version)))
        self.assertEqual(len(httpretty.latest_requests()), 0)

    @httpretty.activate
    def test_skip_auto_load_if_disabled(self):
        httpretty.register_uri(
            httpretty.GET, self.base_domain, body=self.api_description, status=200
        )
        expected_version = DEFAULT_API_VERSION
        client = GeocodioClient(self.TEST_API_KEY, auto_load_api_version=False)
        self.assertEqual(client.version, expected_version)
        self.assertTrue(
            client.BASE_URL.startswith(
                "{domain}/v{version}".format(domain=self.base_domain, version=expected_version)))
        self.assertEqual(len(httpretty.latest_requests()), 0)


class TestClientErrors(ClientFixtures, unittest.TestCase):
    @httpretty.activate
    def test_auth_error(self):
        """Ensure an HTTP 403 code raises GeocodioAuthError"""
        httpretty.register_uri(
            httpretty.GET, self.parse_url, body="This does not matter", status=403
        )
        self.assertRaises(exceptions.GeocodioAuthError, self.client.parse, "")
        httpretty.register_uri(
            httpretty.GET, self.geocode_url, body="This does not matter", status=403
        )
        self.assertRaises(exceptions.GeocodioAuthError, self.client.geocode, "")
        httpretty.register_uri(
            httpretty.POST, self.geocode_url, body="This does not matter", status=403
        )
        self.assertRaises(exceptions.GeocodioAuthError, self.client.geocode, [""])

    @httpretty.activate
    def test_data_error(self):
        """Ensure an HTTP 422 code raises GeocodioDataError"""
        httpretty.register_uri(httpretty.GET, self.parse_url, body=self.err, status=422)
        self.assertRaises(exceptions.GeocodioDataError, self.client.parse, "")
        httpretty.register_uri(
            httpretty.GET, self.geocode_url, body=self.err, status=422
        )
        self.assertRaises(exceptions.GeocodioDataError, self.client.geocode, "")
        httpretty.register_uri(
            httpretty.POST, self.geocode_url, body=self.err, status=422
        )
        self.assertRaises(exceptions.GeocodioDataError, self.client.geocode, [""])

    @httpretty.activate
    def test_server_error(self):
        """Ensure an HTTP 500 code raises GeocodioServerError"""
        httpretty.register_uri(
            httpretty.GET, self.parse_url, body="This does not matter", status=500
        )
        self.assertRaises(exceptions.GeocodioServerError, self.client.parse, "")
        httpretty.register_uri(
            httpretty.GET, self.geocode_url, body="This does not matter", status=500
        )
        self.assertRaises(exceptions.GeocodioServerError, self.client.geocode, "")
        httpretty.register_uri(
            httpretty.POST, self.geocode_url, body="This does not matter", status=500
        )
        self.assertRaises(exceptions.GeocodioServerError, self.client.geocode, [""])

    @httpretty.activate
    def test_default_error(self):
        """Ensure any other HTTP code raises a general error"""
        httpretty.register_uri(
            httpretty.GET, self.parse_url, body="This does not matter", status=418
        )
        self.assertRaises(exceptions.GeocodioError, self.client.parse, "")


class TestClientMethods(ClientFixtures, unittest.TestCase):
    """
    Integration testing for client service methods.
    """

    def setUp(self):
        super(TestClientMethods, self).setUp()
        fixtures = os.path.join(os.path.dirname(os.path.abspath(__file__)), "response/")
        with open(os.path.join(fixtures, "single_components.json"), "r") as single_components_json:
            self.single_components = single_components_json.read()
        with open(os.path.join(fixtures, "batch_components.json"), "r") as batch_components_json:
            self.batch_components = batch_components_json.read()
        with open(os.path.join(fixtures, "reverse.json"), "r") as reverse_json:
            self.single_reverse = reverse_json.read()
        with open(
                os.path.join(fixtures, "batch_reverse.json"), "r"
        ) as batch_reverse_json:
            self.batch_reverse = batch_reverse_json.read()

    @httpretty.activate
    def test_return_none_with_no_address_or_components(self):
        """Ensure None is returned when geocoding with no passed in address or components data"""
        httpretty.register_uri(
            httpretty.GET, self.geocode_url, body=self.single_components, status=200
        )
        self.assertEqual(self.client.geocode(), None)

    @httpretty.activate
    def test_return_none_with_both_address_and_components(self):
        """Ensure None is returned when geocoding with no passed in address or components data"""
        httpretty.register_uri(
            httpretty.GET, self.geocode_url, body=self.single_components, status=200
        )
        self.assertEqual(self.client.geocode(address_data="Toronto, CA", components_data={
            'city': 'Toronto',
            'country': 'CA'
        }), None)

    @httpretty.activate
    def test_single_components_response(self):
        """Ensure components geocoding results in a single Location"""
        httpretty.register_uri(
            httpretty.GET, self.geocode_url, body=self.single_components, status=200
        )
        self.assertTrue(isinstance(self.client.geocode(components_data={'postal_code': '02210'}), Location))

    @httpretty.activate
    def test_batch_components_response(self):
        """Ensure batch components geocoding results in a Location Collection"""
        httpretty.register_uri(
            httpretty.POST, self.geocode_url, body=self.batch_components, status=200
        )
        self.assertTrue(isinstance(self.client.geocode(components_data=[{
            'street': '1109 N Highland St',
            'city': 'Arlington',
            'state': 'VA'
        }, {
            'city': 'Toronto',
            'country': 'CA'
        }]), LocationCollection))

    @httpretty.activate
    def test_reverse_response(self):
        """Ensure reverse geocoding results in a single Location"""
        httpretty.register_uri(
            httpretty.GET, self.reverse_url, body=self.single_reverse, status=200
        )
        self.assertTrue(isinstance(self.client.reverse((-1, 1)), Location))

    @httpretty.activate
    def test_batch_reverse_response(self):
        """Ensure batch reverse geocoding results in LocationCollection"""
        httpretty.register_uri(
            httpretty.POST, self.reverse_url, body=self.batch_reverse, status=200
        )
        self.assertTrue(
            isinstance(self.client.reverse([(-1, 1), (3, 43)]), LocationCollection)
        )
        self.assertTrue(
            isinstance(
                self.client.reverse([(-1, 1), (3, 43)], fields=["cd"]),
                LocationCollection,
            )
        )

    @httpretty.activate
    def test_bad_field_spec(self):
        """Ensure a bad field name raises a ValueError"""
        httpretty.register_uri(
            httpretty.POST, self.reverse_url, body=self.batch_reverse, status=200
        )
        self.assertRaises(
            ValueError, self.client.reverse, (-1, 1), (3, 43), fields=["none"]
        )

    def test_json_points(self):
        """Ensure function returns JSON formatted list of strings"""
        self.assertEqual(
            '["35.9746,-77.9658", "32.87937,-96.63039", "33.83371,-117.836232", "35.417124,-80.678476"]',  # noqa
            json_points(
                [
                    (35.9746000, -77.9658000),
                    (32.8793700, -96.6303900),
                    (33.8337100, -117.8362320),
                    (35.4171240, -80.6784760),
                ]
            ),  # noqa
        )
