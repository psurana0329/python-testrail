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
        self.r = self.p.get_run(TEST_SUITE_NAME)
        self.ts = self.r.get_test(TEST_TEST_NAME)
        self.res = self.ts.get_results()[0]

    def test_result_id(self):
        self.assertIsNotNone(self.res.id)
        self.assertIsInstance(self.res.id, int)

        def change_id():
            self.res.id = 0

        self.assertRaises(RuntimeError, change_id)

    def test_result_test(self):
        self.assertIsNotNone(self.res.test)
        self.assertIsInstance(self.res.test, testrail.models.Test)

        def change_test():
            self.res.test = 0

        self.assertRaises(RuntimeError, change_test)

    def test_result_status(self):
        self.assertIsNotNone(self.res.status)
        self.assertIsInstance(self.res.status, testrail.models.Status)

        def change_status():
            self.res.status = 0

        self.assertRaises(RuntimeError, change_status)

    def test_result_version(self):
        if self.res.version is not None:
            if IS_PY3:
                self.assertIsInstance(self.res.version, str)
            else:
                self.assertIsInstance(self.res.version, unicode)

        def change_version():
            self.res.version = 0

        self.assertRaises(RuntimeError, change_version)

    def test_result_created_by(self):
        self.assertIsNotNone(self.res.created_by)
        self.assertIsInstance(self.res.created_by, testrail.models.User)

        def change_created_by():
            self.res.created_by = 0

        self.assertRaises(RuntimeError, change_created_by)

    def test_result_created_on(self):
        self.assertIsNotNone(self.res.created_on)
        self.assertIsInstance(self.res.created_on, datetime.datetime)

        def change_created_on():
            self.res.created_on = 0

        self.assertRaises(RuntimeError, change_created_on)

    def test_result_assigned_to(self):
        if self.res.assigned_to is not None:
            self.assertIsInstance(self.res.assigned_to, testrail.models.User)

        def change_assigned_to():
            self.res.assigned_to = 0

        self.assertRaises(RuntimeError, change_assigned_to)

    def test_result_comment(self):
        if self.res.comment is not None:
            if IS_PY3:
                self.assertIsInstance(self.res.comment, str)
            else:
                self.assertIsInstance(self.res.comment, unicode)

        def change_comment():
            self.res.comment = 0

        self.assertRaises(RuntimeError, change_comment)

    def test_result_elapsed(self):
        if self.res.elapsed is not None:
            if IS_PY3:
                self.assertIsInstance(self.res.elapsed, str)
            else:
                self.assertIsInstance(self.res.elapsed, unicode)

        def change_elapsed():
            self.res.elapsed = 0

        self.assertRaises(RuntimeError, change_elapsed)

    def test_result_defects(self):
        if self.res.defects is not None:
            if IS_PY3:
                self.assertIsInstance(self.res.defects, str)
            else:
                self.assertIsInstance(self.res.defects, unicode)

        def change_defects():
            self.res.defects = 0

        self.assertRaises(RuntimeError, change_defects)

    def test_result_fields(self):
        self.assertIsNotNone(self.res.fields)
        self.assertIsInstance(self.res.fields, testrail.models.CustomFieldsContainer)

        def change_fields():
            self.res.fields = 0

        self.assertRaises(RuntimeError, change_fields)

    def test_result_string(self):
        self.assertIsNotNone(str(self.res))
        self.assertIsNotNone(repr(self.res))




