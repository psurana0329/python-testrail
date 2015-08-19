#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

import testrail
import testrail.core.utils as utils


class CustomFieldSpecification(object):
    """
    Service class.
    Never exposed to User.
    """
    def __init__(self, attributes):

        self.configs = attributes['configs']

        self.id = attributes['id']
        self.type_id = attributes['type_id']
        self.is_active = attributes['is_active']

        self.name = attributes['name']
        self.system_name = attributes['system_name']
        self.label = attributes['label']

        self.description = attributes['description']

        self.display_order = attributes['display_order']

    def construct_field(self, project_id):

        if not self.is_active:
            return None

        def switch_field_type(config):
            if self.type_id == 1:
                return StringField(project_id, self, config)
            elif self.type_id == 2:
                return IntegerField(project_id, self, config)
            elif self.type_id == 3:
                return TextField(project_id, self, config)
            elif self.type_id == 4:
                return UrlField(project_id, self, config)
            elif self.type_id == 5:
                return CheckboxField(project_id, self, config)
            elif self.type_id == 6:
                return DropdownField(project_id, self, config)
            elif self.type_id == 7:
                return UserField(project_id, self, config)
            elif self.type_id == 8:
                return DateField(project_id, self, config)
            elif self.type_id == 9:
                return MilestoneField(project_id, self, config)
            elif self.type_id == 10:
                return StepsField(project_id, self, config)
            elif self.type_id == 12:
                return MultiselectField(project_id, self, config)

        for config in self.configs:
            if config['context']['is_global']:
                return switch_field_type(config)

            elif project_id in config['context']['project_ids']:
                return switch_field_type(config)


class CaseField(CustomFieldSpecification):
    def __init__(self, attributes):
        CustomFieldSpecification.__init__(self, attributes)

    def __str__(self):
        return '<CaseField %s [%s]>' % (self.system_name, self.id)


class ResultField(CustomFieldSpecification):
    def __init__(self, attributes):
        CustomFieldSpecification.__init__(self, attributes)

    def __str__(self):
        return '<ResultField %s [%s]>' % (self.system_name, self.id)


class CustomField(object):
    def __init__(self, project_id, spec, config):
        self.__project_id = int(project_id)
        self.__id = config['id']
        self.__is_required = bool(config['options']['is_required'])
        self.__name = spec.name
        self.__system_name = spec.system_name
        self.__label = spec.label
        self.__description = spec.description
        self.__display_order = spec.display_order

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        raise RuntimeError('Attribute CustomField.id cannot be modified.')

    @property
    def project(self):
        return testrail.core.data.TestrailData.get_project_by_id(self.__project_id)

    @project.setter
    def project(self, value):
        raise RuntimeError('Attribute CustomField.project cannot be modified.')

    @property
    def is_required(self):
        return self.__is_required

    @is_required.setter
    def is_required(self, value):
        raise RuntimeError('Attribute CustomField.is_required cannot be modified.')

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        raise RuntimeError('Attribute CustomField.name cannot be modified.')

    @property
    def system_name(self):
        return self.__system_name

    @system_name.setter
    def system_name(self, value):
        raise RuntimeError('Attribute CustomField.system_name cannot be modified.')

    @property
    def label(self):
        return self.__label

    @label.setter
    def label(self, value):
        raise RuntimeError('Attribute CustomField.label cannot be modified.')

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        raise RuntimeError('Attribute CustomField.description cannot be modified.')

    @property
    def display_order(self):
        return self.__display_order

    @display_order.setter
    def display_order(self, value):
        raise RuntimeError('Attribute CustomField.display_order cannot be modified.')


class StringField(CustomField):
    def __init__(self, project_id, specification, config):
        CustomField.__init__(self, project_id, specification, config)
        self.__type_id = 1
        self.__default_value = str(config['options']['default_value'])

    def __str__(self):
        return '<StringField %s [%s]>' % (self.system_name, self.id)

    def __repr__(self):
        return self.__str__()

    @property
    def type_id(self):
        return self.__type_id

    @type_id.setter
    def type_id(self, value):
        raise RuntimeError('Attribute CustomField.type_id cannot be modified.')

    @property
    def default_value(self):
        return self.__default_value

    @default_value.setter
    def default_value(self, value):
        raise RuntimeError('Attribute StringField.default_value cannot be modified.')


class IntegerField(CustomField):
    def __init__(self, project_id, specification, config):
        CustomField.__init__(self, project_id, specification, config)
        self.__type_id = 2
        self.__default_value = int(config['options']['default_value'])

    def __str__(self):
        return '<IntegerField %s [%s]>' % (self.system_name, self.id)

    def __repr__(self):
        return self.__str__()

    @property
    def type_id(self):
        return self.__type_id

    @type_id.setter
    def type_id(self, value):
        raise RuntimeError('Attribute CustomField.type_id cannot be modified.')

    @property
    def default_value(self):
        return self.__default_value

    @default_value.setter
    def default_value(self, value):
        raise RuntimeError('Attribute IntegerField.default_value cannot be modified.')


class TextField(CustomField):
    def __init__(self, project_id, specification, config):
        CustomField.__init__(self, project_id, specification, config)
        self.__type_id = 3
        self.__default_value = str(config['options']['default_value'])
        self.__format = str(config['options']['format'])
        try:
            self.__rows = int(config['options']['rows'])
        except ValueError:
            self.__rows = None

    def __str__(self):
        return '<TextField %s [%s]>' % (self.system_name, self.id)

    def __repr__(self):
        return self.__str__()

    @property
    def type_id(self):
        return self.__type_id

    @type_id.setter
    def type_id(self, value):
        raise RuntimeError('Attribute CustomField.type_id cannot be modified.')

    @property
    def default_value(self):
        return self.__default_value

    @default_value.setter
    def default_value(self, value):
        raise RuntimeError('Attribute TextField.default_value cannot be modified.')

    @property
    def format(self):
        return self.__format

    @format.setter
    def format(self, value):
        raise RuntimeError('Attribute TextField.format cannot be modified.')

    @property
    def rows(self):
        return self.__rows

    @rows.setter
    def rows(self, value):
        raise RuntimeError('Attribute TextField.rows cannot be modified.')


class UrlField(CustomField):
    def __init__(self, project_id, specification, config):
        CustomField.__init__(self, project_id, specification, config)
        self.__type_id = 4
        self.__default_value = str(config['options']['default_value'])

    def __str__(self):
        return '<UrlField %s [%s]>' % (self.system_name, self.id)

    def __repr__(self):
        return self.__str__()

    @property
    def type_id(self):
        return self.__type_id

    @type_id.setter
    def type_id(self, value):
        raise RuntimeError('Attribute CustomField.type_id cannot be modified.')

    @property
    def default_value(self):
        return self.__default_value

    @default_value.setter
    def default_value(self, value):
        raise RuntimeError('Attribute UrlField.default_value cannot be modified.')


class CheckboxField(CustomField):
    def __init__(self, project_id, specification, config):
        CustomField.__init__(self, project_id, specification, config)
        self.__type_id = 5
        self.__default_value = bool(int(config['options']['default_value']))

    def __str__(self):
        return '<CheckboxField %s [%s]>' % (self.system_name, self.id)

    def __repr__(self):
        return self.__str__()

    @property
    def type_id(self):
        return self.__type_id

    @type_id.setter
    def type_id(self, value):
        raise RuntimeError('Attribute CustomField.type_id cannot be modified.')

    @property
    def default_value(self):
        return self.__default_value

    @default_value.setter
    def default_value(self, value):
        raise RuntimeError('Attribute CheckboxField.default_value cannot be modified.')


class DropdownField(CustomField):
    def __init__(self, project_id, specification, config):
        CustomField.__init__(self, project_id, specification, config)
        self.__type_id = 6
        self.__default_value = int(config['options']['default_value'])
        self.__items = {}
        for line in config['options']['items'].splitlines():
            key, value = line.split(',')
            self.__items[int(key.strip())] = value.strip()

    def __str__(self):
        return '<DropdownField %s [%s]>' % (self.system_name, self.id)

    def __repr__(self):
        return self.__str__()

    @property
    def type_id(self):
        return self.__type_id

    @type_id.setter
    def type_id(self, value):
        raise RuntimeError('Attribute CustomField.type_id cannot be modified.')

    @property
    def default_value(self):
        return self.__default_value

    @default_value.setter
    def default_value(self, value):
        raise RuntimeError('Attribute DropdownField.default_value cannot be modified.')

    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, value):
        raise RuntimeError('Attribute DropdownField.items cannot be modified.')


class UserField(CustomField):
    def __init__(self, project_id, specification, config):
        CustomField.__init__(self, project_id, specification, config)
        self.__type_id = 7
        try:
            self.__default_value = int(config['options']['default_value'])
        except ValueError:
            self.__default_value = None

    def __str__(self):
        return '<UserField %s [%s]>' % (self.system_name, self.id)

    def __repr__(self):
        return self.__str__()

    @property
    def type_id(self):
        return self.__type_id

    @type_id.setter
    def type_id(self, value):
        raise RuntimeError('Attribute CustomField.type_id cannot be modified.')

    @property
    def default_value(self):
        return self.__default_value

    @default_value.setter
    def default_value(self, value):
        raise RuntimeError('Attribute UserField.default_value cannot be modified.')


class DateField(CustomField):
    def __init__(self, project_id, specification, config):
        CustomField.__init__(self, project_id, specification, config)
        self.__type_id = 8

    def __str__(self):
        return '<DateField %s [%s]>' % (self.system_name, self.id)

    def __repr__(self):
        return self.__str__()

    @property
    def type_id(self):
        return self.__type_id

    @type_id.setter
    def type_id(self, value):
        raise RuntimeError('Attribute CustomField.type_id cannot be modified.')


class MilestoneField(CustomField):
    def __init__(self, project_id, specification, config):
        CustomField.__init__(self, project_id, specification, config)
        self.__type_id = 9

    def __str__(self):
        return '<MilestoneField %s [%s]>' % (self.system_name, self.id)

    def __repr__(self):
        return self.__str__()

    @property
    def type_id(self):
        return self.__type_id

    @type_id.setter
    def type_id(self, value):
        raise RuntimeError('Attribute CustomField.type_id cannot be modified.')


class StepsField(CustomField):
    def __init__(self, project_id, specification, config):
        CustomField.__init__(self, project_id, specification, config)
        self.__type_id = 10
        self.__format = str(config['options']['format'])
        self.__has_expected = bool(config['options']['has_expected'])
        try:
            self.__rows = int(config['options']['rows'])
        except ValueError:
            self.__rows = None

    def __str__(self):
        return '<StepsField %s [%s]>' % (self.system_name, self.id)

    def __repr__(self):
        return self.__str__()

    @property
    def type_id(self):
        return self.__type_id

    @type_id.setter
    def type_id(self, value):
        raise RuntimeError('Attribute CustomField.type_id cannot be modified.')

    @property
    def has_expected(self):
        return self.__has_expected

    @has_expected.setter
    def has_expected(self, value):
        raise RuntimeError('Attribute StepsField.has_expected cannot be modified.')

    @property
    def format(self):
        return self.__format

    @format.setter
    def format(self, value):
        raise RuntimeError('Attribute StepsField.format cannot be modified.')

    @property
    def rows(self):
        return self.__rows

    @rows.setter
    def rows(self, value):
        raise RuntimeError('Attribute StepsField.rows cannot be modified.')


class MultiselectField(CustomField):
    def __init__(self, project_id, specification, config):
        CustomField.__init__(self, project_id, specification, config)
        self.__type_id = 12
        self.__items = {}
        for line in config['options']['items'].splitlines():
            key, value = line.split(',')
            self.__items[int(key.strip())] = value.strip()

    def __str__(self):
        return '<MultiselectField %s [%s]>' % (self.system_name, self.id)

    def __repr__(self):
        return self.__str__()

    @property
    def type_id(self):
        return self.__type_id

    @type_id.setter
    def type_id(self, value):
        raise RuntimeError('Attribute CustomField.type_id cannot be modified.')

    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, value):
        raise RuntimeError('Attribute DropdownField.items cannot be modified.')


class CustomFieldsContainer(object):
    def __init__(self, fields_specification, attributes):
        self.__specs = {}
        self.__values = {}

        for item in fields_specification:
            key = str(item.name)
            try:
                value = attributes[item.system_name]
            except KeyError:
                value = None

            self.__specs[key] = item

            spec = self.__specs[key]

            if value is None:
                self.__values[key] = value

            elif spec.type_id in [1, 2, 3, 4, 5, 10]:
                # simple types like string, int or list
                self.__values[key] = value

            elif spec.type_id == 6:
                # dropdown selection is provided via item id
                self.__values[key] = spec.items[value]

            elif spec.type_id == 12:
                # similar multiselect is a list of ids
                self.__values[key] = [spec.items[i] for i in value]

            elif spec.type_id == 7:
                # user id
                self.__values[key] = testrail.core.data.TestrailData.get_user_by_id(value)

            elif spec.type_id == 8:
                # date is shitty - it is string in a format determined by User config
                # cannot do anything about it
                self.__values[key] = value

            elif spec.type_id == 9:
                # milestone id
                self.__values[key] = testrail.core.data.TestrailData.get_milestone_by_id(value)

    def __iter__(self):
        return self.__values.__iter__()

    def items(self):
        return self.__values.items()

    def __getitem__(self, item):
        item = str(item)
        if item.startswith('custom_'):
            item = item[7:]

        try:
            return self.__values[item]
        except KeyError:
            return None

    def __setitem__(self, key, value):
        raise RuntimeError('Cannot modify field %s directly. Use Case.update(%s=%s) method for this.' %
                           (key, key, value))

    def get_code(self, key, value):
        if key.startswith('custom_'):
            key = key[7:]

        spec = self.__specs[key]

        if spec.type_id in [1, 2, 3, 4, 5, 10]:
            return value

        elif spec.type_id == 6:
            for k, v in spec.items.items():
                if v == value:
                    return k
            return None

        elif spec.type_id == 12:
            result = []
            for k, v in spec.items.items():
                if v in value:
                    result.append(k)
            return result

        elif spec.type_id == 7:
            return utils.guess_user_id(value)

        elif spec.type_id == 8:
            # date is shitty - it is string in a format determined by User config
            # cannot do anything about it
            return value

        elif spec.type_id == 9:
            return utils.guess_milestone_id(testrail.core.data.TestrailData.get_project_by_id(spec.project_id),
                                            value)




