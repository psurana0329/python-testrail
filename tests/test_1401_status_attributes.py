#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import

import unittest
import platform
import datetime

import testrail
from tests.config import *

IS_PY3 = platform.python_version_tuple() >= ('3', '0')


class StatusAttributes(unittest.TestCase):
    def setUp(self):
        self.t = testrail.Testrail(SERVER, USER, PASS)
        self.p = self.t.get_project(name=TEST_PROJECT_NAME)
        self.r = self.p.get_run(TEST_RUN_NAME)
        self.ts = self.r.get_test(TEST_TEST_NAME)
        self.sta = self.ts.status

    def test_status_id(self):
        self.assertIsNotNone(self.sta.id)
        self.assertIsInstance(self.sta.id, int)

        def change_id():
            self.sta.id = 0

        self.assertRaises(RuntimeError, change_id)

    def test_status_name(self):
        self.assertIsNotNone(self.sta.name)
        if IS_PY3:
            self.assertIsInstance(self.sta.name, str)
        else:
            self.assertIsInstance(self.sta.name, unicode)

        def change_name():
            self.sta.name = u'asdf'

        self.assertRaises(RuntimeError, change_name)

    def test_status_label(self):
        self.assertIsNotNone(self.sta.label)
        if IS_PY3:
            self.assertIsInstance(self.sta.label, str)
        else:
            self.assertIsInstance(self.sta.label, unicode)

        def change_label():
            self.sta.label = u'asdf'

        self.assertRaises(RuntimeError, change_label)

    def test_status_is_system(self):
        self.assertIsNotNone(self.sta.is_system)
        self.assertIsInstance(self.sta.is_system, bool)

        def change_is_system():
            self.sta.is_system = u'asdf'

        self.assertRaises(RuntimeError, change_is_system)

    def test_status_is_untested(self):
        self.assertIsNotNone(self.sta.is_untested)
        self.assertIsInstance(self.sta.is_untested, bool)

        def change_is_untested():
            self.sta.is_untested = u'asdf'

        self.assertRaises(RuntimeError, change_is_untested)

    def test_status_is_final(self):
        self.assertIsNotNone(self.sta.is_final)
        self.assertIsInstance(self.sta.is_final, bool)

        def change_is_final():
            self.sta.is_final = u'asdf'

        self.assertRaises(RuntimeError, change_is_final)

    def test_status_color_bright(self):
        self.assertIsNotNone(self.sta.color_bright)
        self.assertIsInstance(self.sta.color_bright, int)

        def change_color_bright():
            self.sta.color_bright = u'asdf'

        self.assertRaises(RuntimeError, change_color_bright)

    def test_status_color_medium(self):
        self.assertIsNotNone(self.sta.color_medium)
        self.assertIsInstance(self.sta.color_medium, int)

        def change_color_medium():
            self.sta.color_medium = u'asdf'

        self.assertRaises(RuntimeError, change_color_medium)
    
    def test_status_color_dark(self):
        self.assertIsNotNone(self.sta.color_dark)
        self.assertIsInstance(self.sta.color_dark, int)

        def change_color_dark():
            self.sta.color_dark = u'asdf'

        self.assertRaises(RuntimeError, change_color_dark)

    def test_status_string(self):
        self.assertIsNotNone(str(self.sta))
        self.assertIsNotNone(repr(self.sta))
        
