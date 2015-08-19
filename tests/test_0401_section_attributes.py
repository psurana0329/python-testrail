#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import

import unittest
import platform

import testrail
from tests.config import *

IS_PY3 = platform.python_version_tuple() >= ('3', '0')


class SectionAttributes(unittest.TestCase):
    def setUp(self):
        self.t = testrail.Testrail(SERVER, USER, PASS)
        self.p = self.t.get_project(name=TEST_PROJECT_NAME)
        self.s = self.p.get_suite(TEST_SUITE_NAME)
        self.sec = self.s.get_section(TEST_SECTION_NAME)

    def test_section_id(self):
        self.assertIsNotNone(self.sec.id)
        self.assertIsInstance(self.sec.id, int)

        def change_id():
            self.sec.id = 0

        self.assertRaises(RuntimeError, change_id)

    def test_section_suite(self):
        self.assertIsNotNone(self.sec.suite)
        self.assertIsInstance(self.sec.suite, testrail.models.Suite)

        def change_suite():
            self.sec.suite = None

        self.assertRaises(RuntimeError, change_suite)

    def test_section_project(self):
        self.assertIsNotNone(self.sec.project)
        self.assertIsInstance(self.sec.project, testrail.models.Project)

        def change_project():
            self.sec.project = None

        self.assertRaises(RuntimeError, change_project)

    def test_section_name(self):
        self.assertIsNotNone(self.sec.name)
        if IS_PY3:
            self.assertIsInstance(self.sec.name, str)
        else:
            self.assertIsInstance(self.sec.name, unicode)

        def change_name():
            self.sec.name = 'asdf'

        self.assertRaises(RuntimeError, change_name)

    def test_section_description(self):
        if self.sec.description is not None:
            if IS_PY3:
                self.assertIsInstance(self.sec.name, str)
            else:
                self.assertIsInstance(self.sec.name, unicode)

        def change_description():
            self.sec.description = u'adsadf32sdf'

        self.assertRaises(RuntimeError, change_description)

    def test_section_parent(self):
        if self.sec.parent is not None:
            self.assertIsInstance(self.sec.parent, testrail.models.Section)

        def change_parent():
            self.sec.parent = None

        self.assertRaises(RuntimeError, change_parent)

    def test_section_depth(self):
        self.assertIsNotNone(self.sec.depth)
        self.assertIsInstance(self.sec.depth, int)

        def change_depth():
            self.sec.depth = 0

        self.assertRaises(RuntimeError, change_depth)

    def test_section_display_order(self):
        self.assertIsNotNone(self.sec.display_order)
        self.assertIsInstance(self.sec.display_order, int)

        def change_display_order():
            self.sec.display_order = 0

        self.assertRaises(RuntimeError, change_display_order)

    def test_suite_string(self):
        self.assertIsNotNone(str(self.s))
        self.assertIsNotNone(repr(self.s))