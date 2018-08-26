__author__ = 'jacob@vsee.com'

import os, sys
from waiting import wait

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from page.backend.clinic.clinic_page import EligibilityPage
from page.backend.clinic.clinic_page import ClinicPage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.assertions import Assert
from util.setting import _domain


class ClinicSteps(Assert):
    on_clinic_page = ClinicPage()

    # Add new Eligibility
    def view_eligibility(self, domain=_domain):
        self.on_clinic_page \
            .search_clinic(domain=domain) \
            .click_on_view_eligibility()
        return self


class EligibilitySteps(Assert):
    on_eligibility_page = EligibilityPage()

    def creat_new_eligibility(self, eligibility):
        self.eligibility = eligibility
        self.on_eligibility_page.click_on_new_eligibility_button() \
            .enter_first_name(eligibility.firstname) \
            .enter_last_name(eligibility.lastname) \
            .enter_ssn(eligibility.SSN) \
            .enter_dob(eligibility.DOB) \
            .enter_status(eligibility.status[0]) \
            .enter_account_code(eligibility.account_code) \
            .click_on_submit()
        return self

    def should_see_success_alert_message(self):
        self.verifyContainsString('Eligibility created successfully', self.on_eligibility_page.get_alert_message())
        return self

    def search_eligibility(self, value):
        self.on_eligibility_page.enter_search_eligibilities(value)
        return self

    def should_see_eligibility_in_table(self):
        self.search_eligibility(self.eligibility.lastname)
        self.verifyEquals(self.on_eligibility_page.get_account_code(), self.eligibility.account_code)
        self.verifyEquals(self.on_eligibility_page.get_first_name(), self.eligibility.firstname)
        self.verifyEquals(self.on_eligibility_page.get_last_name(), self.eligibility.lastname)
        self.verifyEquals(self.on_eligibility_page.get_dob(), self.eligibility.DOB)
        self.verifyEquals(self.on_eligibility_page.get_snn(), self.eligibility.SSN)
        self.verifyEquals(self.on_eligibility_page.get_status(), self.eligibility.status[1])
        return self

    def delete_eligibility(self, ssn):
        self.search_eligibility(ssn)
        self.on_eligibility_page.click_on_delete_button()
        return self

    def should_see(self, msg):
        self.assertEquals(
            self.on_eligibility_page.get_text_no_matching_records_found(), msg)
        return self
