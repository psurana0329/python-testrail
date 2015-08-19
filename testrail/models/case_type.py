#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function


class CaseType(object):
    """
    Case Type: Functionality, Performance, Stress, etc...

    Attributes:
       id           -- (int) Unique case type ID
       name         -- (str) Case type name
       is_default   -- (bool) True if this type is set by default in new test cases
    """
    def __init__(self, attributes):
        self.__id = int(attributes['id'])
        self.__name = attributes['name']
        self.__is_default = bool(attributes['is_default'])

    def __str__(self):
        return '<CaseType: %s [%s]>' % (self.name, self.id)

    def __repr__(self):
        return self.__str__()

    ###########################################################################
    # Getters/Setters

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        raise RuntimeError('Attribute CaseType.id cannot be modified.')

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        raise RuntimeError('Attribute CaseType.name cannot be modified.')

    @property
    def is_default(self):
        return self.__is_default

    @is_default.setter
    def is_default(self, value):
        raise RuntimeError('Attribute CaseType.is_default cannot be modified.')