#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

from datetime import datetime

import testrail


class Run(object):
    """
    Test run container

    Attributes:
       id                   -- (int) Unique test run ID
       project              -- (Project) The project this test run belongs to
       plan                 -- (Plan) The test plan this test run belongs to (if any)
       config               -- (str) Human representation of this run configuration (if any)
       configs              -- (list) Configuration objects list of this test run (if any)
       suite                -- (Suite) The test suite this test run is created from
       include_all          -- (bool) If True - all test cases from suite are included in run
       name                 -- (str) Test run name
       description          -- (str) Test run description
       url                  -- (str) Test run web-page
       milestone            -- (Milestone) The milestone this test plan belongs to
       created_on           -- (datetime) Date when the test plan was created
       created_by           -- (User) The user who created this test plan
       assigned_to          -- (User) The user this test plan is assigned to
       is_completed         -- (bool) True if this test plan was closed and false otherwise
       completed_on         -- (datetime) Date when this test plan was closed
       passed_count         -- (int) The amount of tests in this test plan marked as passed
       failed_count         -- (int) The amount of tests in this test plan marked as failed
       retest_count         -- (int) The amount of tests in this test plan marked as retest
       blocked_count        -- (int) The amount of tests in this test plan marked as blocked
       untested_count       -- (int) The amount of tests in this test plan marked as untested
       custom_status1_count -- (int) The amount of tests in this test plan with the respective custom status
       custom_status2_count -- (int) The amount of tests in this test plan with the respective custom status
       custom_status3_count -- (int) The amount of tests in this test plan with the respective custom status
       custom_status4_count -- (int) The amount of tests in this test plan with the respective custom status
       custom_status5_count -- (int) The amount of tests in this test plan with the respective custom status
       custom_status6_count -- (int) The amount of tests in this test plan with the respective custom status
       custom_status7_count -- (int) The amount of tests in this test plan with the respective custom status
    """
    def __init__(self, attributes):
        self.__id = int(attributes['id'])
        self.__name = attributes['name']
        self.__project_id = int(attributes['project_id'])
        self.__description = attributes['description']
        self.__url = attributes['url']

        try:
            self.__plan_id = int(attributes['plan_id'])
            self.__entry_id = attributes['entry_id']
        except TypeError:
            self.__plan_id = None
            self.__entry_id = None

        self.__suite_id = int(attributes['suite_id'])

        try:
            self.__milestone_id = int(attributes['milestone_id'])
        except TypeError:
            self.__milestone_id = None

        self.__created_on = datetime.fromtimestamp(attributes['created_on'])
        self.__created_by = int(attributes['created_by'])

        try:
            self.__assigned_to = int(attributes['assignedto_id'])
        except TypeError:
            self.__assigned_to = None

        self.__is_completed = attributes['is_completed']
        try:
            self.__completed_on = datetime.fromtimestamp(attributes['completed_on'])
        except TypeError:
            self.__completed_on = None

        self.__passed_count = int(attributes['passed_count'])
        self.__failed_count = int(attributes['failed_count'])
        self.__retest_count = int(attributes['retest_count'])
        self.__blocked_count = int(attributes['blocked_count'])
        self.__untested_count = int(attributes['untested_count'])

        self.__custom_status1_count = int(attributes['custom_status1_count'])
        self.__custom_status2_count = int(attributes['custom_status2_count'])
        self.__custom_status3_count = int(attributes['custom_status3_count'])
        self.__custom_status4_count = int(attributes['custom_status4_count'])
        self.__custom_status5_count = int(attributes['custom_status5_count'])
        self.__custom_status6_count = int(attributes['custom_status6_count'])
        self.__custom_status7_count = int(attributes['custom_status7_count'])

        try:
            # testrail 3.1
            self.__config = attributes['config']
            self.__config_ids = [int(x) for x in attributes['config_ids']]
        except KeyError:
            self.__config = None
            self.__config_ids = None

        self.__include_all = attributes['include_all']

    def __str__(self):
        return '<TestRun %s [%s]>' % (self.name, self.id)

    def __repr__(self):
        return self.__str__()

    ###########################################################################
    # Getters/Setters

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        raise RuntimeError('Attribute Run.id cannot be modified.')

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        raise RuntimeError('Attribute Run.name cannot be modified directly. '
                           'Please use Run.update(name=<new_name>) for this.')

    @property
    def project(self):
        return testrail.core.data.TestrailData.get_project_by_id(self.__project_id)

    @project.setter
    def project(self, value):
        raise RuntimeError('Attribute Run.project cannot be modified.')

    @property
    def plan(self):
        return testrail.core.data.TestrailData.get_plan_by_id(self.__plan_id)

    @plan.setter
    def plan(self, value):
        raise RuntimeError('Attribute Run.plan cannot be modified.')

    @property
    def config(self):
        return self.__config

    @config.setter
    def config(self, value):
        raise RuntimeError('Attribute Run.config cannot be modified.')

    @property
    def configs(self):
        return self.__config_ids

    @configs.setter
    def configs(self, value):
        raise RuntimeError('Attribute Run.configs cannot be modified.')

    @property
    def suite(self):
        return testrail.core.data.TestrailData.get_suite_by_id(self.__suite_id)

    @suite.setter
    def suite(self, value):
        raise RuntimeError('Attribute Run.suite cannot be modified.')

    @property
    def include_all(self):
        return self.__include_all

    @include_all.setter
    def include_all(self, value):
        raise RuntimeError('Attribute Run.include_all cannot be modified.')

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        raise RuntimeError('Attribute Run.description cannot be modified directly. '
                           'Please use Run.update(description=<new_description>) for this.')

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        raise RuntimeError('Attribute Run.url cannot be modified.')

    @property
    def milestone(self):
        return testrail.core.data.TestrailData.get_milestone_by_id(self.__milestone_id)

    @milestone.setter
    def milestone(self, value):
        raise RuntimeError('Attribute Run.milestone cannot be modified directly. '
                           'Please use Run.update(milestone=<new_milestone>) for this.')

    @property
    def created_on(self):
        return self.__created_on

    @created_on.setter
    def created_on(self, value):
        raise RuntimeError('Attribute Run.created_on cannot be modified.')

    @property
    def created_by(self):
        return testrail.core.data.TestrailData.get_user_by_id(self.__created_by)

    @created_by.setter
    def created_by(self, value):
        raise RuntimeError('Attribute Run.created_by cannot be modified.')

    @property
    def assigned_to(self):
        return testrail.core.data.TestrailData.get_user_by_id(self.__assigned_to)

    @assigned_to.setter
    def assigned_to(self, value):
        raise RuntimeError('Attribute Run.assigned_to cannot be modified.')

    @property
    def is_completed(self):
        return self.__is_completed

    @is_completed.setter
    def is_completed(self, value):
        raise RuntimeError('Attribute Run.is_completed cannot be modified directly. '
                           'Please use Run.set_completed() for this.')

    @property
    def completed_on(self):
        return self.__completed_on

    @completed_on.setter
    def completed_on(self, value):
        raise RuntimeError('Attribute Run.completed_on cannot be modified.')

    @property
    def passed_count(self):
        return self.__passed_count

    @passed_count.setter
    def passed_count(self, value):
        raise RuntimeError('Attribute Run.passed_count cannot be modified.')

    @property
    def failed_count(self):
        return self.__failed_count

    @failed_count.setter
    def failed_count(self, value):
        raise RuntimeError('Attribute Run.failed_count cannot be modified.')

    @property
    def retest_count(self):
        return self.__retest_count

    @retest_count.setter
    def retest_count(self, value):
        raise RuntimeError('Attribute Run.retest_count cannot be modified.')

    @property
    def blocked_count(self):
        return self.__blocked_count

    @blocked_count.setter
    def blocked_count(self, value):
        raise RuntimeError('Attribute Run.blocked_count cannot be modified.')

    @property
    def untested_count(self):
        return self.__untested_count

    @untested_count.setter
    def untested_count(self, value):
        raise RuntimeError('Attribute Run.untested_count cannot be modified.')

    @property
    def custom_status1_count(self):
        return self.__custom_status1_count

    @custom_status1_count.setter
    def custom_status1_count(self, value):
        raise RuntimeError('Attribute Run.custom_status1_count cannot be modified.')

    @property
    def custom_status2_count(self):
        return self.__custom_status2_count

    @custom_status2_count.setter
    def custom_status2_count(self, value):
        raise RuntimeError('Attribute Run.custom_status2_count cannot be modified.')

    @property
    def custom_status3_count(self):
        return self.__custom_status3_count

    @custom_status3_count.setter
    def custom_status3_count(self, value):
        raise RuntimeError('Attribute Run.custom_status3_count cannot be modified.')

    @property
    def custom_status4_count(self):
        return self.__custom_status4_count

    @custom_status4_count.setter
    def custom_status4_count(self, value):
        raise RuntimeError('Attribute Run.custom_status4_count cannot be modified.')

    @property
    def custom_status5_count(self):
        return self.__custom_status5_count

    @custom_status5_count.setter
    def custom_status5_count(self, value):
        raise RuntimeError('Attribute Run.custom_status5_count cannot be modified.')

    @property
    def custom_status6_count(self):
        return self.__custom_status6_count

    @custom_status6_count.setter
    def custom_status6_count(self, value):
        raise RuntimeError('Attribute Run.custom_status6_count cannot be modified.')

    @property
    def custom_status7_count(self):
        return self.__custom_status7_count

    @custom_status7_count.setter
    def custom_status7_count(self, value):
        raise RuntimeError('Attribute Run.custom_status7_count cannot be modified.')

    ###########################################################################
    # LifeCycle Methods

    def update(self, **attributes):
        """
        Update run attributes.

        Available for update:
            name              -- Run name
            description       -- The description of the run
            milestone         -- Milestone name, Milestone id or Milestone object to associate test run with
            include_all       -- if True - all cases in suite included in run
            cases             -- if include_all is False - list of cases to include
        """
        try:
            milestone = attributes['milestone']
        except KeyError:
            pass
        else:
            del attributes['milestone']
            if isinstance(milestone, str):
                try:
                    attributes['milestone_id'] = self.project().get_milestone_by_name(milestone).id
                except AttributeError:
                    pass
            elif isinstance(milestone, int):
                attributes['milestone_id'] = milestone
            elif isinstance(milestone, testrail.models.Milestone):
                attributes['milestone_id'] = milestone.id

        try:
            cases = attributes['cases']
        except KeyError:
            pass
        else:
            del attributes['cases']
            if len(cases) > 0:
                if isinstance(cases[0], str):
                    try:
                        attributes['case_ids'] = [self.suite().get_case_by_name(c).id for c in cases]
                    except AttributeError:
                        pass
                elif isinstance(cases[0], int):
                    attributes['case_ids'] = cases
                elif isinstance(cases[0], testrail.models.Case):
                    attributes['case_ids'] = [c.id for c in cases]

        p = testrail.core.data.TestrailData.update_run(self.id, **attributes)

        self.name = p.name
        self.description = p.description
        self.milestone_id = p.milestone_id
        self.include_all = p.include_all

    def close(self):
        """
        Close this run, saving its state and preventing any further changes.
        """
        p = testrail.core.data.TestrailData.close_run(self.id)

        self.is_completed = p.is_completed
        self.completed_on = p.completed_on

    def delete(self):
        """
        Delete this run and all its data.
        """
        testrail.core.data.TestrailData.delete_run(self.id)

    def get_tests(self):
        """
        Get tests in this run.

        :rtype: list of [testrail.models.Test]
        """
        return testrail.core.data.TestrailData.get_tests(self.id)

    def get_test(self, title):
        """
        Get test in this run by its title.
        Since title is not unique will return first match.

        :rtype: testrail.models.Test
        """
        for test in self.get_tests():
            if test.title == title:
                return test
        return None



