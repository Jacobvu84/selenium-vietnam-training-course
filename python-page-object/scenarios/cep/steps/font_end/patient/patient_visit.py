__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from page.font_end.patient.patient_visit import PatientVisitPage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from util.assertions import Assert
from util.logger import Test


class PatientVisitSteps(Assert):
    on_visit_page = PatientVisitPage()

    @Test(("Group Steps", ""))
    def should_see_the_upcoming_visits_table_with_columns(self, columns):
        cols = columns.split(",")
        col_index = 1
        for col in cols:
            self.verifyEquals(col, self.on_visit_page.get_column_title_of_upcoming_visits(col_index))
            col_index = col_index + 1
        return self

    @Test(("Group Steps", ""))
    def should_see_the_past_visit_table_with_columns(self, columns):
        cols = columns.split(",")
        col_index = 1
        for col in cols:
            self.verifyEquals(col, self.on_visit_page.get_column_title_of_visit_history(col_index))
            col_index = col_index + 1
        return self
