#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import

import unittest
import platform
import datetime

import testrail
from tests.config import *

IS_PY3 = platform.python_version_tuple() >= ('3', '0')


class PriorityAttributes(unittest.TestCase):
    def setUp(self):
        self.t = testrail.Testrail(SERVER, USER, PASS)
        self.p = self.t.get_project(name=TEST_PROJECT_NAME)
        self.s = self.p.get_suite(TEST_SUITE_NAME)
        self.sec = self.s.get_section(TEST_SECTION_NAME)
        self.c = self.sec.get_case(TEST_CASE_NAME)
        self.pri = self.c.priority

    def test_priority_id(self):
        self.assertIsNotNone(self.pri.id)
        self.assertIsInstance(self.pri.id, int)

        def change_id():
            self.pri.id = 0

        self.assertRaises(RuntimeError, change_id)

    def test_priority_name(self):
        self.assertIsNotNone(self.pri.name)
        if IS_PY3:
            self.assertIsInstance(self.pri.name, str)
        else:
            self.assertIsInstance(self.pri.name, unicode)

        def change_name():
            self.pri.name = u'asdf'

        self.assertRaises(RuntimeError, change_name)

    def test_priority_short_name(self):
        self.assertIsNotNone(self.pri.short_name)
        if IS_PY3:
            self.assertIsInstance(self.pri.short_name, str)
        else:
            self.assertIsInstance(self.pri.short_name, unicode)

        def change_short_name():
            self.pri.short_name = u'asdf'

        self.assertRaises(RuntimeError, change_short_name)

    def test_priority_is_default(self):
        self.assertIsNotNone(self.pri.is_default)
        self.assertIsInstance(self.pri.is_default, bool)

        def change_is_default():
            self.pri.is_default = 0

        self.assertRaises(RuntimeError, change_is_default)

    def test_priority_value(self):
        self.assertIsNotNone(self.pri.value)
        self.assertIsInstance(self.pri.value, int)

        def change_value():
            self.pri.value = 0

        self.assertRaises(RuntimeError, change_value)



