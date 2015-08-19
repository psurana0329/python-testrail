#!/usr/bin/env python
# -*- coding:  utf-8 -*-

# This plans are pain in the arse

from __future__ import absolute_import
from __future__ import print_function

from datetime import datetime

import testrail
import testrail.core.utils as utils


class Plan(object):
    """
    Test plan container.

    Attributes:
       id                   -- (int) Unique test plan ID
       project              -- (Project) The project this test plan belongs to
       name                 -- (str) Test plan name
       description          -- (str) Test plan description
       url                  -- (str) Test plan web-page
       milestone            -- (Milestone) The milestone this test plan belongs to
       created_on           -- (datetime) Date/time when this test plan was created
       created_by           -- (User) User who created the test plan
       assigned_to          -- (User) User this plan is assigned to
       is_completed         -- (bool) True if this test plan was closed and false otherwise
       completed_on         -- (datetime) Date/time when this test plan was closed

       passed_count         -- (int) The amount of tests in test plan marked as passed
       failed_count         -- (int) The amount of tests in test plan marked as failed
       retest_count         -- (int) The amount of tests in test plan marked as retest
       blocked_count        -- (int) The amount of tests in test plan marked as blocked
       untested_count       -- (int) The amount of tests in test plan marked as untested
       custom_status1_count -- (int) The amount of tests in test plan with the respective custom status
       custom_status2_count -- (int) The amount of tests in test plan with the respective custom status
       custom_status3_count -- (int) The amount of tests in test plan with the respective custom status
       custom_status4_count -- (int) The amount of tests in test plan with the respective custom status
       custom_status5_count -- (int) The amount of tests in test plan with the respective custom status
       custom_status6_count -- (int) The amount of tests in test plan with the respective custom status
       custom_status7_count -- (int) The amount of tests in test plan with the respective custom status
    """

    def __init__(self, attributes):
        self.__id = int(attributes['id'])
        self.__project_id = int(attributes['project_id'])
        self.__name = attributes['name']
        self.__description = attributes['description']
        self.__url = attributes['url']

        try:
            self.__milestone_id = int(attributes['milestone_id'])
        except TypeError:
            self.__milestone_id = None

        try:
            self.__created_on = datetime.fromtimestamp(attributes['created_on'])
        except TypeError:
            self.__created_on = None

        self.__created_by = int(attributes['created_by'])
        try:
            self.__assigned_to = int(attributes['assignedto_id'])
        except TypeError:
            self.__assigned_to = None

        self.__is_completed = bool(attributes['is_completed'])
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

        self.__entries = []
        try:
            self.__entries = [PlanEntry(pe) for pe in attributes['entries']]
        except KeyError:
            self.__entries = []

    def __str__(self):
        return '<TestPlan %s [%s]>' % (self.name, self.id)

    def __repr__(self):
        return self.__str__()

    ###########################################################################
    # Getters/Setters

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        raise RuntimeError('Attribute Plan.id cannot be modified.')

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        raise RuntimeError('Attribute Plan.name cannot be modified directly. '
                           'Please use Plan.update(name=<new_name>) for this.')

    @property
    def project(self):
        return testrail.core.data.TestrailData.get_project_by_id(self.__project_id)

    @project.setter
    def project(self, value):
        raise RuntimeError('Attribute Plan.project cannot be modified.')

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        raise RuntimeError('Attribute Plan.description cannot be modified directly. '
                           'Please use Plan.update(description=<new_description>) for this.')

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        raise RuntimeError('Attribute Plan.url cannot be modified.')

    @property
    def milestone(self):
        return testrail.core.data.TestrailData.get_milestone_by_id(self.__milestone_id)

    @milestone.setter
    def milestone(self, value):
        raise RuntimeError('Attribute Plan.milestone cannot be modified directly. '
                           'Please use Plan.update(milestone=<new_milestone>) for this.')

    @property
    def created_on(self):
        return self.__created_on

    @created_on.setter
    def created_on(self, value):
        raise RuntimeError('Attribute Plan.created_on cannot be modified.')

    @property
    def created_by(self):
        return testrail.core.data.TestrailData.get_user_by_id(self.__created_by)

    @created_by.setter
    def created_by(self, value):
        raise RuntimeError('Attribute Plan.created_by cannot be modified.')

    @property
    def assigned_to(self):
        return testrail.core.data.TestrailData.get_user_by_id(self.__assigned_to)

    @assigned_to.setter
    def assigned_to(self, value):
        raise RuntimeError('Attribute Plan.assigned_to cannot be modified.')

    @property
    def is_completed(self):
        return self.__is_completed

    @is_completed.setter
    def is_completed(self, value):
        raise RuntimeError('Attribute Plan.is_completed cannot be modified directly. '
                           'Please use Plan.set_completed() for this.')

    @property
    def completed_on(self):
        return self.__completed_on

    @completed_on.setter
    def completed_on(self, value):
        raise RuntimeError('Attribute Plan.completed_on cannot be modified.')

    @property
    def passed_count(self):
        return self.__passed_count

    @passed_count.setter
    def passed_count(self, value):
        raise RuntimeError('Attribute Plan.passed_count cannot be modified.')

    @property
    def failed_count(self):
        return self.__failed_count

    @failed_count.setter
    def failed_count(self, value):
        raise RuntimeError('Attribute Plan.failed_count cannot be modified.')

    @property
    def retest_count(self):
        return self.__retest_count

    @retest_count.setter
    def retest_count(self, value):
        raise RuntimeError('Attribute Plan.retest_count cannot be modified.')

    @property
    def blocked_count(self):
        return self.__blocked_count

    @blocked_count.setter
    def blocked_count(self, value):
        raise RuntimeError('Attribute Plan.blocked_count cannot be modified.')

    @property
    def untested_count(self):
        return self.__untested_count

    @untested_count.setter
    def untested_count(self, value):
        raise RuntimeError('Attribute Plan.untested_count cannot be modified.')

    @property
    def custom_status1_count(self):
        return self.__custom_status1_count

    @custom_status1_count.setter
    def custom_status1_count(self, value):
        raise RuntimeError('Attribute Plan.custom_status1_count cannot be modified.')

    @property
    def custom_status2_count(self):
        return self.__custom_status2_count

    @custom_status2_count.setter
    def custom_status2_count(self, value):
        raise RuntimeError('Attribute Plan.custom_status2_count cannot be modified.')

    @property
    def custom_status3_count(self):
        return self.__custom_status3_count

    @custom_status3_count.setter
    def custom_status3_count(self, value):
        raise RuntimeError('Attribute Plan.custom_status3_count cannot be modified.')

    @property
    def custom_status4_count(self):
        return self.__custom_status4_count

    @custom_status4_count.setter
    def custom_status4_count(self, value):
        raise RuntimeError('Attribute Plan.custom_status4_count cannot be modified.')

    @property
    def custom_status5_count(self):
        return self.__custom_status5_count

    @custom_status5_count.setter
    def custom_status5_count(self, value):
        raise RuntimeError('Attribute Plan.custom_status5_count cannot be modified.')

    @property
    def custom_status6_count(self):
        return self.__custom_status6_count

    @custom_status6_count.setter
    def custom_status6_count(self, value):
        raise RuntimeError('Attribute Plan.custom_status6_count cannot be modified.')

    @property
    def custom_status7_count(self):
        return self.__custom_status7_count

    @custom_status7_count.setter
    def custom_status7_count(self, value):
        raise RuntimeError('Attribute Plan.custom_status7_count cannot be modified.')

    @property
    def entries(self):
        return self.__entries

    @entries.setter
    def entries(self, value):
        raise RuntimeError('Attribute Plan.entries cannot be modified directly. '
                           'Please use Plan.add_entry() for this.')

    ###########################################################################
    # LifeCycle Methods

    def update(self, **attributes):
        """
        Update plan attributes.

        Available for update:
            name              -- Plan name
            description       -- The description of the plan
            milestone         -- Milestone name, Milestone id or Milestone object to associate new test plan with
        """
        try:
            attributes['milestone_id'] = utils.guess_milestone_id(self.project, attributes['milestone'])
        except KeyError:
            pass
        else:
            del attributes['milestone']

        p = testrail.core.data.TestrailData.update_plan(self.id, **attributes)

        self.__name = p.name
        self.__description = p.description
        self.__milestone_id = p.milestone.id

    def close(self):
        """
        Close this plan, saving its state and preventing any further changes.
        """
        p = testrail.core.data.TestrailData.close_plan(self.id)

        self.__is_completed = p.is_completed
        self.__completed_on = p.completed_on

    def delete(self):
        """
        Delete this plan and all its data.
        """
        testrail.core.data.TestrailData.delete_plan(self.id)

    ###########################################################################
    # Query Methods
    def get_entries(self):
        """
        Return list of entries in this plan.

        :rtype: list of [testrail.models.PlanEntry]
        """
        return self.entries

    # TODO: implement 'add entry'
    # def add_entry(self, name, suite, assigned_to=None, include_all=None, cases=None, configs=None):
    #     """
    #     Add new entry to this plan.
    #     Return newly created Entry.
    #
    #     :return:
    #     """
    #     raise NotImplementedError


class PlanEntry(object):
    """
    Plan entry container.
    For service usage.
    """
    def __init__(self, attributes):
        self.id = attributes['id']
        self.name = attributes['name']
        self.suite_id = attributes['suite_id']
        self.runs = [testrail.models.Run(r) for r in attributes['run']]