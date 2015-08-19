#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

import datetime

import testrail
import testrail.core.utils as utils


class Milestone(object):
    """
    Milestone container.

    Attributes:
        id              -- (int) Unique milestone ID
        project         -- (Project) The project this milestone belongs to
        name            -- (str) Name of the milestone
        description     -- (str) Description of the milestone
        url             -- (str) Milestone web-page
        due_on          -- (datetime) Due date of this milestone
        is_completed    -- (bool) True if the milestone is marked as completed and false
                            otherwise
        completed_on    -- (datetime) The date when the milestone was
                            marked as completed
    """
    def __init__(self, attributes):
        self.__id = int(attributes['id'])
        self.__project_id = int(attributes['project_id'])

        self.__name = attributes['name']
        self.__description = attributes['description']
        self.__url = attributes['url']

        self.__is_completed = bool(attributes['is_completed'])

        try:
            self.__due_on = datetime.datetime.fromtimestamp(attributes['due_on'])
        except TypeError:
            self.__due_on = None

        try:
            self.__completed_on = datetime.datetime.fromtimestamp(attributes['completed_on'])
        except TypeError:
            self.__completed_on = None

    def __str__(self):
        return '<Milestone: %s [%s]>' % (self.name, self.id)

    def __repr__(self):
        return self.__str__()

    ###########################################################################
    # Getters/Setters

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        raise RuntimeError('Attribute Milestone.id cannot be modified.')

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        raise RuntimeError('Attribute Milestone.name cannot be modified directly. '
                           'Please use Milestone.update(name=<new_name>) for this.')

    @property
    def project(self):
        return testrail.core.data.TestrailData.get_project_by_id(self.__project_id)

    @project.setter
    def project(self, value):
        raise RuntimeError('Attribute Milestone.project cannot be modified.')

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        raise RuntimeError('Attribute Milestone.description cannot be modified directly. '
                           'Please use Milestone.update(description=<new_description>) for this.')

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        raise RuntimeError('Attribute Milestone.url cannot be modified.')

    @property
    def is_completed(self):
        return self.__is_completed

    @is_completed.setter
    def is_completed(self, value):
        raise RuntimeError('Attribute Milestone.is_completed cannot be modified directly. '
                           'Please use Milestone.set_completed() for this.')

    @property
    def due_on(self):
        return self.__due_on

    @due_on.setter
    def due_on(self, value):
        raise RuntimeError('Attribute Milestone.due_on cannot be modified directly. '
                           'Please use Milestone.update(due_on=<date>) for this.')

    @property
    def completed_on(self):
        return self.__completed_on

    @completed_on.setter
    def completed_on(self, value):
        raise RuntimeError('Attribute Milestone.completed_on cannot be modified.')

    ###########################################################################
    # LifeCycle Methods

    def update(self, **attributes):
        """
        Update milestone attributes.

        Available for update:
            name
            description
            due_on*
            is_completed

        * date can be specified by time.struct_time, datetime.datetime, int timestamp,
          float timestamp, string timestamp or string in '%Y%m%d%H%M%S' format.
        """
        try:
            attributes['due_on'] = utils.make_timestamp(attributes['due_on'])
        except KeyError:
            pass

        m = testrail.core.data.TestrailData.update_milestone(self.id, **attributes)

        self.__name = m.name
        self.__description = m.description
        self.__is_completed = m.is_completed
        self.__completed_on = m.completed_on
        self.__due_on = m.due_on

    def set_completed(self):
        """
        Mark this milestone as completed.
        """
        self.update(is_completed=True)

    def delete(self):
        """
        Completely delete this milestone.
        """
        testrail.core.data.TestrailData.delete_milestone(self.id)

    def add_plan(self, name, description=''):
        """
        Add new test plan to the project and associate it with this milestone.
        Return newly created plan object.

        :param name: Desired name of new test plan.
        :type name: str
        :param description: Description of the new test plan.
        :type description: str
        :rtype: testrail.models.Plan
        """
        return self.project.add_plan(name, description, self.id)

    def add_run(self, suite, name, description='', assigned_to=None, include_all=None, cases=None):
        """
        Create new test run in this project and associate it with this milestone.
        Return newly created run object.

        :param suite: Test Suite to create run from*.
        :type suite: str or int or testrail.models.Suite
        :param name: Name of new test run
        :type name: str
        :param description: Description of new test run.
        :type description: str
        :param assigned_to: User to assign this run to**.
        :type assigned_to: str or int or testrail.models.User
        :param include_all: Include all cases from suite (overrides 'cases')
        :type include_all: bool
        :param cases: list of cases to include in run (if include_all is False)***.
        :type cases: list of [str] or list of [int] or list of [testrail.models.Cases]
        :rtype: testrail.models.Run

          * suite can be specified by suite ID, suite name or Suite object.
         ** user can be specified by user ID, user name, email or User object.
        *** cases can be specified by case ID or Case object.
        """
        return self.project.add_run(suite, name, description, self.id, assigned_to, include_all, cases)

    ###########################################################################
    # Query Methods

    def get_plans(self, **filters):
        """
        Get plans associated with this milestone.

        Possible filters:
            created_after 	    -- Return test plans created after this date*.
            created_before 	    -- Return test plans created before this date*.
            created_by 	        -- Return test plans created by this users**.
            is_completed 	    -- (bool) True to return completed test plans only.
                                   False - only incomplete.
            limit               -- (int) Limit the result to 'limit' test plans.
            offset              -- (int) Skip first 'offset' records in output.

          * date can be specified by time.struct_time, datetime.datetime, int timestamp,
            float timestamp, string timestamp or string in '%Y%m%d%H%M%S' format.
         ** users can be specified by user ID, user name, email or User object.

        :rtype: list of [testrail.models.Plan]
        """
        return self.project.get_plans(milestones=self.id, **filters)

    def get_runs(self, **filters):
        """
        Get Runs associated with this milestone.

        Possible filters:
            created_after 	    -- Return test runs created after this date*.
            created_before 	    -- Return test runs created before this date*.
            created_by 	        -- Return test runs created by this users**.
            is_completed 	    -- (bool) True to return completed test runs only.
                                   False - only incomplete.
            limit               -- (int) Limit the result to 'limit' test runs.
            offset              -- (int) Skip first 'offset' records in output.
            suites              -- Return test runs created from this suites***.

           * date can be specified by time.struct_time, datetime.datetime, int timestamp,
             float timestamp, string timestamp or string in '%Y%m%d%H%M%S' format.
          ** users can be specified by user ID, user name, email or User object.
         *** suites can be specified by suite ID, suite name or Suite object.

        :rtype: list of [testrail.models.Run]
        """
        return self.project.get_runs(milestones=self.id, **filters)


