#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import

import unittest
import platform
import datetime

import testrail
from tests.config import *

IS_PY3 = platform.python_version_tuple() >= ('3', '0')


class CaseAttributes(unittest.TestCase):
    def setUp(self):
        self.t = testrail.Testrail(SERVER, USER, PASS)
        self.p = self.t.get_project(name=TEST_PROJECT_NAME)
        self.s = self.p.get_suite(TEST_SUITE_NAME)
        self.sec = self.s.get_section(TEST_SECTION_NAME)
        self.c = self.sec.get_case(TEST_CASE_NAME)

    def test_case_id(self):
        self.assertIsNotNone(self.c.id)
        self.assertIsInstance(self.c.id, int)

        def change_id():
            self.c.id = 0

        self.assertRaises(RuntimeError, change_id)

    def test_case_suite(self):
        self.assertIsNotNone(self.c.suite)
        self.assertIsInstance(self.c.suite, testrail.models.Suite)

        def change_suite():
            self.c.suite = 0

        self.assertRaises(RuntimeError, change_suite)

    def test_case_section(self):
        self.assertIsNotNone(self.c.section)
        self.assertIsInstance(self.c.section, testrail.models.Section)

        def change_section():
            self.c.section = 0

        self.assertRaises(RuntimeError, change_section)

    def test_case_title(self):
        self.assertIsNotNone(self.c.title)
        if IS_PY3:
            self.assertIsInstance(self.c.title, str)
        else:
            self.assertIsInstance(self.c.title, unicode)

        def change_title():
            self.c.title = 'asdf'

        self.assertRaises(RuntimeError, change_title)

    def test_case_type(self):
        self.assertIsNotNone(self.c.type)
        self.assertIsInstance(self.c.type, testrail.models.CaseType)

        def change_type():
            self.c.type = 0

        self.assertRaises(RuntimeError, change_type)

    def test_case_priority(self):
        self.assertIsNotNone(self.c.priority)
        self.assertIsInstance(self.c.priority, testrail.models.Priority)

        def change_priority():
            self.c.priority = 0

        self.assertRaises(RuntimeError, change_priority)

    def test_case_milestone(self):
        if self.c.milestone is not None:
            self.assertIsInstance(self.c.milestone, testrail.models.Milestone)

        def change_milestone():
            self.c.milestone = 0

        self.assertRaises(RuntimeError, change_milestone)

    def test_case_refs(self):
        if self.c.refs is not None:
            if IS_PY3:
                self.assertIsInstance(self.c.refs, str)
            else:
                self.assertIsInstance(self.c.refs, unicode)

        def change_refs():
            self.c.refs = 0

        self.assertRaises(RuntimeError, change_refs)

    def test_case_estimate(self):
        if self.c.estimate is not None:
            if IS_PY3:
                self.assertIsInstance(self.c.estimate, str)
            else:
                self.assertIsInstance(self.c.estimate, unicode)

        def change_estimate():
            self.c.estimate = 0

        self.assertRaises(RuntimeError, change_estimate)

    def test_case_estimate_forecast(self):
        if self.c.estimate_forecast is not None:
            if IS_PY3:
                self.assertIsInstance(self.c.estimate_forecast, str)
            else:
                self.assertIsInstance(self.c.estimate_forecast, unicode)

        def change_estimate_forecast():
            self.c.estimate_forecast = 0

        self.assertRaises(RuntimeError, change_estimate_forecast)

    def test_case_created_on(self):
        self.assertIsNotNone(self.c.created_on)
        self.assertIsInstance(self.c.created_on, datetime.datetime)

        def change_created_on():
            self.c.created_on = 0

        self.assertRaises(RuntimeError, change_created_on)

    def test_case_created_by(self):
        self.assertIsNotNone(self.c.created_by)
        self.assertIsInstance(self.c.created_by, testrail.models.User)

        def change_created_by():
            self.c.created_by = 0

        self.assertRaises(RuntimeError, change_created_by)
    
    def test_case_updated_on(self):
        self.assertIsNotNone(self.c.updated_on)
        self.assertIsInstance(self.c.updated_on, datetime.datetime)

        def change_updated_on():
            self.c.updated_on = 0

        self.assertRaises(RuntimeError, change_updated_on)

    def test_case_updated_by(self):
        self.assertIsNotNone(self.c.updated_by)
        self.assertIsInstance(self.c.updated_by, testrail.models.User)

        def change_updated_by():
            self.c.updated_by = 0

        self.assertRaises(RuntimeError, change_updated_by)

    def test_case_fields(self):
        self.assertIsNotNone(self.c.fields)
        self.assertIsInstance(self.c.fields, testrail.models.CustomFieldsContainer)

        def change_fields():
            self.c.fields = 0

        self.assertRaises(RuntimeError, change_fields)

    def test_case_string(self):
        self.assertIsNotNone(str(self.c))
        self.assertIsNotNone(repr(self.c))




