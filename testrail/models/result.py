#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

from datetime import datetime

import testrail


class Result(object):
    """
    Test results container.

    Attributes:
       id               -- (int) Unique test result ID
       test             -- (Test) The test this test result belongs to
       status           -- (Status) The status of the test result
       version          -- (str) The (build) version this test was executed against
       created_by       -- (User) The user who created this test result
       assigned_to      -- (User) The new assignee of the test after this result
       created_on       -- (datetime) Date when the test result was created
       comment          -- (str) Comment or error message of this test result
       elapsed          -- (str) Amount of time it took to execute the test
       defects          -- (str) A comma-separated list of defects linked to the test
                           result
       fields['<name>'] -- custom result fields
    """
    def __init__(self, attributes):
        self.__id = int(attributes['id'])
        self.__test_id = int(attributes['test_id'])
        self.__status_id = int(attributes['status_id'])
        self.__version = attributes['version']
        self.__created_on = datetime.fromtimestamp(attributes['created_on'])
        self.__created_by = int(attributes['created_by'])
        self.__assigned_to = int(attributes['assignedto_id'])
        self.__comment = attributes['comment']
        self.__elapsed = attributes['elapsed']
        self.__defects = attributes['defects']

        # and all the custom fields:
        self.__fields = testrail.models.CustomFieldsContainer(self.custom_fields(), attributes)

    def __str__(self):
        return '<Result [%s]>' % self.id

    def __repr__(self):
        return self.__str__()

    ###########################################################################
    # Getters/Setters

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        raise RuntimeError('Attribute Result.id cannot be modified.')

    @property
    def test(self):
        return testrail.core.data.TestrailData.get_test_by_id(self.__test_id)

    @test.setter
    def test(self, value):
        raise RuntimeError('Attribute Result.test cannot be modified.')

    @property
    def status(self):
        return testrail.core.data.TestrailData.get_status_by_id(self.__status_id)

    @status.setter
    def status(self, value):
        raise RuntimeError('Attribute Result.status cannot be modified.')

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, value):
        raise RuntimeError('Attribute Result.version cannot be modified.')

    @property
    def created_by(self):
        return testrail.core.data.TestrailData.get_user_by_id(self.__created_by)

    @created_by.setter
    def created_by(self, value):
        raise RuntimeError('Attribute Result.created_by cannot be modified.')

    @property
    def created_on(self):
        return self.__created_on

    @created_on.setter
    def created_on(self, value):
        raise RuntimeError('Attribute Result.created_on cannot be modified.')

    @property
    def assigned_to(self):
        return testrail.core.data.TestrailData.get_user_by_id(self.__assigned_to)

    @assigned_to.setter
    def assigned_to(self, value):
        raise RuntimeError('Attribute Result.assigned_to cannot be modified.')

    @property
    def comment(self):
        return self.__comment

    @comment.setter
    def comment(self, value):
        raise RuntimeError('Attribute Result.comment cannot be modified.')

    @property
    def elapsed(self):
        return self.__elapsed

    @elapsed.setter
    def elapsed(self, value):
        raise RuntimeError('Attribute Result.elapsed cannot be modified.')

    @property
    def defects(self):
        return self.__defects

    @defects.setter
    def defects(self, value):
        raise RuntimeError('Attribute Result.defects cannot be modified.')

    @property
    def fields(self):
        return self.__fields

    @fields.setter
    def fields(self, value):
        raise RuntimeError('Attribute Result.fields cannot be modified.')

    def custom_fields(self):
        return self.test.run.project.get_result_fields()