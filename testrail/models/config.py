#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

import testrail


class Configuration(object):
    """
    Configuration container.

    Attributes:
        id          -- (int) Unique configuration ID
        name        -- (str) Configuration name
        project     -- (Project) The project this configuration is applied to
        items       -- (dict) Values of configuration

    """
    def __init__(self, attributes):
        self.__id = attributes['id']
        self.__name = attributes['name']
        self.__project_id = attributes['project_id']
        self.__items = {}
        for c in attributes['configs']:
            self.__items[c['id']] = c['name']

    def __str__(self):
        return '<Configuration %s [%s]>' % (self.name, self.id)

    def __repr__(self):
        return self.__str__()

    ###########################################################################
    # Getters/Setters

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        raise RuntimeError('Attribute Configuration.id cannot be modified.')

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        raise RuntimeError('Attribute Configuration.name cannot be modified.')

    @property
    def project(self):
        return testrail.core.data.TestrailData.get_project_by_id(self.__project_id)

    @project.setter
    def project(self, value):
        raise RuntimeError('Attribute Configuration.project cannot be modified.')

    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, value):
        raise RuntimeError('Attribute Configuration.items cannot be modified.')




