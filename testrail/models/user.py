#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function


class User(object):
    """
    User container.

    Attributes:
       id           -- (int) Unique user ID
       name         -- (str) Full name of the user
       email        -- (str) Email of the user
       is_active    -- (bool) True if the user is active and false otherwise
    """

    def __init__(self, attributes):
        self.__id = attributes['id']
        self.__name = attributes['name']
        self.__email = attributes['email']
        self.__is_active = attributes['is_active']

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '<User: %s [%s]>' % (self.name, self.id)

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
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        raise RuntimeError('Attribute Priority.email cannot be modified.')

    @property
    def is_active(self):
        return self.__is_active

    @is_active.setter
    def is_active(self, value):
        raise RuntimeError('Attribute Priority.is_active cannot be modified.')