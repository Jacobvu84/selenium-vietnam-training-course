__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from page.font_end.provider.dashboard import DashBoardPage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from util.assertions import Assert
from resource import ODTC


class DashBoardSteps(Assert):
    on_dashboard_page = DashBoardPage()
    odtc = ODTC()

    def select_patient_in_lounge(self, env='cep', index=0):
        """
        Click view button follow patient name
        
        patients[x].split(",")[y]
            x: order of patient in the list
            y: 0 - email
               1 - first name
               2 - last name (fixed)
        """
        if 'cep' == env:
            patients = self.odtc.get_cep_patient()
        elif 'snf' == env:
            patients = self.odtc.get_snf_patient()
        else:
            patients = self.odtc.get_tele_patient()
        f_name = patients[index].split(",")[1]

        self.on_dashboard_page \
            .wait_for_patient_available(f_name) \
            .view_patient_by_name(f_name)
        return self

    def wait_for_patient_on_dashboard(self, name):
        self.on_dashboard_page \
            .wait_for_patient_available(name)
        return self

    def wait_for_patient_getting_ready(self, number='1'):
        self.on_dashboard_page \
            .wait_for_patient_in_getting_ready(number)
        return self

    def wait_for_patient_in_progress(self, number='1'):
        self.on_dashboard_page \
            .wait_for_patient_has_in_progress(number)
        return self


    def should_see_the_patient_info(self, full_name, gender="", dob="", room="", reason=""):
        # tpsych-25:
        self.verifyContainsString(full_name, self.on_dashboard_page.get_full_name())
        if "" != gender:
            self.verifyContainsString(gender, self.on_dashboard_page.get_gender())
        if "" != dob:
            self.verifyContainsString(dob, self.on_dashboard_page.get_dob())
        if "" != room:
            self.verifyContainsString(room, self.on_dashboard_page.get_room_infor())
        if "" != reason:
            self.verifyContainsString(reason, self.on_dashboard_page.get_reason_visit())
        return self

    def should_see_the_intake_attachment_file(self, file_name):
        self.verifyContainsString(file_name, self.on_dashboard_page.get_attachment_file())
        return self

    def should_see_vsee_status_is_online(self, patient):
        self.verifyEquals(self.on_dashboard_page.is_patient_online(patient), True)
        return self

    def should_see_vsee_status_is_offline(self, patient):
        self.verifyEquals(self.on_dashboard_page.is_patient_offline(patient), True)
        return self

    def should_see_vsee_status_is_incall(self, patient):
        self.verifyEquals(self.on_dashboard_page.is_patient_incall(patient), True)
        return self

    def resume(self,patient):
        self.on_dashboard_page.click_on_resume(patient)
        return self

    def should_see_provider_is_online(self, provider):
        self.verifyEquals(self.on_dashboard_page.is_provider_online(provider), True)
        return self

    def select_patient_to_view(self, name):
        self.on_dashboard_page \
            .view_patient_by_name(name)
        return self

    def should_see_the_schedule(self, patients, index):
        f_name = patients[index].split(",")[1]
        l_name = patients[index].split(",")[2]
        full_name = f_name + " " + l_name
        self.verifyContainsString(full_name, self.on_dashboard_page.get_schedule())
        return self

    def should_see_patient_in_waiting_room_at_ready_for_visit_part(self):
        """ If there is View button in the Ready for Visit
        :return: Patient online
        """
        self.on_dashboard_page.wait_for_patient_available("User CEP")
        self.verifyEquals(self.on_dashboard_page.is_view_button_visible(), True)
        return self

    def should_not_see_patient_in_waiting_room(self):
        self.verifyContainsString(
            self.on_dashboard_page.get_visit_empty(), "There are no patients waiting at this time.")

    # Telepsych
    def should_see_section(self, section_name):
        self.verifyEquals(self.on_dashboard_page.is_section_present(section_name), True)
        return self

    def should_see_today_schedule_section(self):
        self.verifyEquals(self.on_dashboard_page.is_today_schedule_section_present(), True)
        return self

    def should_see_create_new_visit_option(self):
        self.verifyEquals(self.on_dashboard_page.is_create_new_visit_button_visible(), True)
        return self

    def should_not_see_the_start_appointment_button(self, patient):
        self.verifyEquals(self.on_dashboard_page.is_start_appointment_button_visible(patient), False)
        return self

    def should_see_the_cancel_button(self, patient):
        self.verifyEquals(self.on_dashboard_page.is_cancel_button_visible(patient), True)
        return self

    def cancel_appointment(self, patient, reason, des):
        self. \
            on_dashboard_page\
            .click_on_cancel_button(patient)\
            .select_the_reason(reason) \
            .enter_description(des) \
            .click_on_yes_to_cancel()
        return self

    def start_appointment_for(self, patient):
        self.on_dashboard_page \
            .click_on_start_appointment_by_name(patient)
        return self

    def resume_appointment_for(self, patient):
        self.on_dashboard_page \
            .click_on_resume_appointment_by_name(patient)
        return self

    def should_not_see_login_button(self):
        self.verifyEquals(self.on_dashboard_page.is_login_button_visible(), False)
        return self

    def should_see_see_a_doctor_now_button(self):
        self.verifyEquals(self.on_dashboard_page.is_see_doctor_now_visible(), True)
        return self

    def should_see_current_number_of_patients_waiting(self, number):
        self.verifyEquals(self.on_dashboard_page.get_current_number_of_patients_waiting(), number)
        return self

    def should_see_room_description(self, room_description):
        self.verifyEquals(self.on_dashboard_page.is_room_description(room_description), True)
        return self

    def see_a_doctor_now(self):
        self.on_dashboard_page.click_on_see_a_doctor_now()
        return self