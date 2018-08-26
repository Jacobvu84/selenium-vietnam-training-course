__author__ = 'jacob@vsee.com'

import sys, os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from page.font_end.nurse.nurse_page import NursePage
from page.font_end.nurse.contact_infor import ContactInforPage
from page.font_end.nurse.health_infor import PatientHealthInforPage
from page.font_end.nurse.situational_snapshot import SituationalPage
from page.font_end.nurse.menu_bar import MenuBarPage
from steps.patient_steps import PatientHomeSteps

from util.assertions import Assert


class SituationalSteps():
    on_situational_page = SituationalPage()

    def reason_for_visit(self, reasons):
        self.on_situational_page.enter_reason_for_visit(reasons)
        return self

    def who_brought_the_patient_in(self, name, phone, relationship):
        self.on_situational_page \
            .enter_patientinby_name(name) \
            .enter_patientinby_phone(phone) \
            .enter_relationship_to_patient(relationship)
        return self

    def what_did_the_person_witness(self, description, threaten_violence, overdose, person_witnessed):
        self.on_situational_page \
            .enter_description(description) \
            .choose_threaten_violence(threaten_violence) \
            .choose_overdose(overdose) \
            .enter_who_witnessed_this(person_witnessed)
        return self

    def is_this_patient_on_an_involuntary_psychiatric_hold(self, answer):
        self.on_situational_page.choose_involuntary_psychiatric(answer)
        return self

    def is_this_patient_currently_in_the_criminal_justrice_system(self, answer):
        self.on_situational_page.choose_criminal_justrice_system(answer)
        return self

    def does_the_patient_appear_to_be_under_the_influence_of_drug_or_alcohol(self, answer, relevant_test_results):
        self.on_situational_page.choose_influence_of_drug_or_alcohol(answer, relevant_test_results)
        return self


class PatientHealthInforSteps(Assert):
    on_patient_health_infor_page = PatientHealthInforPage()

    def patient_vitals(self, hr, bp, temp, rr, height='', weight='', upload='No', SpO2='', glucose=''):
        self.on_patient_health_infor_page \
            .enter_hr(hr) \
            .enter_bp(bp) \
            .enter_temp(temp) \
            .enter_rr(rr) \
            .enter_height(height) \
            .enter_weight(weight) \
            .enter_spO2(SpO2)\
            .enter_glucose(glucose) \
            .upload(upload, path_file="patient_record.png")
        return self

    def past_medical_history(self, conditions):
        self.on_patient_health_infor_page \
            .click_on_update_past_medical_history()
        values = conditions.split(",")
        for value in values:
            self.on_patient_health_infor_page.click_on_conditions(value.strip())

        self.on_patient_health_infor_page \
            .click_on_cancel_past_medical_history()
        return self

    def should_see_the_past_medical_history_is_updated(self, conditions):
        values = conditions.split(",")
        for value in values:
            self.verifyContainsString(value.strip(), self.on_patient_health_infor_page.get_conditions())
        return self

    def past_surgeries(self, procedures):
        self.on_patient_health_infor_page \
            .click_on_update_past_surgeries()
        values = procedures.split(",")
        for value in values:
            self.on_patient_health_infor_page.click_on_procedures(value.strip())

        self.on_patient_health_infor_page \
            .click_on_cancel_past_surgeries()
        return self

    def should_see_the_past_surgeries_is_updated(self, conditions):
        values = conditions.split(",")
        for value in values:
            self.verifyContainsString(value.strip(), self.on_patient_health_infor_page.get_procedures())
        return self

    def medications(self, names):
        self.on_patient_health_infor_page \
            .click_on_update_medications()
        values = names.split(",")
        for value in values:
            self.on_patient_health_infor_page.enter_medications(value.strip())

        self.on_patient_health_infor_page \
            .click_on_cancel_medications()
        return self

    def should_see_the_medications_is_updated(self, medications):
        values = medications.split(",")
        for value in values:
            self.verifyContainsString(value.strip(), self.on_patient_health_infor_page.get_medications())
        return self

    def allergies(self, drug_name):
        self.on_patient_health_infor_page \
            .click_on_update_allergies()
        values = drug_name.split(",")
        for value in values:
            self.on_patient_health_infor_page.enter_allergies(value.strip())

        self.on_patient_health_infor_page \
            .click_on_cancel_allergies()
        return self

    def should_see_the_allergies_is_updated(self, drug_name):
        values = drug_name.split(",")
        for value in values:
            self.verifyContainsString(value.strip(), self.on_patient_health_infor_page.get_drug_name())
        return self


class ContactInforSteps(Assert):
    on_contact_infor_page = ContactInforPage()

    def add_contact_information(self, option="", ED_facility="",
                                facility_phone_number="",
                                person_requesting_the_call="",
                                nurse_phone_number="",
                                emergency_room_doctor="",
                                doctor_phone_number=""):
        if 'ignore' == option:
            self.click_to_continue()
        else:
            self.verifyEquals(self.on_contact_infor_page.get_ed_facility_name(), ED_facility)
            self.verifyEquals(self.on_contact_infor_page.get_nurse_name(), person_requesting_the_call)
            self.verifyEquals(self.on_contact_infor_page.get_nurse_phone_number(), nurse_phone_number)
            self.on_contact_infor_page \
                .enter_facility_phone_number(facility_phone_number) \
                .enter_emergency_room_doctor(emergency_room_doctor) \
                .enter_doctor_phone_number(doctor_phone_number) \
                .click_on_continue()
        return self

    def click_to_continue(self):
        self.on_contact_infor_page \
            .click_on_continue()
        return self


class MenuBar(Assert):
    on_menu_bar = MenuBarPage()

    def should_see_menu_bar(self, menu):
        items = menu.split(",")
        for item in items:
            self.verifyEquals(self.on_menu_bar.is_item_present(item.strip()), True)
        return self

    def should_see_menu_item_default(self, item):
        self.verifyEquals(self.on_menu_bar.is_menu_active(item), True)
        return self

    def should_contains_menu_item(self, menu):
        items = menu.split(",")
        for item in items:
            self.verifyContainsString(item.strip(), self.on_menu_bar.get_all_menu_items())
        return self


class NurseSteps(ContactInforSteps, SituationalSteps, PatientHealthInforSteps, PatientHomeSteps,
                 MenuBar):
    on_nurse_page = NursePage()

    def enter_patient_information(self, first_name, last_name, dob, gender,
                                  encounter_no="", medical_record_no="", insurance_type=""):
        self.on_nurse_page \
            .enter_first_name_nurse(first_name) \
            .enter_last_name_nurse(last_name) \
            .enter_date_of_birth(dob).select_gender(gender) \
            .enter_encounter_number(encounter_no) \
            .enter_medical_record_number(medical_record_no) \
            .select_insurance_type(insurance_type) \
            .click_on_next()
        return self

    def add_more_patient_information(self, reason_for_visit,
                                           date_of_most_recent_admission='',
                                           principal_diagnosis_upon_admission_to_the_facility=''):
        self.on_nurse_page \
            .enter_date_of_most_recent_admission(date_of_most_recent_admission) \
            .enter_principal_diagnosis_upon_admission_to_the_facility(principal_diagnosis_upon_admission_to_the_facility) \
            .enter_reason_for_visit(reason_for_visit) \
            .click_on_confirm()
        return self

    def please_help_us_improve_our_service_by_answering_the_followin(self, option):
        self.on_nurse_page \
            .choose_option_to_improve(option)\
            .click_on_submit()
        return self

    def account_lookup(self, patient='new'):
        if 'new' == patient:
            self.on_nurse_page \
                .click_on_create_new_patient()
        else:
            self.on_nurse_page \
                .select_patient(name=patient)
        return self

    def create_new_patient_record(self, legal_status):
        self.on_nurse_page \
            .select_legal_status(legal_status)
        return self

    def please_select_a_visit_option(self, visit_option):
        self.on_nurse_page \
            .select_visit_option(visit_option) \
            .click_on_visit_button()
        return self

    def select_the_psychiatrist_to_see_availability(self, provider):
        self.on_nurse_page \
            .select_provider(provider)
        return self

    def pick_an_available_time_slot(self):
        self.time = self.get_time_lost()
        self.pick_an_available_time_slot_for_your_appointment(time=self.time)
        return self

    def should_see_the_chat_button(self, email, provider):
        self.on_nurse_page.wait_for_chat_button_clickable(email, provider)
        self.verifyEquals(self.on_nurse_page.chat_button_is_present(email, provider), True)
        return self

    def should_see_the_exit_button(self):
        self.verifyEquals(self.on_nurse_page.exit_button_is_present(), True)
        return self

    def should_see_notify(self, msg):
        self.verifyContainsString(msg, self.on_nurse_page.get_first_message())
        return self

    def should_see_visit_status(self, msg):
        self.verifyContainsString(msg, self.on_nurse_page.get_visit_status())
        return self

    def start_to_chat_with(self, email, provider):
        self.on_nurse_page.click_on_chat_button(email, provider)
        return self

    def exit_the_appointment(self):
        self.on_nurse_page.click_on_exit_button()
        return self

    def upload_intake_attachment_file(self):
        self.on_nurse_page.upload_attachment(path_file="patient_record.png")
        return self

    # not in use
    def should_see_good_bye(self):
        self.verifyEquals(self.on_nurse_page.get_thanks(), "Thank you. Goodbye!")
        return self