#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import

import unittest
import platform
import datetime

import testrail
from tests.config import *

IS_PY3 = platform.python_version_tuple() >= ('3', '0')


class PlanAttributes(unittest.TestCase):
    def setUp(self):
        self.t = testrail.Testrail(SERVER, USER, PASS)
        self.p = self.t.get_project(name=TEST_PROJECT_NAME)
        self.pl = self.p.get_plan(TEST_PLAN_NAME)

    def test_plan_id(self):
        self.assertIsNotNone(self.pl.id)
        self.assertIsInstance(self.pl.id, int)

        def change_id():
            self.pl.id = 0

        self.assertRaises(RuntimeError, change_id)

    def test_plan_project(self):
        self.assertIsNotNone(self.pl.project)
        self.assertIsInstance(self.pl.project, testrail.models.Project)

        def change_project():
            self.pl.project = None

        self.assertRaises(RuntimeError, change_project)

    def test_plan_milestone(self):
        if self.pl.milestone is not None:
            self.assertIsInstance(self.pl.milestone, testrail.models.Milestone)

        def change_milestone():
            self.pl.milestone = None

        self.assertRaises(RuntimeError, change_milestone)

    def test_plan_name(self):
        self.assertIsNotNone(self.pl.name)
        if IS_PY3:
            self.assertIsInstance(self.pl.name, str)
        else:
            self.assertIsInstance(self.pl.name, unicode)

        def change_name():
            self.pl.name = 'asdf'

        self.assertRaises(RuntimeError, change_name)

    def test_plan_description(self):
        if self.pl.description is not None:
            if IS_PY3:
                self.assertIsInstance(self.pl.name, str)
            else:
                self.assertIsInstance(self.pl.name, unicode)

        def change_description():
            self.pl.description = u'adsadf32sdf'

        self.assertRaises(RuntimeError, change_description)

    def test_plan_url(self):
        self.assertIsNotNone(self.pl.url)
        if IS_PY3:
            self.assertIsInstance(self.pl.name, str)
        else:
            self.assertIsInstance(self.pl.name, unicode)

        def change_url():
            self.pl.url = 'asdf'

        self.assertRaises(RuntimeError, change_url)

    def test_plan_is_completed(self):
        self.assertIsNotNone(self.pl.is_completed)
        self.assertIsInstance(self.pl.is_completed, bool)

        def change_is_completed():
            self.pl.is_completed = True

        self.assertRaises(RuntimeError, change_is_completed)

    def test_plan_completed_on(self):
        if self.pl.completed_on is not None:
            self.assertIsInstance(self.pl.completed_on, datetime.datetime)

        def change_completed_on():
            self.pl.completed_on = 123456

        self.assertRaises(RuntimeError, change_completed_on)

    def test_plan_created_on(self):
        self.assertIsNotNone(self.pl.created_on)
        self.assertIsInstance(self.pl.created_on, datetime.datetime)

        def change_created_on():
            self.pl.created_on = 123456

        self.assertRaises(RuntimeError, change_created_on)

    def test_plan_created_by(self):
        self.assertIsNotNone(self.pl.created_by)
        self.assertIsInstance(self.pl.created_by, testrail.models.User)

        def change_created_by():
            self.pl.created_by = 123456

        self.assertRaises(RuntimeError, change_created_by)

    def test_plan_assigned_to(self):
        if self.pl.assigned_to is not None:
            self.assertIsInstance(self.pl.assigned_to, testrail.models.User)

        def change_assigned_to():
            self.pl.assigned_to = None

        self.assertRaises(RuntimeError, change_assigned_to)

    def test_plan_passed_count(self):
        self.assertIsNotNone(self.pl.passed_count)
        self.assertIsInstance(self.pl.passed_count, int)

        def change_passed_count():
            self.pl.passed_count = 0

        self.assertRaises(RuntimeError, change_passed_count)

    def test_plan_failed_count(self):
        self.assertIsNotNone(self.pl.failed_count)
        self.assertIsInstance(self.pl.failed_count, int)

        def change_failed_count():
            self.pl.failed_count = 0

        self.assertRaises(RuntimeError, change_failed_count)

    def test_plan_retest_count(self):
        self.assertIsNotNone(self.pl.retest_count)
        self.assertIsInstance(self.pl.retest_count, int)

        def change_retest_count():
            self.pl.retest_count = 0

        self.assertRaises(RuntimeError, change_retest_count)

    def test_plan_blocked_count(self):
        self.assertIsNotNone(self.pl.blocked_count)
        self.assertIsInstance(self.pl.blocked_count, int)

        def change_blocked_count():
            self.pl.blocked_count = 0

        self.assertRaises(RuntimeError, change_blocked_count)

    def test_plan_untested_count(self):
        self.assertIsNotNone(self.pl.untested_count)
        self.assertIsInstance(self.pl.untested_count, int)

        def change_untested_count():
            self.pl.untested_count = 0

        self.assertRaises(RuntimeError, change_untested_count)

    def test_plan_custom_status1_count(self):
        self.assertIsNotNone(self.pl.custom_status1_count)
        self.assertIsInstance(self.pl.custom_status1_count, int)

        def change_custom_status1_count():
            self.pl.custom_status1_count = 0

        self.assertRaises(RuntimeError, change_custom_status1_count)

    def test_plan_custom_status2_count(self):
        self.assertIsNotNone(self.pl.custom_status2_count)
        self.assertIsInstance(self.pl.custom_status2_count, int)

        def change_custom_status2_count():
            self.pl.custom_status2_count = 0

        self.assertRaises(RuntimeError, change_custom_status2_count)

    def test_plan_custom_status3_count(self):
        self.assertIsNotNone(self.pl.custom_status3_count)
        self.assertIsInstance(self.pl.custom_status3_count, int)

        def change_custom_status3_count():
            self.pl.custom_status3_count = 0

        self.assertRaises(RuntimeError, change_custom_status3_count)

    def test_plan_custom_status4_count(self):
        self.assertIsNotNone(self.pl.custom_status4_count)
        self.assertIsInstance(self.pl.custom_status4_count, int)

        def change_custom_status4_count():
            self.pl.custom_status4_count = 0

        self.assertRaises(RuntimeError, change_custom_status4_count)

    def test_plan_custom_status5_count(self):
        self.assertIsNotNone(self.pl.custom_status5_count)
        self.assertIsInstance(self.pl.custom_status5_count, int)

        def change_custom_status5_count():
            self.pl.custom_status5_count = 0

        self.assertRaises(RuntimeError, change_custom_status5_count)

    def test_plan_custom_status6_count(self):
        self.assertIsNotNone(self.pl.custom_status6_count)
        self.assertIsInstance(self.pl.custom_status6_count, int)

        def change_custom_status6_count():
            self.pl.custom_status6_count = 0

        self.assertRaises(RuntimeError, change_custom_status6_count)

    def test_plan_custom_status7_count(self):
        self.assertIsNotNone(self.pl.custom_status7_count)
        self.assertIsInstance(self.pl.custom_status7_count, int)

        def change_custom_status7_count():
            self.pl.custom_status7_count = 0

        self.assertRaises(RuntimeError, change_custom_status7_count)

    def test_plan_entries(self):
        self.assertIsNotNone(self.pl.entries)
        self.assertIsInstance(self.pl.entries, list)

        def change_entries():
            self.pl.entries = 0

        self.assertRaises(RuntimeError, change_entries)

    def test_plan_string(self):
        self.assertIsNotNone(str(self.pl))
        self.assertIsNotNone(repr(self.pl))
