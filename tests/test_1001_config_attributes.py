#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import

import unittest
import platform
import datetime

import testrail
from tests.config import *

IS_PY3 = platform.python_version_tuple() >= ('3', '0')


class ConfigurationAttributes(unittest.TestCase):
    def setUp(self):
        self.t = testrail.Testrail(SERVER, USER, PASS)
        self.p = self.t.get_project(name=TEST_PROJECT_NAME)
        self.cfg = self.p.get_configurations()[0]

    def test_config_id(self):
        self.assertIsNotNone(self.cfg.id)
        self.assertIsInstance(self.cfg.id, int)

        def change_id():
            self.cfg.id = 0

        self.assertRaises(RuntimeError, change_id)

    def test_config_project(self):
        self.assertIsNotNone(self.cfg.project)
        self.assertIsInstance(self.cfg.project, testrail.models.Project)

        def change_project():
            self.cfg.project = None

        self.assertRaises(RuntimeError, change_project)

    def test_config_name(self):
        self.assertIsNotNone(self.cfg.name)
        if IS_PY3:
            self.assertIsInstance(self.cfg.name, str)
        else:
            self.assertIsInstance(self.cfg.name, unicode)

        def change_name():
            self.cfg.name = u'asdf'

        self.assertRaises(RuntimeError, change_name)

    def test_config_items(self):
        self.assertIsNotNone(self.cfg.items)
        self.assertIsInstance(self.cfg.items, dict)

        def change_items():
            self.cfg.items = None

        self.assertRaises(RuntimeError, change_items)

    def test_config_string(self):
        self.assertIsNotNone(str(self.cfg))
        self.assertIsNotNone(repr(self.cfg))








