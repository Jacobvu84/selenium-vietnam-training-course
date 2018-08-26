__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webium.base_page import BasePage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.logger import Test


class GuestPage(BasePage):

    first_name = (By.NAME, 'first_name')
    last_name = (By.NAME, 'last_name')
    reason = (By.XPATH, "//label[text()='Reason for visit']/following-sibling::input")
    confirm = (By.NAME, 'telemedicine_consent')
    continue_btn = (By.XPATH, "//div[@id='IntakeModal']//a[@class = 'btn btn-primary btn-next']")

    @Test(first_name)
    def enter_first_name(self, value):
        self.element(*self.first_name).type(value)
        return self

    @Test(last_name)
    def enter_last_name(self, value):
        self.element(*self.last_name).type(value)
        return self

    @Test(reason)
    def enter_reason_for_visit(self, reasons):
        symptoms = reasons.split(",")
        for symptom in symptoms:
            self.element(*self.reason).wait_until_clickable() \
                .highlight_element().type(symptom).type(Keys.ENTER).type(Keys.TAB)
        return self

    @Test(confirm)
    def click_on_confirm(self):
        self.element(*self.confirm).check()
        return self

    @Test(continue_btn)
    def click_on_continue(self):
        self.element(*self.continue_btn).click_and_wait()
        return self