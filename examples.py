#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

# one import to rule them all
from testrail import Testrail

# first thing to do is to configure where your testrail connection
t = Testrail('192.168.1.1:8080',
             user='someuser@domain.dom', password='somepassword')

################################################################################
# Basic usage