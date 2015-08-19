#!/usr/bin/env python
# -*- coding:  utf-8 -*-

# TODO: Provide 'update' for select fields

from __future__ import absolute_import
from __future__ import print_function

import datetime

import testrail


class Case(object):
    """
    Test case container.

    Attributes:
        id                   -- (int) Unique test case ID
        suite                -- (Suite) The test suite this test case belongs to
        section              -- (Section) The section this test case belongs to
        title                -- (str) Test case title
        type                 -- (CaseType) Type of this test case
        priority             -- (Priority) Priority of this test case
        milestone            -- (Milestone) Milestone this test case is linked to
        refs                 -- (str) A comma-separated list of references/requirements
        estimate             -- (str) The estimate, e.g. "30s" or "1m 45s"
        estimate_forecast    -- (str) The estimate forecast, e.g. "30s" or "1m 45s"
        created_on           -- (datetime) Date when this test case was created
        created_by           -- (User) User who created this test case
        updated_on           -- (datetime) Date when this test case was last updated
        updated_by           -- (User) User who last updated this test case

        fields['<name>']     -- custom fields of this case
    """
    def __init__(self, attributes):
        self.__id = int(attributes['id'])
        self.__suite_id = int(attributes['suite_id'])
        self.__section_id = int(attributes['section_id'])
        self.__type_id = int(attributes['type_id'])
        self.__priority_id = int(attributes['priority_id'])
        try:
            self.__milestone_id = int(attributes['milestone_id'])
        except TypeError:
            self.__milestone_id = None

        self.__title = attributes['title']
        self.__refs = attributes['refs']
        self.__estimate = attributes['estimate']
        self.__estimate_forecast = attributes['estimate_forecast']

        try:
            self.__created_on = datetime.datetime.fromtimestamp(attributes['created_on'])
        except TypeError:
            self.__created_on = None
        try:
            self.__updated_on = datetime.datetime.fromtimestamp(attributes['updated_on'])
        except TypeError:
            self.__updated_on = None

        self.__created_by = attributes['created_by']
        self.__updated_by = attributes['updated_by']

        # and all the custom fields:
        self.__fields = testrail.models.CustomFieldsContainer(self.custom_fields(), attributes)

    def __str__(self):
        return '<Case: %s [%s]>' % (self.title, self.id)

    def __repr__(self):
        return self.__str__()

    ###########################################################################
    # Getters/Setters

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        raise RuntimeError('Attribute Case.id cannot be modified.')

    @property
    def suite(self):
        return testrail.core.data.TestrailData.get_suite_by_id(self.__suite_id)

    @suite.setter
    def suite(self, value):
        raise RuntimeError('Attribute Case.suite cannot be modified.')

    @property
    def section(self):
        return testrail.core.data.TestrailData.get_section_by_id(self.__section_id)

    @section.setter
    def section(self, value):
        raise RuntimeError('Attribute Case.section cannot be modified.')

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        raise RuntimeError('Attribute Case.title cannot be modified directly. '
                           'Please use Case.update() for this.')

    @property
    def type(self):
        return testrail.core.data.TestrailData.get_case_type_by_id(self.__type_id)

    @type.setter
    def type(self, value):
        raise RuntimeError('Attribute Case.type cannot be modified directly. '
                           'Please use Case.update() for this.')

    @property
    def priority(self):
        return testrail.core.data.TestrailData.get_priority_by_id(self.__priority_id)

    @priority.setter
    def priority(self, value):
        raise RuntimeError('Attribute Case.priority cannot be modified directly. '
                           'Please use Case.update() for this.')

    @property
    def milestone(self):
        return testrail.core.data.TestrailData.get_milestone_by_id(self.__milestone_id)

    @milestone.setter
    def milestone(self, value):
        raise RuntimeError('Attribute Case.milestone cannot be modified directly. '
                           'Please use Case.update() for this.')

    @property
    def refs(self):
        return self.__refs

    @refs.setter
    def refs(self, value):
        raise RuntimeError('Attribute Case.refs cannot be modified directly. '
                           'Please use Case.update() for this.')

    @property
    def estimate(self):
        return self.__estimate

    @estimate.setter
    def estimate(self, value):
        raise RuntimeError('Attribute Case.estimate cannot be modified directly. '
                           'Please use Case.update() for this.')

    @property
    def estimate_forecast(self):
        return self.__estimate_forecast

    @estimate_forecast.setter
    def estimate_forecast(self, value):
        raise RuntimeError('Attribute Case.estimate_forecast cannot be modified.')

    @property
    def created_on(self):
        return self.__created_on

    @created_on.setter
    def created_on(self, value):
        raise RuntimeError('Attribute Case.created_on cannot be modified.')

    @property
    def updated_on(self):
        return self.__updated_on

    @updated_on.setter
    def updated_on(self, value):
        raise RuntimeError('Attribute Case.updated_on cannot be modified.')

    @property
    def created_by(self):
        return testrail.core.data.TestrailData.get_user_by_id(self.__created_by)

    @created_by.setter
    def created_by(self, value):
        raise RuntimeError('Attribute Case.created_by cannot be modified.')

    @property
    def updated_by(self):
        return testrail.core.data.TestrailData.get_user_by_id(self.__updated_by)

    @updated_by.setter
    def updated_by(self, value):
        raise RuntimeError('Attribute Case.updated_by cannot be modified.')

    @property
    def fields(self):
        return self.__fields

    @fields.setter
    def fields(self, value):
        raise RuntimeError('Attribute Case.fields cannot be modified.')

    ###########################################################################
    # API Methods

    def update(self, **attributes):
        """
        Update this case attributes.

        Available for update:
            title                -- The ID of the suite the test case belongs to
            type_id              -- The ID of the test case type that is linked to
                                   the test case
            priority_id          -- The ID of the priority that is linked to
                                   the test case
            milestone_id         -- The ID of the milestone that is linked to
                                   the test case
            refs                 -- A comma-separated list of references/requirements
            estimate             -- The estimate, e.g. "30s" or "1m 45s"
            custom_<field_name>  -- custom fields of this case

        You can also provide:
            case_type           -- human name of type_id of CaseType object
            priority            -- human name of priority_id of Priority object
            milestone           -- human name of milestone_id of Milestone object
        """
        try:
            case_type = attributes['case_type']
        except KeyError:
            pass
        else:
            del attributes['case_type']
            if isinstance(case_type, testrail.models.CaseType):
                attributes['type_id'] = case_type.id
            elif isinstance(case_type, str):
                case_type = testrail.core.data.TestrailData.get_case_type_by_name(case_type)
                if case_type is not None:
                    attributes['type_id'] = case_type.id
                else:
                    raise testrail.errors.NotFoundError('Not found Case Type with name "%s"' % case_type)
            else:
                raise testrail.errors.TestrailError('Wrong type of parameter "type" in method "update_case".'
                                                    'Got: "%s". Must be either "str" or "testrail.models.CaseType"' % type(case_type))

        try:
            priority = attributes['priority']
        except KeyError:
            pass
        else:
            if isinstance(priority, testrail.models.Priority):
                attributes['priority_id'] = priority.id
            elif isinstance(priority, str):
                priority = testrail.core.data.TestrailData.get_priority_by_name(priority)
                if priority is not None:
                    attributes['priority_id'] = priority.id
                else:
                    raise testrail.errors.NotFoundError('Not found Priority with name "%s"' % priority)
            else:
                raise testrail.errors.TestrailError('Wrong type of parameter "priority" in method "update_case".'
                                                    'Got: "%s". Must be either "str" or "testrail.models.Priority"' % type(priority))

        try:
            milestone = attributes['milestone']
        except KeyError:
            pass
        else:
            if isinstance(milestone, testrail.models.Milestone):
                attributes['milestone_id'] = milestone.id
            elif isinstance(milestone, str):
                milestone = self.project().get_milestone_by_name(milestone)
                if milestone is not None:
                    attributes['milestone_id'] = milestone.id
                else:
                    raise testrail.errors.NotFoundError('Not found Milestone with name "%s" '
                                                        'In project "%s".' % (milestone, self.project().name))
            else:
                raise testrail.errors.TestrailError('Wrong type of parameter "milestone" in method "update_case". '
                                                    'Got: "%s". Must be either "str" or "testrail.models.Milestone"' % type(milestone))

        testrail.core.data.TestrailData.update_case(self.id, **attributes)

    def delete(self):
        """
        Delete this case.
        """
        testrail.core.data.TestrailData.delete_case(self.id)

    def custom_fields(self):
        """
        Description of custom fields this case has.
        """
        return self.suite.project.get_case_fields()

    def get_results(self):
        raise NotImplementedError

    def add_results(self):
        raise NotImplementedError