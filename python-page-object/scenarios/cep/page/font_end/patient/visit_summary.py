__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../../../")
from webium.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../../")
from util.logger import Test


class PatientVisitSummaryPage(BasePage):
    search_box = (By.XPATH, "//div[@id='visitSummaries']//input[@type='search']")
    view_btn = (By.XPATH, "//button[@class='btn btn-primary btn-xs']")
    reason_visit = (By.XPATH, "//h3[text()='Reason for visit']/following-sibling::p[1]")
    plan_instr = (By.XPATH, "//h3[text()='Plan / Discharge Instructions']/following-sibling::p[2]")
    close_btn = (By.XPATH, "//h4[contains(text(),'Visit Summary')]/preceding-sibling::button")

    @Test(search_box)
    def search_visit(self, value=None):
        self.element(*self.search_box).type(value).type_and_wait(Keys.TAB, 3)
        return self

    @Test(view_btn)
    def click_on_view_button(self):
        self.element(*self.view_btn).wait_until_clickable() \
            .highlight_element().click()
        return self

    @Test(reason_visit)
    def get_reasons_visit(self):
        return self.element(*self.reason_visit) \
            .highlight_element().get_text_value()

    @Test(plan_instr)
    def get_plan_or_discharge_instructions(self):
        return self.element(*self.plan_instr).highlight_element().get_text_value()

    @Test(close_btn)
    def click_on_close_visit_summary(self):
        self.element(*self.close_btn).highlight_element().click()
