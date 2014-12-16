#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

# one import to rule them all
from testrail import Testrail

# first thing to do is to configure where your testrail connection
Testrail(host='192.168.1.1', port='8080',
         user='someuser@domain.dom', password='somepassword')

################################################################################
# Basic usage

# Get users list
for user in Testrail.users():
    print(user.name)


# Get user by his name
me = Testrail.get_user_by_name('Super QA')
print(me.id, me.email)


# Get all projects
for project in Testrail.projects():
    print(project.name)


# Or get only active (not completed) projects
for project in Testrail.projects(is_completed=False):
    print(project.name)


# Change project description
my_project = Testrail.get_project_by_name('My Favourite Project')
print(my_project.announcement)
my_project.update(announcement='This announcement was updated!')
print(my_project.announcement)


# Explore project`s milestones, suites, test plans and test runs
my_project = Testrail.get_project_by_name('My Favourite Project')

for milestone in my_project.milestones():
    print(milestone.name)

for suite in my_project.suites():
    print(suite.name)

for plan in my_project.plans():
    print(plan.name)

for run in my_project.runs():
    print(run.name)


# Create new test run
my_project = Testrail.get_project_by_name('My Favourite Project')
suite = my_project.get_suite_by_name('Master')

cases_to_run = suite.cases(types=['Functionality', 'UI'],
                           priorities=['Normal'])

new_run = suite.add_run(name='Normal func test', assignedto='V.Spiridonov',
                        include_all=False, cases=cases_to_run)

print(new_run.id)


# Change test statuses
my_project = Testrail.get_project_by_name('My Favourite Project')

some_run = my_project.runs(suites=['Master'], limit=1)[0]

for test in some_run.tests(statuses=['Untested']):
    test.set_passed(comment='OK')