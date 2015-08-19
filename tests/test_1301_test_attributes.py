#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import

import unittest
import platform
import datetime

import testrail
from tests.config import *

IS_PY3 = platform.python_version_tuple() >= ('3', '0')


class TestAttributes(unittest.TestCase):
    def setUp(self):
        self.t = testrail.Testrail(SERVER, USER, PASS)
        self.p = self.t.get_project(name=TEST_PROJECT_NAME)
        self.r = self.p.get_run(TEST_RUN_NAME)
        self.ts = self.r.get_test(TEST_TEST_NAME)

    def test_test_id(self):
        self.assertIsNotNone(self.ts.id)
        self.assertIsInstance(self.ts.id, int)

        def change_id():
            self.ts.id = 0

        self.assertRaises(RuntimeError, change_id)

    def test_test_run(self):
        self.assertIsNotNone(self.ts.run)
        self.assertIsInstance(self.ts.run, testrail.models.Run)

        def change_run():
            self.ts.run = 0

        self.assertRaises(RuntimeError, change_run)

    def test_test_case(self):
        self.assertIsNotNone(self.ts.case)
        self.assertIsInstance(self.ts.case, testrail.models.Case)

        def change_case():
            self.ts.case = 0

        self.assertRaises(RuntimeError, change_case)

    def test_test_status(self):
        self.assertIsNotNone(self.ts.status)
        self.assertIsInstance(self.ts.status, testrail.models.Status)

        def change_status():
            self.ts.status = 0

        self.assertRaises(RuntimeError, change_status)

    def test_test_title(self):
        self.assertIsNotNone(self.ts.title)
        if IS_PY3:
            self.assertIsInstance(self.ts.title, str)
        else:
            self.assertIsInstance(self.ts.title, unicode)

        def change_title():
            self.ts.title = 'asdf'

        self.assertRaises(RuntimeError, change_title)

    def test_test_type(self):
        self.assertIsNotNone(self.ts.type)
        self.assertIsInstance(self.ts.type, testrail.models.CaseType)

        def change_type():
            self.ts.type = 0

        self.assertRaises(RuntimeError, change_type)

    def test_test_priority(self):
        self.assertIsNotNone(self.ts.priority)
        self.assertIsInstance(self.ts.priority, testrail.models.Priority)

        def change_priority():
            self.ts.priority = 0

        self.assertRaises(RuntimeError, change_priority)

    def test_test_milestone(self):
        if self.ts.milestone is not None:
            self.assertIsInstance(self.ts.milestone, testrail.models.Milestone)

        def change_milestone():
            self.ts.milestone = 0

        self.assertRaises(RuntimeError, change_milestone)

    def test_test_refs(self):
        if self.ts.refs is not None:
            if IS_PY3:
                self.assertIsInstance(self.ts.refs, str)
            else:
                self.assertIsInstance(self.ts.refs, unicode)

        def change_refs():
            self.ts.refs = 0

        self.assertRaises(RuntimeError, change_refs)

    def test_test_estimate(self):
        if self.ts.estimate is not None:
            if IS_PY3:
                self.assertIsInstance(self.ts.estimate, str)
            else:
                self.assertIsInstance(self.ts.estimate, unicode)

        def change_estimate():
            self.ts.estimate = 0

        self.assertRaises(RuntimeError, change_estimate)

    def test_test_estimate_forecast(self):
        if self.ts.estimate_forecast is not None:
            if IS_PY3:
                self.assertIsInstance(self.ts.estimate_forecast, str)
            else:
                self.assertIsInstance(self.ts.estimate_forecast, unicode)

        def change_estimate_forecast():
            self.ts.estimate_forecast = 0

        self.assertRaises(RuntimeError, change_estimate_forecast)

    def test_test_fields(self):
        self.assertIsNotNone(self.ts.fields)
        self.assertIsInstance(self.ts.fields, testrail.models.CustomFieldsContainer)

        def change_fields():
            self.ts.fields = 0

        self.assertRaises(RuntimeError, change_fields)

    def test_test_assigned_to(self):
        if self.ts.assigned_to is not None:
            self.assertIsInstance(self.ts.assigned_to, testrail.models.User)

        def change_assigned_to():
            self.ts.assigned_to = 0

        self.assertRaises(RuntimeError, change_assigned_to)

    def test_test_string(self):
        self.assertIsNotNone(str(self.ts))
        self.assertIsNotNone(repr(self.ts))




