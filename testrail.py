#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
A high-level interface to Testrail API.

This is not a complete implementation of API methods provided by Testrail in
documentation here: http://docs.gurock.com/testrail-api2/start
I was creating a library useful for scripting. Many operations should not be
perform via scripts. For example managing suite structure is easier in
user interface. Also bulk methods provided by API is quite useless in script,
which can easily do bulk operations itself. So I did not implement some methods
to keep it simple.

One thing to remember = this module is not designed for long-time work, it is
for single-run scripts. So it will be better to re-run entire script rather
than do something in endless loop.
"""
#TODO: Previous versions support
#TODO: Test Plan full support

from __future__ import absolute_import
from __future__ import print_function

import time
import datetime
import json
from collections import defaultdict

try:
    import requests
    import requests.auth as auth
except ImportError:
    raise RuntimeError('Module "requests" is required.')


__author__ = 'Vyacheslav Spiridonov'

__version__ = '0.1.0'
__maintainer__ = 'Vyacheslav Spiridonov'
__email__ = 'namelessorama@gmail.com'
__status__ = 'Development'


################################################################################
# Exceptions
################################################################################
class NotFound(Exception):
    """
    Will be raised when request results to 400 code on server, meaning there is
    no object with requested parameters.
    """
    pass


class AccessDenied(Exception):
    """
    Will be raised when request results to 403 code on server, meaning you don`t
    have required permissions.
    """
    pass


################################################################################
# Service Classes
################################################################################
class _Comparable(object):
    def __lt__(self, other):
        # Override me
        raise NotImplementedError

    def __eq__(self, other):
        return not self < other and not other < self

    def __ne__(self, other):
        return self < other or other < self

    def __gt__(self, other):
        return other < self

    def __ge__(self, other):
        return not self < other

    def __le__(self, other):
        return not other < self


class _TestrailObject(object):

    cache = None

    def __init__(self, attributes):
        """
        :arg attributes: dictionary of object fields (attributes)
        :type attributes: dict
        """
        self.id = None

        self._settle_attributes(attributes)

        # store links to the object in cache
        self.cache[self.id] = self

    def _settle_attributes(self, attributes):
        raise NotImplementedError

    def __str__(self):
        return '<%s object [%s]>' % (self.__class__.__name__, self.id)


class _CustomField(object):
    def __init__(self):
        self.configs = []

    def present_in_project(self, project_id):
        """
        Return True if this field is applicable to provided project_id,
        False otherwise
        """
        for config in self.configs:
            if project_id in config.project_ids:
                return True
        return False


################################################################################
# Main Class
################################################################################
class Testrail(object):
    """
    Main class for testrail communication.

    Start with initializing this class, this will configuring your testrail
    connection.
    """

    session = requests.Session()
    base_url = ''

    version = (4, 0)

    def __init__(self,
                 host='', port='80',
                 user='', password='',
                 compatibility=(4, 0)):
        Testrail.base_url = 'http://%s:%s/testrail/index.php?api/v2/' % (
            host,
            port
        )

        Testrail.session.headers.update({
            'Content-Type': 'application/json'
        })

        Testrail.session.auth = auth.HTTPBasicAuth(user, password)

        Testrail.version = compatibility

    ############################################################################
    # Shortcuts to access API by relative path and do common error processing

    @staticmethod
    def get(url, **kwargs):
        print('GET ', url, kwargs)  # debug

        result = Testrail.session.get(Testrail.base_url + url, **kwargs)

        if result.status_code == 200:
            return json.loads(result.text)
        elif result.status_code == 400:
            raise NotFound(json.loads(result.text)['error'])
        elif result.status_code == 403:
            raise AccessDenied(json.loads(result.text)['error'])
        else:
            return defaultdict(lambda: None)

    @staticmethod
    def post(url, data=None, **kwargs):
        print('POST', url, kwargs)  # debug

        if data is not None:
            result = Testrail.session.post(Testrail.base_url + url,
                                           data=json.dumps(data),
                                           **kwargs)
        else:
            result = Testrail.session.post(Testrail.base_url + url,
                                           **kwargs)

        if result.status_code == 200:
            return json.loads(result.text)
        elif result.status_code == 400:
            raise NotFound(json.loads(result.text)['error'])
        elif result.status_code == 403:
            raise AccessDenied(json.loads(result.text)['error'])
        else:
            return defaultdict(lambda: None)

    ############################################################################
    # Common Logic to work with read-only objects (Users, Priorities,
    # Test Statuses, Case Types, Case Fields and Result Fields)
    #
    # 1. Objects are loaded from server all at once when any of them required.
    # 2. And stay in memory to the end of the script.
    # 3. No reload attempts will be made

    @staticmethod
    def _get_objects_list(object_class):

        if object_class.cache is not None:
            return object_class.cache.values()

        else:
            object_class.cache = {}
            return object_class.get_all()

    @staticmethod
    def _get_object_from_list(object_class,
                              search_attribute, search_value):

        for item in Testrail._get_objects_list(object_class):
            if getattr(item, search_attribute) == search_value:
                return item

        raise NotFound('No %s with %s: %s' % (object_class.__name__,
                                              search_attribute,
                                              search_value))

    ############################################################################
    # User methods

    @staticmethod
    def users():
        """
        Get list of all testrail users.

        :rtype: list of [User]
        """
        return Testrail._get_objects_list(User)

    @staticmethod
    def get_user_by_id(user_id):
        """
        :type user_id: int
        :rtype: User
        """
        return Testrail._get_object_from_list(User, 'id', user_id)

    @staticmethod
    def get_user_by_name(user_name):
        """
        :type user_name: str
        :rtype: User
        """
        return Testrail._get_object_from_list(User, 'name', user_name)

    @staticmethod
    def get_user_by_email(user_email):
        """
        :type user_email: str
        :rtype: User
        """
        return Testrail._get_object_from_list(User, 'email', user_email)

    ############################################################################
    # Priority methods

    @staticmethod
    def priorities():
        """
        Get list of all configured priorities.

        :rtype: list of [Priority]
        """
        return Testrail._get_objects_list(Priority)

    @staticmethod
    def get_priority_by_id(priority_id):
        """
        :type priority_id: int
        :rtype: Priority
        """
        return Testrail._get_object_from_list(Priority, 'id', priority_id)

    @staticmethod
    def get_priority_by_name(priority_name):
        """
        :arg priority_name: A short_name (abbreviation) of the priority.

        :type priority_name: str
        :rtype: Priority
        """
        return Testrail._get_object_from_list(Priority, 'short_name',
                                              priority_name)

    @staticmethod
    def get_priority_by_value(priority_value):
        """
        :type priority_value: int
        :rtype: Priority
        """
        return Testrail._get_object_from_list(Priority, 'priority',
                                              priority_value)

    ############################################################################
    # Test Status methods

    @staticmethod
    def statuses():
        """
        Returns a list of all active test statuses.

        :rtype: list of [Status]
        """
        return Testrail._get_objects_list(Status)

    @staticmethod
    def get_status_by_id(status_id):
        """
        :type status_id: int
        :rtype: Status
        """
        return Testrail._get_object_from_list(Status, 'id', status_id)

    @staticmethod
    def get_status_by_name(status_name):
        """
        :arg status_name: a Label (human name) of the status.

        :type status_name: str
        :rtype: Status
        """
        return Testrail._get_object_from_list(Status, 'label', status_name)

    ############################################################################
    # Case Type methods

    @staticmethod
    def case_types():
        """
        Returns a list of available case types.

        :rtype: list of [CaseType]
        """
        return Testrail._get_objects_list(CaseType)

    @staticmethod
    def get_case_type_by_id(case_type_id):
        """
        :type case_type_id: int
        :rtype: CaseType
        """
        return Testrail._get_object_from_list(CaseType, 'id', case_type_id)

    @staticmethod
    def get_case_type_by_name(case_type_name):
        """
        :type case_type_name: str
        :rtype: CaseType
        """
        return Testrail._get_object_from_list(CaseType, 'name', case_type_name)

    ############################################################################
    # Case Field methods

    @staticmethod
    def case_fields():
        """
        Returns a list of all case custom fields.

        :rtype: list of [CaseField]
        """
        return Testrail._get_objects_list(CaseField)

    @staticmethod
    def get_case_field_by_id(case_field_id):
        """
        :type case_field_id: int
        :rtype: CaseField
        """
        return Testrail._get_object_from_list(CaseField, 'id', case_field_id)

    @staticmethod
    def get_case_field_by_name(case_field_name):
        """
        :arg case_field_name: a Label of the field (used in the user interface)

        :type case_field_name: str
        :rtype: CaseField
        """
        return Testrail._get_object_from_list(CaseField, 'label',
                                              case_field_name)

    ############################################################################
    # Result Field methods

    @staticmethod
    def result_fields():
        """
        Returns a list of all result custom fields.

        :rtype: list of [ResultField]
        """
        return Testrail._get_objects_list(ResultField)

    @staticmethod
    def get_result_field_by_id(result_field_id):
        """
        :type result_field_id: int
        :rtype: ResultField
        """
        return Testrail._get_object_from_list(ResultField, 'id',
                                              result_field_id)

    @staticmethod
    def get_result_field_by_name(result_field_name):
        """
        :arg result_field_name: a Label of the field (used in the user
                                interface)

        :type result_field_name: str
        :rtype: ResultField
        """
        return Testrail._get_object_from_list(ResultField, 'label',
                                              result_field_name)

    ############################################################################
    # Common Logic to work with read-write objects (Projects, Milestones,
    # Suites, Sections, Runs, Plans, Runs, Tests and Results)
    #
    # 1. Requests for a list of objects always is forwarded to server.
    # 2. All loaded objects go to the cache.
    # 3. When single object is requested - cache is checked first.

    @staticmethod
    def _get_object_by_id(object_class, object_id):

        try:
            return object_class.cache[object_id]

        except KeyError:
            return object_class.get_one(object_id)

    ############################################################################
    # Project methods

    @staticmethod
    def projects(is_completed=None):
        """
        Get list of projects.

        :arg is_completed: True - to return only completed projects.
                           False - only incomplete.
                           None - return all projects.
        :type is_completed: bool
        :rtype: list of [Project]
        """
        return [Project(p) for p in TestrailAPI.get_projects(is_completed)]

    @staticmethod
    def get_project_by_id(project_id):
        """
        :type project_id: int
        :rtype: Project
        """
        return Testrail._get_object_by_id(Project, project_id)

    @staticmethod
    def get_project_by_name(project_name):
        """
        :type project_name: str
        :rtype: Project
        """
        for p in Testrail.projects():
            if p.name == project_name:
                return p

        raise NotFound('No Project with name: %s' % project_name)

    @staticmethod
    def add_project(name, announcement='', show_announcement=False,
                    suite_mode=3):
        """
        Creates new project.
        Returns newly created project object.

        :arg name: Name of new project
        :arg announcement: Announcement/Description of new project
        :arg show_announcement: True to show the announcement/description on
                                project page and false otherwise
        :arg suite_mode: The suite mode of the project:
                         1 - single suite mode
                         2 - single suite + baselines mode
                         3 - multiple suites mode

        :type name: str
        :type announcement: str
        :type show_announcement: bool
        :type suite_mode: int
        :rtype: Project
        """
        return Project(TestrailAPI.add_project(name=name,
                                               announcement=announcement,
                                               show_announcement=show_announcement,
                                               suite_mode=suite_mode))

    ############################################################################
    # Direct access by object ID

    @staticmethod
    def get_suite_by_id(suite_id):
        """
        :type suite_id: int
        :rtype: Suite
        """
        return Testrail._get_object_by_id(Suite,
                                          suite_id)

    @staticmethod
    def get_milestone_by_id(milestone_id):
        """
        :type milestone_id: int
        :rtype: Milestone
        """
        return Testrail._get_object_by_id(Milestone,
                                          milestone_id)

    @staticmethod
    def get_section_by_id(section_id):
        """
        :type section_id: int
        :rtype: Section
        """
        return Testrail._get_object_by_id(Section,
                                          section_id)

    @staticmethod
    def get_case_by_id(case_id):
        """
        :type case_id: int
        :rtype: Case
        """
        return Testrail._get_object_by_id(Case,
                                          case_id)

    @staticmethod
    def get_plan_by_id(plan_id):
        """
        :type plan_id: int
        :rtype: Plan
        """
        return Testrail._get_object_by_id(Plan,
                                          plan_id)

    @staticmethod
    def get_run_by_id(run_id):
        """
        :type run_id: int
        :rtype: Run
        """
        return Testrail._get_object_by_id(Run,
                                          run_id)

    @staticmethod
    def get_test_by_id(test_id):
        """
        :type test_id: int
        :rtype: Test
        """
        return Testrail._get_object_by_id(Test,
                                          test_id)


################################################################################
# API methods as-is (can be used, but not intended to)
################################################################################
class TestrailAPI(object):

    @staticmethod
    def get_case(case_id):
        return Testrail.get('get_case/%s' % case_id)

    @staticmethod
    def get_cases(project_id, suite_id, section_id=None, created_after=None,
                created_before=None, created_by=None, milestone_id=None,
                priority_id=None, type_id=None, updated_after=None,
                updated_before=None, updated_by=None):
        pattern = 'get_cases/%s&suite_id=%s' % (project_id, suite_id)

        if section_id is not None:
            pattern += '&section_id=%s' % section_id

        if created_after is not None:
            pattern += '&created_after=%s' % created_after

        if created_before is not None:
            pattern += '&created_before=%s' % created_before

        if created_by is not None:
            pattern += '&created_by=%s' % ','.join(created_by)

        if milestone_id is not None:
            pattern += '&milestone_id=%s' % ','.join(milestone_id)

        if priority_id is not None:
            pattern += '&priority_id=%s' % ','.join(priority_id)

        if type_id is not None:
            pattern += '&type_id=%s' % ','.join(type_id)

        if updated_after is not None:
            pattern += '&updated_after=%s' % updated_after

        if updated_before is not None:
            pattern += '&updated_before=%s' % updated_before

        if updated_by is not None:
            pattern += '&updated_by=%s' % ','.join(updated_by)

        return Testrail.get(pattern)

    @staticmethod
    def add_case(section_id, **kwargs):
        """
        The following POST fields are supported (system fields):

        title	    string	    The title of the test case (required)
        type_id	    int	        The ID of the case type
        priority_id	int	        The ID of the case priority
        estimate	timespan	The estimate, e.g. "30s" or "1m 45s"
        milestone_id	int	    The ID of the milestone to link to the test case
        refs	    string	    A comma-separated list of references/
                                requirements
        """
        return Testrail.post('add_case/%s' % section_id,
                             data=kwargs)

    @staticmethod
    def update_case(case_id, **kwargs):
        """
        Same fields as _add_case
        """
        return Testrail.post('update_case/%s' % case_id,
                             data=kwargs)

    @staticmethod
    def delete_case(case_id):
        return Testrail.post('delete_case/%s' % case_id)

    @staticmethod
    def get_case_fields():
        return Testrail.get('get_case_fields')

    @staticmethod
    def get_case_types():
        return Testrail.get('get_case_types')

    @staticmethod
    def get_configs(project_id):
        return Testrail.get('get_configs/%s' % project_id)

    @staticmethod
    def get_milestone(milestone_id):
        return Testrail.get('get_milestone/%s' % milestone_id)

    @staticmethod
    def get_milestones(project_id, is_completed=None):
        pattern = 'get_milestones/%s' % project_id

        if is_completed is not None:
            pattern += '&is_completed=%s' % int(is_completed)

        return Testrail.get(pattern)

    @staticmethod
    def add_milestone(project_id, **kwargs):
        """
        The following POST fields are supported:

        name	    string	    The name of the milestone (required)
        description	string	    The description of the milestone
        due_on	    timestamp	The due date of the milestone
                                (as UNIX timestamp)
        """
        return Testrail.post('add_milestone/%s' % project_id,
                             data=kwargs)

    @staticmethod
    def update_milestone(milestone_id, **kwargs):
        """
        Same fields as _add_milestone, and also:

        is_completed	bool	Specifies whether a milestone is considered
                                completed or not
        """
        return Testrail.post('update_milestone/%s' % milestone_id,
                             data=kwargs)

    @staticmethod
    def delete_milestone(milestone_id):
        return Testrail.post('delete_milestone/%s' % milestone_id)

    @staticmethod
    def get_plan(plan_id):
        return Testrail.get('get_plan/%s' % plan_id)

    @staticmethod
    def get_plans(project_id, created_after=None, created_before=None,
                  created_by=None, is_completed=None, limit=None,
                  offset=None, milestone_id=None):
        pattern = 'get_plans/%s' % project_id

        if created_after is not None:
            pattern += '&created_after=%s' % created_after

        if created_before is not None:
            pattern += '&created_before=%s' % created_before

        if created_by is not None:
            pattern += '&created_by=%s' % ','.join(created_by)

        if is_completed is not None:
            pattern += '&is_completed=%s' % int(is_completed)

        if limit is not None:
            pattern += '&limit=%s' % limit

        if offset is not None:
            pattern += '&offset=%s' % offset

        if milestone_id is not None:
            pattern += '&milestone_id=%s' % ','.join(milestone_id)

        return Testrail.get(pattern)

    @staticmethod
    def add_plan(project_id, **kwargs):
        """
        The following POST fields are supported:

        name	    string	    The name of the test plan (required)
        description	string	    The description of the test plan
        milestone_id	int	    The ID of the milestone to link to the test plan
        entries	    array	    An array of objects describing the test runs of
                                the plan, see _add_plan_entry
        """
        return Testrail.post('add_plan/%s' % project_id,
                             data=kwargs)

    @staticmethod
    def add_plan_entry(plan_id, **kwargs):
        """
        The following POST fields are supported:

        suite_id	    int	    The ID of the test suite for the test run(s)
                                (required)
        name	        string	The name of the test run (s)
        assignedto_id	int	    The ID of the user the test run(s) should be
                                assigned to
        include_all	    bool	True for including all test cases of the test
                                suite and false for a custom case selection
                                (default: true)
        case_ids	    array	An array of case IDs for the custom case
                                selection
        config_ids	    array	An array of configuration IDs used for the test
                                runs of the test plan entry
                                (requires TestRail 3.1 or later)
        runs	        array	An array of test runs with configurations
                                (requires TestRail 3.1 or later)
        """
        return Testrail.post('add_plan_entry/%s' % plan_id,
                             data=kwargs)

    @staticmethod
    def update_plan(plan_id, **kwargs):
        """
        Same fields as _add_plan
        """
        return Testrail.post('update_plan/%s' % plan_id,
                             data=kwargs)

    @staticmethod
    def update_plan_entry(plan_id, entry_id, **kwargs):
        """
        The following POST fields are supported:

        name	        string	The name of the test run(s)
        assignedto_id	int	    The ID of the user the test run(s) should be
                                assigned to
        include_all	    bool	True for including all test cases of the test
                                suite and false for a custom case selection
                                (default: true)
        case_ids	    array	An array of case IDs for the custom case
                                selection
        """
        return Testrail.post('update_plan_entry/%s/%s' % (plan_id, entry_id),
                             data=kwargs)

    @staticmethod
    def close_plan(plan_id):
        return Testrail.post('close_plan/%s' % plan_id)

    @staticmethod
    def delete_plan(plan_id):
        return Testrail.post('delete_plan/%s' % plan_id)

    @staticmethod
    def delete_plan_entry(plan_id, entry_id):
        return Testrail.post('delete_plan_entry/%s/%s' % (plan_id, entry_id))

    @staticmethod
    def get_priorities():
        return Testrail.get('get_priorities')

    @staticmethod
    def get_project(project_id):
        return Testrail.get('get_project/%s' % project_id)

    @staticmethod
    def get_projects(is_completed=None):
        pattern = 'get_projects'

        if is_completed is not None:
            pattern += '&is_completed=%s' % int(is_completed)

        return Testrail.get(pattern)

    @staticmethod
    def add_project(**kwargs):
        """
        The following POST fields are supported:

        name	        string	    The name of the project (required)
        announcement	string	    The description of the project
        show_announcement	bool	True if the announcement should be displayed
                                    on the project's overview page and
                                    false otherwise
        suite_mode	    integer	    The suite mode of the project (1 for single
                                    suite mode, 2 for single suite + baselines,
                                    3 for multiple suites)
                                    (added with TestRail 4.0)
        """
        return Testrail.post('add_project',
                             data=kwargs)

    @staticmethod
    def update_project(project_id, **kwargs):
        """
        Same fields as _add_project, and also:

        is_completed	bool	Specifies whether a project is considered
                                completed or not
        """
        return Testrail.post('update_project/%s' % project_id,
                             data=kwargs)

    @staticmethod
    def delete_project(project_id):
        return Testrail.post('delete_project/%s' % project_id)

    @staticmethod
    def get_results(test_id, limit=None, offset=None, status_id=None):
        pattern = 'get_results/%s' % test_id

        if limit is not None:
            pattern += '&limit=%s' % limit

        if offset is not None:
            pattern += '&offset=%s' % offset

        if status_id is not None:
            pattern += '&status_id=%s' % ','.join(status_id)

        return Testrail.get(pattern)

    @staticmethod
    def get_results_for_case(run_id, case_id, limit=None,
                             offset=None, status_id=None):
        pattern = 'get_results_for_case/%s/%s' % (run_id, case_id)

        if limit is not None:
            pattern += '&limit=%s' % limit

        if offset is not None:
            pattern += '&offset=%s' % offset

        if status_id is not None:
            pattern += '&status_id=%s' % ','.join(status_id)

        return Testrail.get(pattern)

    @staticmethod
    def get_results_for_run(run_id, created_after=None,
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

        return Testrail.get(pattern)

    @staticmethod
    def add_result(test_id, **kwargs):
        """
        The following POST fields are supported (system fields):

        status_id	    int	    The ID of the test status. The built-in system
                                statuses have the following IDs:
                                1	Passed
                                2	Blocked
                                3	Untested
                                4	Retest
                                5	Failed
                                You can get a full list of system and custom
                                statuses via get_statuses.
        comment	        string	The comment / description for the test result
        version	        string	The version or build you tested against
        elapsed	        timespan	The time it took to execute the test,
                                    e.g. "30s" or "1m 45s"
        defects	        string	A comma-separated list of defects to link to
                                the test result
        assignedto_id	int	    The ID of a user the test should be assigned to
        """
        return Testrail.post('add_result/%s' % test_id,
                             data=kwargs)

    @staticmethod
    def add_result_for_case(run_id, case_id, **kwargs):
        """
        Same fields as _add_result
        """
        return Testrail.post('add_result_for_case/%s/%s' % (run_id, case_id),
                             data=kwargs)

    @staticmethod
    def add_results(run_id, **kwargs):
        """
        This method expects an array of test results (via the 'results' field).
        Each test result must specify the test ID and can pass in the same
        fields as _add_result
        """
        return Testrail.post('add_results/%s' % run_id,
                             data=kwargs)

    @staticmethod
    def add_results_for_cases(run_id, **kwargs):
        """
        Same as _add_results but with Case_ID rather than Test_ID.
        """
        return Testrail.post('add_results_for_cases/%s' % run_id,
                             data=kwargs)

    @staticmethod
    def get_result_fields():
        return Testrail.get('get_result_fields')

    @staticmethod
    def get_run(run_id):
        return Testrail.get('get_run/%s' % run_id)

    @staticmethod
    def get_runs(project_id, created_after=None, created_before=None,
                 created_by=None, is_completed=None, limit=None,
                 offset=None, milestone_id=None, suite_id=None):
        pattern = 'get_runs/%s' % project_id

        if created_after is not None:
            pattern += '&created_after=%s' % created_after

        if created_before is not None:
            pattern += '&created_before=%s' % created_before

        if created_by is not None:
            pattern += '&created_by=%s' % ','.join(created_by)

        if is_completed is not None:
            pattern += '&is_completed=%s' % int(is_completed)

        if limit is not None:
            pattern += '&limit=%s' % limit

        if offset is not None:
            pattern += '&offset=%s' % offset

        if milestone_id is not None:
            pattern += '&milestone_id=%s' % ','.join(milestone_id)

        if suite_id is not None:
            pattern += '&suite_id=%s' % ','.join(suite_id)

        return Testrail.get(pattern)

    @staticmethod
    def add_run(project_id, **kwargs):
        """
        The following POST fields are supported:

        suite_id	    int	    The ID of the test suite for the test run
                                (optional if the project is operating in single
                                suite mode, required otherwise)
        name	        string	The name of the test run
        description	    string	The description of the test run
        milestone_id	int	    The ID of the milestone to link to the test run
        assignedto_id	int	    The ID of the user the test run should be
                                assigned to
        include_all	    bool	True for including all test cases of the test
                                suite and false for a custom case selection
                                (default: true)
        case_ids	    array	An array of case IDs for the custom case
                                selection
        """
        return Testrail.post('add_run/%s' % project_id,
                             data=kwargs)

    @staticmethod
    def update_run(run_id, **kwargs):
        """
        Same fields as _add_run
        """
        return Testrail.post('update_run/%s' % run_id,
                             data=kwargs)

    @staticmethod
    def close_run(run_id):
        return Testrail.post('close_run/%s' % run_id)

    @staticmethod
    def delete_run(run_id):
        return Testrail.post('delete_run/%s' % run_id)

    @staticmethod
    def get_section(section_id):
        return Testrail.get('get_section/%s' % section_id)

    @staticmethod
    def get_sections(project_id, suite_id):
        return Testrail.get('get_sections/%s&suite_id=%s' % (project_id,
                                                             suite_id))

    @staticmethod
    def add_section(project_id, **kwargs):
        """
        The following POST fields are supported:

        description	string	The description of the section
                            (added with TestRail 4.0)
        suite_id	int	    The ID of the test suite (ignored if the project
                            is operating in single suite mode,
                            required otherwise)
        parent_id	int	    The ID of the parent section (to build
                            section hierarchies)
        name	    string	The name of the section (required)
        """
        return Testrail.post('add_section/%s' % project_id,
                             data=kwargs)

    @staticmethod
    def update_section(section_id, **kwargs):
        """
        The following POST fields are supported:

        description	string	The description of the section
                            (added with TestRail 4.0)
        name	    string	The name of the section (required)
        """
        return Testrail.post('update_section/%s' % section_id,
                             data=kwargs)

    @staticmethod
    def delete_section(section_id):
        return Testrail.post('delete_section/%s' % section_id)

    @staticmethod
    def get_statuses():
        return Testrail.get('get_statuses')

    @staticmethod
    def get_suite(suite_id):
        return Testrail.get('get_suite/%s' % suite_id)

    @staticmethod
    def get_suites(project_id):
        return Testrail.get('get_suites/%s' % project_id)

    @staticmethod
    def add_suite(project_id, **kwargs):
        """
        The following POST fields are supported:

        name	    string	The name of the test suite (required)
        description	string	The description of the test suite
        """
        return Testrail.post('add_suite/%s' % project_id,
                             data=kwargs)

    @staticmethod
    def update_suite(suite_id, **kwargs):
        """
        Same fields as _add_suite
        """
        return Testrail.post('update_suite/%s' % suite_id,
                             data=kwargs)

    @staticmethod
    def delete_suite(suite_id):
        return Testrail.post('delete_suite/%s' % suite_id)

    @staticmethod
    def get_test(test_id):
        return Testrail.get('get_test/%s' % test_id)

    @staticmethod
    def get_tests(run_id, status_id=None):
        pattern = 'get_tests/%s' % run_id

        if status_id is not None:
            pattern += '&status_id=%s' % ','.join(status_id)

        return Testrail.get(pattern)

    @staticmethod
    def get_user(user_id):
        return Testrail.get('get_user/%s' % user_id)

    @staticmethod
    def get_user_by_email(email):
        return Testrail.get('get_user_by_email&email=%s' % email)

    @staticmethod
    def get_users():
        return Testrail.get('get_users')


################################################################################
# Read-Only Objects
################################################################################
class User(_TestrailObject):
    """
    User container.

    Attributes:
       id           -- The unique ID of the user
       name         -- The full name of the user
       email        -- The email address of the user as configured in TestRail
       is_active    -- True if the user is active and false otherwise
    """

    cache = None

    def _settle_attributes(self, attributes):
        self.id = attributes['id']
        self.name = attributes['name']
        self.email = attributes['email']
        self.is_active = attributes['is_active']

    @staticmethod
    def get_all():
        return [User(u) for u in TestrailAPI.get_users()]


class Priority(_TestrailObject, _Comparable):
    """
    Priority of Test or Case: Blocker, Critical, Normal and others.

    Attributes:
       id           -- The ID of the priority
       name         -- The full name of the priority
       short_name   -- The short name of the priority (is used in tables)
       is_default   -- True if this priority is set by default in new test cases
       priority     -- Priority value
    """

    cache = None

    def _settle_attributes(self, attributes):
        self.id = attributes['id']
        self.name = attributes['name']

        self.short_name = attributes['short_name']
        self.is_default = attributes['is_default']
        self.priority = attributes['priority']

    def __lt__(self, other):
        return self.priority < other.priority

    def __hash__(self):
        return hash(self.priority)

    @staticmethod
    def get_all():
        return [Priority(p) for p in TestrailAPI.get_priorities()]


class Status(_TestrailObject):
    """
    Test Status: Passed, Failed, Blocked, Retest and custom.

    Attributes:
       id           -- The ID of the test status
       name         -- The system name of the test status
       label        -- The human-readable name of status (used in interface)
       is_system    -- True if this is a system (read-only) status
       is_untested  -- True if this status treated as 'Untested'
       is_final     -- True if this status treated as 'Final'
       color_bright -- Interface color (see docs.)
       color_medium -- Interface color (see docs.)
       color_dark   -- Interface color (see docs.)
    """

    cache = None

    def _settle_attributes(self, attributes):
        self.id = attributes['id']
        self.name = attributes['name']

        self.label = attributes['label']
        self.is_system = attributes['is_system']
        self.is_untested = attributes['is_untested']
        self.is_final = attributes['is_final']

        self.color_bright = attributes['color_bright']
        self.color_medium = attributes['color_medium']
        self.color_dark = attributes['color_dark']

    @staticmethod
    def get_all():
        return [Status(p) for p in TestrailAPI.get_statuses()]


class CaseType(_TestrailObject):
    """
    Case Type: Functionality, Performance, Stress, etc...

    Attributes:
       id           -- The ID of the case type
       name         -- The name of the case type
       is_default   -- True if this type is set by default in new test cases
    """

    cache = None

    def _settle_attributes(self, attributes):
        self.id = attributes['id']
        self.name = attributes['name']
        self.is_default = attributes['is_default']

    @staticmethod
    def get_all():
        return [CaseType(t) for t in TestrailAPI.get_case_types()]


class CaseField(_TestrailObject, _CustomField):
    """
    Custom case field.

    Attributes:
       id           -- The ID of the custom case field
       type_id      -- Type of this field:
                       1 - String
                       2 - Integer
                       3 - Text
                       4 - URL
                       5 - Checkbox
                       6 - Dropdown
                       7 - User
                       8 - Date
                       9 - Milestone
                       10 - Steps
                       12 - Multi-select
       name         -- The name of the custom case field
       system_name  -- The system name of custom case field
       label        -- The name of the field, used in the user interface
       description  -- The description of the field
       display_order    -- Position of the field in the user Interface
       configs      -- list of configuration
    """

    cache = None

    def _settle_attributes(self, attributes):
        self.id = attributes['id']
        self.type_id = attributes['type_id']

        self.name = attributes['name']
        self.system_name = attributes['system_name']
        self.label = attributes['label']

        self.description = attributes['description']

        self.display_order = attributes['display_order']

        self.configs = [_FieldConfig(c) for c in attributes['configs']]

    @staticmethod
    def get_all():
        return [CaseField(f) for f in TestrailAPI.get_case_fields()]


class ResultField(_TestrailObject, _CustomField):
    """
    Custom result field.

    Attributes:
       id           -- The ID of the custom result field
       type_id      -- Type of this field:
                       1 - String
                       2 - Integer
                       3 - Text
                       4 - URL
                       5 - Checkbox
                       6 - Dropdown
                       7 - User
                       8 - Date
                       9 - Milestone
                       10 - Steps
                       12 - Multi-select
       name         -- The name of the custom result field
       system_name  -- The system name of custom result field
       label        -- The name of the field, used in the user interface
       description  -- The description of the field
       display_order    -- Position of the field in the user Interface
       configs      -- list of configuration
    """

    cache = None

    def _settle_attributes(self, attributes):
        self.id = attributes['id']
        self.type_id = attributes['type_id']

        self.name = attributes['name']
        self.system_name = attributes['system_name']
        self.label = attributes['label']

        self.description = attributes['description']

        self.display_order = attributes['display_order']

        self.configs = [_FieldConfig(c) for c in attributes['configs']]

    @staticmethod
    def get_all():
        return [ResultField(f) for f in TestrailAPI.get_result_fields()]


class _FieldConfig(object):
    """
    Custom field (case or result) config.

    Attributes:
       id               -- The ID of the custom field
       is_global        -- If True this config applies to all projects
       project_ids      -- List of projects to apply this config (if not global)
       is_required      -- True if this field is required
       default_value    -- Default value of the field
       options          -- Some more parameters, depending of Field Type
    """
    def __init__(self, attributes):
        self.id = attributes['id']

        self.is_global = attributes['context']['is_global']

        if self.is_global:
            self.project_ids = [
                p.id for p in Testrail.projects()
            ]
        else:
            self.project_ids = [
                int(i) for i in attributes['context']['project_ids']
            ]

        self.is_required = attributes['options']['is_required']
        del attributes['options']['is_required']
        try:
            self.default_value = attributes['options']['default_value']
            del attributes['options']['default_value']
        except KeyError:
            self.default_value = None

        self.options = attributes['options']

    def __str__(self):
        return '<CaseFieldConfig object: [%s]>' % self.id


################################################################################
# Read-Write Objects
################################################################################
class Project(_TestrailObject):
    """
    Testrail Project container.

    Testrail Attributes:
       id                -- Project id (unique)
       name              -- Project name
       url               -- Url of the project web-page in the user interface
       suite_mode        -- The suite mode of the project:
                            1 - single suite mode
                            2 - single suite + baselines mode
                            3 - multiple suites mode
       announcement      -- The description/announcement of the project
       show_announcement -- True to show the announcement/description on
                            project page and false otherwise
       is_completed      -- True if the project is marked as completed and
                            false otherwise
       completed_on      -- The date/time when the project was marked as
                            completed (as UNIX timestamp)
    """

    cache = {}

    def _settle_attributes(self, attributes):
        self.id = attributes['id']
        self.name = attributes['name']
        self.url = attributes['url']
        self.suite_mode = attributes['suite_mode']

        self.announcement = attributes['announcement']
        self.show_announcement = attributes['show_announcement']
        self.is_completed = attributes['is_completed']
        self.completed_on = attributes['completed_on']

        self.custom_case_fields = []
        for custom_case_field in Testrail.case_fields():
            if custom_case_field.present_in_project(self.id):
                self.custom_case_fields.append(custom_case_field)

        self.custom_result_fields = []
        for custom_result_field in Testrail.result_fields():
            if custom_result_field.present_in_project(self.id):
                self.custom_result_fields.append(custom_result_field)

        self._milestones = None
        self._suites = None

    @staticmethod
    def get_one(project_id):
        return Project(TestrailAPI.get_project(project_id))

    def update(self, name=None, announcement=None, show_announcement=None,
               suite_mode=None, is_completed=None):
        """
        Change project parameters.

        :rtype: None
        """
        data = {}
        if name is not None:
            data['name'] = name

        if announcement is not None:
            data['announcement'] = announcement

        if show_announcement is not None:
            data['show_announcement'] = show_announcement

        if suite_mode is not None:
            data['suite_mode'] = suite_mode

        if is_completed is not None:
            data['is_completed'] = is_completed

        self._settle_attributes(TestrailAPI.update_project(self.id, **data))

    def delete(self):
        """
        Wipe out this project.

        !!! Deleting a project cannot be undone and also permanently deletes
        all test suites & cases, test runs & results and everything else
        that is part of the project.
        """
        TestrailAPI.delete_project(self.id)
        self._settle_attributes(defaultdict(lambda: None))

    def configs(self):
        """
        Get project configuration groups

        :rtype: list of [ConfigGroup]
        """
        return [ConfigGroup(c) for c in TestrailAPI.get_configs(self.id)]

    def milestones(self, is_completed=None):
        """
        Get list of milestones in this project.

        :arg is_completed: True - to return only completed milestones.
                           False - only incomplete.
                           None - return all milestones.

        :type is_completed: bool
        :rtype: list of [Milestone]
        """
        if self._milestones is not None:
            return self._milestones

        else:
            self._milestones = [
                Milestone(m) for m in
                TestrailAPI.get_milestones(self.id, is_completed)
            ]
            return self._milestones

    def get_milestone_by_name(self, milestone_name):
        """
        :type milestone_name: str
        :rtype: Milestone
        """
        for m in self.milestones():
            if m.name == milestone_name:
                return m

        raise NotFound('No milestone with name: %s' % milestone_name)

    def add_milestone(self, name, description='', due_on=None):
        """
        Creates new milestone.
        Returns newly created milestone object.

        :arg name: Name of new milestone
        :arg due_on: The due date of the milestone
        :arg description: Description of new milestone

        :type name: str
        :type description: str
        :type due_on: datetime.datetime
        :rtype: Milestone
        """
        data = {
            'name': name,
            'description': description
        }
        if due_on is not None:
            data['due_on'] = int(time.mktime(
                due_on.timetuple()
            ))

        return Milestone(TestrailAPI.add_milestone(self.id, **data))

    def suites(self):
        """
        Returns list of all suites in the project.

        :rtype: list of [Suite]
        """
        if self._suites is not None:
            return self._suites

        else:
            self._suites = [Suite(s) for s in TestrailAPI.get_suites(self.id)]
            return self._suites

    def get_suite_by_name(self, suite_name):
        """
        :type suite_name: str
        :rtype: Suite
        """
        for s in self.suites():
            if s.name == suite_name:
                return s

        raise NotFound('No suite with name: %s' % suite_name)

    def add_suite(self, name, description=''):
        """
        Creates new test suite.
        Returns newly created test suite object.

        :type name: str
        :type description: str
        :rtype: Suite
        """
        data = {
            'name': name,
            'description': description
        }

        return Suite(TestrailAPI.add_suite(self.id, **data))

    def plans(self, milestones=None, limit=None, offset=None,
              is_completed=None, created_by=None, created_after=None,
              created_before=None):
        """
        Returns list of test plans in the project.

        :arg created_after: Only return test runs created after this date.
        :arg created_before: Only return test runs created before this date.
        :arg created_by: A comma-separated list of creators names to filter by.
        :arg is_completed: True to return completed test runs only.
                           False to return active test runs only.
        :arg limit: Limit the result to 'limit' test runs.
        :arg offset: Skip 'offset' records.
        :arg milestones: A comma-separated list of milestone names to filter by.

        :type created_after: datetime.datetime
        :type created_before: datetime.datetime
        :type created_by: list of [str]
        :type is_completed: bool
        :type limit: int
        :type offset: int
        :type milestones: list of [str]
        :rtype: list of [Plan]
        """
        data = {
            'milestone_id': milestones,
            'limit': limit,
            'offset': offset,
            'is_completed': is_completed,
            'created_by': created_by,
            'created_after': created_after,
            'created_before': created_before
        }

        if milestones is not None:
            data['milestone_id'] = [
                str(self.get_milestone_by_name(milestone).id)
                for milestone in milestones
            ]

        if created_by is not None:
            data['created_by'] = [
                str(Testrail.get_user_by_name(user).id)
                for user in created_by
            ]

        if created_after is not None:
            data['created_after'] = int(time.mktime(
                created_after.timetuple()
            ))

        if created_before is not None:
            data['created_before'] = int(time.mktime(
                created_before.timetuple()
            ))

        return [Plan(p) for p in TestrailAPI.get_plans(self.id, **data)]

    def add_plan(self):
        raise NotImplementedError

    def runs(self, suites=None, milestones=None, limit=None, offset=None,
             is_completed=None, created_by=None, created_after=None,
             created_before=None):
        """
        Returns list of test runs in the project. (Not those which are part
        of a test plan).

        :arg created_after: Only return test runs created after this date.
        :arg created_before: Only return test runs created before this date.
        :arg created_by: A comma-separated list of creators names to filter by.
        :arg is_completed: True to return completed test runs only.
                           False to return active test runs only.
        :arg limit: Limit the result to 'limit' test runs.
        :arg offset: Skip 'offset' records.
        :arg milestones: A comma-separated list of milestone names to filter by.
        :arg suites: A list of test suite names to filter by.

        :type created_after: datetime.datetime
        :type created_before: datetime.datetime
        :type created_by: list of [str]
        :type is_completed: bool
        :type limit: int
        :type offset: int
        :type milestones: list of [str]
        :type suites: list of [str]
        :rtype: list of [Run]
        """
        data = {
            'suite_id': suites,
            'milestone_id': milestones,
            'limit': limit,
            'offset': offset,
            'is_completed': is_completed,
            'created_by': created_by,
            'created_after': created_after,
            'created_before': created_before
        }

        if suites is not None:
            data['suite_id'] = [
                str(self.get_suite_by_name(suite).id) for suite in suites
            ]

        if milestones is not None:
            data['milestone_id'] = [
                str(self.get_milestone_by_name(milestone).id)
                for milestone in milestones
            ]

        if created_by is not None:
            data['created_by'] = [
                str(Testrail.get_user_by_name(user).id)
                for user in created_by
            ]

        if created_after is not None:
            data['created_after'] = int(time.mktime(
                created_after.timetuple()
            ))

        if created_before is not None:
            data['created_before'] = int(time.mktime(
                created_before.timetuple()
            ))

        return [Run(p) for p in TestrailAPI.get_runs(self.id,
                                                     **data)]

    def add_run(self, name, suite, description='',
                milestone=None, assignedto=None,
                include_all=True, cases=None):
        """
        Creates new test run.
        Returns newly created run object.

        :arg name: Name of new test run
        :arg description: Description of new test run
        :arg suite: Name of the suite to create tesr run from
        :arg milestone: Name of the milestone to link run to
        :arg assignedto: Name of the user to assing run to
        :arg include_all: if True all cases in suite will be included in run
        :arg cases: if include_all is False - include only this cases

        :type name: str
        :type description: str
        :type suite: str
        :type milestone: str
        :type assignedto: str
        :type include_all: bool
        :type cases: list of [Cases]
        :rtype: Run
        """
        data = {
            'name': name,
            'suite_id': self.get_suite_by_name(suite).id,
            'description': description,
        }

        if milestone is not None:
            data['milestone_id'] = self.get_milestone_by_name(milestone).id

        if assignedto is not None:
            data['assignedto_id'] = Testrail.get_user_by_name(assignedto).id

        if include_all:
            data['include_all'] = True
        else:
            data['include_all'] = False
            data['case_ids'] = [str(c.id) for c in cases]

        return Run(TestrailAPI.add_run(self.id, **data))


class ConfigGroup(object):
    def __init__(self, attributes):
        self.id = attributes['id']
        self.name = attributes['name']
        self.project_id = attributes['project_id']
        self.configs = {}
        for k in attributes['configs']:
            k['id'] = k['name']


class Milestone(_TestrailObject):
    """
    Milestone container

    Module Attributes:
       project      -- Project object the milestone belongs to

    Testrail Attributes:
       id           -- The unique ID of the milestone
       project_id   -- The ID of the project the milestone belongs to
       name         -- The name of the milestone
       description  -- The description of the milestone
       url          -- The address/URL of the milestone in the user interface
       due_on       -- The due date/time of the milestone (as UNIX timestamp)
       is_completed -- True if the milestone is marked as completed and false
                       otherwise
       completed_on -- The date/time when the milestone was marked as completed
                       (as UNIX timestamp)
    """

    cache = {}

    def _settle_attributes(self, attributes):
        self.id = attributes['id']
        self.project_id = attributes['project_id']

        self.name = attributes['name']
        self.description = attributes['description']
        self.url = attributes['url']

        self.due_on_stamp = attributes['due_on']
        self.due_on = datetime.datetime.fromtimestamp(attributes['due_on'])
        self.is_completed = attributes['is_completed']
        self.completed_on = attributes['completed_on']

    @property
    def project(self):
        return Testrail.get_project_by_id(self.project_id)

    @staticmethod
    def get_one(milestone_id):
        return Milestone(TestrailAPI.get_milestone(milestone_id))

    def update(self, name=None, description=None, due_on=None,
               is_completed=None):
        """
        Change milestone parameters.

        :rtype: None
        """
        data = {}
        if name is not None:
            data['name'] = name

        if description is not None:
            data['description'] = description

        if due_on is not None:
            data['due_on'] = due_on

        if is_completed is not None:
            data['is_completed'] = is_completed

        self._settle_attributes(Testrail.post('update_milestone/%s' % self.id,
                                data=json.dumps(data)))

    def delete(self):
        """
        Delete this milestone.

        !!! Deleting a milestone cannot be undone.
        """
        Testrail.post('delete_milestone/%s' % self.id)
        self._settle_attributes(defaultdict(lambda: None))

    def plans(self, limit=None, offset=None,
              is_completed=None, created_by=None, created_after=None,
              created_before=None):
        """
        Returns list of test plans in the project.

        :arg created_after: Only return test runs created after this date.
        :arg created_before: Only return test runs created before this date.
        :arg created_by: A comma-separated list of creators names to filter by.
        :arg is_completed: True to return completed test runs only.
                           False to return active test runs only.
        :arg limit: Limit the result to 'limit' test runs.
        :arg offset: Skip 'offset' records.

        :type created_after: datetime.datetime
        :type created_before: datetime.datetime
        :type created_by: list of [str]
        :type is_completed: bool
        :type limit: int
        :type offset: int
        :rtype: list of [Plan]
        """
        data = {
            'milestone_id': self.id,
            'limit': limit,
            'offset': offset,
            'is_completed': is_completed,
            'created_by': created_by,
            'created_after': created_after,
            'created_before': created_before
        }

        if created_by is not None:
            data['created_by'] = [
                str(Testrail.get_user_by_name(user).id)
                for user in created_by
            ]

        if created_after is not None:
            data['created_after'] = int(time.mktime(
                created_after.timetuple()
            ))

        if created_before is not None:
            data['created_before'] = int(time.mktime(
                created_before.timetuple()
            ))

        return [Plan(p) for p in TestrailAPI.get_plans(self.project_id, **data)]

    def add_plan(self):
        raise NotImplementedError

    def runs(self, suites=None, limit=None, offset=None,
             is_completed=None, created_by=None, created_after=None,
             created_before=None):
        """
        Returns list of test runs in the project. (Not those which are part
        of a test plan).

        :arg created_after: Only return test runs created after this date.
        :arg created_before: Only return test runs created before this date.
        :arg created_by: A comma-separated list of creators names to filter by.
        :arg is_completed: True to return completed test runs only.
                           False to return active test runs only.
        :arg limit: Limit the result to 'limit' test runs.
        :arg offset: Skip 'offset' records.
        :arg suites: A list of test suite names to filter by.

        :type created_after: datetime.datetime
        :type created_before: datetime.datetime
        :type created_by: list of [str]
        :type is_completed: bool
        :type limit: int
        :type offset: int
        :type suites: list of [str]
        :rtype: list of [Run]
        """
        data = {
            'suite_id': suites,
            'milestone_id': self.id,
            'limit': limit,
            'offset': offset,
            'is_completed': is_completed,
            'created_by': created_by,
            'created_after': created_after,
            'created_before': created_before
        }

        if suites is not None:
            data['suite_id'] = [
                str(self.project.get_suite_by_name(suite).id) for suite in suites
            ]

        if created_by is not None:
            data['created_by'] = [
                str(Testrail.get_user_by_name(user).id)
                for user in created_by
            ]

        if created_after is not None:
            data['created_after'] = int(time.mktime(
                created_after.timetuple()
            ))

        if created_before is not None:
            data['created_before'] = int(time.mktime(
                created_before.timetuple()
            ))

        return [Run(p) for p in TestrailAPI.get_runs(self.project_id,
                                                     **data)]

    def add_run(self, name, suite, description='', assignedto=None,
                include_all=True, cases=None):
        """
        Creates new test run.
        Returns newly created run object.

        :arg name: Name of new test run
        :arg description: Description of new test run
        :arg suite: Name of the suite to create tesr run from
        :arg assignedto: Name of the user to assing run to
        :arg include_all: if True all cases in suite will be included in run
        :arg cases: if include_all is False - include only this cases

        :type name: str
        :type description: str
        :type suite: str
        :type assignedto: str
        :type include_all: bool
        :type cases: list of [Cases]
        :rtype: Run
        """
        data = {
            'name': name,
            'suite_id': self.project.get_suite_by_name(suite).id,
            'description': description,
            'milestone_id': self.id
        }

        if assignedto is not None:
            data['assignedto_id'] = Testrail.get_user_by_name(assignedto).id

        if include_all:
            data['include_all'] = True
        else:
            data['include_all'] = False
            data['case_ids'] = [str(c.id) for c in cases]

        return Run(TestrailAPI.add_run(self.project_id, **data))


class Suite(_TestrailObject):
    """
    Test suite container.

    Module Attributes:
       project      -- Project object the test suite belongs to

    Testrail Attributes:
       id           -- The unique ID of the test suite
       project_id   -- The ID of the project this test suite belongs to
       name         -- The name of the test suite
       description  -- The description of the test suite
       url          -- The address/URL of the test suite in the user interface
       is_master    -- True if the test suite is a master test suite and
                       false otherwise
       is_baseline  -- True if the test suite is a baseline test suite and
                       false otherwise
       is_completed -- True if the test suite is marked as completed/archived
                       and false otherwise
       completed_on -- The date/time when the test suite was closed
                       (as UNIX timestamp)
    """

    cache = {}

    def _settle_attributes(self, attributes):
        self.id = attributes['id']
        self.project_id = attributes['project_id']

        self.name = attributes['name']
        self.description = attributes['description']
        self.url = attributes['url']
        self.is_master = attributes['is_master']
        self.is_baseline = attributes['is_baseline']

        self.is_completed = attributes['is_completed']
        self.completed_on = attributes['completed_on']

        self._sections = None
        self._root_sections = None

    @property
    def project(self):
        return Testrail.get_project_by_id(self.project_id)

    @staticmethod
    def get_one(suite_id):
        return Suite(TestrailAPI.get_suite(suite_id))

    def update(self, name=None, description=None):
        """
        Change suite parameters.

        :rtype: None
        """
        data = {}

        if name is not None:
            data['name'] = name

        if description is not None:
            data['description'] = description

        self._settle_attributes(TestrailAPI.update_suite(self.id, **data))

    def delete(self):
        """
        Delete this test suite.

        !!! Deleting a test suite cannot be undone and also deletes all active
        test runs & results, i.e. test runs & results that weren't closed
        (archived) yet.
        """
        TestrailAPI.delete_suite(self.id)
        self._settle_attributes(defaultdict(lambda: None))

    def sections(self):
        """
        Returns list of all sections in the suite.

        :rtype: list of [Section]
        """
        if self._sections is not None:
            return self._sections

        else:
            self._sections = [Section(s) for s in TestrailAPI.get_sections(
                self.project_id,
                self.id
            )]
            self._build_sections_tree()
            return self._sections

    def _build_sections_tree(self):
        self._root_sections = []
        for s in self._sections:
            s.children = []

        for s in self._sections:
            if s.parent_id is None:
                self._root_sections.append(s)
            else:
                Testrail.get_section_by_id(s.parent_id).children.append(s)

    def get_section_by_path(self, *path):
        """
        :rtype: Section
        """
        if self._sections is None:
            self.sections()

        if len(path) < 1:
            raise NotFound()

        current_section = None
        for s in self._root_sections:
            if s.name == path[0]:
                current_section = s

        if current_section is None:
            raise NotFound()

        if len(path) > 1:
            for item in path[1:]:
                for s in current_section.children:
                    if s.name == item:
                        current_section = s
                        break
                else:
                    raise NotFound()

        return current_section

    def add_section(self, name, description='', parent=None):
        """
        Creates new section in current suite.
        Returns newly created section object.

        :arg name: Name of new section
        :arg description: Description of new section
        :arg parent: Parent section object (if any)

        :type name: str
        :type description: str
        :type parent: Section
        :rtype: Section
        """
        data = {
            'name': name,
            'suite_id': self.id,
            'description': description,
            'parent_id': parent.id,
        }

        return Section(TestrailAPI.add_section(self.project_id, **data))

    @property
    def custom_case_fields(self):
        """
        Returns list of custom case fields applied to this suite.

        :rtype: list of [CaseField]
        """
        return self.project.custom_case_fields

    def cases(self,
              section=None,
              types=None,
              priorities=None,
              milestones=None,
              created_by=None,
              created_after=None,
              created_before=None,
              updated_by=None,
              updated_after=None,
              updated_before=None):
        """
        Find and filter cases.

        :arg types: A list of case type names to filter by
        :arg priorities: list of priorities names to filter by
        :arg milestones: list of milestones names to filter by
        :arg created_by: list of user names who created cases to include
        :arg created_after: Only return test cases created after this date
        :arg created_before: Only return test cases created before this date
        :arg updated_by: list of user names who updated cases to include
        :arg updated_after: Only return test cases updated after this date
        :arg updated_before: Only return test cases updated before this date

        :type types: list of [str]
        :type priorities: list os [str]
        :type milestones: list of [str]
        :type created_by: list of [str]
        :type created_after: datetime.datetime
        :type created_before: datetime.datetime
        :type updated_by: list of [str]
        :type updated_after: datetime.datetime
        :type updated_before: datetime.datetime
        :rtype: list of [Case]
        """
        data = {}

        if types is not None:
            data['type_id'] = [
                str(Testrail.get_case_type_by_name(ctype).id)
                for ctype in types
            ]

        if priorities is not None:
            data['priority_id'] = [
                str(Testrail.get_priority_by_name(priority).id)
                for priority in priorities
            ]

        if milestones is not None:
            data['milestone_id'] = [
                str(self.project.get_milestone_by_name(milestone).id)
                for milestone in milestones
            ]

        if created_by is not None:
            data['created_by'] = [
                str(Testrail.get_user_by_name(user).id)
                for user in created_by
            ]

        if created_after is not None:
            data['created_after'] = int(time.mktime(
                created_after.timetuple()
            ))

        if created_before is not None:
            data['created_before'] = int(time.mktime(
                created_before.timetuple()
            ))

        if updated_by is not None:
            data['updated_by'] = [
                str(Testrail.get_user_by_name(user).id)
                for user in updated_by
            ]

        if updated_after is not None:
            data['updated_after'] = int(time.mktime(
                updated_after.timetuple()
            ))

        if updated_before is not None:
            data['updated_before'] = int(time.mktime(
                updated_before.timetuple()
            ))

        return [Case(c) for c in TestrailAPI.get_cases(self.project_id,
                                                       self.id,
                                                       section.id,
                                                       **data)]

    def add_run(self, name, description='', milestone=None,
                assignedto=None, include_all=None, cases=None):
        """
        Creates new test run on this suite.
        Returns newly created run object.

        :arg name: Name of new test run
        :arg description: Description of new test run
        :arg milestone: Name of the milestone to link run to
        :arg assignedto: Name of the user to assign run to
        :arg include_all: if True all cases in suite will be included in run
        :arg cases: if include_all is False - include only this cases

        :type name: str
        :type description: str
        :type milestone: str
        :type assignedto: str
        :type include_all: bool
        :type cases: list of [Cases]
        :rtype: Run
        """
        data = {
            'name': name,
            'suite_id': self.id,
            'description': description,
        }

        if milestone is not None:
            data['milestone_id'] = self.project.get_milestone_by_name(milestone).id

        if assignedto is not None:
            data['assignedto_id'] = Testrail.get_user_by_name(assignedto).id

        if include_all:
            data['include_all'] = True
        else:
            data['include_all'] = False
            data['case_ids'] = [str(c.id) for c in cases]

        return Run(TestrailAPI.add_run(self.project_id, **data))


class Plan(_TestrailObject):
    """
    Test plan container.

    Testrail Attributes:
       id                   -- The unique ID of the test plan
       project_id           -- The ID of the project this test plan belongs to
       name                 -- The name of the test plan
       description          -- The description of the test plan
       url                  -- The address/URL of the test plan in the user interface
       milestone_id         -- The ID of the milestone this test plan belongs to
       created_on           -- The date/time when the test plan was created (as UNIX timestamp)
       created_by           -- The ID of the user who created the test plan
       assignedto_id        -- The ID of the user the entire test plan is
                               assigned to
       is_completed         -- True if the test plan was closed and false otherwise
       completed_on         -- The date/time when the test plan was closed (as UNIX timestamp)
       entries              -- An array of 'entries', i.e. group of test runs
       passed_count         -- The amount of tests in the test plan marked as passed
       failed_count         -- The amount of tests in the test plan marked as failed
       retest_count         -- The amount of tests in the test plan marked as retest
       blocked_count        -- The amount of tests in the test plan marked as blocked
       untested_count       -- The amount of tests in the test plan marked as untested
       custom_status1_count -- The amount of tests in the test plan with the respective custom status
       custom_status2_count -- The amount of tests in the test plan with the respective custom status
       custom_status3_count -- The amount of tests in the test plan with the respective custom status
       custom_status4_count -- The amount of tests in the test plan with the respective custom status
       custom_status5_count -- The amount of tests in the test plan with the respective custom status
       custom_status6_count -- The amount of tests in the test plan with the respective custom status
       custom_status7_count -- The amount of tests in the test plan with the respective custom status
    """

    cache = {}

    def _settle_attributes(self, attributes):
        self.id = attributes['id']
        self.project_id = attributes['project_id']
        self.name = attributes['name']
        self.description = attributes['description']
        self.url = attributes['url']

        self.milestone_id = attributes['milestone_id']

        self.created_on = attributes['created_on']
        self.created_by_id = attributes['created_by']
        self.assignedto_id = attributes['assignedto_id']

        self.is_completed = attributes['is_completed']
        self.completed_on = attributes['completed_on']

        self.passed_count = attributes['passed_count']
        self.failed_count = attributes['failed_count']
        self.retest_count = attributes['retest_count']
        self.blocked_count = attributes['blocked_count']
        self.untested_count = attributes['untested_count']

        self.custom_status1_count = attributes['custom_status1_count']
        self.custom_status2_count = attributes['custom_status2_count']
        self.custom_status3_count = attributes['custom_status3_count']
        self.custom_status4_count = attributes['custom_status4_count']
        self.custom_status5_count = attributes['custom_status5_count']
        self.custom_status6_count = attributes['custom_status6_count']
        self.custom_status7_count = attributes['custom_status7_count']

        try:
            self.entries = attributes['entries']
        except KeyError:
            self.entries = []

    @property
    def project(self):
        return Testrail.get_project_by_id(self.project_id)

    @property
    def milestone(self):
        return Testrail.get_milestone_by_id(self.milestone_id)

    @property
    def created_by(self):
        return Testrail.get_user_by_id(self.created_by_id)

    @property
    def assignedto(self):
        return Testrail.get_user_by_id(self.assignedto_id)

    @staticmethod
    def get_one(plan_id):
        return Plan(TestrailAPI.get_plan(plan_id))

    def runs(self):
        result = []
        for e in self.entries:
            for r in e['runs']:
                result.append(r)
        return result

    def add_entry(self):
        raise NotImplementedError

    def update_entry(self):
        raise NotImplementedError

    def delete_entry(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError


class Run(_TestrailObject):
    """
    Test run container

    Testrail Attributes:
       id                   -- The unique ID of the test run
       project_id           -- The ID of the project this test run belongs to
       plan_id              -- The ID of the test plan this test run belongs to
       suite_id             -- The ID of the test suite this test run is derived from
       name                 -- The name of the test run
       description          -- The description of the test run
       url                  -- The address/URL of the test run in the user interface
       milestone_id         -- The ID of the milestone this test plan belongs to
       created_on           -- The date/time when the test plan was created (as UNIX timestamp)
       created_by           -- The ID of the user who created the test plan
       assignedto_id        -- The ID of the user the entire test plan is
                               assigned to
       is_completed         -- True if the test plan was closed and false otherwise
       completed_on         -- The date/time when the test plan was closed (as UNIX timestamp)
       entries              -- An array of 'entries', i.e. group of test runs
       passed_count         -- The amount of tests in the test plan marked as passed
       failed_count         -- The amount of tests in the test plan marked as failed
       retest_count         -- The amount of tests in the test plan marked as retest
       blocked_count        -- The amount of tests in the test plan marked as blocked
       untested_count       -- The amount of tests in the test plan marked as untested
       custom_status1_count -- The amount of tests in the test plan with the respective custom status
       custom_status2_count -- The amount of tests in the test plan with the respective custom status
       custom_status3_count -- The amount of tests in the test plan with the respective custom status
       custom_status4_count -- The amount of tests in the test plan with the respective custom status
       custom_status5_count -- The amount of tests in the test plan with the respective custom status
       custom_status6_count -- The amount of tests in the test plan with the respective custom status
       custom_status7_count -- The amount of tests in the test plan with the respective custom status
    """

    cache = {}

    def _settle_attributes(self, attributes):
        self.id = attributes['id']
        self.name = attributes['name']
        self.project_id = attributes['project_id']
        self.description = attributes['description']
        self.url = attributes['url']

        self.plan_id = attributes['plan_id']
        self.suite_id = attributes['suite_id']
        self.milestone_id = attributes['milestone_id']

        self.created_on_stamp = attributes['created_on']
        self.created_by_id = attributes['created_by']
        self.assignedto_id = attributes['assignedto_id']

        self.is_completed = attributes['is_completed']
        self.completed_on_stamp = attributes['completed_on']

        try:
            self.created_on = datetime.datetime.fromtimestamp(attributes['created_on'])
            self.completed_on = datetime.datetime.fromtimestamp(attributes['completed_on'])
        except TypeError:
            self.created_on = None
            self.completed_on = None

        self.passed_count = attributes['passed_count']
        self.failed_count = attributes['failed_count']
        self.retest_count = attributes['retest_count']
        self.blocked_count = attributes['blocked_count']
        self.untested_count = attributes['untested_count']

        self.custom_status1_count = attributes['custom_status1_count']
        self.custom_status2_count = attributes['custom_status2_count']
        self.custom_status3_count = attributes['custom_status3_count']
        self.custom_status4_count = attributes['custom_status4_count']
        self.custom_status5_count = attributes['custom_status5_count']
        self.custom_status6_count = attributes['custom_status6_count']
        self.custom_status7_count = attributes['custom_status7_count']

        self.config = attributes['config']
        self.config_ids = attributes['config_ids']
        self.include_all = attributes['include_all']

    @property
    def project(self):
        return Testrail.get_project_by_id(self.project_id)

    @property
    def test_plan(self):
        return Testrail.get_plan_by_id(self.plan_id)

    @property
    def suite(self):
        return Testrail.get_suite_by_id(self.suite_id)

    @property
    def milestone(self):
        return Testrail.get_milestone_by_id(self.milestone_id)

    @property
    def created_by(self):
        return Testrail.get_user_by_id(self.created_by_id)

    @property
    def assignedto(self):
        return Testrail.get_user_by_id(self.assignedto_id)

    @staticmethod
    def get_one(run_id):
        return Run(TestrailAPI.get_run(run_id))

    def tests(self, statuses=None):
        """
        Return list of tests in this test run

        :arg statuses: List of statuses names to include

        :type statuses: list of [str]
        :rtype: list of [Test]
        """
        data = {}
        if statuses is not None:
            data['status_id'] = [
                str(Testrail.get_status_by_name(s).id)
                for s in statuses
            ]

        return [Test(t) for t in TestrailAPI.get_tests(self.id, **data)]

    @property
    def custom_result_fields(self):
        """
        Returns list of custom result fields applied to this run.

        :rtype: list of [ResultField]
        """
        return self.project.custom_result_fields

    @property
    def custom_case_fields(self):
        """
        Returns list of custom result fields applied to this run.

        :rtype: list of [ResultField]
        """
        return self.project.custom_case_fields

    def results(self,
                statuses=None,
                limit=None,
                offset=None,
                created_by=None,
                created_after=None,
                created_before=None):
        """
        Get results in this run.

        :arg statuses: A list of test status names to filter by
        :arg limit: Limit the output to this number of records
        :arg offset: Skip this number of records.
        :arg created_by: list of user names who added results to include
        :arg created_after: Only return results created after this date
        :arg created_before: Only return results created before this date

        :type statuses: list of [str]
        :type limit: int
        :type offset: int
        :type created_by: list
        :type created_after: datetime.datetime
        :type created_before: datetime.datetime
        :rtype: list of [Result]
        """
        data = {
            'limit': limit,
            'offset': offset,
        }

        if statuses is not None:
            data['status_id'] = [
                str(Testrail.get_status_by_name(s).id)
                for s in statuses
            ]

        if created_by is not None:
            data['status_id'] = [
                str(Testrail.get_user_by_name(u).id)
                for u in created_by
            ]

        if created_after is not None:
            data['created_after'] = int(time.mktime(
                created_after.timetuple()
            ))

        if created_before is not None:
            data['created_before'] = int(time.mktime(
                created_before.timetuple()
            ))

        return [Result(r) for r in TestrailAPI.get_results_for_run(self.id,
                                                                   **data)]

    def results_for_case(self,
                         case,
                         statuses=None,
                         limit=None,
                         offset=None):
        """
        Return results list for a test in this run for provided case.

        :arg case: A case object which is a 'father' for test
        :arg statuses: A list of test status names to filter by
        :arg limit: Limit the output to this number of records
        :arg offset: Skip this number of records.

        :type case: Case
        :type statuses: list of [str]
        :type limit: int
        :type offset: int
        :rtype: list of [Result]
        """
        data = {
            'limit': limit,
            'offset': offset,
        }

        if statuses is not None:
            data['status_id'] = [
                str(Testrail.get_status_by_name(s).id)
                for s in statuses
            ]

        return [Result(r) for r in TestrailAPI.get_results_for_case(self.id,
                                                                    case.id,
                                                                    **data)]

    def add_result_for_case(self,
                            case,
                            status_name,
                            comment='',
                            version=None,
                            elapsed=None,
                            defects=None,
                            assignedto=None):
        data = {
            'status_id': Testrail.get_status_by_name(status_name).id,
            'comment': comment
        }

        if version is not None:
            data['version'] = version

        if elapsed is not None:
            data['elapsed'] = elapsed

        if defects is not None:
            data['defects'] = defects

        if assignedto is not None:
            data['assignedto_id'] = Testrail.get_user_by_name(assignedto).id

        return Result(TestrailAPI.add_result_for_case(self.id, case.id, **data))


class Section(_TestrailObject):
    """
    Section container

    Module Attributes:
       parent           -- Link to parent Section object
       suite            -- Link to Suite object this section belongs to

    Testrail Attributes:
       id               -- The unique ID of the section
       suite_id         -- The ID of the test suite this section belongs to
       name             -- The name of the section
       description      -- The description of the section
       display_order    -- The order in the test suite
       parent_id        -- The ID of the parent section in the test suite
       depth            -- The level in the section hierarchy of the test suite
    """

    cache = {}

    def _settle_attributes(self, attributes):
        self.id = attributes['id']
        self.suite_id = attributes['suite_id']
        self.name = attributes['name']
        self.description = attributes['description']

        self.display_order = attributes['display_order']
        self.parent_id = attributes['parent_id']
        self.depth = attributes['depth']

        self.children = []

    @property
    def parent(self):
        return Testrail.get_section_by_id(self.parent_id)

    @property
    def suite(self):
        return Testrail.get_suite_by_id(self.suite_id)

    @staticmethod
    def get_one(section_id):
        return Section(TestrailAPI.get_section(section_id))

    def update(self, name=None, description=None):
        """
        Change section parameters.

        :rtype: None
        """
        raise NotImplementedError

    def delete(self):
        """
        Delete section.

        !!! Deleting a section cannot be undone and also deletes all related
        test cases as well as active tests & results, i.e. tests & results
        that weren't closed (archived) yet.
        """
        raise NotImplementedError

    def add_subsection(self, name, description=''):
        """
        Creates new section in current suite.
        Returns newly created section object.

        :arg name: Name of new section
        :arg description: Description of new section
        :arg parent: Parent section object (if any)

        :type name: str
        :type description: str
        :type parent: Section
        :rtype: Section
        """
        data = {
            'name': name,
            'suite_id': self.suite_id,
            'description': description,
            'parent_id': self.id,
        }

        return Section(TestrailAPI.add_section(self.suite.project_id, **data))

    def cases(self,
              include_subsections=False,
              types=None,
              priorities=None,
              milestones=None,
              created_by=None,
              created_after=None,
              created_before=None,
              updated_by=None,
              updated_after=None,
              updated_before=None):
        """
        This is most important method to find and filter cases.

        :arg include_subsections: if True - search recursive
        :arg types: A list of case type names to filter by
        :arg priorities: list of priorities names to filter by
        :arg milestones: list of milestones names to filter by
        :arg created_by: list of user names who created cases to include
        :arg created_after: Only return test cases created after this date
        :arg created_before: Only return test cases created before this date
        :arg updated_by: list of user names who updated cases to include
        :arg updated_after: Only return test cases updated after this date
        :arg updated_before: Only return test cases updated before this date

        :type include_subsections: bool
        :type types: list od [str]
        :type priorities: list of [str]
        :type milestones: list of [str]
        :type created_by: list of [str]
        :type created_after: datetime.datetime
        :type created_before: datetime.datetime
        :type updated_by: list of [str]
        :type updated_after: datetime.datetime
        :type updated_before: datetime.datetime
        """
        data = {}

        if types is not None:
            data['type_id'] = [
                str(Testrail.get_case_type_by_name(t).id) for t in types
            ]

        if priorities is not None:
            data['priority_id'] = [
                str(Testrail.get_priority_by_name(p).id) for p in priorities
            ]

        if milestones is not None:
            data['milestone_id'] = [
                str(self.suite.project.get_milestone_by_name(m).id) for m in milestones
            ]

        if created_by is not None:
            data['created_by'] = [
                str(Testrail.get_user_by_name(u).id) for u in created_by
            ]

        if created_after is not None:
            data['created_after'] = int(time.mktime(
                created_after.timetuple()
            ))

        if created_before is not None:
            data['created_before'] = int(time.mktime(
                created_before.timetuple()
            ))

        if updated_by is not None:
            data['updated_by'] = [
                str(Testrail.get_user_by_name(user).id)
                for user in updated_by
            ]

        if updated_after is not None:
            data['updated_after'] = int(time.mktime(
                updated_after.timetuple()
            ))

        if updated_before is not None:
            data['updated_before'] = int(time.mktime(
                updated_before.timetuple()
            ))

        if not include_subsections:
            return [Case(c) for c in TestrailAPI.get_cases(self.suite.project_id,
                                                           self.suite_id,
                                                           self.id,
                                                           **data)]
        else:
            result = [
                Case(c) for c in TestrailAPI.get_cases(self.suite.project_id,
                                                       self.suite_id,
                                                       self.id,
                                                       **data)
            ]
            for sec in self.children:
                result.extend(
                    sec.cases(True, types, priorities, milestones, created_by,
                              created_after, created_before, updated_by,
                              updated_after, updated_before)
                )
            return result

    def add_case(self):
        raise NotImplementedError


class Case(_TestrailObject):
    """
    Test case container

    Module Attributes:
       suite            -- Suite object the test case belongs to
       section          -- Section object the test case belongs to
       case_type        -- CaseType object the test case has
       priority         -- Priority object the test case has
       milestone        -- Milestone object the test case belongs to
       created_by       -- User object the test case was created by
       updated_by       -- User object the test case was updated by
       created_on       -- datetime object when the test case was created
       updated_on       -- datetime object when the test case was last updated

    Testrail Attributes:
       id                   -- The unique ID of the test case
       suite_id             -- The ID of the suite the test case belongs to
       section_id           -- The ID of the section the test case belongs to
       title                -- The ID of the suite the test case belongs to
       type_id              -- The ID of the test case type that is linked to
                               the test case
       priority_id          -- The ID of the priority that is linked to
                               the test case
       milestone_id         -- The ID of the milestone that is linked to
                               the test case
       refs                 -- A comma-separated list of references/requirements
       estimate             -- The estimate, e.g. "30s" or "1m 45s"
       estimate_forecast    -- The estimate forecast, e.g. "30s" or "1m 45s"
       created_on_stamp     -- The date/time when the test case was created
                               (as UNIX timestamp)
       created_by_id        -- The ID of the user who created the test case
       updated_on_stamp     -- The date/time when the test case was last updated
                               (as UNIX timestamp)
       updated_by_id        -- The ID of the user who last updated the test case
       + custom fields...
    """
    cache = {}

    def _settle_attributes(self, attributes):
        self.id = attributes['id']
        self.suite_id = attributes['suite_id']
        self.section_id = attributes['section_id']

        self.title = attributes['title']
        self.type_id = attributes['type_id']
        self.priority_id = attributes['priority_id']
        self.milestone_id = attributes['milestone_id']

        self.refs = attributes['refs']
        self.estimate = attributes['estimate']
        self.estimate_forecast = attributes['estimate_forecast']

        self.created_on_stamp = attributes['created_on']
        self.created_on = datetime.datetime.fromtimestamp(attributes['created_on'])
        self.created_by_id = attributes['created_by']
        self.updated_on_stamp = attributes['updated_on']
        self.updated_on = datetime.datetime.fromtimestamp(attributes['updated_on'])
        self.updated_by_id = attributes['updated_by']

        # and all the custom fields:
        for custom in self.suite.custom_case_fields:
            setattr(self, custom.system_name, attributes[custom.system_name])

    @property
    def suite(self):
        return Testrail.get_suite_by_id(self.suite_id)

    @property
    def section(self):
        return Testrail.get_section_by_id(self.section_id)

    @property
    def milestone(self):
        return Testrail.get_milestone_by_id(self.milestone_id)

    @property
    def case_type(self):
        return Testrail.get_case_type_by_id(self.type_id).name

    @property
    def priority(self):
        return Testrail.get_priority_by_id(self.priority_id).short_name

    @property
    def created_by(self):
        return Testrail.get_user_by_id(self.created_by_id).name

    @property
    def updated_by(self):
        return Testrail.get_user_by_id(self.updated_by_id).name

    @staticmethod
    def get_one(case_id):
        return Case(TestrailAPI.get_case(case_id))

    def update(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    def results_in_run(self,
                       run,
                       statuses=None,
                       limit=None,
                       offset=None):
        """
        Return results list for a test created from this case in provided run.

        :arg run: A run object to grab results from
        :arg statuses: A list of test status names to filter by
        :arg limit: Limit the output to this number of records
        :arg offset: Skip this number of records.

        :type run: Run
        :type statuses: list of [str]
        :type limit: int
        :type offset: int
        :rtype: list of [Result]
        """
        data = {
            'limit': limit,
            'offset': offset
        }

        if statuses is not None:
            data['status_id'] = [
                str(Testrail.get_status_by_name(s).id) for s in statuses
            ]

        return [Result(r) for r in TestrailAPI.get_results_for_case(run.id,
                                                                    self.id,
                                                                    **data)]

    def add_result_in_run(self,
                          run,
                          status_name,
                          comment='',
                          version=None,
                          elapsed=None,
                          defects=None,
                          assignedto=None):
        raise NotImplementedError


class Test(_TestrailObject):
    """
    Test container

    Testrail Attributes:
       id                   -- The unique ID of the test
       run_id               -- The ID of the test run the test belongs to
       case_id              -- The ID of the related test case
       status_id            -- The ID of the current status of the test
       title                -- The title of the related test case
       type_id              -- The ID of the test case type that is linked to
                               the test case
       priority_id          -- The ID of the priority that is linked to
                               the test case
       milestone_id         -- The ID of the milestone that is linked to
                               the test case
       refs                 -- A comma-separated list of references/requirements
                               that are linked to the test case
       estimate             -- The estimate of the related test case
       estimate_forecast    -- The estimate forecast of the related test case
       assignedto_id        -- The ID of the user the test is assigned to
       + custom fields

    Extra Attributes:
       run          -- Run object the test belongs to
       case         -- related Case object
       status       -- Status object of the test
       type         -- CaseType object of the test
       priority     -- Priority object of the test
       milestone    -- Milestone object the test is linked to
       assignedto   -- User object the test is assigned to
    """

    cache = {}

    def _settle_attributes(self, attributes):
        self.id = attributes['id']
        self.run_id = attributes['run_id']
        self.case_id = attributes['case_id']
        self.status_id = attributes['status_id']
        self.title = attributes['title']
        self.type_id = attributes['type_id']
        self.priority_id = attributes['priority_id']

        self.milestone_id = attributes['milestone_id']
        self.refs = attributes['refs']
        self.estimate = attributes['estimate']
        self.estimate_forecast = attributes['estimate_forecast']

        self.assignedto_id = attributes['assignedto_id']

        # and all the custom fields:
        for custom in self.run.custom_case_fields:
            setattr(self, custom.system_name, attributes[custom.system_name])

    @property
    def run(self):
        return Testrail.get_run_by_id(self.run_id)

    @property
    def case(self):
        return Testrail.get_case_by_id(self.case_id)

    @property
    def status(self):
        return Testrail.get_status_by_id(self.status_id).name

    @property
    def type(self):
        return Testrail.get_case_type_by_id(self.type_id).name

    @property
    def priority(self):
        return Testrail.get_priority_by_id(self.priority_id).short_name

    @property
    def milestone(self):
        return Testrail.get_milestone_by_id(self.milestone_id)

    @property
    def assignedto(self):
        try:
            return Testrail.get_user_by_id(self.assignedto_id).name
        except NotFound:
            return 'Unassigned'

    @staticmethod
    def get_one(test_id):
        return Test(TestrailAPI.get_test(test_id))

    def add_result(self,
                   status_name,
                   comment='',
                   version=None,
                   elapsed=None,
                   defects=None,
                   assignedto=None):
        data = {
            'status_id': Testrail.get_status_by_name(status_name).id,
            'comment': comment
        }

        if version is not None:
            data['version'] = version

        if elapsed is not None:
            data['elapsed'] = elapsed

        if defects is not None:
            data['defects'] = defects

        if assignedto is not None:
            data['assignedto_id'] = Testrail.get_user_by_name(assignedto).id

        return Result(TestrailAPI.add_result(self.id, **data))

    def set_passed(self, **kwargs):
        return self.add_result(1, **kwargs)

    def set_blocked(self, **kwargs):
        return self.add_result(2, **kwargs)

    def set_untested(self, **kwargs):
        return self.add_result(3, **kwargs)

    def set_retest(self, **kwargs):
        return self.add_result(4, **kwargs)

    def set_failed(self, **kwargs):
        return self.add_result(5, **kwargs)

    def results(self,
                statuses=None,
                limit=None,
                offset=None):
        """
        Return results list for this test.

        :arg statuses: A list of test status names to filter by
        :arg limit: Limit the output to this number of records
        :arg offset: Skip this number of records.

        :type statuses: list of [str]
        :type limit: int
        :type offset: int
        :rtype: list of [Result]
        """
        data = {
            'limit': limit,
            'offset': offset
        }

        if statuses is not None:
            data['status_id'] = [
                str(Testrail.get_status_by_name(s).id)
                for s in statuses
            ]

        return [Result(r) for r in TestrailAPI.get_results(self.id, **data)]


class Result(_TestrailObject):
    """
    Test results container.

    Testrail Attributes:
       id               -- The unique ID of the test result
       test_id          -- The ID of the test this test result belongs to
       status_id        -- The status of the test result
       version          -- The (build) version the test was executed against
       created_on_timestamp -- The timestamp when the test result was created
       created_by_id    -- The ID of the user who created the test result
       assignedto_id    -- The ID of the assignee (user) of the test result
       comment          -- The comment or error message of the test result
       elapsed          -- The amount of time it took to execute the test
       defects          -- A comma-separated list of defects linked to the test
                           result
       + custom fields

    Extra Attributes:
       test             -- Test object this test result belongs to
       status           -- Status object of the test result
       created_on       -- Datetime object when the test result was created
       created_by       -- User object who created the test result
       assignedto       -- User object who is assignee of the test result
    """

    cache = {}

    def _settle_attributes(self, attributes):
        self.id = attributes['id']
        self.test_id = attributes['test_id']
        self.status_id = attributes['status_id']
        self.version = attributes['version']
        self.created_on_stamp = attributes['created_on']
        self.created_on = datetime.datetime.fromtimestamp(attributes['created_on'])
        self.created_by_id = attributes['created_by']
        self.assignedto_id = attributes['assignedto_id']
        self.comment = attributes['comment']
        self.elapsed = attributes['elapsed']
        self.defects = attributes['defects']

        # and all the custom fields:
        for custom in self.test.run.custom_result_fields:
            setattr(self, custom.system_name, attributes[custom.system_name])

    @property
    def test(self):
        return Testrail.get_test_by_id(self.test_id)

    @property
    def status(self):
        return Testrail.get_status_by_id(self.status_id)

    @property
    def assignedto(self):
        return Testrail.get_user_by_id(self.assignedto_id)

    @property
    def created_by(self):
        return Testrail.get_user_by_id(self.created_by_id)