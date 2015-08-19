#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import

import unittest

import testrail
from tests.config import *


class ProjectLifecycle(unittest.TestCase):
    def setUp(self):
        self.t = testrail.Testrail(SERVER, USER, PASS)

        name = TEST_PROJECT_NAME+'_lifecycle'
        project = self.t.get_project(name=name)
        if project is not None:
            project.delete()

        name = TEST_PROJECT_NAME+'_lifecycle_temp'
        project = self.t.get_project(name=name)
        if project is not None:
            project.delete()

    def tearDown(self):
        name = TEST_PROJECT_NAME+'_lifecycle'
        project = self.t.get_project(name=name)
        if project is not None:
            project.delete()

        name = TEST_PROJECT_NAME+'_lifecycle_temp'
        project = self.t.get_project(name=name)
        if project is not None:
            project.delete()

    @unittest.skip("heavy load test, enable it manually if needed")
    def test_project_lifecycle(self):
        test_name = TEST_PROJECT_NAME + '_lifecycle'

        project = self.t.add_project(name=test_name,
                                     announcement='this',
                                     show_announcement=True,
                                     suite_mode=2)

        self.assertIsInstance(project, testrail.models.Project)
        self.assertEqual(project.name, test_name)
        self.assertEqual(project.announcement, 'this')
        self.assertTrue(project.show_announcement)
        self.assertEqual(project.suite_mode, 2)
        self.assertFalse(project.is_completed)
        self.assertIsNone(project.completed_on)

        test_name_temp = test_name + '_temp'

        project.update(name=test_name_temp,
                       announcement='this',
                       show_announcement=False)

        self.t.clear_cache()

        project = self.t.get_project(name=test_name_temp)

        self.assertIsInstance(project, testrail.models.Project)
        self.assertEqual(project.name, test_name_temp)
        self.assertEqual(project.announcement, 'this')
        self.assertFalse(project.show_announcement)
        self.assertFalse(project.is_completed)
        self.assertIsNone(project.completed_on)

        project.set_completed()

        self.t.clear_cache()

        project = self.t.get_project(name=test_name_temp)

        self.assertTrue(project.is_completed)
        self.assertIsNotNone(project.completed_on)

        project.delete()

        self.t.clear_cache()

        project = self.t.get_project(name=test_name_temp)

        self.assertIsNone(project)
