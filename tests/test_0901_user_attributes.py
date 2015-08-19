#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import

import unittest
import platform
import datetime

import testrail
from tests.config import *

IS_PY3 = platform.python_version_tuple() >= ('3', '0')


class UserAttributes(unittest.TestCase):
    def setUp(self):
        self.t = testrail.Testrail(SERVER, USER, PASS)
        self.u = self.t.get_user(name='Spiridonov Vyacheslav')

    def test_user_id(self):
        self.assertIsNotNone(self.u.id)
        self.assertIsInstance(self.u.id, int)

        def change_id():
            self.u.id = 0

        self.assertRaises(RuntimeError, change_id)

    def test_user_name(self):
        self.assertIsNotNone(self.u.name)
        if IS_PY3:
            self.assertIsInstance(self.u.name, str)
        else:
            self.assertIsInstance(self.u.name, unicode)

        def change_name():
            self.u.name = u'asdf'

        self.assertRaises(RuntimeError, change_name)

    def test_user_email(self):
        self.assertIsNotNone(self.u.email)
        if IS_PY3:
            self.assertIsInstance(self.u.email, str)
        else:
            self.assertIsInstance(self.u.email, unicode)

        def change_email():
            self.u.email = u'asdf'

        self.assertRaises(RuntimeError, change_email)

    def test_user_is_active(self):
        self.assertIsNotNone(self.u.is_active)
        self.assertIsInstance(self.u.is_active, bool)

        def change_is_active():
            self.u.is_active = 0

        self.assertRaises(RuntimeError, change_is_active)

