#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import

import unittest
import platform
import datetime

import testrail
from tests.config import *


IS_PY3 = platform.python_version_tuple() >= ('3', '0')


class ProjectAttributes(unittest.TestCase):
    def setUp(self):
        self.t = testrail.Testrail(SERVER, USER, PASS)
        self.p = self.t.get_project(name=TEST_PROJECT_NAME)

    def test_project_id(self):
        self.assertIsNotNone(self.p.id)
        self.assertIsInstance(self.p.id, int)

        def change_id():
            self.p.id = 0

        self.assertRaises(RuntimeError, change_id)

    def test_project_name(self):
        self.assertIsNotNone(self.p.name)
        if IS_PY3:
            self.assertIsInstance(self.p.name, str)
        else:
            self.assertIsInstance(self.p.name, unicode)

        def change_name():
            self.p.name = u'asdf'

        self.assertRaises(RuntimeError, change_name)

    def test_project_url(self):
        self.assertIsNotNone(self.p.url)
        if IS_PY3:
            self.assertIsInstance(self.p.name, str)
        else:
            self.assertIsInstance(self.p.name, unicode)

        def change_url():
            self.p.url = u'asdf'

        self.assertRaises(RuntimeError, change_url)

    def test_project_announcement(self):
        if self.p.announcement is not None:
            if IS_PY3:
                self.assertIsInstance(self.p.name, str)
            else:
                self.assertIsInstance(self.p.name, unicode)

        def change_announcement():
            self.p.announcement = u'adsadf32sdf'

        self.assertRaises(RuntimeError, change_announcement)

    def test_project_show_announcement(self):
        self.assertIsNotNone(self.p.show_announcement)
        self.assertIsInstance(self.p.show_announcement, bool)

        def change_show_announcement():
            self.p.show_announcement = True

        self.assertRaises(RuntimeError, change_show_announcement)

    def test_project_is_completed(self):
        self.assertIsNotNone(self.p.is_completed)
        self.assertIsInstance(self.p.is_completed, bool)

        def change_is_completed():
            self.p.is_completed = True

        self.assertRaises(RuntimeError, change_is_completed)

    def test_project_completed_on(self):
        if self.p.completed_on is not None:
            self.assertIsInstance(self.p.completed_on, datetime.datetime)

        def change_completed_on():
            self.p.completed_on = 123456

        self.assertRaises(RuntimeError, change_completed_on)

    def test_project_suite_mode(self):
        self.assertIsNotNone(self.p.suite_mode)
        self.assertIsInstance(self.p.suite_mode, int)

        def change_suite_mode():
            self.p.suite_mode = 3

        self.assertRaises(RuntimeError, change_suite_mode)

    def test_project_string(self):
        self.assertIsNotNone(str(self.p))
        self.assertIsNotNone(repr(self.p))