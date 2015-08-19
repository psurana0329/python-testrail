#!/usr/bin/env python
# -*- coding:  utf-8 -*-
"""
Welcome to actual API calls.

This module do nothing more than implements urls specified in Testrail Docs.
"""

from __future__ import absolute_import
from __future__ import print_function


import testrail.core.errors as errors


############################################################################
# We gonna provide version compatibility
def since(version_string):
    version_tuple = version_string.split('.')

    def get_version_protected_api_call(method):

        def version_protected_api_call(self, *args, **kwargs):
            if self.compatibility >= version_tuple:
                return method(self, *args, **kwargs)
            else:
                raise errors.CompatibilityError("Method %s is unavailable due to your Testrail version limitations. "
                                                "Minimum required version is %s (you have %s)." % (method.__name__,
                                                                                                   '.'.join(version_tuple),
                                                                                                   '.'.join(self.compatibility)))

        return version_protected_api_call

    return get_version_protected_api_call


def new_parameter(version_string, parameter_name):
    version_tuple = version_string.split('.')

    def get_version_protected_api_call(method):

        def version_protected_api_call(self, *args, **kwargs):
            if self.compatibility >= version_tuple:
                return method(self, *args, **kwargs)
            else:
                if parameter_name in kwargs:
                    raise errors.CompatibilityError("Parameter '%s' in method '%s' is unavailable due to your "
                                                    "Testrail version limitations. "
                                                    "Minimum required version is %s (you have %s)." % (
                                                        parameter_name,
                                                        method.__name__,
                                                        '.'.join(version_tuple),
                                                        '.'.join(self.compatibility)
                                                    ))
                else:
                    method(self, *args, **kwargs)

        return version_protected_api_call

    return get_version_protected_api_call


def encode(**kwargs):
    pattern = ''
    for k, v in kwargs.items():
        if isinstance(v, list) or isinstance(v, tuple):
            pattern += '&%s=%s' % (k, ','.join([str(i) for i in v]))
        elif isinstance(v, bool):
            pattern += '&%s=%s' % (k, int(v))
        elif v is None:
            pass
        else:
            pattern += '&%s=%s' % (k, v)

    return pattern


class TestrailAPI(object):

    def __init__(self, connection, version=None):

        self.connection = connection
        self.compatibility = version.split('.')

    ############################################################################
    # Users
    # http://docs.gurock.com/testrail-api2/reference-users

    @since('3.0')
    def get_user(self, user_id):
        return self.connection.get('get_user/%s' % user_id)

    @since('3.0')
    def get_user_by_email(self, email):
        return self.connection.get('get_user_by_email&email=%s' % email)

    @since('3.0')
    def get_users(self):
        return self.connection.get('get_users')

    ############################################################################
    # Priorities
    # http://docs.gurock.com/testrail-api2/reference-priorities

    @since('3.0')
    def get_priorities(self):
        return self.connection.get('get_priorities')

    ############################################################################
    # Statuses
    # http://docs.gurock.com/testrail-api2/reference-statuses

    @since('3.0')
    def get_statuses(self):
        return self.connection.get('get_statuses')

    ############################################################################
    # Case Types
    # http://docs.gurock.com/testrail-api2/reference-cases-types

    @since('3.0')
    def get_case_types(self):
        return self.connection.get('get_case_types')

    ############################################################################
    # Case Fields
    # http://docs.gurock.com/testrail-api2/reference-cases-fields

    @since('3.0')
    def get_case_fields(self):
        return self.connection.get('get_case_fields')

    ############################################################################
    # Result Fields
    # http://docs.gurock.com/testrail-api2/reference-results-fields

    @since('3.0')
    def get_result_fields(self):
        return self.connection.get('get_result_fields')

    ############################################################################
    # Projects
    # http://docs.gurock.com/testrail-api2/reference-projects

    @since('3.0')
    def get_project(self, project_id):
        return self.connection.get('get_project/%s' % project_id)

    @since('3.0')
    def get_projects(self, is_completed=None):
        pattern = 'get_projects'

        if is_completed is not None:
            pattern += '&is_completed=%s' % int(is_completed)

        return self.connection.get(pattern)

    @since('3.0')
    @new_parameter('4.0', 'suite_mode')
    def add_project(self, **kwargs):
        return self.connection.post('add_project', data=kwargs)

    @since('3.0')
    @new_parameter('4.0', 'suite_mode')
    def update_project(self, project_id, **kwargs):
        return self.connection.post('update_project/%s' % project_id, data=kwargs)

    @since('3.0')
    def delete_project(self, project_id):
        return self.connection.post('delete_project/%s' % project_id)

    ############################################################################
    # Milestones
    # http://docs.gurock.com/testrail-api2/reference-milestones

    @since('3.0')
    def get_milestone(self, milestone_id):
        return self.connection.get('get_milestone/%s' % milestone_id)

    @since('3.0')
    def get_milestones(self, project_id, is_completed=None):
        pattern = 'get_milestones/%s' % project_id

        if is_completed is not None:
            pattern += '&is_completed=%s' % int(is_completed)

        return self.connection.get(pattern)

    @since('3.0')
    def add_milestone(self, project_id, **kwargs):
        return self.connection.post('add_milestone/%s' % project_id, data=kwargs)

    @since('3.0')
    def update_milestone(self, milestone_id, **kwargs):
        return self.connection.post('update_milestone/%s' % milestone_id, data=kwargs)

    @since('3.0')
    def delete_milestone(self, milestone_id):
        return self.connection.post('delete_milestone/%s' % milestone_id)

    ############################################################################
    # Suites
    # http://docs.gurock.com/testrail-api2/reference-suites

    @since('3.0')
    def get_suite(self, suite_id):
        return self.connection.get('get_suite/%s' % suite_id)

    @since('3.0')
    def get_suites(self, project_id):
        return self.connection.get('get_suites/%s' % project_id)

    @since('3.0')
    def add_suite(self, project_id, **kwargs):
        return self.connection.post('add_suite/%s' % project_id, data=kwargs)

    @since('3.0')
    def update_suite(self, suite_id, **kwargs):
        return self.connection.post('update_suite/%s' % suite_id, data=kwargs)

    @since('3.0')
    def delete_suite(self, suite_id):
        return self.connection.post('delete_suite/%s' % suite_id)

    ############################################################################
    # Sections
    # http://docs.gurock.com/testrail-api2/reference-sections

    @since('3.0')
    def get_section(self, section_id):
        return self.connection.get('get_section/%s' % section_id)

    @since('3.0')
    def get_sections(self, project_id, suite_id):
        return self.connection.get('get_sections/%s&suite_id=%s' % (project_id, suite_id))

    @since('3.0')
    @new_parameter('4.0', 'description')
    def add_section(self, project_id, **kwargs):
        return self.connection.post('add_section/%s' % project_id, data=kwargs)

    @since('3.0')
    @new_parameter('4.0', 'description')
    def update_section(self, section_id, **kwargs):
        return self.connection.post('update_section/%s' % section_id, data=kwargs)

    @since('3.0')
    def delete_section(self, section_id):
        return self.connection.post('delete_section/%s' % section_id)

    ############################################################################
    # Cases
    # http://docs.gurock.com/testrail-api2/reference-cases

    @since('3.0')
    def get_case(self, case_id):
        return self.connection.get('get_case/%s' % case_id)

    @since('3.0')
    @new_parameter('4.0', 'created_after')
    @new_parameter('4.0', 'created_before')
    @new_parameter('4.0', 'created_by')
    @new_parameter('4.0', 'milestone_id')
    @new_parameter('4.0', 'priority_id')
    @new_parameter('4.0', 'type_id')
    @new_parameter('4.0', 'updated_after')
    @new_parameter('4.0', 'updated_before')
    @new_parameter('4.0', 'updated_by')
    def get_cases(self, project_id, **kwargs):
        pattern = 'get_cases/%s' % project_id

        pattern += encode(**kwargs)

        return self.connection.get(pattern)

    @since('3.0')
    def add_case(self, section_id, **kwargs):
        return self.connection.post('add_case/%s' % section_id, data=kwargs)

    @since('3.0')
    def update_case(self, case_id, **kwargs):
        return self.connection.post('update_case/%s' % case_id, data=kwargs)

    @since('3.0')
    def delete_case(self, case_id):
        return self.connection.post('delete_case/%s' % case_id)

    ############################################################################
    # Configurations
    # http://docs.gurock.com/testrail-api2/reference-configs

    @since('3.1')
    def get_configs(self, project_id):
        return self.connection.get('get_configs/%s' % project_id)

    ############################################################################
    # Plans
    # http://docs.gurock.com/testrail-api2/reference-plans

    @since('3.0')
    def get_plan(self, plan_id):
        return self.connection.get('get_plan/%s' % plan_id)

    @since('3.0')
    @new_parameter('4.0', 'created_after')
    @new_parameter('4.0', 'created_before')
    @new_parameter('4.0', 'created_by')
    @new_parameter('4.0', 'milestone_id')
    @new_parameter('4.0', 'is_completed')
    @new_parameter('4.0', 'limit')
    @new_parameter('4.0', 'offset')
    def get_plans(self, project_id, **kwargs):
        pattern = 'get_plans/%s' % project_id

        pattern += encode(**kwargs)

        return self.connection.get(pattern)

    @since('3.0')
    def add_plan(self, project_id, **kwargs):
        return self.connection.post('add_plan/%s' % project_id, data=kwargs)

    @since('3.0')
    def add_plan_entry(self, plan_id, **kwargs):
        return self.connection.post('add_plan_entry/%s' % plan_id, data=kwargs)

    @since('3.0')
    def update_plan(self, plan_id, **kwargs):
        """
        Same fields as _add_plan
        """
        return self.connection.post('update_plan/%s' % plan_id, data=kwargs)

    @since('3.0')
    def update_plan_entry(self, plan_id, entry_id, **kwargs):
        return self.connection.post('update_plan_entry/%s/%s' % (plan_id, entry_id), data=kwargs)

    @since('3.0')
    def close_plan(self, plan_id):
        return self.connection.post('close_plan/%s' % plan_id)

    @since('3.0')
    def delete_plan(self, plan_id):
        return self.connection.post('delete_plan/%s' % plan_id)

    @since('3.0')
    def delete_plan_entry(self, plan_id, entry_id):
        return self.connection.post('delete_plan_entry/%s/%s' % (plan_id, entry_id))

    ############################################################################
    # Runs
    # http://docs.gurock.com/testrail-api2/reference-runs

    @since('3.0')
    def get_run(self, run_id):
        return self.connection.get('get_run/%s' % run_id)

    @since('3.0')
    @new_parameter('4.0', 'created_after')
    @new_parameter('4.0', 'created_before')
    @new_parameter('4.0', 'created_by')
    @new_parameter('4.0', 'milestone_id')
    @new_parameter('4.0', 'suite_id')
    @new_parameter('4.0', 'is_completed')
    @new_parameter('4.0', 'limit')
    @new_parameter('4.0', 'offset')
    def get_runs(self, project_id, **kwargs):
        pattern = 'get_runs/%s' % project_id

        pattern += encode(**kwargs)

        return self.connection.get(pattern)

    @since('3.0')
    def add_run(self, project_id, **kwargs):
        return self.connection.post('add_run/%s' % project_id, data=kwargs)

    @since('3.0')
    def update_run(self, run_id, **kwargs):
        return self.connection.post('update_run/%s' % run_id, data=kwargs)

    @since('3.0')
    def close_run(self, run_id):
        return self.connection.post('close_run/%s' % run_id)

    @since('3.0')
    def delete_run(self, run_id):
        return self.connection.post('delete_run/%s' % run_id)

    ############################################################################
    # Tests
    # http://docs.gurock.com/testrail-api2/reference-tests

    @since('3.0')
    def get_test(self, test_id):
        return self.connection.get('get_test/%s' % test_id)

    @since('3.0')
    def get_tests(self, run_id, **kwargs):
        pattern = 'get_tests/%s' % run_id

        pattern += encode(**kwargs)

        return self.connection.get(pattern)

    ############################################################################
    # Results
    # http://docs.gurock.com/testrail-api2/reference-results

    @since('3.0')
    def get_results(self, test_id, limit=None, offset=None, status_id=None):
        pattern = 'get_results/%s' % test_id

        if limit is not None:
            pattern += '&limit=%s' % limit

        if offset is not None:
            pattern += '&offset=%s' % offset

        if status_id is not None:
            pattern += '&status_id=%s' % ','.join(status_id)

        return self.connection.get(pattern)

    @since('3.0')
    def get_results_for_case(self, run_id, case_id, limit=None,
                             offset=None, status_id=None):
        pattern = 'get_results_for_case/%s/%s' % (run_id, case_id)

        if limit is not None:
            pattern += '&limit=%s' % limit

        if offset is not None:
            pattern += '&offset=%s' % offset

        if status_id is not None:
            pattern += '&status_id=%s' % ','.join(status_id)

        return self.connection.get(pattern)

    @since('4.0')
    def get_results_for_run(self, run_id, created_after=None,
                            created_before=None, created_by=None, limit=None,
                            offset=None, status_id=None):
        pattern = 'get_results_for_run/%s' % run_id

        if created_after is not None:
            pattern += '&created_after=%s' % created_after

        if created_before is not None:
            pattern += '&created_before=%s' % created_before

        if created_by is not None:
            pattern += '&created_by=%s' % ','.join(created_by)

        if limit is not None:
            pattern += '&limit=%s' % limit

        if offset is not None:
            pattern += '&offset=%s' % offset

        if status_id is not None:
            pattern += '&status_id=%s' % ','.join(status_id)

        return self.connection.get(pattern)

    @since('3.0')
    def add_result(self, test_id, **kwargs):
        return self.connection.post('add_result/%s' % test_id, data=kwargs)

    @since('3.0')
    def add_result_for_case(self, run_id, case_id, **kwargs):
        return self.connection.post('add_result_for_case/%s/%s' % (run_id, case_id), data=kwargs)

    @since('3.0')
    def add_results(self, run_id, **kwargs):
        return self.connection.post('add_results/%s' % run_id, data=kwargs)

    @since('3.0')
    def add_results_for_cases(self, run_id, **kwargs):
        return self.connection.post('add_results_for_cases/%s' % run_id, data=kwargs)


