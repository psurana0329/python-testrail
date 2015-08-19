#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

import testrail


class Section(object):
    """
    Section container.

    Attributes:
        id               -- (int) Unique section ID
        project          -- (Project) The project this section belongs to
        suite            -- (Suite) The test suite this section belongs to
        name             -- (str) Name of the section
        description      -- (str) Description of the section
        display_order    -- (int) Position in the web-page
        parent           -- (Section) Parent section
        depth            -- (int) Level in the section hierarchy
    """

    def __init__(self, attributes):
        self.__id = int(attributes['id'])
        self.__suite_id = int(attributes['suite_id'])
        self.__project_id = self.suite.project.id
        self.__depth = int(attributes['depth'])
        self.__display_order = int(attributes['display_order'])

        try:
            self.__parent_id = int(attributes['parent_id'])
        except TypeError:
            self.__parent_id = None

        self.__name = attributes['name']
        try:
            # this present only since 4.0
            self.__description = attributes['description']
        except KeyError:
            self.__description = None

    def __str__(self):
        return '<Section: %s [%s]>' % (self.name, self.id)

    def __repr__(self):
        return self.__str__()

    ###########################################################################
    # Getters/Setters

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        raise RuntimeError('Attribute Section.id cannot be modified.')

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        raise RuntimeError('Attribute Section.name cannot be modified directly. '
                           'Please use Section.update(name=<new_name>) for this.')

    @property
    def suite(self):
        return testrail.core.data.TestrailData.get_suite_by_id(self.__suite_id)

    @suite.setter
    def suite(self, value):
        raise RuntimeError('Attribute Section.suite cannot be modified.')

    @property
    def project(self):
        return testrail.core.data.TestrailData.get_project_by_id(self.__project_id)

    @project.setter
    def project(self, value):
        raise RuntimeError('Attribute Section.project cannot be modified.')

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        raise RuntimeError('Attribute Section.description cannot be modified directly. '
                           'Please use Section.update(description=<new_description>) for this.')

    @property
    def parent(self):
        return testrail.core.data.TestrailData.get_section_by_id(self.__parent_id)

    @parent.setter
    def parent(self, value):
        raise RuntimeError('Attribute Section.parent cannot be modified.')

    @property
    def depth(self):
        return self.__depth

    @depth.setter
    def depth(self, value):
        raise RuntimeError('Attribute Section.depth cannot be modified.')

    @property
    def display_order(self):
        return self.__display_order

    @display_order.setter
    def display_order(self, value):
        raise RuntimeError('Attribute Section.display_order cannot be modified.')

    ###########################################################################
    # LifeCycle Methods

    def update(self, **attributes):
        """
        Update this section attributes.

        Available for update:
            name            -- Project name
            description     -- The description of the milestone
        """
        s = testrail.core.data.TestrailData.update_section(self.id, **attributes)
        self.name = s.name
        self.description = s.description

    def delete(self):
        """
        Remove this section and all cases in it.
        """
        testrail.core.data.TestrailData.delete_section(self.id)

    def add_subsection(self, name, description):
        """
        Create new root-level section in this suite.
        Return newly created Section object.

        :rtype: testrail.models.Section
        """
        parameters = {
            'name': name,
            'description': description,
            'suite_id': self.suite_id,
            'parent_id': self.id
        }
        return testrail.core.data.TestrailData.add_section(self.suite().project_id, **parameters)

    def get_cases(self):
        """
        Return all test cases in this section.

        :rtype: list of [testrail.models.Case]
        """
        return testrail.core.data.TestrailData.get_cases(self.__project_id, self.__suite_id, self.__id)

    def get_case(self, name):
        for case in self.get_cases():
            if case.title == name:
                return case
        return None

    def add_case(self, title, case_type=None, priority=None, estimate=None, milestone=None, refs=None, **custom_fields):
        """
        Create new test case in this section.
        Return newly created case object.

        :param title: Desired name of the new case.
        :type title: str
        :param case_type: Case type of the new case
        :type case_type: str of testrail.models.CaseType
        :param priority: Case Priority of the new case
        :type priority: str or testrail.models.Priority
        :param estimate: The estimate, e.g. "30s" or "1m 45s"
        :type estimate: str
        :param milestone: The milestone to link to the test case
        :type milestone: str ot testrail.models.Milestone
        :param refs: A comma-separated list of references/requirements
        :type refs: str
        :rtype: testrail.models.Case
        """
        parameters = {
            'title': title
        }

        if isinstance(case_type, testrail.models.CaseType):
            parameters['type_id'] = case_type.id
        elif isinstance(case_type, str):
            case_type = testrail.core.data.TestrailData.get_case_type_by_name(case_type)
            if case_type is not None:
                parameters['type_id'] = case_type.id
            else:
                raise testrail.errors.NotFoundError('Not found Case Type with name "%s"' % case_type)
        else:
            raise testrail.errors.TestrailError('Wrong type of parameter "type" in method "add_case".'
                                                'Got: "%s". Must be either "str" or "testrail.models.CaseType"' % type(case_type))

        if isinstance(priority, testrail.models.Priority):
            parameters['priority_id'] = priority.id
        elif isinstance(priority, str):
            priority = testrail.core.data.TestrailData.get_priority_by_name(priority)
            if priority is not None:
                parameters['priority_id'] = priority.id
            else:
                raise testrail.errors.NotFoundError('Not found Priority with name "%s"' % priority)
        else:
            raise testrail.errors.TestrailError('Wrong type of parameter "priority" in method "add_case".'
                                                'Got: "%s". Must be either "str" or "testrail.models.Priority"' % type(priority))

        if isinstance(milestone, testrail.models.Milestone):
            parameters['milestone_id'] = milestone.id
        elif isinstance(milestone, str):
            milestone = self.project().get_milestone_by_name(milestone)
            if priority is not None:
                parameters['milestone_id'] = milestone.id
            else:
                raise testrail.errors.NotFoundError('Not found Milestone with name "%s" '
                                                    'In project "%s".' % (milestone, self.project().name))
        else:
            raise testrail.errors.TestrailError('Wrong type of parameter "milestone" in method "add_case". '
                                                'Got: "%s". Must be either "str" or "testrail.models.Milestone"' % type(milestone))

        if estimate is not None:
            parameters['estimate'] = estimate

        if refs is not None:
            parameters['refs'] = refs

        for field in custom_fields:
            if field.startswith('custom_'):
                parameters[field] = custom_fields[field]
            else:
                parameters['custom_' + field] = custom_fields[field]

        return testrail.core.data.TestrailData.add_case(self.id, **parameters)