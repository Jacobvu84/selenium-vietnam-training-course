__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from selenium.webdriver.common.by import By
from webium.base_page import BasePage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.logger import Test


class ContactInforPage(BasePage):

    continue_btn = (By.XPATH, "//div[@id='IntakeModal']//a[contains(.,'Continue')]")

    ed_facility = (By.NAME, 'ed_facility_name')
    ed_phone = (By.NAME, 'ed_facility_phone')
    nurse_name = (By.NAME, 'requester_name')
    nurse_phone = (By.NAME, 'requester_phone')
    doctor_name = (By.NAME, 'er_doctor_name')
    doctor_phone = (By.NAME, 'er_doctor_phone')

    @Test(continue_btn)
    def click_on_continue(self):
        self.element(*self.continue_btn).wait_until_present().click_and_wait(3)
        return self

    def get_ed_facility_name(self):
        return self.element(*self.ed_facility).wait_until_present().get_value()

    @Test(ed_phone)
    def enter_facility_phone_number(self, phone_number):
        if '' != phone_number:
            self.element(*self.ed_phone).type(phone_number)
        return self

    def get_nurse_name(self):
        return self.element(*self.nurse_name).get_value()

    def get_nurse_phone_number(self):
        return self.element(*self.nurse_phone).get_value()

    @Test(doctor_name)
    def enter_emergency_room_doctor(self, doctor_name):
        if '' != doctor_name:
            self.element(*self.doctor_name).type(doctor_name)
        return self

    @Test(doctor_phone)
    def enter_doctor_phone_number(self, phone_number):
        if '' != phone_number:
            self.element(*self.doctor_phone).type(phone_number)
        return self


