#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import

import unittest
import platform
import datetime

import testrail
from tests.config import *

IS_PY3 = platform.python_version_tuple() >= ('3', '0')


class MilestoneAttributes(unittest.TestCase):
    def setUp(self):
        self.t = testrail.Testrail(SERVER, USER, PASS)
        self.p = self.t.get_project(name=TEST_PROJECT_NAME)
        self.m = self.p.get_milestone(TEST_MILESTONE_NAME)

    def test_milestone_id(self):
        self.assertIsNotNone(self.m.id)
        self.assertIsInstance(self.m.id, int)

        def change_id():
            self.m.id = 0

        self.assertRaises(RuntimeError, change_id)

    def test_milestone_project(self):
        self.assertIsNotNone(self.m.project)
        self.assertIsInstance(self.m.project, testrail.models.Project)

        def change_project():
            self.m.project = None

        self.assertRaises(RuntimeError, change_project)

    def test_milestone_name(self):
        self.assertIsNotNone(self.m.name)
        if IS_PY3:
            self.assertIsInstance(self.m.name, str)
        else:
            self.assertIsInstance(self.m.name, unicode)

        def change_name():
            self.m.name = u'asdf'

        self.assertRaises(RuntimeError, change_name)

    def test_milestone_description(self):
        if self.m.description is not None:
            if IS_PY3:
                self.assertIsInstance(self.m.name, str)
            else:
                self.assertIsInstance(self.m.name, unicode)

        def change_description():
            self.m.description = u'adsadf32sdf'

        self.assertRaises(RuntimeError, change_description)

    def test_milestone_url(self):
        self.assertIsNotNone(self.m.url)
        if IS_PY3:
            self.assertIsInstance(self.m.name, str)
        else:
            self.assertIsInstance(self.m.name, unicode)

        def change_url():
            self.m.url = 'asdf'

        self.assertRaises(RuntimeError, change_url)

    def test_milestone_due_on(self):
        if self.m.due_on is not None:
            self.assertIsInstance(self.m.due_on, datetime.datetime)

        def change_due_on():
            self.m.due_on = 123456

        self.assertRaises(RuntimeError, change_due_on)
        
    def test_milestone_is_completed(self):
        self.assertIsNotNone(self.m.is_completed)
        self.assertIsInstance(self.m.is_completed, bool)

        def change_is_completed():
            self.m.is_completed = True

        self.assertRaises(RuntimeError, change_is_completed)

    def test_milestone_completed_on(self):
        if self.m.completed_on is not None:
            self.assertIsInstance(self.m.completed_on, datetime.datetime)

        def change_completed_on():
            self.m.completed_on = 123456

        self.assertRaises(RuntimeError, change_completed_on)

    def test_milestone_string(self):
        self.assertIsNotNone(str(self.m))
        self.assertIsNotNone(repr(self.m))




