__author__ = 'jacob@vsee.com'

import os, sys, platform

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from page.font_end.provider.visit_note import VisitNotePage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from util.assertions import Assert
from util.date_time import get_current_datetime
from resource import ODTC


class VisitNoteSteps(Assert):
    on_visit_note_page = VisitNotePage()
    odtc = ODTC()

    def scroll_down_bottom_page(self):
        self.on_visit_note_page.scroll_down_page()
        return self

    def search_visit_history_by_date(self):
        now = get_current_datetime()
        self.on_visit_note_page.search_visit_history(now)
        return self

    def edit_visit_note(self):
        self.on_visit_note_page.click_on_edit_visit_note()

    def should_see_the_reason_for_visit_that_sent_by_patient(self, values):
        # data(Back pain...) is fixed in cepPatientWalkin.py
        chief_complaint = self.on_visit_note_page.get_chief_complaint()
        items = values.split(",")
        for item in items:
            self.verifyContainsString(item.strip(), chief_complaint)
        return self

    def provider_edit_chief_complaint(self, values, env='cep', index=0):
        # chief complaint
        self.on_visit_note_page.edit_chief_complaint(values)
        chief_complaint_update = self.on_visit_note_page.get_chief_complaint()
        date_update = self.on_visit_note_page.get_last_update_date_time()
        by_update = self.on_visit_note_page.get_last_update_by()

        self.verifyContainsString(get_current_datetime(), date_update)
        self.verifyEquals(by_update, self.odtc.get_fullname_provider(env, index=index))
        items = values.split(",")
        for item in items:
            self.verifyContainsString(item.strip(), chief_complaint_update)
        return self

    def provider_remove_chief_complaint(self, value):
        self.on_visit_note_page.remove_chief_complaint(value)
        chief_complaint_rm = self.on_visit_note_page.get_chief_complaint()
        self.assertNotContainsString(value, chief_complaint_rm)
        return self

    def should_see_the_past_medical_history_that_sent_by_patient(self, values):
        # data (Depression...) is fixed in cepPatientWalkin.py
        phm = self.on_visit_note_page.get_past_medical_history()
        items = values.split(",")
        for item in items:
            self.verifyContainsString(item.strip(), phm)
        return self

    def provider_edit_past_medical_history(self, values, env='cep', index=0):
        # Past Medical History
        self.on_visit_note_page.edit_past_medical_history(values)
        pmh_update = self.on_visit_note_page.get_past_medical_history()
        date_update = self.on_visit_note_page.get_last_update_date_time_of_pmh()
        by_update = self.on_visit_note_page.get_last_update_by_of_pmh()

        items = values.split(",")
        for item in items:
            self.verifyContainsString(item.strip(), pmh_update)

        self.verifyContainsString(get_current_datetime(), date_update)
        self.verifyEquals(self.odtc.get_fullname_provider(env=env, index=index), by_update)
        return self

    def should_see_the_allergies_that_sent_by_patient(self, values):
        # data (5HT1 agonist,12 Hour Nasal...) is fixed in cepPatientWalkin.py
        allergies = self.on_visit_note_page.get_allergies()
        items = values.split(",")
        for item in items:
            self.verifyContainsString(item.strip(), allergies)
        return self

    def provider_edit_allergies(self, values, env='cep', index=0):
        # Allergies
        self.on_visit_note_page.edit_allergies(values)

        allergies_update = self.on_visit_note_page.get_allergies()
        date_update = self.on_visit_note_page.get_last_update_date_time_of_allergies()
        by_update = self.on_visit_note_page.get_last_update_by_of_allergies()

        items = values.split(",")
        for item in items:
            self.verifyContainsString(item.strip(), allergies_update)

        self.verifyContainsString(get_current_datetime(), date_update)
        self.verifyEquals(self.odtc.get_fullname_provider(env=env, index=index), by_update)
        return self

    def should_see_the_medications_that_sent_by_patient(self, values):
        # data (Amoxicillin,Paracetamol...) is fixed in cepPatientWalkin.py
        medications = self.on_visit_note_page.get_medications()
        items = values.split(",")
        for item in items:
            self.verifyContainsString(item.strip(), medications)
        # self.on_visit_note_page.edit_medications(values)
        return self

    def provider_edit_medications(self, values, env='cep', index=0):
        # Allergies
        self.on_visit_note_page.edit_medications(values)

        medications_update = self.on_visit_note_page.get_medications()
        date_update = self.on_visit_note_page.get_last_update_date_time_of_medications()
        by_update = self.on_visit_note_page.get_last_update_by_of_medications()

        items = values.split(",")
        for item in items:
            self.verifyContainsString(item.strip(), medications_update)

        self.verifyContainsString(get_current_datetime(), date_update)
        self.verifyEquals(self.odtc.get_fullname_provider(env=env, index=index), by_update)
        return self

    def provider_write_comment_plan_or_discharge_instructions(self, comment):
        self.on_visit_note_page.write_comment_into_editor(comment)
        return self

    def provider_write_comment_plan_or_care_instructions(self, comment):
        self.on_visit_note_page.active_plan_care_editor_area()
        self.on_visit_note_page.enter_into_editor(comment)
        return self

    def provider_edit_comment_plan_or_discharge_instructions(self, comment):
        self.on_visit_note_page.edit_comment_into_editor(comment)
        return self

    def complete__and_sent_visit_to_patient(self):
        self.on_visit_note_page \
            .click_on_complete_chart()
        return self

    def feedback_on_patient(self, env='cep'):
        if 'cep' == env or 'snf' == env:
            self.on_visit_note_page \
                .give_question_that("Please provide feedback on your patient visit?") \
                .then_answers_are() \
                .were_you_comfortable_addressing_the_patients_needs_through_this_platform() \
                .did_you_refer_the_patient_for_in_person_care()
        elif 'tele' == env:
            self.on_visit_note_page \
                .give_question_that("Please provide feedback on your patient visit?") \
                .then_answers_are() \
                .did_you_feel_telehealth_was_an_effective_care_delivery_method_for_this_patient() \
                .was_the_audio_and_video_quality_high()\
                .what_disposition_did_you_recommend_for_this_patient('Community Resource') \
                .was_this_patient_on_a_psychiatric_hold_when_they_were_seen() \
                .thinking_about_all_aspects_of_this_consult('Vsee software is good')
        elif 'neu' == env:
            self.on_visit_note_page \
                .disposition_recommendation('Refer to PCP or specialist')
        else:
            pass
        return self

    def submit(self):
        self.on_visit_note_page.click_on_submit()
        return self

    def should_see_back_to_lounge(self):
        self.verifyEquals(self.on_visit_note_page.is_waiting_room(), True)
        return self

    def should_see_intake_information(self, chief_complaint="", hr="", bp="", temp="", rr="", first_name="",
                                      dob="", gender="", encounter_number="", medical_number="", insurance_type="",
                                      legal_status="", files_uploaded_for_this_visit="", last_name="", glucose='',
                                      date_admission='', SpO2=''):
        if "" != chief_complaint:
            self.verifyEquals(chief_complaint, self.on_visit_note_page.get_chief_complaint_intake())
        if "" != hr:
            self.verifyEquals(hr, self.on_visit_note_page.get_hr_intake())
        if "" != bp:
            self.verifyEquals(bp, self.on_visit_note_page.get_bp_intake())
        if "" != temp:
            self.verifyEquals(temp, self.on_visit_note_page.get_temp_intake())
        if "" != rr:
            self.verifyEquals(rr, self.on_visit_note_page.get_rr_intake())
        if "" != first_name:
            self.verifyEquals(first_name, self.on_visit_note_page.get_first_name_intake())
        if "" != last_name:
            self.verifyEquals(last_name, self.on_visit_note_page.get_last_name_intake())
        if "" != dob:
            self.verifyEquals(dob, self.on_visit_note_page.get_dob_intake())
        if "" != gender:
            self.verifyEquals(gender, self.on_visit_note_page.get_gender_intake())
        if "" != encounter_number:
            self.verifyContainsString(encounter_number, self.on_visit_note_page.get_encounter_number_intake())
        if "" != medical_number:
            self.verifyContainsString(medical_number, self.on_visit_note_page.get_medical_number_intake())
        if "" != insurance_type:
            self.verifyEquals(insurance_type, self.on_visit_note_page.get_insurance_type_intake())
        if "" != legal_status:
            self.verifyEquals(legal_status, self.on_visit_note_page.get_legal_status_intake())
        if "" != SpO2:
            self.verifyEquals(SpO2, self.on_visit_note_page.get_SpO2_intake())
        if "" != glucose:
            self.verifyEquals(glucose, self.on_visit_note_page.get_glucose())
        if "" != date_admission:
            self.verifyEquals(date_admission, self.on_visit_note_page.get_date_admission())
        if "" != files_uploaded_for_this_visit:
            self.verifyEquals(files_uploaded_for_this_visit, self.on_visit_note_page.get_files_uploaded_intake())
        return self

    def edit_intake_information(self, encounter_number, medical_number, information_to_provider="", insurance_type=""):
        self\
            .on_visit_note_page\
            .update_intake_information(encounter_number, medical_number,
                                       insurance_type, information_to_provider)
        return self

    def consult_type(self, types):
        self.on_visit_note_page.select_consult_type(types)
        return self

    def history_of_present_illness(self, value):
        self.on_visit_note_page.enter_history_of_present_illness(value)
        return self

    def past_psychiatric_history(self, value):
        self.on_visit_note_page.enter_past_psychiatric_history(value)
        return self

    def suicidal_attempts(self, value):
        self.on_visit_note_page.enter_suicidal_attempts(value)
        return self

    def violence_or_aggression(self, value):
        self.on_visit_note_page.enter_violence_or_aggression(value)
        return self

    def ECT(self, value):
        self.on_visit_note_page.enter_ect(value)
        return self

    def in_outpatient_history(self, value):
        self.on_visit_note_page.enter_in_outpatient_history(value)
        return self

    def recovery_program(self, value):
        self.on_visit_note_page.enter_recovery_program(value)
        return self

    def what_was_the_disposition_of_the_patient(self, value):
        self.on_visit_note_page.enter_disposition_of_the_patient(value)
        return self

    def has_tab(self, tab_name):
        self.verifyEquals(self.on_visit_note_page.is_tab_active(tab_name), True)
        return self

    def complete_without_notification(self):
        self.on_visit_note_page\
            .click_on_complete()\
            .confirm_complete_without_notification()
        return self
