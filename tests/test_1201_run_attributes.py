#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import

import unittest
import platform
import datetime

import testrail
from tests.config import *

IS_PY3 = platform.python_version_tuple() >= ('3', '0')


class RunAttributes(unittest.TestCase):
    def setUp(self):
        self.t = testrail.Testrail(SERVER, USER, PASS)
        self.p = self.t.get_project(name=TEST_PROJECT_NAME)
        self.r = self.p.get_run(TEST_RUN_NAME)

    def test_run_id(self):
        self.assertIsNotNone(self.r.id)
        self.assertIsInstance(self.r.id, int)

        def change_id():
            self.r.id = 0

        self.assertRaises(RuntimeError, change_id)

    def test_run_project(self):
        self.assertIsNotNone(self.r.project)
        self.assertIsInstance(self.r.project, testrail.models.Project)

        def change_project():
            self.r.project = None

        self.assertRaises(RuntimeError, change_project)

    def test_run_plan(self):
        if self.r.plan is not None:
            self.assertIsInstance(self.r.plan, testrail.models.Plan)

        def change_plan():
            self.r.plan = None

        self.assertRaises(RuntimeError, change_plan)

    def test_run_config(self):
        if self.r.config is not None:
            if IS_PY3:
                self.assertIsInstance(self.r.config, str)
            else:
                self.assertIsInstance(self.r.config, unicode)

        def change_config():
            self.r.config = None

        self.assertRaises(RuntimeError, change_config)

    def test_run_configs(self):
        if self.r.configs is not None:
            self.assertIsInstance(self.r.configs, list)
            for item in self.r.configs:
                self.assertIsInstance(item, int)

        def change_configs():
            self.r.configs = None

        self.assertRaises(RuntimeError, change_configs)

    def test_run_suite(self):
        self.assertIsNotNone(self.r.suite)
        self.assertIsInstance(self.r.suite, testrail.models.Suite)

        def change_suite():
            self.r.suite = None

        self.assertRaises(RuntimeError, change_suite)

    def test_run_include_all(self):
        self.assertIsNotNone(self.r.include_all)
        self.assertIsInstance(self.r.include_all, bool)

        def change_include_all():
            self.r.include_all = None

        self.assertRaises(RuntimeError, change_include_all)

    def test_run_milestone(self):
        if self.r.milestone is not None:
            self.assertIsInstance(self.r.milestone, testrail.models.Milestone)

        def change_milestone():
            self.r.milestone = None

        self.assertRaises(RuntimeError, change_milestone)

    def test_run_name(self):
        self.assertIsNotNone(self.r.name)
        if IS_PY3:
            self.assertIsInstance(self.r.name, str)
        else:
            self.assertIsInstance(self.r.name, unicode)

        def change_name():
            self.r.name = 'asdf'

        self.assertRaises(RuntimeError, change_name)

    def test_run_description(self):
        if self.r.description is not None:
            if IS_PY3:
                self.assertIsInstance(self.r.name, str)
            else:
                self.assertIsInstance(self.r.name, unicode)

        def change_description():
            self.r.description = u'adsadf32sdf'

        self.assertRaises(RuntimeError, change_description)

    def test_run_url(self):
        self.assertIsNotNone(self.r.url)
        if IS_PY3:
            self.assertIsInstance(self.r.name, str)
        else:
            self.assertIsInstance(self.r.name, unicode)

        def change_url():
            self.r.url = 'asdf'

        self.assertRaises(RuntimeError, change_url)

    def test_run_is_completed(self):
        self.assertIsNotNone(self.r.is_completed)
        self.assertIsInstance(self.r.is_completed, bool)

        def change_is_completed():
            self.r.is_completed = True

        self.assertRaises(RuntimeError, change_is_completed)

    def test_run_completed_on(self):
        if self.r.completed_on is not None:
            self.assertIsInstance(self.r.completed_on, datetime.datetime)

        def change_completed_on():
            self.r.completed_on = 123456

        self.assertRaises(RuntimeError, change_completed_on)

    def test_run_created_on(self):
        self.assertIsNotNone(self.r.created_on)
        self.assertIsInstance(self.r.created_on, datetime.datetime)

        def change_created_on():
            self.r.created_on = 123456

        self.assertRaises(RuntimeError, change_created_on)

    def test_run_created_by(self):
        self.assertIsNotNone(self.r.created_by)
        self.assertIsInstance(self.r.created_by, testrail.models.User)

        def change_created_by():
            self.r.created_by = 123456

        self.assertRaises(RuntimeError, change_created_by)

    def test_run_assigned_to(self):
        if self.r.assigned_to is not None:
            self.assertIsInstance(self.r.assigned_to, testrail.models.User)

        def change_assigned_to():
            self.r.assigned_to = None

        self.assertRaises(RuntimeError, change_assigned_to)

    def test_run_passed_count(self):
        self.assertIsNotNone(self.r.passed_count)
        self.assertIsInstance(self.r.passed_count, int)

        def change_passed_count():
            self.r.passed_count = 0

        self.assertRaises(RuntimeError, change_passed_count)

    def test_run_failed_count(self):
        self.assertIsNotNone(self.r.failed_count)
        self.assertIsInstance(self.r.failed_count, int)

        def change_failed_count():
            self.r.failed_count = 0

        self.assertRaises(RuntimeError, change_failed_count)

    def test_run_retest_count(self):
        self.assertIsNotNone(self.r.retest_count)
        self.assertIsInstance(self.r.retest_count, int)

        def change_retest_count():
            self.r.retest_count = 0

        self.assertRaises(RuntimeError, change_retest_count)

    def test_run_blocked_count(self):
        self.assertIsNotNone(self.r.blocked_count)
        self.assertIsInstance(self.r.blocked_count, int)

        def change_blocked_count():
            self.r.blocked_count = 0

        self.assertRaises(RuntimeError, change_blocked_count)

    def test_run_untested_count(self):
        self.assertIsNotNone(self.r.untested_count)
        self.assertIsInstance(self.r.untested_count, int)

        def change_untested_count():
            self.r.untested_count = 0

        self.assertRaises(RuntimeError, change_untested_count)

    def test_run_custom_status1_count(self):
        self.assertIsNotNone(self.r.custom_status1_count)
        self.assertIsInstance(self.r.custom_status1_count, int)

        def change_custom_status1_count():
            self.r.custom_status1_count = 0

        self.assertRaises(RuntimeError, change_custom_status1_count)

    def test_run_custom_status2_count(self):
        self.assertIsNotNone(self.r.custom_status2_count)
        self.assertIsInstance(self.r.custom_status2_count, int)

        def change_custom_status2_count():
            self.r.custom_status2_count = 0

        self.assertRaises(RuntimeError, change_custom_status2_count)

    def test_run_custom_status3_count(self):
        self.assertIsNotNone(self.r.custom_status3_count)
        self.assertIsInstance(self.r.custom_status3_count, int)

        def change_custom_status3_count():
            self.r.custom_status3_count = 0

        self.assertRaises(RuntimeError, change_custom_status3_count)

    def test_run_custom_status4_count(self):
        self.assertIsNotNone(self.r.custom_status4_count)
        self.assertIsInstance(self.r.custom_status4_count, int)

        def change_custom_status4_count():
            self.r.custom_status4_count = 0

        self.assertRaises(RuntimeError, change_custom_status4_count)

    def test_run_custom_status5_count(self):
        self.assertIsNotNone(self.r.custom_status5_count)
        self.assertIsInstance(self.r.custom_status5_count, int)

        def change_custom_status5_count():
            self.r.custom_status5_count = 0

        self.assertRaises(RuntimeError, change_custom_status5_count)

    def test_run_custom_status6_count(self):
        self.assertIsNotNone(self.r.custom_status6_count)
        self.assertIsInstance(self.r.custom_status6_count, int)

        def change_custom_status6_count():
            self.r.custom_status6_count = 0

        self.assertRaises(RuntimeError, change_custom_status6_count)

    def test_run_custom_status7_count(self):
        self.assertIsNotNone(self.r.custom_status7_count)
        self.assertIsInstance(self.r.custom_status7_count, int)

        def change_custom_status7_count():
            self.r.custom_status7_count = 0

        self.assertRaises(RuntimeError, change_custom_status7_count)

    def test_run_string(self):
        self.assertIsNotNone(str(self.r))
        self.assertIsNotNone(repr(self.r))
