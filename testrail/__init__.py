#!/usr/bin/env python
# -*- coding:  utf-8 -*-
"""
Docstring.

Note about time zones:
    Testrail uses server timezone to produce timestamps. And since
    there is no obvious way to get information about server timezone via API,
    times may be inaccurate.
    This module uses localtime everywhere in hope that server timezone match
    local computer one. I think it is quite common through installations.
"""

from __future__ import absolute_import
from __future__ import print_function

__author__ = 'Vyacheslav Spiridonov'

__version__ = '0.2.0'
__maintainer__ = 'Vyacheslav Spiridonov'
__email__ = 'namelessorama@gmail.com'
__status__ = 'Development'

import sys


import testrail.core
import testrail.core.errors as errors
import testrail.models

from testrail.core.main import Testrail


# Projects A
# Milestones A
# Suites A
# Sections A
# Cases A
#
# Custom Fields A
# Case Types A
# Priorities A
# Users A
#
# Configurations A
# Plans A
# Runs A
# Tests A
#
# Results
# Statuses


