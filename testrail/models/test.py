#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

import testrail


class Test(object):
    """
    Test container.

    Attributes:
       id                   -- (int) Unique test ID
       title                -- (str) Test title
       assigned_to          -- (User) The user this test is assigned to
       run                  -- (Run) The test run the test belongs to
       case                 -- (Case) The test case this test is created from
       status               -- (Status) The current status of this test
       type                 -- (CaseType) The case type of this test
       priority             -- (Priority) The priority of this test
       milestone            -- (Milestone) The milestone this test is linked to
       estimate             -- (str) The estimate of the related test case
       estimate_forecast    -- (str) The estimate forecast of the related test case
       refs                 -- (str) A comma-separated list of references/requirements
                               that are linked to the test case
       fields['<name>']     -- custom fields of this test
    """
    def __init__(self, attributes):
        self.__id = int(attributes['id'])
        self.__run_id = int(attributes['run_id'])
        self.__case_id = int(attributes['case_id'])
        self.__status_id = int(attributes['status_id'])
        self.__title = attributes['title']
        self.__type_id = int(attributes['type_id'])
        self.__priority_id = int(attributes['priority_id'])
        
        try:
            self.__milestone_id = int(attributes['milestone_id'])
        except TypeError:
            self.__milestone_id = None
            
        self.__refs = attributes['refs']
        self.__estimate = attributes['estimate']
        self.__estimate_forecast = attributes['estimate_forecast']

        try:
            self.__assigned_to = int(attributes['assignedto_id'])
        except TypeError:
            self.__assigned_to = None

        # and all the custom fields:
        self.__fields = testrail.models.CustomFieldsContainer(self.custom_fields(), attributes)

    def __str__(self):
        return '<Test %s [%s]>' % (self.title, self.id)

    def __repr__(self):
        return self.__str__()

    ###########################################################################
    # Getters/Setters

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        raise RuntimeError('Attribute Test.id cannot be modified.')

    @property
    def run(self):
        return testrail.core.data.TestrailData.get_run_by_id(self.__run_id)

    @run.setter
    def run(self, value):
        raise RuntimeError('Attribute Test.run cannot be modified.')

    @property
    def assigned_to(self):
        return testrail.core.data.TestrailData.get_user_by_id(self.__assigned_to)

    @assigned_to.setter
    def assigned_to(self, value):
        raise RuntimeError('Attribute Test.assigned_to cannot be modified.')
    
    @property
    def case(self):
        return testrail.core.data.TestrailData.get_case_by_id(self.__case_id)

    @case.setter
    def case(self, value):
        raise RuntimeError('Attribute Test.case cannot be modified.')
    
    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        raise RuntimeError('Attribute Test.title cannot be modified directly. '
                           'Please use Test.update() for this.')

    @property
    def type(self):
        return testrail.core.data.TestrailData.get_case_type_by_id(self.__type_id)

    @type.setter
    def type(self, value):
        raise RuntimeError('Attribute Test.type cannot be modified directly. '
                           'Please use Test.update() for this.')

    @property
    def priority(self):
        return testrail.core.data.TestrailData.get_priority_by_id(self.__priority_id)

    @priority.setter
    def priority(self, value):
        raise RuntimeError('Attribute Test.priority cannot be modified directly. '
                           'Please use Test.update() for this.')

    @property
    def status(self):
        return testrail.core.data.TestrailData.get_status_by_id(self.__status_id)

    @status.setter
    def status(self, value):
        raise RuntimeError('Attribute Test.status cannot be modified directly. '
                           'Please use Test.update() for this.')
    
    @property
    def milestone(self):
        return testrail.core.data.TestrailData.get_milestone_by_id(self.__milestone_id)

    @milestone.setter
    def milestone(self, value):
        raise RuntimeError('Attribute Test.milestone cannot be modified directly. '
                           'Please use Test.update() for this.')

    @property
    def refs(self):
        return self.__refs

    @refs.setter
    def refs(self, value):
        raise RuntimeError('Attribute Test.refs cannot be modified directly. '
                           'Please use Test.update() for this.')

    @property
    def estimate(self):
        return self.__estimate

    @estimate.setter
    def estimate(self, value):
        raise RuntimeError('Attribute Test.estimate cannot be modified directly. '
                           'Please use Test.update() for this.')

    @property
    def estimate_forecast(self):
        return self.__estimate_forecast

    @estimate_forecast.setter
    def estimate_forecast(self, value):
        raise RuntimeError('Attribute Test.estimate_forecast cannot be modified.')

    @property
    def fields(self):
        return self.__fields

    @fields.setter
    def fields(self, value):
        raise RuntimeError('Attribute Test.fields cannot be modified.')

    ###########################################################################
    # API Methods

    def custom_fields(self):
        return self.run.project.get_result_fields()

    def get_results(self):
        """
        Return list of Result objects for this test.

        :rtype: list of [testrail.models.Result]
        """
        return testrail.core.data.TestrailData.get_test_results(self.id)

    def add_result(self):
        raise NotImplementedError