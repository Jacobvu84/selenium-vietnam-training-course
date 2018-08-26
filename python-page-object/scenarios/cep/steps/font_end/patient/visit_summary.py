__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from page.font_end.patient.visit_summary import PatientVisitSummaryPage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from util.assertions import Assert
from util.date_time import get_current_datetime


class PatientVisitSummarySteps(Assert):
    on_visit_summary_page = PatientVisitSummaryPage()

    def view_visit_summary(self):
        current_date = get_current_datetime()
        self.on_visit_summary_page.search_visit(current_date) \
            .click_on_view_button()
        return self

    def should_see_reason_for_visit(self, reasons):
        values = reasons.split(",")
        for value in values:
            self.verifyContainsString(value, self.on_visit_summary_page.get_reasons_visit())
        return self

    def should_see_plan_or_discharge_instructions(self, plan):
        self.verifyEquals(plan, self.on_visit_summary_page.get_plan_or_discharge_instructions())
        return self

    def finish_view(self):
        self.on_visit_summary_page.click_on_close_visit_summary()
