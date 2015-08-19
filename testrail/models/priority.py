#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function


class Priority(object):
    """
    Priority of Test or Case: Blocker, Critical, Normal and others.

    Attributes:
        id           -- (int) Unique priority ID
        name         -- (str) Full name of the priority
        short_name   -- (str) Short name of the priority (used in tables)
        is_default   -- (bool) True if this priority is set by default in new test cases
        value        -- (int) Priority value
    """

    def __init__(self, attributes):
        self.__id = int(attributes['id'])
        self.__name = attributes['name']

        self.__short_name = attributes['short_name']
        self.__is_default = bool(attributes['is_default'])
        self.__value = int(attributes['priority'])

    def __str__(self):
        return '<Priority: %s [%s]>' % (self.short_name, self.id)

    def __repr__(self):
        return self.__str__()

    ###########################################################################
    # Getters/Setters

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        raise RuntimeError('Attribute Priority.id cannot be modified.')

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        raise RuntimeError('Attribute Priority.name cannot be modified.')

    @property
    def short_name(self):
        return self.__short_name

    @short_name.setter
    def short_name(self, value):
        raise RuntimeError('Attribute Priority.short_name cannot be modified.')

    @property
    def is_default(self):
        return self.__is_default

    @is_default.setter
    def is_default(self, value):
        raise RuntimeError('Attribute Priority.is_default cannot be modified.')

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        raise RuntimeError('Attribute Priority.value cannot be modified.')