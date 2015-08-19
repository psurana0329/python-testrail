#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import

import unittest
import time
import datetime

import testrail
from tests.config import *


class ProjectQuery(unittest.TestCase):
    def setUp(self):
        self.t = testrail.Testrail(SERVER, USER, PASS)
        self.p = self.t.get_project(name=TEST_PROJECT_NAME)

    #################################################################################
    # get_milestones()

    def test_project_get_all_milestones(self):
        all_milestones = self.p.get_milestones()
        self.assertIsInstance(all_milestones, list)
        for milestone in all_milestones:
            self.assertIsInstance(milestone, testrail.models.Milestone)
            self.assertEqual(milestone.project.id, self.p.id)

    def test_project_get_completed_milestones(self):
        completed_milestones = self.p.get_milestones(True)
        self.assertIsInstance(completed_milestones, list)
        for milestone in completed_milestones:
            self.assertIsInstance(milestone, testrail.models.Milestone)
            self.assertEqual(milestone.project.id, self.p.id)
            self.assertTrue(milestone.is_completed)
            self.assertIsInstance(milestone.completed_on, datetime.datetime)

    def test_project_get_uncompleted_milestones(self):
        uncompleted_milestones = self.p.get_milestones(False)
        self.assertIsInstance(uncompleted_milestones, list)
        for milestone in uncompleted_milestones:
            self.assertIsInstance(milestone, testrail.models.Milestone)
            self.assertEqual(milestone.project.id, self.p.id)
            self.assertFalse(milestone.is_completed)
            self.assertIsNone(milestone.completed_on)

    #################################################################################
    # get_milestone()

    def test_project_get_milestone_by_name(self):
        milestone = self.p.get_milestone('more stones')
        self.assertIsInstance(milestone, testrail.models.Milestone)
        self.assertEqual(milestone.project.id, self.p.id)
        self.assertEqual(milestone.name, 'more stones')

        milestone = self.p.get_milestone('sisisi')
        self.assertIsNone(milestone)

    #################################################################################
    # get_suites()

    def test_project_get_all_suites(self):
        all_suites = self.p.get_suites()
        self.assertIsInstance(all_suites, list)
        for suite in all_suites:
            self.assertIsInstance(suite, testrail.models.Suite)
            self.assertEqual(suite.project.id, self.p.id)

    #################################################################################
    # get_suite()

    def test_project_get_suite_by_name(self):
        suite = self.p.get_suite('Master')
        self.assertIsInstance(suite, testrail.models.Suite)
        self.assertEqual(suite.project.id, self.p.id)
        self.assertEqual(suite.name, 'Master')

        suite = self.p.get_suite('I`m not exist.')
        self.assertIsNone(suite)

    #################################################################################
    # get_case_fields()

    def test_project_get_case_fields(self):
        case_fields = self.p.get_case_fields()
        self.assertIsInstance(case_fields, list)
        for field in case_fields:
            self.assertEqual(field.project_id, self.p.id)
            self.assertIsNotNone(field.system_name)

    #################################################################################
    # get_result_fields()

    def test_project_get_result_fields(self):
        result_fields = self.p.get_result_fields()
        self.assertIsInstance(result_fields, list)
        for field in result_fields:
            self.assertEqual(field.project_id, self.p.id)
            self.assertIsNotNone(field.system_name)

    #################################################################################
    # get_plans()

    def test_project_get_all_plans(self):
        all_plans = self.p.get_plans()
        self.assertIsInstance(all_plans, list)
        for plan in all_plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)

    def test_project_get_completed_plans(self):
        plans = self.p.get_plans(is_completed=True)
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertTrue(plan.is_completed)
            self.assertIsInstance(plan.completed_on, datetime.datetime)

    def test_project_get_uncompleted_plans(self):
        plans = self.p.get_plans(is_completed=False)
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertFalse(plan.is_completed)
            self.assertIsNone(plan.completed_on)

    def test_project_get_plans_limit(self):
        plans = self.p.get_plans(limit=1)
        self.assertIsInstance(plans, list)
        self.assertEqual(len(plans), 1)

    def test_project_get_plans_offset(self):
        plans = self.p.get_plans()
        plans_shift = self.p.get_plans(offset=2)
        self.assertEqual(plans[2].id, plans_shift[0].id)

    def test_project_get_plan_by_milestone_name(self):
        plans = self.p.get_plans(milestones=['one'])
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertEqual(plan.milestone.id, 39)

    def test_project_get_plan_by_milestone_id(self):
        plans = self.p.get_plans(milestones=[39])
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertEqual(plan.milestone.id, 39)

    def test_project_get_plan_by_milestone_obj(self):
        plans = self.p.get_plans(milestones=[self.p.get_milestone('one')])
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertEqual(plan.milestone.id, 39)

    def test_project_get_plan_by_milestone_list(self):
        plans = self.p.get_plans(milestones=['one', 'two', 'more stones'])
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertIn(plan.milestone.id, [39, 40, 41])

    def test_project_get_plan_by_milestone_single(self):
        plans = self.p.get_plans(milestones='one')
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertEqual(plan.milestone.id, 39)

    def test_project_get_plan_by_create_date_datetime(self):
        d = datetime.datetime.strptime('20150608000000', '%Y%m%d%H%M%S')
        plans = self.p.get_plans(created_after=d)
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertGreater(plan.created_on, d)

        d = datetime.datetime.strptime('20150608163010', '%Y%m%d%H%M%S')
        plans = self.p.get_plans(created_before=d)
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertLess(plan.created_on, d)

    def test_project_get_plan_by_create_date_str_date(self):
        d = datetime.datetime.strptime('20150608000000', '%Y%m%d%H%M%S')
        plans = self.p.get_plans(created_after='20150608000000')
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertGreater(plan.created_on, d)

        d = datetime.datetime.strptime('20150608163010', '%Y%m%d%H%M%S')
        plans = self.p.get_plans(created_before='20150608163010')
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertLess(plan.created_on, d)

    def test_project_get_plan_by_create_date_str_stamp(self):
        plans = self.p.get_plans(created_after='1339280582')
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertGreater(plan.created_on,
                               datetime.datetime.fromtimestamp(int('1339280582')))

        plans = self.p.get_plans(created_before='1439280582')
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertLess(plan.created_on,
                            datetime.datetime.fromtimestamp(int('1439280582')))

    def test_project_get_plan_by_create_date_int(self):
        plans = self.p.get_plans(created_after=1339280582)
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertGreater(plan.created_on,
                               datetime.datetime.fromtimestamp(1339280582))

        plans = self.p.get_plans(created_before=1439280582)
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertLess(plan.created_on,
                            datetime.datetime.fromtimestamp(1439280582))

    def test_project_get_plan_by_create_date_float(self):
        plans = self.p.get_plans(created_after=1339280582.032)
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertGreater(plan.created_on,
                               datetime.datetime.fromtimestamp(1339280582.032))

        plans = self.p.get_plans(created_before=1439280582.032)
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertLess(plan.created_on,
                            datetime.datetime.fromtimestamp(1439280582.032))

    def test_project_get_plan_by_create_date_timetuple(self):
        plans = self.p.get_plans(created_after=time.localtime(1339280582))
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertGreater(plan.created_on,
                               datetime.datetime.fromtimestamp(time.mktime(time.localtime(1339280582))))

        plans = self.p.get_plans(created_before=time.localtime())
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertLess(plan.created_on,
                            datetime.datetime.fromtimestamp(time.mktime(time.localtime())))

    def test_project_get_plan_by_creator_name(self):
        plans = self.p.get_plans(created_by=['Spiridonov Vyacheslav'])
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertEqual(plan.created_by.id, 13)

    def test_project_get_plan_by_creator_id(self):
        plans = self.p.get_plans(created_by=[13])
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertEqual(plan.created_by.id, 13)

    def test_project_get_plan_by_creator_email(self):
        plans = self.p.get_plans(created_by=['vspiridonov@bcc.ru'])
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertEqual(plan.created_by.id, 13)

    def test_project_get_plan_by_creator_obj(self):
        plans = self.p.get_plans(created_by=[self.t.get_user(13)])
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertEqual(plan.created_by.id, 13)

    def test_project_get_plan_by_creator_list(self):
        plans = self.p.get_plans(created_by=['Spiridonov Vyacheslav', 'Guest', 'Elecard'])
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertIn(plan.created_by.id, [13, 4, 8])

    def test_project_get_plan_by_creator_single(self):
        plans = self.p.get_plans(created_by=13)
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertEqual(plan.created_by.id, 13)

    #################################################################################
    # get_plan()

    def test_project_get_plan_by_name(self):
        plan = self.p.get_plan('plan1')
        self.assertIsInstance(plan, testrail.models.Plan)
        self.assertEqual(plan.project.id, self.p.id)
        self.assertEqual(plan.name, 'plan1')

        plan = self.p.get_plan('Bigoody Boo!')
        self.assertIsNone(plan)

    #################################################################################
    # get_runs()

    def test_project_get_all_runs(self):
        runs = self.p.get_runs()
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)

    def test_project_get_completed_runs(self):
        runs = self.p.get_runs(is_completed=True)
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertTrue(run.is_completed)
            self.assertIsInstance(run.completed_on, datetime.datetime)

    def test_project_get_uncompleted_runs(self):
        runs = self.p.get_runs(is_completed=False)
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertFalse(run.is_completed)
            self.assertIsNone(run.completed_on)

    def test_project_get_runs_limit(self):
        runs = self.p.get_runs(limit=1)
        self.assertIsInstance(runs, list)
        self.assertEqual(len(runs), 1)

    def test_project_get_runs_offset(self):
        runs = self.p.get_runs()
        runs_shift = self.p.get_runs(offset=2)
        self.assertEqual(runs[2].id, runs_shift[0].id)

    def test_project_get_run_by_create_date_datetime(self):
        d = datetime.datetime.strptime('20150608000000', '%Y%m%d%H%M%S')
        runs = self.p.get_runs(created_after=d)
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertGreater(run.created_on, d)

        d = datetime.datetime.strptime('20150608170600', '%Y%m%d%H%M%S')
        runs = self.p.get_runs(created_before=d)
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertLess(run.created_on, d)

    def test_project_get_run_by_create_date_str_date(self):
        d = datetime.datetime.strptime('20150608000000', '%Y%m%d%H%M%S')
        runs = self.p.get_runs(created_after='20150608000000')
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertGreater(run.created_on, d)

        d = datetime.datetime.strptime('20150608163010', '%Y%m%d%H%M%S')
        runs = self.p.get_runs(created_before='20150608163010')
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertLess(run.created_on, d)

    def test_project_get_run_by_create_date_str_stamp(self):
        runs = self.p.get_runs(created_after='1339280582')
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertGreater(run.created_on,
                               datetime.datetime.fromtimestamp(int('1339280582')))

        runs = self.p.get_runs(created_before='1439280582')
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertLess(run.created_on,
                            datetime.datetime.fromtimestamp(int('1439280582')))

    def test_project_get_run_by_create_date_int(self):
        runs = self.p.get_runs(created_after=1339280582)
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertGreater(run.created_on,
                               datetime.datetime.fromtimestamp(1339280582))

        runs = self.p.get_runs(created_before=1439280582)
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertLess(run.created_on,
                            datetime.datetime.fromtimestamp(1439280582))

    def test_project_get_run_by_create_date_float(self):
        runs = self.p.get_runs(created_after=1339280582.032)
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertGreater(run.created_on,
                               datetime.datetime.fromtimestamp(1339280582.032))

        runs = self.p.get_runs(created_before=1439280582.032)
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertLess(run.created_on,
                            datetime.datetime.fromtimestamp(1439280582.032))

    def test_project_get_run_by_create_date_timetuple(self):
        runs = self.p.get_runs(created_after=time.localtime(1339280582))
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertGreater(run.created_on,
                               datetime.datetime.fromtimestamp(time.mktime(time.localtime(1339280582))))

        runs = self.p.get_runs(created_before=time.localtime())
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertLess(run.created_on,
                            datetime.datetime.fromtimestamp(time.mktime(time.localtime())))

    def test_project_get_run_by_creator_name(self):
        runs = self.p.get_runs(created_by=['Spiridonov Vyacheslav'])
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.created_by_id, 13)

    def test_project_get_run_by_creator_id(self):
        runs = self.p.get_runs(created_by=[13])
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.created_by_id, 13)

    def test_project_get_run_by_creator_obj(self):
        runs = self.p.get_runs(created_by=[self.t.get_user(13)])
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.created_by_id, 13)

    def test_project_get_run_by_creator_list(self):
        runs = self.p.get_runs(created_by=['Spiridonov Vyacheslav', 'Guest', 'Elecard'])
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertIn(run.created_by_id, [13, 4, 8])

    def test_project_get_run_by_creator_single(self):
        runs = self.p.get_runs(created_by='Spiridonov Vyacheslav')
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.created_by_id, 13)

    def test_project_get_run_by_milestone_name(self):
        runs = self.p.get_runs(milestones=['one'])
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.milestone_id, 39)

    def test_project_get_run_by_milestone_id(self):
        runs = self.p.get_runs(milestones=[39])
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.milestone_id, 39)

    def test_project_get_run_by_milestone_obj(self):
        runs = self.p.get_runs(milestones=[self.p.get_milestone('one')])
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.milestone_id, 39)

    def test_project_get_run_by_milestone_list(self):
        runs = self.p.get_runs(milestones=['one', 'two', 'more stones'])
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertIn(run.milestone_id, [39, 40, 41])

    def test_project_get_run_by_milestone_single(self):
        runs = self.p.get_runs(milestones='one')
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.milestone_id, 39)

    def test_project_get_run_by_suite_name(self):
        runs = self.p.get_runs(suites=['Master'])
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.suite_id, 1496)

    def test_project_get_run_by_suite_id(self):
        runs = self.p.get_runs(suites=[1496])
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.suite_id, 1496)

    def test_project_get_run_by_suite_obj(self):
        runs = self.p.get_runs(suites=[self.p.get_suite('Master')])
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.suite_id, 1496)

    def test_project_get_run_by_suite_list(self):
        runs = self.p.get_runs(suites=['Master', 'wasap'])
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertIn(run.suite_id, [1496, 1499])

    def test_project_get_run_by_suite_single(self):
        runs = self.p.get_runs(suites='Master')
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.suite_id, 1496)

    #################################################################################
    # get_run()

    def test_project_get_run_by_name(self):
        run = self.p.get_run('run1')
        self.assertIsInstance(run, testrail.models.Run)
        self.assertEqual(run.name, 'run1')

        run = self.p.get_run('Run Forest! Run!')
        self.assertIsNone(run)

