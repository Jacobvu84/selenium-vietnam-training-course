__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../../../")
from webium.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../../")
from util.logger import Test


class PatientVisitPage(BasePage):

    def get_column_title_of_upcoming_visits(self, col_index):
        table_col = (By.XPATH, "//table[@id='DataTables_Table_0']/thead/tr/th[{0}]".format(col_index))
        return self.element(*table_col).get_text_value()

    def get_column_title_of_visit_history(self, col_index):
        table_col = (By.XPATH, "//table[@id='DataTables_Table_1']/thead/tr/th[{0}]".format(col_index))
        return self.element(*table_col).get_text_value()
