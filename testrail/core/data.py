#!/usr/bin/env python
# -*- coding:  utf-8 -*-
"""
Data modeling and cache layer.
"""

from __future__ import absolute_import
from __future__ import print_function

from datetime import datetime

from testrail.core.api import TestrailAPI

import testrail.core.errors as errors
import testrail.models as models


class TestrailCache(object):
    """
    'Key -> value' cache.

    Cache key construction convention:
        key="<class_name>:<request_parameters>"
        request_parameters="parameter1=value1,parameter2=value2,..." , where parameters are sorted in alphabetical order
        see 'TestrailData.cache_or_call' method
    """
    def __init__(self, max_cache_age_seconds):
        self.storage = {}
        self.max_age = max_cache_age_seconds

    def store(self, key, obj):
        self.storage[key] = {
            'object': obj,
            'birthday': datetime.now()
        }
        print('Cache store: %s = %s' % (key, obj))  # debug

    def get(self, key):
        # get record
        try:
            record = self.storage[key]
        except KeyError:
            return None
        else:
            # check expiration
            if (datetime.now() - record['birthday']).seconds > self.max_age:
                del self.storage[key]
                print('Cache expired: %s' % key)  # debug
                return None
            else:
                return record['object']

    def wipe(self, key):
        try:
            del self.storage[key]
            print('Cache wipe: %s' % key)  # debug
        except KeyError:
            pass

    def wipe_all(self):
        print('Cache full wipe')  # debug
        self.storage = {}


class GentleFuckOff:
    """
    This is a stub to protect from faceless AttributeError throw, when
    you try to access methods before configuring connection.
    """
    def __init__(self):
        pass

    def __getattr__(self, item):
        raise errors.NotConfiguredError('Cannot access TestrailData. Have you configured your connection?')


class TestrailData(object):
    """
    Provides access to Testrail data.
    Manages cache.
    Convert json to models.
    """

    api = GentleFuckOff()
    cache = TestrailCache(max_cache_age_seconds=20)  # TODO: add config file for max_cache_age

    def __init__(self, connection, version):
        TestrailData.api = TestrailAPI(connection, version)

    @staticmethod
    def _cache_or_call(class_object, method, **kwargs):
        key = '%s:%s' % (class_object.__name__, ','.join(['%s=%s' % (k, kwargs[k]) for k in sorted(kwargs.keys())]))

        print('Cache query: %s' % key)  # debug
        result = TestrailData.cache.get(key)
        if result is None:
            print('Cache miss')  # debug
            try:
                data = method(**kwargs)
            except errors.NotFoundError:
                return None

            if isinstance(data, list):
                result = [class_object(d) for d in data]
                for r in result:
                    single_key = '%s:%s_id=%s' % (class_object.__name__, class_object.__name__.lower(), r.id)
                    TestrailData.cache.store(single_key, r)

            else:
                result = class_object(data)

            TestrailData.cache.store(key, result)

        else:
            print('Cache hit')  # debug

        return result

    @staticmethod
    def _store_in_cache(instance, **kwargs):
        key = '%s:%s' % (instance.__class__.__name__, ','.join(['%s=%s' % (k, kwargs[k]) for k in sorted(kwargs.keys())]))
        TestrailData.cache.store(key, instance)

    @staticmethod
    def _remove_from_cache(class_object, **kwargs):
        key = '%s:%s' % (class_object.__name__, ','.join(['%s=%s' % (k, kwargs[k]) for k in sorted(kwargs.keys())]))
        TestrailData.cache.wipe(key)

    @staticmethod
    def clear_cache():
        TestrailData.cache.wipe_all()

    ############################################################################
    #
    # Projects methods
    #
    ############################################################################

    @staticmethod
    def get_project_by_id(project_id):
        """
        :type project_id: int
        :rtype: testrail.models.Project
        """
        return TestrailData._cache_or_call(
            models.Project,
            TestrailData.api.get_project,
            project_id=project_id
        )

    @staticmethod
    def get_project_by_name(project_name):
        """
        :type project_name: str
        :rtype: testrail.models.Project
        """
        for p in TestrailData.get_projects(None):
            if p.name == project_name:
                return p
        return None

    @staticmethod
    def get_projects(is_completed):
        """
        :type is_completed: bool or None
        :rtype: list of [testrail.models.Project]
        """
        projects = TestrailData._cache_or_call(
            models.Project,
            TestrailData.api.get_projects
        )

        if is_completed is None:
            return projects
        elif is_completed:
            return [p for p in projects if p.is_completed]
        else:
            return [p for p in projects if not p.is_completed]

    @staticmethod
    def add_project(**parameters):
        """
        :rtype: testrail.models.Project
        """
        new_project = models.Project(TestrailData.api.add_project(**parameters))
        TestrailData._store_in_cache(new_project, project_id=new_project.id)
        return new_project

    @staticmethod
    def update_project(project_id, **parameters):
        """
        :type project_id: int
        :rtype: testrail.models.Project
        """
        updated_project = models.Project(TestrailData.api.update_project(project_id, **parameters))
        TestrailData._store_in_cache(updated_project, project_id=updated_project.id)
        return updated_project

    @staticmethod
    def delete_project(project_id):
        """
        :type project_id: int
        :rtype: None
        """
        TestrailData.api.delete_project(project_id)
        TestrailData._remove_from_cache(models.Project, project_id=project_id)

    ############################################################################
    #
    # Milestones methods
    #
    ############################################################################

    @staticmethod
    def get_milestone_by_id(milestone_id):
        """
        :type milestone_id: int
        :rtype: testrail.models.Milestone
        """
        return TestrailData._cache_or_call(
            models.Milestone,
            TestrailData.api.get_milestone,
            milestone_id=milestone_id
        )

    @staticmethod
    def get_milestones(project_id, is_completed):
        """
        :type is_completed: bool or None
        :rtype: list of [testrail.models.Milestone]
        """
        result = TestrailData._cache_or_call(
            models.Milestone,
            TestrailData.api.get_milestones,
            project_id=project_id
        )

        if is_completed is None:
            return result
        elif is_completed:
            return [m for m in result if m.is_completed]
        else:
            return [m for m in result if not m.is_completed]

    @staticmethod
    def add_milestone(project_id, **parameters):
        """
        :rtype: testrail.models.Milestone
        """
        new_milestone = models.Milestone(TestrailData.api.add_milestone(project_id, **parameters))
        TestrailData._store_in_cache(new_milestone, milestone_id=new_milestone.id)
        return new_milestone

    @staticmethod
    def update_milestone(milestone_id, **parameters):
        """
        :rtype: testrail.models.Milestone
        """
        updated_milestone = models.Milestone(TestrailData.api.update_milestone(milestone_id, **parameters))
        TestrailData._store_in_cache(updated_milestone, milestone_id=updated_milestone.id)
        return updated_milestone

    @staticmethod
    def delete_milestone(milestone_id):
        """
        :type milestone_id: int
        :rtype: None
        """
        TestrailData.api.delete_milestone(milestone_id)
        TestrailData._remove_from_cache(models.Milestone, milestone_id=milestone_id)

    ############################################################################
    #
    # Suites methods
    #
    ############################################################################

    @staticmethod
    def get_suite_by_id(suite_id):
        """
        :type suite_id: int
        :rtype: testrail.models.Suite
        """
        return TestrailData._cache_or_call(
            models.Suite,
            TestrailData.api.get_suite,
            suite_id=suite_id
        )

    @staticmethod
    def get_suites(project_id):
        """
        :type project_id: int
        :rtype: list of [testrail.models.Suite]
        """
        return TestrailData._cache_or_call(
            models.Suite,
            TestrailData.api.get_suites,
            project_id=project_id
        )

    @staticmethod
    def add_suite(project_id, **parameters):
        """
        :rtype: testrail.models.Suite
        """
        new_suite = models.Suite(TestrailData.api.add_suite(project_id, **parameters))
        TestrailData._store_in_cache(new_suite, suite_id=new_suite.id)
        return new_suite

    @staticmethod
    def update_suite(suite_id, **parameters):
        """
        :rtype: testrail.models.Suite
        """
        updated_suite = models.Suite(TestrailData.api.update_suite(suite_id, **parameters))
        TestrailData._store_in_cache(updated_suite, suite_id=updated_suite.id)
        return updated_suite

    @staticmethod
    def delete_suite(suite_id):
        """
        :type suite_id: int
        :rtype: None
        """
        TestrailData.api.delete_suite(suite_id)
        TestrailData._remove_from_cache(models.Suite, suite_id=suite_id)

    ############################################################################
    #
    # Sections methods
    #
    ############################################################################

    @staticmethod
    def get_section_by_id(section_id):
        """
        :type section_id: int
        :rtype: testrail.models.Section
        """
        return TestrailData._cache_or_call(
            models.Section,
            TestrailData.api.get_section,
            section_id=section_id
        )

    @staticmethod
    def get_sections(project_id, suite_id):
        """
        :type project_id: int
        :type suite_id: int
        :rtype: list of [testrail.models.Section]
        """
        return TestrailData._cache_or_call(
            models.Section,
            TestrailData.api.get_sections,
            project_id=project_id,
            suite_id=suite_id
        )

    @staticmethod
    def add_section(project_id, **parameters):
        """
        :type project_id: int
        :rtype: testrail.models.Section
        """
        new_section = models.Section(TestrailData.api.add_section(project_id, **parameters))
        TestrailData._store_in_cache(new_section, section_id=new_section.id)
        return new_section

    @staticmethod
    def update_section(section_id, **parameters):
        """
        :type section_id: int
        :rtype: testrail.models.Section
        """
        updated_section = models.Section(TestrailData.api.update_section(section_id, **parameters))
        TestrailData._store_in_cache(updated_section, section_id=updated_section.id)
        return updated_section

    @staticmethod
    def delete_section(section_id):
        """
        :type section_id: int
        :rtype: None
        """
        TestrailData.api.delete_section(section_id)
        TestrailData._remove_from_cache(models.Section, section_id=section_id)

    ############################################################################
    #
    # Cases methods
    #
    ############################################################################

    @staticmethod
    def get_case_by_id(case_id):
        """
        :type case_id: int
        :rtype: testrail.models.Case
        """
        return TestrailData._cache_or_call(
            models.Case,
            TestrailData.api.get_case,
            case_id=case_id
        )

    @staticmethod
    def get_cases(project_id, suite_id, section_id=None, **filters):
        """
        :type project_id: int
        :type suite_id: int
        :type section_id: int
        :rtype: list of [testrail.models.Case]
        """
        return TestrailData._cache_or_call(
            models.Case,
            TestrailData.api.get_cases,
            project_id=project_id,
            suite_id=suite_id,
            section_id=section_id,
            **filters
        )

    @staticmethod
    def add_case(section_id, **parameters):
        """
        :type section_id: int
        :rtype: testrail.models.Case
        """
        new_case = models.Case(TestrailData.api.add_case(section_id, **parameters))
        TestrailData._store_in_cache(new_case, case_id=new_case.id)
        return new_case

    @staticmethod
    def update_case(case_id, **parameters):
        """
        :type section_id: int
        :rtype: testrail.models.Case
        """
        updated_case = models.Case(TestrailData.api.update_case(case_id, **parameters))
        TestrailData._store_in_cache(updated_case, case_id=updated_case.id)
        return updated_case

    @staticmethod
    def delete_case(case_id):
        """
        :type case_id: int
        :rtype: None
        """
        TestrailData.api.delete_case(case_id)
        TestrailData._remove_from_cache(models.Case, case_id=case_id)

    ############################################################################
    #
    # Case Fields methods
    #
    ############################################################################

    @staticmethod
    def get_case_fields():
        """
        :rtype: list of [testrail.models.CaseField]
        """
        return TestrailData._cache_or_call(
            models.CaseField,
            TestrailData.api.get_case_fields
        )

    ############################################################################
    #
    # Result Fields methods
    #
    ############################################################################

    @staticmethod
    def get_result_fields():
        """
        :rtype: list of [testrail.models.ResultField]
        """
        return TestrailData._cache_or_call(
            models.ResultField,
            TestrailData.api.get_result_fields
        )

    ############################################################################
    #
    # Case Types methods
    #
    ############################################################################

    @staticmethod
    def get_case_type_by_id(case_type_id):
        """
        :type case_type_id: int
        :rtype: testrail.models.CaseType or None
        """
        for case_type in TestrailData.get_case_types():
            if case_type.id == case_type_id:
                return case_type

        return None

    @staticmethod
    def get_case_type_by_name(case_type_name):
        """
        :type case_type_name: str
        :rtype: testrail.models.CaseType or None
        """
        for case_type in TestrailData.get_case_types():
            if case_type.name == case_type_name:
                return case_type

        return None

    @staticmethod
    def get_case_types():
        """
        :rtype: list of [testrail.models.CaseType]
        """
        return TestrailData._cache_or_call(
            models.CaseType,
            TestrailData.api.get_case_types
        )

    @staticmethod
    def get_default_case_type():
        """
        :rtype: testrail.models.CaseType
        """
        for case_type in TestrailData.get_case_types():
            if case_type.is_default:
                return case_type

        return None

    ############################################################################
    #
    # Priorities methods
    #
    ############################################################################

    @staticmethod
    def get_priority_by_id(priority_id):
        """
        :type priority_id: int
        :rtype: testrail.models.Priority or None
        """
        for priority in TestrailData.get_priorities():
            if priority.id == priority_id:
                return priority

        return None

    @staticmethod
    def get_priority_by_name(priority_name):
        """
        :type priority_name: str
        :rtype: testrail.models.Priority or None
        """
        for priority in TestrailData.get_priorities():
            if priority.name == priority_name:
                return priority

        return None

    @staticmethod
    def get_priority_by_short_name(priority_short_name):
        """
        :type priority_short_name: str
        :rtype: testrail.models.Priority or None
        """
        for priority in TestrailData.get_priorities():
            if priority.short_name == priority_short_name:
                return priority

        return None

    @staticmethod
    def get_priority_by_value(priority_value):
        """
        :type priority_value: int
        :rtype: testrail.models.Priority or None
        """
        for priority in TestrailData.get_priorities():
            if priority.priority == priority_value:
                return priority

        return None

    @staticmethod
    def get_priorities():
        """
        :rtype: list of [testrail.models.Priority]
        """
        return TestrailData._cache_or_call(
            models.Priority,
            TestrailData.api.get_priorities
        )

    @staticmethod
    def get_default_priority():
        """
        :rtype: testrail.models.Priority
        """
        for priority in TestrailData.get_priorities():
            if priority.is_default:
                return priority

        return None

    ############################################################################
    #
    # Users methods
    #
    ############################################################################

    @staticmethod
    def get_user_by_id(user_id):
        """
        :type user_id: int
        :rtype: testrail.models.User
        """
        return TestrailData._cache_or_call(
            models.User,
            TestrailData.api.get_user,
            user_id=user_id
        )

    @staticmethod
    def get_user_by_name(user_name):
        """
        :type user_name: str
        :rtype: testrail.models.User
        """
        for user in TestrailData.get_users(None):
            if user.name == user_name:
                return user

        return None

    @staticmethod
    def get_user_by_email(user_email):
        """
        :type user_email: str
        :rtype: testrail.models.User
        """
        for user in TestrailData.get_users(None):
            if user.email == user_email:
                return user

        return None

    @staticmethod
    def get_users(is_active):
        """
        :type is_active: bool
        :rtype: list of [testrail.models.Priority]
        """
        result = TestrailData._cache_or_call(
            models.User,
            TestrailData.api.get_users
        )

        if is_active is None:
            return result
        elif is_active:
            return [u for u in result if u.is_active]
        else:
            return [u for u in result if not u.is_active]

    ############################################################################
    #
    # Plans methods
    #
    ############################################################################

    @staticmethod
    def get_plan_by_id(plan_id):
        """
        :type plan_id: int
        :rtype: testrail.models.Plan
        """
        return TestrailData._cache_or_call(
            models.Plan,
            TestrailData.api.get_plan,
            plan_id=plan_id
        )

    @staticmethod
    def get_plans(project_id, **filters):
        """
        :type project_id: int
        :rtype: list of [testrail.models.Plan]
        """
        return TestrailData._cache_or_call(
            models.Plan,
            TestrailData.api.get_plans,
            project_id=project_id,
            **filters
        )

    @staticmethod
    def add_plan(project_id, **parameters):
        """
        :type project_id: int
        :rtype: testrail.models.Plan
        """
        new_plan = models.Case(TestrailData.api.add_plan(project_id, **parameters))
        TestrailData._store_in_cache(new_plan, plan_id=new_plan.id)
        return new_plan

    @staticmethod
    def update_plan(plan_id, **parameters):
        """
        :type plan_id: int
        :rtype: testrail.models.Plan
        """
        updated_plan = models.Case(TestrailData.api.update_plan(plan_id, **parameters))
        TestrailData._store_in_cache(updated_plan, plan_id=updated_plan.id)
        return updated_plan

    @staticmethod
    def add_plan_entry(plan_id, **parameters):
        raise NotImplementedError

    @staticmethod
    def update_plan_entry(plan_id, entry_id, **parameters):
        raise NotImplementedError

    @staticmethod
    def delete_plan_entry(plan_id, entry_id):
        raise NotImplementedError

    @staticmethod
    def close_plan(plan_id):
        """
        :type plan_id: int
        :rtype: testrail.models.Plan
        """
        closed_plan = models.Case(TestrailData.api.close_plan(plan_id))
        TestrailData._store_in_cache(closed_plan, plan_id=closed_plan.id)
        return closed_plan

    @staticmethod
    def delete_plan(plan_id):
        """
        :type plan_id: int
        :rtype: None
        """
        TestrailData.api.delete_plan(plan_id)
        TestrailData._remove_from_cache(models.Plan, plan_id=plan_id)

    ############################################################################
    #
    # Configurations methods
    #
    ############################################################################

    @staticmethod
    def get_config_groups(project_id):
        """
        :type project_id: int
        :rtype: list of [testrail.models.ConfigGroup]
        """
        return TestrailData._cache_or_call(
            models.Configuration,
            TestrailData.api.get_configs,
            project_id=project_id
        )

    ############################################################################
    #
    # Runs methods
    #
    ############################################################################

    @staticmethod
    def get_run_by_id(run_id):
        """
        :type run_id: int
        :rtype: testrail.models.Run
        """
        return TestrailData._cache_or_call(
            models.Run,
            TestrailData.api.get_run,
            run_id=run_id
        )

    @staticmethod
    def get_runs(project_id, **filters):
        """
        :type project_id: int
        :rtype: list of [testrail.models.Run]
        """
        return TestrailData._cache_or_call(
            models.Run,
            TestrailData.api.get_runs,
            project_id=project_id,
            **filters
        )

    @staticmethod
    def add_run(project_id, **parameters):
        """
        :type project_id: int
        :rtype: testrail.models.Run
        """
        new_run = models.Run(TestrailData.api.add_run(project_id, **parameters))
        TestrailData._store_in_cache(new_run, run_id=new_run.id)
        return new_run

    @staticmethod
    def update_run(run_id, **parameters):
        """
        :type project_id: int
        :rtype: testrail.models.Run
        """
        updated_run = models.Run(TestrailData.api.update_run(run_id, **parameters))
        TestrailData._store_in_cache(updated_run, run_id=updated_run.id)
        return updated_run

    @staticmethod
    def close_run(run_id):
        """
        :type run_id: int
        :rtype: testrail.models.Run
        """
        closed_run = models.Run(TestrailData.api.close_run(run_id))
        TestrailData._store_in_cache(closed_run, run_id=closed_run.id)
        return closed_run

    @staticmethod
    def delete_run(run_id):
        """
        :type run_id: int
        :rtype: None
        """
        TestrailData.api.delete_run(run_id)
        TestrailData._remove_from_cache(models.Run, run_id=run_id)

    ############################################################################
    #
    # Tests methods
    #
    ############################################################################

    @staticmethod
    def get_test_by_id(test_id):
        """
        :type test_id: int
        :rtype: testrail.models.Test
        """
        return TestrailData._cache_or_call(
            models.Test,
            TestrailData.api.get_test,
            test_id=test_id
        )

    @staticmethod
    def get_tests(run_id, **filters):
        """
        :type run_id: int
        :rtype: list of [testrail.models.Test]
        """
        return TestrailData._cache_or_call(
            models.Test,
            TestrailData.api.get_tests,
            run_id=run_id
        )

    ############################################################################
    #
    # Statuses methods
    #
    ############################################################################

    @staticmethod
    def get_status_by_id(status_id):
        for s in TestrailData.get_statuses():
            if s.id == status_id:
                return s
        return None

    @staticmethod
    def get_statuses():
        """
        :rtype: list of [testrail.models.Status]
        """
        return TestrailData._cache_or_call(
            models.Status,
            TestrailData.api.get_statuses
        )

    ############################################################################
    #
    # Results methods
    #
    ############################################################################

    @staticmethod
    def get_test_results(test_id, **filters):
        """
        :type test_id: int
        :rtype: list of [testrail.models.Result]
        """
        return TestrailData._cache_or_call(
            models.Result,
            TestrailData.api.get_results,
            test_id=test_id
        )

    @staticmethod
    def get_case_results(case_id, run_id, **filters):
        """
        :type case_id: int
        :type run_id: int
        :rtype: list of [testrail.models.Result]
        """
        return TestrailData._cache_or_call(
            models.Result,
            TestrailData.api.get_results_for_case,
            case_id=case_id,
            run_id=run_id
        )

    @staticmethod
    def get_run_results(run_id, **filters):
        """
        :type run_id: int
        :rtype: list of [testrail.models.Result]
        """
        return TestrailData._cache_or_call(
            models.Result,
            TestrailData.api.get_results_for_run,
            run_id=run_id
        )

    @staticmethod
    def add_test_result(test_id, **parameters):
        """
        :type test_id: int
        :rtype: testrail.models.Result
        """
        new_result = models.Result(TestrailData.api.add_result(test_id, **parameters))
        TestrailData._store_in_cache(new_result, result_id=new_result.id)
        return new_result

    @staticmethod
    def add_case_result(run_id, case_id, **parameters):
        """
        :type case_id: int
        :type run_id: int
        :rtype: testrail.models.Result
        """
        new_result = models.Result(TestrailData.api.add_result_for_case(run_id, case_id, **parameters))
        TestrailData._store_in_cache(new_result, result_id=new_result.id)
        return new_result

    # TODO: implement 'add results'
    # @staticmethod
    # def add_results(run_id, **parameters):
    #     raise NotImplementedError