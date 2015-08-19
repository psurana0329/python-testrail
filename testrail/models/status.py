#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

import testrail


class Status(object):
    """
    Test Status: Passed, Failed, Blocked, Retest and custom.

    Attributes:
       id           -- (int) Unique test status ID
       name         -- (str) System name of the test status
       label        -- (str) Human name of status (used in web-interface)
       is_system    -- (bool) True if this is a system status
       is_untested  -- (bool) True if this status treated as 'Untested'
       is_final     -- (bool) True if this status treated as 'Final'
       color_bright -- (str) Interface color (see docs.)
       color_medium -- (str) Interface color (see docs.)
       color_dark   -- (str) Interface color (see docs.)
    """

    def __init__(self, attributes):
        self.__id = attributes['id']
        self.__name = attributes['name']

        self.__label = attributes['label']
        self.__is_system = attributes['is_system']
        self.__is_untested = attributes['is_untested']
        self.__is_final = attributes['is_final']

        self.__color_bright = int(attributes['color_bright'])
        self.__color_medium = int(attributes['color_medium'])
        self.__color_dark = int(attributes['color_dark'])

    def __str__(self):
        return '<Status: %s [%s]>' % (self.label, self.id)

    def __repr__(self):
        return self.__str__()

    ###########################################################################
    # Getters/Setters

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        raise RuntimeError('Attribute Status.id cannot be modified.')

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        raise RuntimeError('Attribute Status.name cannot be modified.')

    @property
    def label(self):
        return self.__label

    @label.setter
    def label(self, value):
        raise RuntimeError('Attribute Status.label cannot be modified.')

    @property
    def is_system(self):
        return self.__is_system

    @is_system.setter
    def is_system(self, value):
        raise RuntimeError('Attribute Status.is_system cannot be modified.')

    @property
    def is_untested(self):
        return self.__is_untested

    @is_untested.setter
    def is_untested(self, value):
        raise RuntimeError('Attribute Status.is_untested cannot be modified.')

    @property
    def is_final(self):
        return self.__is_final

    @is_final.setter
    def is_final(self, value):
        raise RuntimeError('Attribute Status.is_final cannot be modified.')

    @property
    def color_bright(self):
        return self.__color_bright

    @color_bright.setter
    def color_bright(self, value):
        raise RuntimeError('Attribute Status.color_bright cannot be modified.')

    @property
    def color_medium(self):
        return self.__color_medium

    @color_medium.setter
    def color_medium(self, value):
        raise RuntimeError('Attribute Status.color_medium cannot be modified.')

    @property
    def color_dark(self):
        return self.__color_dark

    @color_dark.setter
    def color_dark(self, value):
        raise RuntimeError('Attribute Status.color_dark cannot be modified.')




