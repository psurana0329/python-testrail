#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import

import unittest
import platform
import datetime

import testrail
from tests.config import *

IS_PY3 = platform.python_version_tuple() >= ('3', '0')


class CaseTypeAttributes(unittest.TestCase):
    def setUp(self):
        self.t = testrail.Testrail(SERVER, USER, PASS)
        self.p = self.t.get_project(name=TEST_PROJECT_NAME)
        self.s = self.p.get_suite(TEST_SUITE_NAME)
        self.sec = self.s.get_section(TEST_SECTION_NAME)
        self.c = self.sec.get_case(TEST_CASE_NAME)
        self.ty = self.c.type

    def test_case_type_id(self):
        self.assertIsNotNone(self.ty.id)
        self.assertIsInstance(self.ty.id, int)

        def change_id():
            self.ty.id = 0

        self.assertRaises(RuntimeError, change_id)

    def test_case_type_name(self):
        self.assertIsNotNone(self.ty.name)
        if IS_PY3:
            self.assertIsInstance(self.ty.name, str)
        else:
            self.assertIsInstance(self.ty.name, unicode)

        def change_name():
            self.ty.name = u'asdf'

        self.assertRaises(RuntimeError, change_name)

    def test_case_type_is_default(self):
        self.assertIsNotNone(self.ty.is_default)
        self.assertIsInstance(self.ty.is_default, bool)

        def change_is_default():
            self.ty.is_default = 0

        self.assertRaises(RuntimeError, change_is_default)