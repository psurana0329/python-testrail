#!/usr/bin/env python
# -*- coding:  utf-8 -*-

from __future__ import absolute_import

import unittest
import time
import datetime

import testrail
from tests.config import *


class MilestoneQuery(unittest.TestCase):
    def setUp(self):
        self.t = testrail.Testrail(SERVER, USER, PASS)
        self.p = self.t.get_project(name=TEST_PROJECT_NAME)
        self.m = self.p.get_milestone(TEST_MILESTONE_NAME)

    #################################################################################
    # get_plans()

    def test_milestone_get_all_plans(self):
        all_plans = self.m.get_plans()
        self.assertIsInstance(all_plans, list)
        for plan in all_plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.milestone.id, self.m.id)
            self.assertEqual(plan.project.id, self.p.id)

    def test_milestone_get_completed_plans(self):
        plans = self.m.get_plans(is_completed=True)
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertEqual(plan.milestone.id, self.m.id)
            self.assertTrue(plan.is_completed)
            self.assertIsInstance(plan.completed_on, datetime.datetime)

    def test_milestone_get_uncompleted_plans(self):
        plans = self.m.get_plans(is_completed=False)
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertEqual(plan.milestone.id, self.m.id)
            self.assertFalse(plan.is_completed)
            self.assertIsNone(plan.completed_on)

    def test_milestone_get_plans_limit(self):
        plans = self.m.get_plans(limit=1)
        self.assertIsInstance(plans, list)
        self.assertEqual(len(plans), 1)

    def test_milestone_get_plans_offset(self):
        plans = self.m.get_plans()
        plans_shift = self.p.get_plans(offset=2)
        self.assertEqual(plans[2].id, plans_shift[0].id)

    def test_milestone_get_plan_by_create_date_datetime(self):
        d = datetime.datetime.strptime('20150608000000', '%Y%m%d%H%M%S')
        plans = self.m.get_plans(created_after=d)
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertEqual(plan.milestone.id, self.m.id)
            self.assertGreater(plan.created_on, d)

        d = datetime.datetime.strptime('20150818163010', '%Y%m%d%H%M%S')
        plans = self.m.get_plans(created_before=d)
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertEqual(plan.milestone.id, self.m.id)
            self.assertLess(plan.created_on, d)

    def test_milestone_get_plan_by_create_date_str_date(self):
        d = datetime.datetime.strptime('20150608000000', '%Y%m%d%H%M%S')
        plans = self.m.get_plans(created_after='20150608000000')
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertEqual(plan.milestone.id, self.m.id)
            self.assertGreater(plan.created_on, d)

        d = datetime.datetime.strptime('20150818163010', '%Y%m%d%H%M%S')
        plans = self.m.get_plans(created_before='20150818163010')
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertEqual(plan.milestone.id, self.m.id)
            self.assertLess(plan.created_on, d)

    def test_milestone_get_plan_by_create_date_str_stamp(self):
        plans = self.m.get_plans(created_after='1339280582')
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertEqual(plan.milestone.id, self.m.id)
            self.assertGreater(plan.created_on,
                               datetime.datetime.fromtimestamp(int('1339280582')))

        plans = self.m.get_plans(created_before='1439280582')
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertEqual(plan.milestone.id, self.m.id)
            self.assertLess(plan.created_on,
                            datetime.datetime.fromtimestamp(int('1439280582')))

    def test_milestone_get_plan_by_create_date_int(self):
        plans = self.m.get_plans(created_after=1339280582)
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertEqual(plan.milestone.id, self.m.id)
            self.assertGreater(plan.created_on,
                               datetime.datetime.fromtimestamp(1339280582))

        plans = self.m.get_plans(created_before=1439280582)
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertEqual(plan.milestone.id, self.m.id)
            self.assertLess(plan.created_on,
                            datetime.datetime.fromtimestamp(1439280582))

    def test_milestone_get_plan_by_create_date_float(self):
        plans = self.m.get_plans(created_after=1339280582.032)
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertEqual(plan.milestone.id, self.m.id)
            self.assertGreater(plan.created_on,
                               datetime.datetime.fromtimestamp(1339280582.032))

        plans = self.m.get_plans(created_before=1439280582.032)
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertEqual(plan.milestone.id, self.m.id)
            self.assertLess(plan.created_on,
                            datetime.datetime.fromtimestamp(1439280582.032))

    def test_milestone_get_plan_by_create_date_timetuple(self):
        plans = self.m.get_plans(created_after=time.localtime(1339280582))
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertEqual(plan.milestone.id, self.m.id)
            self.assertGreater(plan.created_on,
                               datetime.datetime.fromtimestamp(time.mktime(time.localtime(1339280582))))

        plans = self.m.get_plans(created_before=time.localtime())
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertEqual(plan.milestone.id, self.m.id)
            self.assertLess(plan.created_on,
                            datetime.datetime.fromtimestamp(time.mktime(time.localtime())))

    def test_milestone_get_plan_by_creator_name(self):
        plans = self.m.get_plans(created_by=['Spiridonov Vyacheslav'])
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertEqual(plan.milestone.id, self.m.id)
            self.assertEqual(plan.created_by.id, 13)

    def test_milestone_get_plan_by_creator_id(self):
        plans = self.m.get_plans(created_by=[13])
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertEqual(plan.milestone.id, self.m.id)
            self.assertEqual(plan.created_by.id, 13)

    def test_milestone_get_plan_by_creator_email(self):
        plans = self.m.get_plans(created_by=['vspiridonov@bcc.ru'])
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertEqual(plan.milestone.id, self.m.id)
            self.assertEqual(plan.created_by.id, 13)

    def test_milestone_get_plan_by_creator_obj(self):
        plans = self.m.get_plans(created_by=[self.t.get_user(13)])
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertEqual(plan.milestone.id, self.m.id)
            self.assertEqual(plan.created_by.id, 13)

    def test_milestone_get_plan_by_creator_list(self):
        plans = self.m.get_plans(created_by=['Spiridonov Vyacheslav', 'Guest', 'Elecard'])
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertEqual(plan.milestone.id, self.m.id)
            self.assertIn(plan.created_by.id, [13, 4, 8])

    def test_milestone_get_plan_by_creator_single(self):
        plans = self.m.get_plans(created_by=13)
        self.assertIsInstance(plans, list)
        for plan in plans:
            self.assertIsInstance(plan, testrail.models.Plan)
            self.assertEqual(plan.project.id, self.p.id)
            self.assertEqual(plan.milestone.id, self.m.id)
            self.assertEqual(plan.created_by.id, 13)
    
    #################################################################################
    # get_runs()
    
    def test_milestone_get_all_runs(self):
        runs = self.m.get_runs()
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.milestone_id, self.m.id)

    def test_milestone_get_completed_runs(self):
        runs = self.m.get_runs(is_completed=True)
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.milestone_id, self.m.id)
            self.assertTrue(run.is_completed)
            self.assertIsInstance(run.completed_on, datetime.datetime)

    def test_milestone_get_uncompleted_runs(self):
        runs = self.m.get_runs(is_completed=False)
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.milestone_id, self.m.id)
            self.assertFalse(run.is_completed)
            self.assertIsNone(run.completed_on)

    def test_milestone_get_runs_limit(self):
        runs = self.m.get_runs(limit=1)
        self.assertIsInstance(runs, list)
        self.assertEqual(len(runs), 1)

    def test_milestone_get_runs_offset(self):
        runs = self.m.get_runs()
        runs_shift = self.m.get_runs(offset=2)
        self.assertEqual(runs[2].id, runs_shift[0].id)

    def test_milestone_get_run_by_create_date_datetime(self):
        d = datetime.datetime.strptime('20150608000000', '%Y%m%d%H%M%S')
        runs = self.m.get_runs(created_after=d)
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.milestone_id, self.m.id)
            self.assertGreater(run.created_on, d)

        d = datetime.datetime.strptime('20150608170600', '%Y%m%d%H%M%S')
        runs = self.m.get_runs(created_before=d)
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.milestone_id, self.m.id)
            self.assertLess(run.created_on, d)

    def test_milestone_get_run_by_create_date_str_date(self):
        d = datetime.datetime.strptime('20150608000000', '%Y%m%d%H%M%S')
        runs = self.m.get_runs(created_after='20150608000000')
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.milestone_id, self.m.id)
            self.assertGreater(run.created_on, d)

        d = datetime.datetime.strptime('20150608163010', '%Y%m%d%H%M%S')
        runs = self.m.get_runs(created_before='20150608163010')
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.milestone_id, self.m.id)
            self.assertLess(run.created_on, d)

    def test_milestone_get_run_by_create_date_str_stamp(self):
        runs = self.m.get_runs(created_after='1339280582')
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.milestone_id, self.m.id)
            self.assertGreater(run.created_on,
                               datetime.datetime.fromtimestamp(int('1339280582')))

        runs = self.m.get_runs(created_before='1439280582')
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.milestone_id, self.m.id)
            self.assertLess(run.created_on,
                            datetime.datetime.fromtimestamp(int('1439280582')))

    def test_milestone_get_run_by_create_date_int(self):
        runs = self.m.get_runs(created_after=1339280582)
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.milestone_id, self.m.id)
            self.assertGreater(run.created_on,
                               datetime.datetime.fromtimestamp(1339280582))

        runs = self.m.get_runs(created_before=1439280582)
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.milestone_id, self.m.id)
            self.assertLess(run.created_on,
                            datetime.datetime.fromtimestamp(1439280582))

    def test_milestone_get_run_by_create_date_float(self):
        runs = self.m.get_runs(created_after=1339280582.032)
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.milestone_id, self.m.id)
            self.assertGreater(run.created_on,
                               datetime.datetime.fromtimestamp(1339280582.032))

        runs = self.m.get_runs(created_before=1439280582.032)
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.milestone_id, self.m.id)
            self.assertLess(run.created_on,
                            datetime.datetime.fromtimestamp(1439280582.032))

    def test_milestone_get_run_by_create_date_timetuple(self):
        runs = self.m.get_runs(created_after=time.localtime(1339280582))
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.milestone_id, self.m.id)
            self.assertGreater(run.created_on,
                               datetime.datetime.fromtimestamp(time.mktime(time.localtime(1339280582))))

        runs = self.m.get_runs(created_before=time.localtime())
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.milestone_id, self.m.id)
            self.assertLess(run.created_on,
                            datetime.datetime.fromtimestamp(time.mktime(time.localtime())))

    def test_milestone_get_run_by_creator_name(self):
        runs = self.m.get_runs(created_by=['Spiridonov Vyacheslav'])
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.milestone_id, self.m.id)
            self.assertEqual(run.created_by_id, 13)

    def test_milestone_get_run_by_creator_id(self):
        runs = self.m.get_runs(created_by=[13])
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.milestone_id, self.m.id)
            self.assertEqual(run.created_by_id, 13)

    def test_milestone_get_run_by_creator_obj(self):
        runs = self.m.get_runs(created_by=[self.t.get_user(13)])
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.milestone_id, self.m.id)
            self.assertEqual(run.created_by_id, 13)

    def test_milestone_get_run_by_creator_list(self):
        runs = self.m.get_runs(created_by=['Spiridonov Vyacheslav', 'Guest', 'Elecard'])
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.milestone_id, self.m.id)
            self.assertIn(run.created_by_id, [13, 4, 8])

    def test_milestone_get_run_by_creator_single(self):
        runs = self.m.get_runs(created_by='Spiridonov Vyacheslav')
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.milestone_id, self.m.id)
            self.assertEqual(run.created_by_id, 13)

    def test_milestone_get_run_by_suite_name(self):
        runs = self.m.get_runs(suites=['Master'])
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.milestone_id, self.m.id)
            self.assertEqual(run.suite_id, 1496)

    def test_milestone_get_run_by_suite_id(self):
        runs = self.m.get_runs(suites=[1496])
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.milestone_id, self.m.id)
            self.assertEqual(run.suite_id, 1496)

    def test_milestone_get_run_by_suite_obj(self):
        runs = self.m.get_runs(suites=[self.p.get_suite('Master')])
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.milestone_id, self.m.id)
            self.assertEqual(run.suite_id, 1496)

    def test_milestone_get_run_by_suite_list(self):
        runs = self.m.get_runs(suites=['Master', 'wasap'])
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.milestone_id, self.m.id)
            self.assertIn(run.suite_id, [1496, 1499])

    def test_milestone_get_run_by_suite_single(self):
        runs = self.m.get_runs(suites='Master')
        self.assertIsInstance(runs, list)
        for run in runs:
            self.assertIsInstance(run, testrail.models.Run)
            self.assertEqual(run.project_id, self.p.id)
            self.assertEqual(run.milestone_id, self.m.id)
            self.assertEqual(run.suite_id, 1496)