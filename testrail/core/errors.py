#!/usr/bin/env python
# -*- coding:  utf-8 -*-


class TestrailError(Exception):
    """
    Common class for all exceptions in this module
    """
    pass


class NotConfiguredError(TestrailError):
    """
    Will be raised when you make a request to server without configuring
    the connection.
    """
    pass


class NotFoundError(TestrailError):
    """
    Will be raised when request results to 400 code on server, meaning there is
    no object with requested parameters.
    """
    pass


class AuthenticationError(TestrailError):
    """
    Will be raised when request results to 401 code on server, meaning there are
    problems with username/password.
    """
    pass


class AccessError(TestrailError):
    """
    Will be raised when request results to 403 code on server, meaning you don`t
    have required permissions.
    """
    pass


class CompatibilityError(TestrailError):
    """
    Will be raised when you try to use methods and parameters from future versions.
    """
    pass


class ParameterFormatError(TestrailError):
    """
    Will be raised when you provide method parameter in wrong format.
    """
    pass