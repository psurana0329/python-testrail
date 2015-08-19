#!/usr/bin/env python
# -*- coding:  utf-8 -*-
"""
"Be conservative in what you do, be liberal in what you accept from others." (c) Principle of robustness

Idea is to provide possibility for user to specify testrail object in different way. By ID, name or by providing
this module`s class.
"""

import time
import datetime

import testrail


def make_timestamp(parameter):
    """
    Testrail system wants all date/times to be UNIX timestamps.
    But it is not useful in scripts.

    This is a translator from most possible inputs to timestamp (as int).
    """
    if isinstance(parameter, datetime.datetime):
        return int(time.mktime(parameter.timetuple()))

    elif isinstance(parameter, time.struct_time):
        return int(time.mktime(parameter))

    elif isinstance(parameter, str):
        try:
            stamp = int(time.mktime(time.strptime(parameter, '%Y%m%d%H%M%S')))
        except ValueError:
            pass
        else:
            # python 3 is so flexible, that it interpret some timestamps as a date
            if stamp > 0:
                return stamp

        try:
            return int(time.mktime(time.localtime(int(parameter))))
        except ValueError:
            pass

    elif isinstance(parameter, int):
        try:
            return int(time.mktime(time.localtime(parameter)))
        except ValueError:
            pass

    elif isinstance(parameter, float):
        try:
            return int(time.mktime(time.localtime(int(parameter))))
        except ValueError:
            pass

    raise testrail.errors.ParameterFormatError('Cannot decode timestamp from %s' % parameter)


def guess_user_id(something):
    """
    User can be specified by:
        user ID
        user name
        user email
        Milestone object
    """
    if isinstance(something, testrail.models.User):
        return something.id
    elif isinstance(something, int):
        return something
    elif isinstance(something, str):
        try:
            return testrail.core.data.TestrailData.get_user_by_name(something).id
        except AttributeError:
            pass

        try:
            return testrail.core.data.TestrailData.get_user_by_email(something).id
        except AttributeError:
            pass

    raise testrail.errors.ParameterFormatError('Cannot find appropriate User: %s' % something)


def guess_milestone_id(project, something):
    """
    Milestone can be specified by:
        milestone ID
        milestone name
        Milestone object
    """
    if isinstance(something, testrail.models.Milestone):
        return something.id
    elif isinstance(something, int):
        return something
    elif isinstance(something, str):
        try:
            return project.get_milestone(something).id
        except AttributeError:
            pass

    raise testrail.errors.ParameterFormatError('Cannot find appropriate milestone. Got: %s' % something)


def guess_suite_id(project, something):
    """
    Suite can be specified by:
        suite ID
        suite name
        Suite object
    """
    if isinstance(something, testrail.models.Suite):
        return something.id
    elif isinstance(something, int):
        return something
    elif isinstance(something, str):
        try:
            return project.get_suite(something).id
        except AttributeError:
            pass

    raise testrail.errors.ParameterFormatError('Cannot find appropriate suite. Got: %s' % something)


def guess_case_id(something):
    """
    Case can be specified by:
        case ID
        Case object
    """
    if isinstance(something, testrail.models.Case):
        return something.id
    elif isinstance(something, int):
        return something

    raise testrail.errors.ParameterFormatError('Cannot find appropriate case. Got: %s' % something)


def guess_priority_id(something):
    """
    Priority can be specified by:
        priority ID
        priority name
        priority short name
        Priority object
    """
    if isinstance(something, testrail.models.Priority):
        return something.id
    elif isinstance(something, int):
        return something
    elif isinstance(something, str):
        try:
            return testrail.core.data.TestrailData.get_priority_by_name(something).id
        except AttributeError:
            pass

        try:
            return testrail.core.data.TestrailData.get_priority_by_short_name(something).id
        except AttributeError:
            pass

    raise testrail.errors.ParameterFormatError('Cannot find appropriate priority. Got: %s' % something)


def guess_case_type_id(something):
    """
    Case Type can be specified by:
        case type ID
        case type name
        CaseType object
    """
    if isinstance(something, testrail.models.CaseType):
        return something.id
    elif isinstance(something, int):
        return something
    elif isinstance(something, str):
        try:
            return testrail.core.data.TestrailData.get_case_type_by_name(something).id
        except AttributeError:
            pass

    raise testrail.errors.ParameterFormatError('Cannot find appropriate case type. Got: %s' % something)

