__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from page.font_end.provider.new_visit import NewVisitPage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from util.assertions import Assert
from util.date_time import get_current_datetime
from resource import ODTC


class NewVisitSteps(Assert):
    on_new_visit_page = NewVisitPage()

    def open_new_visit_form(self):
        self.on_new_visit_page\
            .click_on_new_visit()
        return self

    def create_new_visit(self, room, patient_name, visit_type, visit_option, date_time, encounter_number="",
                               medical_record_no="", insurance_type="", information_to_provider="", date='', time=''):
        self.on_new_visit_page\
            .select_room(room) \
            .select_patient(patient_name)\
            .select_visit_type(visit_type)\
            .select_option(visit_option)\
            .select_date_time(date_time, date, time) \
            .enter_encounter_number(encounter_number) \
            .enter_medical_record_number(medical_record_no) \
            .select_insurance_type(insurance_type) \
            .enter_information_to_provider(information_to_provider) \
            .go_to_continue()
        return self

    def create_visit_with_new_patient(self, room, first_name, last_name, email, gender , dob, visit_type,
                                            visit_option, date_time, encounter_number="", medical_record_no="",
                                            insurance_type="", information_to_provider="", date="", time=""):
        self.on_new_visit_page\
            .select_room(room) \
            .create_new_patient(name = first_name + " " + last_name)\
            .enter_first_name(first_name)\
            .enter_last_name(last_name)\
            .enter_email(email)\
            .select_gender(gender)\
            .enter_date_of_birth(dob) \
            .click_on_create_button() \
            .select_visit_type(visit_type)\
            .select_option(visit_option)\
            .select_date_time(date_time, date, time)\
            .enter_encounter_number(encounter_number)\
            .enter_medical_record_number(medical_record_no)\
            .select_insurance_type(insurance_type)\
            .enter_information_to_provider(information_to_provider) \
            .go_to_continue()
        return self

    def should_see_visit_details(self, visit_type, visit_option, date_time, patient_name,
                                 encounter_number="", medical_record_no="",
                                 insurance_type="", information_to_provider=""):
        self.verifyEquals(self.on_new_visit_page.get_visit_type(), visit_type)
        self.verifyEquals(self.on_new_visit_page.get_visit_option(), visit_option)
        self.verifyContainsString(date_time, self.on_new_visit_page.get_date_time(date_time))
        self.verifyEquals(self.on_new_visit_page.get_patient_name(), patient_name)
        if "" != encounter_number:
            self.verifyEquals(self.on_new_visit_page.get_encounter_number(), encounter_number)
        if "" != medical_record_no:
            self.verifyEquals(self.on_new_visit_page.get_medical_record_number(), medical_record_no)
        if "" != insurance_type:
            self.verifyEquals(self.on_new_visit_page.get_insurance_type(), insurance_type)
        if "" != information_to_provider:
            self.verifyEquals(self.on_new_visit_page.get_information_for_provider(), information_to_provider)
        self.on_new_visit_page.click_on_confirm()
        return self

    def should_see_visit_type(self, types):
        values = types.split(",")
        for value in values:
            self.verifyEquals(self.on_new_visit_page.is_visit_type_present(value.strip()), True)
        return self

    def should_see_visit_type_focus_on(self, value):
        self.verifyEquals(self.on_new_visit_page.is_visit_type_active(value), True)
        return self

    def should_see_date_and_time_type(self, types):
        values = types.split(",")
        for value in values:
            self.verifyEquals(self.on_new_visit_page.is_date_time(value.strip()), True)
        return self

    def should_see_date_and_time_focus_on(self, value):
        self.verifyEquals(self.on_new_visit_page.is_date_time_active(value), True)
        return self

    def go_to_visit_detail_page(self, alert_msg, option):
        """
        :param alert_msg:
        :param option:
            yes: directed to visit detail page
            no: stayed in Dashboard
        """
        self.on_new_visit_page.accept_go_to_detail_page(alert_msg, option)
        return self


