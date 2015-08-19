#!/usr/bin/env python
# -*- coding:  utf-8 -*-
#
# TODO: implement 'get_sections_hierarchy' - to return a tree of sections

from __future__ import absolute_import
from __future__ import print_function

from datetime import datetime

import testrail
import testrail.core.utils as utils


class Suite(object):
    """
    Test Suite container.

    Attributes:
        id           -- (int) Unique test suite ID
        project      -- (Project) The project this test suite belongs to
        name         -- (str) Name of the test suite
        description  -- (str) Description of the test suite
        url          -- (str) Suite web-page
        is_master    -- (bool) True if the test suite is a master test suite and
                       false otherwise
        is_baseline  -- (bool) True if the test suite is a baseline test suite and
                       false otherwise
        is_completed -- (bool) True if the test suite is marked as completed/archived
                       and false otherwise
        completed_on -- (datetime) The date when the test suite was closed
    """

    def __init__(self, attributes):
        self.__id = int(attributes['id'])
        self.__project_id = int(attributes['project_id'])

        self.__name = attributes['name']
        self.__description = attributes['description']
        self.__url = attributes['url']

        try:
            # this present only since 4.0
            self.__is_master = bool(attributes['is_master'])
            self.__is_baseline = bool(attributes['is_baseline'])
            self.__is_completed = bool(attributes['is_completed'])
        except KeyError:
            self.__is_master = None
            self.__is_baseline = None
            self.__is_completed = None

        try:
            self.__completed_on = datetime.fromtimestamp(attributes['completed_on'])
        except KeyError:
            self.__completed_on = None
        except TypeError:
            self.__completed_on = None

    def __str__(self):
        return '<Suite: %s [%s]>' % (self.name, self.id)

    def __repr__(self):
        return self.__str__()

    ###########################################################################
    # Getters/Setters

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        raise RuntimeError('Attribute Suite.id cannot be modified.')

    @property
    def project(self):
        return testrail.core.data.TestrailData.get_project_by_id(self.__project_id)

    @project.setter
    def project(self, value):
        raise RuntimeError('Attribute Suite.project cannot be modified.')

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
        raise RuntimeError('Attribute Suite.name cannot be modified directly. '
                           'Please use Suite.update() for this.')

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        raise RuntimeError('Attribute Suite.description cannot be modified directly. '
                           'Please use Suite.update() for this.')

    @property
    def is_master(self):
        return self.__is_master

    @is_master.setter
    def is_master(self, value):
        raise RuntimeError('Attribute Suite.is_master cannot be modified.')

    @property
    def is_baseline(self):
        return self.__is_baseline

    @is_baseline.setter
    def is_baseline(self, value):
        raise RuntimeError('Attribute Suite.is_baseline cannot be modified.')

    @property
    def is_completed(self):
        return self.__is_completed

    @is_completed.setter
    def is_completed(self, value):
        raise RuntimeError('Attribute Suite.is_completed cannot be modified.')

    @property
    def completed_on(self):
        return self.__completed_on

    @completed_on.setter
    def completed_on(self, value):
        raise RuntimeError('Attribute Suite.completed_on cannot be modified.')

    ###########################################################################
    # LifeCycle Methods

    def update(self, **attributes):
        """
        Update suite attributes.

        Available for update:
            name
            description
        """
        s = testrail.core.data.TestrailData.update_suite(self.id, **attributes)

        self.__name = s.name
        self.__description = s.description

    def delete(self):
        """
        Completely remove this suite and all cases in it.
        """
        testrail.core.data.TestrailData.delete_suite(self.id)

    def add_section(self, name, description):
        """
        Create new root-level section in this suite.
        Return newly created Section object.

        :rtype: testrail.models.Section
        """
        parameters = {
            'name': name,
            'description': description,
            'suite_id': self.id
        }
        return testrail.core.data.TestrailData.add_section(self.project_id, **parameters)

    ###########################################################################
    # Query Methods

    def get_sections(self):
        """
        Return list of all sections in this suite.

        :rtype: list of [testrail.models.Section]
        """
        return testrail.core.data.TestrailData.get_sections(self.__project_id, self.__id)

    def get_section(self, name):
        """
        Return a section with this name.
        Since name is not unique - first match will be returned.

        :rtype: testrail.models.Section
        """
        for section in self.get_sections():
            if section.name == name:
                return section
        return None

    def get_sections_hierarchy(self):
        """
        Return structure of all sections in this suite.
        Respective to parent_ids.

        :rtype: list of [testrail.models.Section]
        """
        raise NotImplementedError

    def get_cases(self, **filters):
        """
        Return list of test cases in this suite.

        Possible Filters:
            created_after 	    -- Return cases created after this date*.
            created_before 	    -- Return cases created before this date*.
            created_by 	        -- Return cases created by this users**.
            updated_after 	    -- Return cases updated after this date*.
            updated_before 	    -- Return cases updated before this date*.
            updated_by 	        -- Return cases updated by this users**.
            milestones          -- Return test plans attached to this milestones***.
            priorities          -- Return cases of this priority****.
            types               -- Return cases of case types*****.

            * date can be specified by time.struct_time, datetime.datetime, int timestamp,
              float timestamp, string timestamp or string in '%Y%m%d%H%M%S' format.
           ** users can be specified by user ID, user name, email or User object.
          *** milestones can be specified by milestone ID, milestone name or Milestone object.
         **** priority can be specified by priority ID, priority name of Priority object.
        ***** case type can be specified vy type ID, type name or CaseType object

        :rtype: list of [testrail.models.Case]
        """
        parameters = {}

        for p in ['created_after', 'created_before', 'updated_after', 'updated_before']:
            try:
                parameters[p] = utils.make_timestamp(filters[p])
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
            if not isinstance(filters['updated_by'], list):
                filters['updated_by'] = [filters['updated_by']]
        except KeyError:
            pass
        else:
            parameters['updated_by'] = [utils.guess_user_id(u) for u in filters['updated_by']]

        try:
            if not isinstance(filters['milestones'], list):
                filters['milestones'] = [filters['milestones']]
        except KeyError:
            pass
        else:
            parameters['milestone_id'] = [utils.guess_milestone_id(self, m) for m in filters['milestones']]

        try:
            if not isinstance(filters['priorities'], list):
                filters['priorities'] = [filters['priorities']]
        except KeyError:
            pass
        else:
            parameters['priority_id'] = [utils.guess_priority_id(m) for m in filters['priorities']]

        try:
            if not isinstance(filters['types'], list):
                filters['types'] = [filters['types']]
        except KeyError:
            pass
        else:
            parameters['type_id'] = [utils.guess_case_type_id(m) for m in filters['types']]

        return testrail.core.data.TestrailData.get_cases(self.project_id, self.id, **parameters)

    def get_case(self, case_title):
        """
        Search for a test case with specified title.
        Since title of case is not unique, will return first match.

        :param case_title: Title to search for
        :type case_title: str
        :rtype: testrail.models.Case
        """
        for c in self.get_cases():
            if c.title == case_title:
                return c
        return None

    def get_runs(self, **filters):
        """
        Return list of test runs created from this test suite.

        Possible Filters:
            created_after 	    -- Return test runs created after this date*.
            created_before 	    -- Return test runs created before this date*.
            created_by 	        -- Return test runs created by this users**.
            is_completed 	    -- (bool) True to return completed test runs only.
                                   False - only incomplete.
            limit               -- (int) Limit the result to 'limit' test runs.
            offset              -- (int) Skip first 'offset' records in output.
            milestones          -- Return test runs attached to this milestones***.

           * date can be specified by time.struct_time, datetime.datetime, int timestamp,
             float timestamp, string timestamp or string in '%Y%m%d%H%M%S' format.
          ** users can be specified by user ID, user name, email or User object.
         *** milestones can be specified by milestone ID, milestone name or Milestone object.

        :rtype: list of [testrail.models.Run]
        """
        return self.project().get_runs(suites=self.id, **filters)
