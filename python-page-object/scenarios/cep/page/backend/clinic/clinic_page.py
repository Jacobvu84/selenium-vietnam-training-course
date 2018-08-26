__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webium.base_page import BasePage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.logger import Test

search_txt = (By.XPATH, '//input[@type="search"]')


class EligibilityPage(BasePage):
    new_btn = (By.XPATH, '//a[@data-action="Eligibilities.add"]')
    first_name = (By.NAME, "first_name")
    last_name = (By.NAME, "last_name")
    ssn_field = (By.NAME, "ssn")
    dob_field = (By.NAME, "dob")
    status_field = (By.NAME, "status")
    account_code = (By.NAME, "account_code")
    submit_code = (By.XPATH, "//button[@type='submit']")
    alert_success = (By.XPATH, "//*[contains(text(),'Eligibility created successfully.')]")
    del_button = (By.XPATH, "//a[@data-action='Eligibilities.delete']")
    col_xpath = "//table[@id='eligibility-table']/tbody/tr/td[" \
                "count(//table[@id='eligibility-table']/thead/tr/th[text()='{0}']/preceding-sibling::*)+1]"
    no_record = (By.XPATH, "//*[@id='eligibility-table']//*[@class='dataTables_empty']")

    @Test(new_btn)
    def click_on_new_eligibility_button(self):
        self.element(*self.new_btn).click_and_wait(1)
        return self

    @Test(first_name)
    def enter_first_name(self, fname):
        self.element(*self.first_name).type(fname)
        return self

    @Test(last_name)
    def enter_last_name(self, lname):
        self.element(*self.last_name).type(lname)
        return self

    @Test(ssn_field)
    def enter_ssn(self, ssn):
        self.element(*self.ssn_field).type(ssn)
        return self

    @Test(dob_field)
    def enter_dob(self, dob):
        self.element(*self.dob_field).type(dob)
        return self

    @Test(status_field)
    def enter_status(self, status=1):
        """status 1: active & 0: inactive"""
        self.element(*self.status_field).type(status)
        return self

    @Test(account_code)
    def enter_account_code(self, code):
        self.element(*self.account_code).clear().type(code)
        return self

    @Test(submit_code)
    def click_on_submit(self):
        self.element(*self.submit_code).click_and_wait(3)
        return self

    @Test(alert_success)
    def get_alert_message(self):
        return self.element(*self.alert_success).get_text_value()

    @Test(search_txt)
    def enter_search_eligibilities(self, name):
        self.element(*search_txt).highlight_element().clear() \
            .type(name).type_and_wait(Keys.TAB, 2)
        return self

    @Test(del_button)
    def click_on_delete_button(self):
        self.element(*self.del_button).wait_until_clickable() \
            .highlight_element().click().accept_alert()
        return self

    # Get information on the table room
    def get_text_by_col_name(self, name):
        domain_col = (By.XPATH, self.col_xpath.format(name))
        return self.element(*domain_col).get_text_value()

    def get_account_code(self):
        return self.get_text_by_col_name("Account Code")

    def get_first_name(self):
        return self.get_text_by_col_name("First Name")

    def get_last_name(self):
        return self.get_text_by_col_name("Last Name")

    def get_dob(self):
        return self.get_text_by_col_name("Date of Birth")

    def get_snn(self):
        return self.get_text_by_col_name("SSN")

    def get_status(self):
        return self.get_text_by_col_name("Status")

    @Test(no_record)
    def get_text_no_matching_records_found(self):
        return self.element(*self.no_record).wait_for_text_to_appear('No matching records found').get_text_value()


class ClinicPage(BasePage):
    view_xpath = (By.XPATH, "//a[contains(@href,'/admin/eligibilities/?account_code')]")

    @Test(search_txt)
    def search_clinic(self, domain):
        self.element(*search_txt).clear().type(domain).type_and_wait(Keys.TAB, 3)
        return self

    @Test(view_xpath)
    def click_on_view_eligibility(self):
        self.element(*self.view_xpath).click_and_wait(3)
        return self
