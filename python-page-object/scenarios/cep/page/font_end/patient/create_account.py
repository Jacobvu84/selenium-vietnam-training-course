__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../../../")
from webium.base_page import BasePage
from selenium.webdriver.common.by import By

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../../")
from util.logger import Test


class CreateAccountPage(BasePage):
    first_name = (By.NAME, "first_name")
    last_name = (By.NAME, "last_name")
    month = (By.XPATH, "//*[@class='form-control month']")
    day_txt = (By.XPATH, "//*[@class='form-control day']")
    year_txt = (By.XPATH, "//*[@class='form-control year']")
    ssn_txt = (By.NAME, "ssn")
    email_txt = (By.NAME, "email")
    newsletter_chk = (By.NAME, "newsletter")
    submit_btn = (By.XPATH, "//input[@type='submit']")

    @Test(first_name)
    def enter_first_name(self, fname):
        self.element(*self.first_name).type(fname)
        return self

    @Test(last_name)
    def enter_last_name(self, lname):
        self.element(*self.last_name).type(lname)
        return self

    @Test(month)
    def select_month(self, month):
        self.element(*self.month).select_option_by_value(month)
        return self

    @Test(day_txt)
    def enter_day(self, day):
        self.element(*self.day_txt).type(day)
        return self

    @Test(year_txt)
    def enter_year(self, year):
        self.element(*self.year_txt).type(year)
        return self

    @Test(ssn_txt)
    def enter_ssn(self, ssn):
        self.element(*self.ssn_txt).type(ssn)
        return self

    @Test(email_txt)
    def enter_email(self, email):
        self.element(*self.email_txt).type(email)
        return self

    @Test(newsletter_chk)
    def click_on_newsletter(self):
        # Hot fix to run scripts on TeleSychs
        newsletter = self.element(*self.newsletter_chk)
        if newsletter.is_present():
            newsletter.click()
        return self

    @Test(submit_btn)
    def click_on_submit(self):
        self.element(*self.submit_btn).click()
        return self


class RegisterPage(BasePage):
    # Account information
    fname_txt = (By.ID, "AppUserFirstName")
    lname_txt = (By.ID, "AppUserLastName")
    email_txt = (By.ID, "AppUserEmail")
    pwd_txt = (By.ID, "AppUserPassword")
    repwd_txt = (By.ID, "FooTemppassword")

    @Test(pwd_txt)
    def enter_new_password(self, pwd):
        self.element(*self.pwd_txt).type(pwd)
        return self

    @Test(repwd_txt)
    def enter_retype_password(self, pwd):
        self.element(*self.repwd_txt).type(pwd)
        return self

    @Test(fname_txt)
    def get_first_name(self):
        return self.element(*self.fname_txt).get_attribute_value('value')

    @Test(lname_txt)
    def get_last_name(self):
        return self.element(*self.lname_txt).get_attribute_value('value')

    @Test(email_txt)
    def get_email(self):
        return self.element(*self.email_txt).get_attribute_value('value')

    # Patient information
    zipcode_txt = (By.ID, "AppUserZip")
    argee_chk = (By.ID, "AppUserTos")
    step1_next = (By.XPATH, "//div[@id='step1']/div[2]/button")

    @Test(zipcode_txt)
    def enter_zip_code(self, zipcode='36445'):
        self.element(*self.zipcode_txt).scroll_element_into_view().clear().type(zipcode)
        return self

    @Test(argee_chk)
    def click_on_argee(self):
        self.element(*self.argee_chk).scroll_element_into_view().click()
        return self

    @Test(step1_next)
    def move_next_patient_from(self):
        self.element(*self.step1_next).scroll_element_into_view().click_and_wait(2)
        return self

    # Patient Form
    step2_next = (By.XPATH, "//div[@id='step2']/div[2]/button")

    @Test(step2_next)
    def move_next_setup_video(self):
        self.element(*self.step2_next).wait_until_present().scroll_element_into_view().click_and_wait(2)
        return self

    # Setup Video
    step3_next = (By.XPATH, "//div[@id='step3']/div[2]/button")

    @Test(step3_next)
    def click_on_complete(self):
        self.element(*self.step3_next).wait_until_present().scroll_element_into_view().click_and_wait(2)
        return self
