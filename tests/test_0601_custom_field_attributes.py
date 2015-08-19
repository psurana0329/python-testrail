#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import

import unittest
import platform
import datetime

import testrail
from tests.config import *

IS_PY3 = platform.python_version_tuple() >= ('3', '0')


class CustomFieldsAttributes(unittest.TestCase):
    def setUp(self):
        self.t = testrail.Testrail(SERVER, USER, PASS)
        self.p = self.t.get_project(name=TEST_PROJECT_NAME)
        self.cf = self.p.get_case_fields()[0]

    def test_case_field_id(self):
        self.assertIsNotNone(self.cf.id)
        if IS_PY3:
            self.assertIsInstance(self.cf.name, str)
        else:
            self.assertIsInstance(self.cf.name, unicode)

        def change_id():
            self.cf.id = 0

        self.assertRaises(RuntimeError, change_id)

    def test_case_field_type_id(self):
        self.assertIsNotNone(self.cf.type_id)
        self.assertIsInstance(self.cf.type_id, int)
        self.assertNotEqual(self.cf.type_id, 0)

        def change_type_id():
            self.cf.type_id = 0

        self.assertRaises(RuntimeError, change_type_id)

    def test_case_field_project(self):
        self.assertIsNotNone(self.cf.project)
        self.assertIsInstance(self.cf.project, testrail.models.Project)

        def change_project():
            self.cf.project = None

        self.assertRaises(RuntimeError, change_project)

    def test_case_field_is_required(self):
        self.assertIsNotNone(self.cf.is_required)
        self.assertIsInstance(self.cf.is_required, bool)

        def change_is_required():
            self.cf.is_required = 0

        self.assertRaises(RuntimeError, change_is_required)

    def test_case_field_name(self):
        self.assertIsNotNone(self.cf.name)
        if IS_PY3:
            self.assertIsInstance(self.cf.name, str)
        else:
            self.assertIsInstance(self.cf.name, unicode)

        def change_name():
            self.cf.name = 0

        self.assertRaises(RuntimeError, change_name)

    def test_case_field_system_name(self):
        self.assertIsNotNone(self.cf.system_name)
        if IS_PY3:
            self.assertIsInstance(self.cf.system_name, str)
        else:
            self.assertIsInstance(self.cf.system_name, unicode)

        def change_system_name():
            self.cf.system_name = 0

        self.assertRaises(RuntimeError, change_system_name)

    def test_case_field_label(self):
        self.assertIsNotNone(self.cf.label)
        if IS_PY3:
            self.assertIsInstance(self.cf.label, str)
        else:
            self.assertIsInstance(self.cf.label, unicode)

        def change_label():
            self.cf.label = 0

        self.assertRaises(RuntimeError, change_label)

    def test_case_field_description(self):
        self.assertIsNotNone(self.cf.description)
        if IS_PY3:
            self.assertIsInstance(self.cf.description, str)
        else:
            self.assertIsInstance(self.cf.description, unicode)

        def change_description():
            self.cf.description = 0

        self.assertRaises(RuntimeError, change_description)

    def test_case_field_display_order(self):
        self.assertIsNotNone(self.cf.display_order)
        self.assertIsInstance(self.cf.display_order, int)

        def change_display_order():
            self.cf.display_order = 0

        self.assertRaises(RuntimeError, change_display_order)





