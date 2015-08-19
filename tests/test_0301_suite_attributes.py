#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import

import unittest
import platform
import datetime

import testrail
from tests.config import *

IS_PY3 = platform.python_version_tuple() >= ('3', '0')


class SuiteAttributes(unittest.TestCase):
    def setUp(self):
        self.t = testrail.Testrail(SERVER, USER, PASS)
        self.p = self.t.get_project(name=TEST_PROJECT_NAME)
        self.s = self.p.get_suite(TEST_SUITE_NAME)

    def test_suite_id(self):
        self.assertIsNotNone(self.s.id)
        self.assertIsInstance(self.s.id, int)

        def change_id():
            self.s.id = 0

        self.assertRaises(RuntimeError, change_id)

    def test_suite_project(self):
        self.assertIsNotNone(self.s.project)
        self.assertIsInstance(self.s.project, testrail.models.Project)

        def change_project():
            self.s.project = None

        self.assertRaises(RuntimeError, change_project)

    def test_suite_name(self):
        self.assertIsNotNone(self.s.name)
        if IS_PY3:
            self.assertIsInstance(self.s.name, str)
        else:
            self.assertIsInstance(self.s.name, unicode)

        def change_name():
            self.s.name = 'asdf'

        self.assertRaises(RuntimeError, change_name)

    def test_suite_description(self):
        if self.s.description is not None:
            if IS_PY3:
                self.assertIsInstance(self.s.name, str)
            else:
                self.assertIsInstance(self.s.name, unicode)

        def change_description():
            self.s.description = u'adsadf32sdf'

        self.assertRaises(RuntimeError, change_description)

    def test_suite_url(self):
        self.assertIsNotNone(self.s.url)
        if IS_PY3:
            self.assertIsInstance(self.s.name, str)
        else:
            self.assertIsInstance(self.s.name, unicode)

        def change_url():
            self.s.url = 'asdf'

        self.assertRaises(RuntimeError, change_url)

    def test_suite_is_master(self):
        if self.s.is_master is not None:
            self.assertIsInstance(self.s.is_master, bool)

        def change_is_master():
            self.s.is_master = True

        self.assertRaises(RuntimeError, change_is_master)

    def test_suite_is_baseline(self):
        if self.s.is_baseline is not None:
            self.assertIsInstance(self.s.is_baseline, bool)

        def change_is_baseline():
            self.s.is_baseline = True

        self.assertRaises(RuntimeError, change_is_baseline)

    def test_suite_is_completed(self):
        if self.s.is_completed is not None:
            self.assertIsInstance(self.s.is_completed, bool)

        def change_is_completed():
            self.s.is_completed = True

        self.assertRaises(RuntimeError, change_is_completed)

    def test_suite_completed_on(self):
        if self.s.completed_on is not None:
            self.assertIsInstance(self.s.completed_on, datetime.datetime)

        def change_completed_on():
            self.s.completed_on = 123456

        self.assertRaises(RuntimeError, change_completed_on)

    def test_suite_string(self):
        self.assertIsNotNone(str(self.s))
        self.assertIsNotNone(repr(self.s))


