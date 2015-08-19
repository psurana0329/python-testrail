#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

from datetime import datetime

import testrail
import testrail.core.utils as utils


class Project(object):
    """
    Testrail Project container.

    Attributes:
        id                -- (int) Unique project ID
        name              -- (unicode) Project name
        url               -- (str) Project web-page
        announcement      -- (str) Description of the project
        show_announcement -- (bool) If True announcement will be displayed
                             on project web-page. If False - it will be hidden.
        is_completed      -- (bool) If True - project is marked as completed.
        completed_on      -- (datetime) The date when the project was marked as
                             completed in server timezone.
        suite_mode        -- (int) Suite mode of the project:
                                1 - single suite mode
                                2 - single suite + baselines mode
                                3 - multiple suites mode
    """
    def __init__(self, attributes):
        self.__id = int(attributes['id'])

        self.__name = attributes['name']
        self.__url = attributes['url']

        if attributes['announcement'] is not None:
            self.__announcement = attributes['announcement']
        else:
            self.__announcement = None

        self.__show_announcement = bool(attributes['show_announcement'])
        self.__is_completed = bool(attributes['is_completed'])

        try:
            self.__completed_on = datetime.fromtimestamp(attributes['completed_on'])
        except TypeError:
            self.__completed_on = None

        try:
            # this will appear only since 4.0
            self.__suite_mode = attributes['suite_mode']
        except KeyError:
            self.__suite_mode = None

    def __str__(self):
        return '<Project: %s [%s]>' % (self.name, self.id)

    def __repr__(self):
        return self.__str__()

    ###########################################################################
    # Getters/Setters

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        raise RuntimeError('Attribute Project.id cannot be modified.')

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        raise RuntimeError('Attribute Project.url cannot be modified.')

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        raise RuntimeError('Attribute Project.name cannot be modified directly. '
                           'Please use Project.update(name=<new_name>) for this.')

    @property
    def announcement(self):
        return self.__announcement

    @announcement.setter
    def announcement(self, value):
        raise RuntimeError('Attribute Project.announcement cannot be modified directly. '
                           'Please use Project.update(announcement=<new_announcement>) for this.')

    @property
    def show_announcement(self):
        return self.__show_announcement

    @show_announcement.setter
    def show_announcement(self, value):
        raise RuntimeError('Attribute Project.show_announcement cannot be modified directly. '
                           'Please use Project.update(show_announcement=<True|False>) for this.')

    @property
    def is_completed(self):
        return self.__is_completed

    @is_completed.setter
    def is_completed(self, value):
        raise RuntimeError('Attribute Project.is_completed cannot be modified directly. '
                           'Please use Project.set_completed() for this.')

    @property
    def completed_on(self):
        return self.__completed_on

    @completed_on.setter
    def completed_on(self, value):
        raise RuntimeError('Attribute Project.completed_on cannot be modified.')

    @property
    def suite_mode(self):
        return self.__suite_mode

    @suite_mode.setter
    def suite_mode(self, value):
        raise RuntimeError('Attribute Project.suite_mode cannot be modified.')

    ###########################################################################
    # LifeCycle Methods

    def update(self, **attributes):
        """
        Update project attributes.

        Available for update:
            name
            announcement
            show_announcement
            is_completed
        """
        p = testrail.core.data.TestrailData.update_project(self.id, **attributes)

        if p is not None:
            self.__name = p.name
            self.__announcement = p.announcement
            self.__show_announcement = p.show_announcement
            self.__is_completed = p.is_completed
            self.__completed_on = p.completed_on

    def set_completed(self):
        """
        Mark this project as completed.
        """
        self.update(is_completed=True)

    def delete(self):
        """
        Wipe out this project.

        !!! Deleting a project cannot be undone and also permanently deletes
        all test suites & cases, test runs & results and everything else
        that is part of the project.
        """
        testrail.core.data.TestrailData.delete_project(self.id)

    def add_milestone(self, name, description='', due_on=None):
        """
        Create new milestone.
        Return newly created milestone object.

        :param name: Desired name of new milestone
        :type name: str
        :param description: description of the new milestone
        :type description: str
        :param due_on: date and time when this milestone due to be completed (as unix timestamp)
        :type due_on: str
        :rtype: testrail.models.Milestone
        """
        parameters = {
            'name': name,
            'description': description,
        }
        if due_on is not None:
            parameters['due_on'] = due_on
        return testrail.core.data.TestrailData.add_milestone(self.id, **parameters)

    def add_suite(self, name, description=''):
        """
        Create new test suite in this project.
        Return newly created suite object.

        :param name: Desired name of the new suite.
        :type name: str
        :param description: Optional description of the suite.
        :type description: str
        :rtype: testrail.models.Suite
        """
        parameters = {
            'name': name,
            'description': description,
        }
        return testrail.core.data.TestrailData.add_suite(self.id, **parameters)

    def add_plan(self, name, description='', milestone=None):
        """
        Create new test plan in this project.
        Return newly created plan object.

        :param name: Desired name of new test plan.
        :type name: str
        :param description: Description of the new test plan.
        :type description: str
        :param milestone: milestone to associate new test plan with*.
        :type milestone: str or int or testrail.models.Milestone
        :rtype: testrail.models.Plan

        * milestone can be specified by milestone ID, milestone name or Milestone object.
        """
        parameters = {
            'name': name,
            'description': description,
        }
        if milestone is not None:
            parameters['milestone_id'] = utils.guess_milestone_id(self, milestone)

        return testrail.core.data.TestrailData.add_plan(self.id, **parameters)

    def add_run(self, suite, name, description='', milestone=None, assigned_to=None, include_all=None, cases=None):
        """
        Create new test run in this project.
        Return newly created run object.

        :param suite: Test Suite to create run from*.
        :type suite: str or int or testrail.models.Suite
        :param name: Name of new test run
        :type name: str
        :param description: Description of new test run.
        :type description: str
        :param milestone: Milestone to associate this run with**.
        :type milestone: str or int or testrail.models.Milestone
        :param assigned_to: User to assign this run to***.
        :type assigned_to: str or int or testrail.models.User
        :param include_all: Include all cases from suite (overrides 'cases')
        :type include_all: bool
        :param cases: list of cases to include in run (if include_all is False)****.
        :type cases: list of [str] or list of [int] or list of [testrail.models.Cases]
        :rtype: testrail.models.Run

           * suite can be specified by suite ID, suite name or Suite object.
          ** milestones can be specified by milestone ID, milestone name or Milestone object.
         *** user can be specified by user ID, user name, email or User object.
        **** cases can be specified by case ID or Case object.
        """
        parameters = {
            'suite_id': utils.guess_suite_id(self, suite),
            'name': name,
            'description': description,
        }

        if milestone is not None:
            parameters['milestone_id'] = utils.guess_milestone_id(self, milestone)

        if assigned_to is not None:
            parameters['assignedto_id'] = utils.guess_user_id(assigned_to)

        if include_all is not None:
            parameters['include_all'] = include_all

        elif cases is not None and len(cases) > 0:
            parameters['case_ids'] = [utils.guess_case_id(c) for c in cases]

        return testrail.core.data.TestrailData.add_run(self.id, **parameters)

    ###########################################################################
    # Query Methods

    def get_milestones(self, is_completed=None):
        """
        Return list of milestones in this project.

        :param is_completed: if True return only completed milestones,
                             if False - only incomplete,
                             if None - return everything
        :type is_completed: bool or None
        :rtype: list of [testrail.models.Milestone]
        """
        return testrail.core.data.TestrailData.get_milestones(self.id, is_completed)

    def get_milestone(self, name):
        """
        Return a milestone from this project by its name.

        :param name: Name of a milestone to return.
        :type name: str
        :rtype: testrail.models.Milestone or None
        """
        for m in self.get_milestones():
            if m.name == name:
                return m
        return None

    def get_suites(self):
        """
        Return all suites in this project.

        :rtype: list of [testrail.models.Suite]
        """
        return testrail.core.data.TestrailData.get_suites(self.id)

    def get_suite(self, name):
        """
        Return a suite from this project by its name.

        :param name: Name of a suite to return.
        :type name: str
        :rtype: testrail.models.Suite or None
        """
        for s in self.get_suites():
            if s.name == name:
                return s
        return None

    def get_case_fields(self):
        """
        Return list of custom case fields for this project.

        :rtype: list of [testrail.models.CaseField]
        """
        result = []
        for field_specification in testrail.core.data.TestrailData.get_case_fields():
            field = field_specification.construct_field(self.id)

            if field is not None:
                result.append(field)

        return result

    def get_result_fields(self):
        """
        Return list of custom result field descriptions applicable to this project.
        Setup attributes of result fields objects with options for this project.

        :rtype: list of [testrail.models.ResultField]
        """
        result = []
        for field_specification in testrail.core.data.TestrailData.get_result_fields():
            field = field_specification.construct_field(self.id)

            if field is not None:
                result.append(field)

        return result

    def get_plans(self, **filters):
        """
        Return list of test plans in this project.

        Possible Filters:
            created_after 	    -- Return test plans created after this date*.
            created_before 	    -- Return test plans created before this date*.
            created_by 	        -- Return test plans created by this users**.
            is_completed 	    -- (bool) True to return completed test plans only.
                                   False - only incomplete.
            limit               -- (int) Limit the result to 'limit' test plans.
            offset              -- (int) Skip first 'offset' records in output.
            milestones          -- Return test plans attached to this milestones***.

          * date can be specified by time.struct_time, datetime.datetime, int timestamp,
            float timestamp, string timestamp or string in '%Y%m%d%H%M%S' format.
         ** users can be specified by user ID, user name, email or User object.
        *** milestones can be specified by milestone ID, milestone name or Milestone object.

        :rtype: list of [testrail.models.Plan]
        """
        parameters = {}

        for p in ['created_after', 'created_before']:
            try:
                parameters[p] = utils.make_timestamp(filters[p])
            except KeyError:
                pass

        for v in ['is_completed', 'limit', 'offset']:
            try:
                parameters[v] = filters[v]
            except KeyError:
                pass

        try:
            if not isinstance(filters['created_by'], list):
                filters['created_by'] = [filters['created_by']]
        except KeyError:
            pass
        else:
            parameters['created_by'] = [utils.guess_user_id(u) for u in filters['created_by']]

        try:
            if not isinstance(filters['milestones'], list):
                filters['milestones'] = [filters['milestones']]
        except KeyError:
            pass
        else:
            parameters['milestone_id'] = [utils.guess_milestone_id(self, m) for m in filters['milestones']]

        return testrail.core.data.TestrailData.get_plans(self.id, **parameters)

    def get_plan(self, name):
        """
        Return a plan by its name.

        :param name: Name of a test plan to return.
        :type name: str
        :rtype: testrail.models.Plan or None
        """
        for p in self.get_plans():
            if p.name == name:
                return p
        return None

    def get_runs(self, **filters):
        """
        Return list of test runs in this project.

        Possible Filters:
            created_after 	    -- Return test runs created after this date*.
            created_before 	    -- Return test runs created before this date*.
            created_by 	        -- Return test runs created by this users**.
            is_completed 	    -- (bool) True to return completed test runs only.
                                   False - only incomplete.
            limit               -- (int) Limit the result to 'limit' test runs.
            offset              -- (int) Skip first 'offset' records in output.
            milestones          -- Return test runs attached to this milestones***.
            suites              -- Return test runs created from this suites****.

           * date can be specified by time.struct_time, datetime.datetime, int timestamp,
             float timestamp, string timestamp or string in '%Y%m%d%H%M%S' format.
          ** users can be specified by user ID, user name, email or User object.
         *** milestones can be specified by milestone ID, milestone name or Milestone object.
        **** suites can be specified by suite ID, suite name or Suite object.

        :rtype: list of [testrail.models.Run]
        """
        parameters = {}

        for p in ['created_after', 'created_before']:
            try:
                parameters[p] = utils.make_timestamp(filters[p])
            except KeyError:
                pass

        for v in ['is_completed', 'limit', 'offset']:
            try:
                parameters[v] = filters[v]
            except KeyError:
                pass

        try:
            if not isinstance(filters['created_by'], list):
                filters['created_by'] = [filters['created_by']]
        except KeyError:
            pass
        else:
            parameters['created_by'] = [utils.guess_user_id(u) for u in filters['created_by']]

        try:
            if not isinstance(filters['milestones'], list):
                filters['milestones'] = [filters['milestones']]
        except KeyError:
            pass
        else:
            parameters['milestone_id'] = [utils.guess_milestone_id(self, m) for m in filters['milestones']]

        try:
            if not isinstance(filters['suites'], list):
                filters['suites'] = [filters['suites']]
        except KeyError:
            pass
        else:
            parameters['suite_id'] = [utils.guess_suite_id(self, s) for s in filters['suites']]

        return testrail.core.data.TestrailData.get_runs(self.id, **parameters)

    def get_run(self, name):
        """
        Return a run by its name.

        :param name: Name of a test run to return.
        :type name: str
        :rtype: testrail.models.Run or None
        """
        for r in self.get_runs():
            if r.name == name:
                return r
        return None

    def get_configurations(self):
        """
        Return a list of all configudations in this project.

        :rtype: testrail.models.Configuration
        """
        return testrail.core.data.TestrailData.get_config_groups(self.id)
