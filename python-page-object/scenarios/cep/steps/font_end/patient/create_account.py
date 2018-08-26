__author__ = 'jacob@vsee.com'

import os, sys, platform
from waiting import wait

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from page.font_end.patient.create_account import CreateAccountPage
from page.font_end.patient.create_account import RegisterPage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from util.assertions import Assert


class CreateAccountSteps(Assert):
    on_create_account_page = CreateAccountPage()

    def create_an_account(self, patient):
        email = patient.split(",")[0]
        f_name = patient.split(",")[1]
        l_name = patient.split(",")[2]
        dob = patient.split(",")[3]
        ssn = patient.split(",")[4]
        account_code = patient.split(",")[5]
        pwd = patient.split(",")[6]

        """dob.split(",")[x]
          - x: 0 - year 
               1 - month
               2 - day
        """
        month = dob.split("-")[1]
        day = dob.split("-")[2]
        year = dob.split("-")[0]

        self.on_create_account_page.enter_first_name(f_name) \
            .enter_last_name(l_name) \
            .select_month(month).enter_day(day).enter_year(year) \
            .enter_ssn(ssn).enter_email(email) \
            .click_on_newsletter() \
            .click_on_submit()
        return self


class RegisterSteps(Assert):
    on_register_page = RegisterPage()

    def set_up_password(self, pwd):
        self.on_register_page.enter_new_password(pwd) \
            .enter_retype_password(pwd)
        return self

    def should_see_default_account_information(self, patient):
        email = patient.split(",")[0]
        f_name = patient.split(",")[1]
        l_name = patient.split(",")[2]
        dob = patient.split(",")[3]
        month = dob.split("-")[1]
        day = dob.split("-")[2]
        year = dob.split("-")[0]

        # verify name, email
        self.verifyEquals(self.on_register_page.get_first_name(), f_name)
        self.verifyEquals(self.on_register_page.get_last_name(), l_name)
        self.verifyEquals(self.on_register_page.get_email(), email)
        """ Pending
        self.assertEquals(self.on_register_page.get_month(), month)
        self.assertEquals(self.on_register_page.get_day(), day)
        self.assertEquals(self.on_register_page.get_year(), year)
        """
        return self

    def complete_patient_information(self):
        """Pending
        self.on_register_page.select_gender(account.gender)\
                             .enter_phone_number(account.phone_number)\
                             .enter_street_address(account.add)\
                             .enter_city(account.city)\
                             .select_states(account.state)\
                             .enter_zip_code(account.zipcode)\
                             .enter_primary_care_physician_name()\
                             .enter_primary_care_physician_phone()
        """
        self.on_register_page.enter_zip_code() \
            .click_on_argee() \
            .move_next_patient_from() \
            .move_next_setup_video() \
            .click_on_complete()

        return self
