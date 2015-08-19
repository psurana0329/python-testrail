#!/usr/bin/env python
# -*- coding:  utf-8 -*-
"""
Main Interface to the module.
"""

from __future__ import absolute_import
from __future__ import print_function

from testrail.core.connection import TestrailConnection
from testrail.core.data import TestrailData


class Testrail:
    """
    Start with initializing this class, it will configure your testrail
    connection.
    """
    def __init__(self, address, user, password, version='4.0'):
        connection = TestrailConnection(address, user, password)
        self.data = TestrailData(connection, version)

    def clear_cache(self):
        """
        Wipe all cached data.
        """
        self.data.clear_cache()

    def add_project(self, name, announcement='', show_announcement=False, suite_mode=None):
        """
        Creates new project.
        Returns newly created project object.

        :param name: Name of the new project.
        :type name: str
        :param announcement: Text to display on project page.
        :type announcement: str
        :param show_announcement: If False announcement text will not be shown.
        :type show_announcement: bool
        :param suite_mode: The suite mode of the project:
                            1 - single suite mode
                            2 - single suite + baselines mode
                            3 - multiple suites mode
                            (require Testrail >= 4.0)
        :type suite_mode: int or None
        :rtype: testrail.models.Project
        """
        parameters = {
            'name': name,
            'announcement': announcement,
            'show_announcement': show_announcement,
        }
        if suite_mode is not None:
            parameters['suite_mode'] = suite_mode
        return self.data.add_project(**parameters)

    def get_project(self, project_id=None, name=None):
        """
        Return project base on its ID or name.

        :param project_id: ID of the project to return
        :type project_id: int or None
        :param name: name of the project to return
        :type name: str of None
        :rtype: testrail.models.Project
        """
        if project_id is not None:
            return self.data.get_project_by_id(project_id)
        elif name is not None:
            return self.data.get_project_by_name(name)
        else:
            return None

    def get_projects(self, is_completed=None):
        """
        Return list of projects.

        :param is_completed: if True return only completed projects,
                             if False - only incomplete,
                             if None - return everything
        :type is_completed: bool
        :rtype: list of [testrail.models.Project]
        """
        return self.data.get_projects(is_completed)

    def get_milestone(self, milestone_id):
        """
        Return milestone base on its ID.

        :param milestone_id: ID of the milestone to return
        :type milestone_id: int
        :rtype: testrail.models.Milestone
        """
        return self.data.get_milestone_by_id(milestone_id)

    def get_suite(self, suite_id):
        """
        Return suite base on its ID.

        :param suite_id: ID of the suite to return
        :type suite_id: int
        :rtype: testrail.models.Suite
        """
        return self.data.get_suite_by_id(suite_id)

    # def get_section(self, section_id):
    #     """
    #     Return suite`s section base on its ID.
    #
    #     :param section_id: ID of the section to return
    #     :type section_id: int
    #     :rtype: testrail.models.Section
    #     """
    #     return self.data.get_section_by_id(section_id)

    def get_case(self, case_id):
        """
        Return test case base on its ID.

        :param case_id: ID of the section to return
        :type case_id: int
        :rtype: testrail.models.Case
        """
        return self.data.get_case_by_id(case_id)

    def get_plan(self, plan_id):
        raise NotImplementedError

    def get_run(self, run_id):
        raise NotImplementedError

####################################################################################################################

    def get_users(self, active=None):
        """
        Return list of users.

        :param active: if True - return only active users.
                       if False - only inactive
                       if None - return all users
        :type active: bool or None
        :rtype: list of [testrail.models.User]
        """
        return self.data.get_users(active)

    def get_user(self, user_id=None, name=None, email=None):
        """
        Return single user base on its ID, name or email.

        :param user_id: ID of user
        :type user_id: int
        :param name: name of user
        :type name: str
        :param email: email of user
        :type email: str
        :rtype: testrail.models.User
        """
        if user_id is not None:
            return self.data.get_user_by_id(user_id)
        elif name is not None:
            return self.data.get_user_by_name(name)
        elif email is not None:
            return self.data.get_user_by_email(email)
        else:
            return None

    def get_default_priority(self):
        """
        Return default priority object.
        """
        return self.data.get_default_priority()

    def get_default_case_type(self):
        """
        Return default case type object.
        """
        return self.data.get_default_case_type()





