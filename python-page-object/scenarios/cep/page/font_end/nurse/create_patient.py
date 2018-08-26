__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webium.base_page import BasePage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.logger import Test
from util.assertions import Assert


class CreatePatientPage(BasePage, Assert):
    # Enter patient's information:
    create_patient_btn = (By.XPATH, "//a[@data-bind='disable:creatingPatient(), click:doCreatePatient']")

    month_admission = (By.ID, "jsonform-4-elt-first_admission_month")
    day_admission = (By.ID, "jsonform-4-elt-first_admission_day")
    year_admission = (By.ID, "jsonform-4-elt-first_admission_year")

    diagnosis = (By.XPATH, '//label[text()="What is the patient\'s principal diagnosis upon admission to the facility?"]'
                           '/following-sibling::input')
    reason_visit = (By.XPATH, '//label[text()="Reason for visit"]/following-sibling::input')
    consented = (By.XPATH, '//label[text()="This patient has consented to be seen via telemedicine"]')
    next_button = (By.XPATH, "//a[@data-bind='visible: showBack']/following-sibling::a[contains(.,'Continue')]")

    @Test(create_patient_btn)
    def click_on_create_new_patient(self, year):
        self.element(*self.create_patient_btn).wait_until_present().click()
        return self

    @Test(month_admission)
    def enter_month_admission(self, month):
        self.element(*self.month_admission).select_option_by_value(month)
        return self

    @Test(day_admission)
    def enter_day_admission(self, day):
        self.element(*self.day_admission).wait_until_present().type(day)
        return self

    @Test(year_admission)
    def enter_year_admission(self, year):
        self.element(*self.year_admission).wait_until_present().type(year)
        return self

    @Test(diagnosis)
    def enter_diagnosis(self, value):
        self.element(*self.diagnosis).click()
        self.element(*self.diagnosis).type_and_wait(value, 5) \
            .type(Keys.ENTER) \
            .type_and_wait(Keys.TAB, 3)
        return self

    @Test(reason_visit)
    def enter_reason_visit(self, reason):
        self.element(*self.reason_visit).click()
        self.element(*self.reason_visit).type_and_wait(reason, 5) \
            .type(Keys.ENTER) \
            .type_and_wait(Keys.TAB, 3)
        return self

    @Test(consented)
    def click_on_consented(self):
        self.element(*self.consented).wait_until_present().click()
        return self

    @Test(next_button)
    def complete_enter_patient_information(self, year):
        self.element(*self.next_button).wait_until_present().click_and_wait(3)
        return self



