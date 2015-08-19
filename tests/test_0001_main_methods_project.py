#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import

import unittest
import datetime

import testrail
from tests.config import *


class MainQueryProject(unittest.TestCase):
    def setUp(self):
        self.t = testrail.Testrail(SERVER, USER, PASS)

    def test_get_all_projects(self):
        all_projects = self.t.get_projects()
        self.assertIsInstance(all_projects, list)
        for project in all_projects:
            self.assertIsInstance(project, testrail.models.Project)

    def test_get_completed_projects(self):
        all_projects = self.t.get_projects(True)
        self.assertIsInstance(all_projects, list)
        for project in all_projects:
            self.assertIsInstance(project, testrail.models.Project)
            self.assertTrue(project.is_completed)
            self.assertIsInstance(project.completed_on, datetime.datetime)

    def test_get_uncompleted_projects(self):
        all_projects = self.t.get_projects(False)
        self.assertIsInstance(all_projects, list)
        for project in all_projects:
            self.assertIsInstance(project, testrail.models.Project)
            self.assertFalse(project.is_completed)
            self.assertIsNone(project.completed_on)

    def test_get_project_by_id(self):
        project = self.t.get_project(3)
        self.assertIsInstance(project, testrail.models.Project)
        self.assertEqual(project.id, 3)

        project = self.t.get_project(project_id=8)
        self.assertIsInstance(project, testrail.models.Project)
        self.assertEqual(project.id, 8)

        project = self.t.get_project(3332233)
        self.assertIsNone(project)

    def test_get_project_by_name(self):
        project = self.t.get_project(name='zProject')
        self.assertIsInstance(project, testrail.models.Project)
        self.assertEqual(project.name, 'zProject')

        project = self.t.get_project(name='blablabla')
        self.assertIsNone(project)
