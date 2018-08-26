__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from page.font_end.patient.patient_health import PatientHealthPage
from page.font_end.patient.patient_health import PatientMedicationPage
from page.font_end.patient.patient_health import PatientAllergiePage
from page.font_end.patient.patient_health import PatientMedicalHistoryPage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from util.assertions import Assert


class PatientHealthSteps(Assert):
    on_health_page = PatientHealthPage()

    def select_medications_tab(self):
        self.on_health_page.click_on_medications_tab()
        return self

    def select_allergies_tab(self):
        self.on_health_page.click_on_allergies_tab()
        return self

    def select_medical_history_tab(self):
        self.on_health_page.click_on_medical_history_tab()
        return self

    def has_tab(self, tab_name):
        self.verifyEquals(self.on_health_page.is_tab_active(tab_name), True)
        return self



class PatientMedicationSteps(Assert):
    on_medication_page = PatientMedicationPage()

    def should_see_the_current_medications(self, medications):
        values = medications.split(",")
        for value in values:
            self.verifyContainsString(value, self.on_medication_page.get_current_medications())
        return self

    def remove_medications(self, medications):
        self.on_medication_page.click_on_update_button()
        values = medications.split(",")
        for value in values:
            self.on_medication_page.uncheck_medications(value)
        return self

    def add_medications(self, medications):
        values = medications.split(",")
        for value in values:
            self.on_medication_page.fill_medication(value).click_on_add_button()
        self.on_medication_page.click_on_done()
        return self


class PatientAllergiesSteps(Assert):
    on_allergies_page = PatientAllergiePage()

    def should_see_the_allergies(self, allergies):
        values = allergies.split(",")
        for value in values:
            self.verifyContainsString(value, self.on_allergies_page.get_allergies())
        return self

    def remove_allergies(self, allergies):
        self.on_allergies_page.click_on_update_button()
        values = allergies.split(",")
        for value in values:
            self.on_allergies_page.uncheck_allergy(value)
        return self

    def add_allergies(self, allergies):
        values = allergies.split(",")
        for value in values:
            self.on_allergies_page.fill_allergy(value).click_on_add_button()
        self.on_allergies_page.click_on_done()
        return self


class PatientMedicalHistorySteps(Assert):
    on_medical_history_page = PatientMedicalHistoryPage()

    # Past Medical History
    def should_see_the_past_medical_history(self, diseases):
        values = diseases.split(",")
        for value in values:
            self.verifyContainsString(value, self.on_medical_history_page.get_past_medical_history())
        return self

    def remove_past_medical_history(self, diseases):
        self.on_medical_history_page.click_on_update_past_medical_history()
        values = diseases.split(",")
        for value in values:
            self.on_medical_history_page.uncheck_or_check_disease(value)
        return self

    def add_past_medical_history(self, diseases):
        self.remove_past_medical_history(diseases)
        return self

    def add_other_condition(self, diseases):
        values = diseases.split(",")
        for value in values:
            self.on_medical_history_page.fill_other_conditions(value).click_on_add_past_medical_history()
        self.on_medical_history_page.click_on_done_past_medical_history()
        return self

    # Past Surgeries
    def update_past_surgeries(self, surgeries):
        self.on_medical_history_page.click_on_update_past_surgeries()
        values = surgeries.split(",")
        for value in values:
            self.on_medical_history_page.change_surgeries(value)
        return self

    def add_more_procedure(self, procedures):
        values = procedures.split(",")
        for value in values:
            self.on_medical_history_page.fill_procedure(value).click_on_add_past_surgeries()
        self.on_medical_history_page.click_on_done_past_surgeries()
        return self

    # Family Medical History
    def open_family_medical_check_list(self):
        self.on_medical_history_page.click_on_update_family_medical_history()
        return self

    def close_family_medical_check_list(self):
        self.on_medical_history_page.click_on_done_family_medical_history()
        return self

    def update_mother_medical_history(self, diseases):
        values = diseases.split(",")
        for value in values:
            self.on_medical_history_page.choose_diseases_for_mother(value)
        return self

    def update_father_medical_history(self, diseases):
        values = diseases.split(",")
        for value in values:
            self.on_medical_history_page.choose_diseases_for_father(value)
        return self

    def update_siblings_medical_history(self, diseases):
        values = diseases.split(",")
        for value in values:
            self.on_medical_history_page.choose_diseases_for_siblings(value)
        return self

    def update_maternal_grandparents_medical_history(self, diseases):
        values = diseases.split(",")
        for value in values:
            self.on_medical_history_page.choose_diseases_for_maternal_grandparents(value)
        return self

    def update_paternal_grandparents_medical_history(self, diseases):
        values = diseases.split(",")
        for value in values:
            self.on_medical_history_page.choose_diseases_for_paternal_grandparents(value)
        return self

    def should_see_family_medical_history_is_updated(self, diseases):
        values = diseases.split(",")
        for value in values:
            self.verifyContainsString(value, self.on_medical_history_page.get_family_medical_history())
        return self

    # Social History
    def update_social_history(self, status, level, occupation, kids):
        self.on_medical_history_page.click_on_update_social_history() \
            .enter_martial_status(status) \
            .enter_highest_level_of_education(level) \
            .enter_occupation(occupation) \
            .enter_number_of_children(kids) \
            .click_on_done_social_history()
        return self

    def should_see_social_history_is_updated(self, social_infor):
        values = social_infor.split(",")
        for value in values:
            self.verifyContainsString(value, self.on_medical_history_page.get_social_history())

        return self

    # Health Habits
    def update_health_habits(self, smoking, alcohol, drug, exercise):
        self.on_medical_history_page.click_on_update_health_habits() \
            .select_smoking_frequency(smoking) \
            .select_alcohol_frequency(alcohol) \
            .enter_street_drugs_used(drug) \
            .select_exercise_frequency(exercise) \
            .click_on_done_health_habits()
        return self

    def should_see_health_habits_is_updated(self, habits):
        values = habits.split(",")
        for value in values:
            self.verifyContainsString(value, self.on_medical_history_page.get_health_habits())
