__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../../../")
from webium.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../../")
from util.logger import Test


class PatientHealthPage(BasePage):
    title = (By.XPATH, "//h2[contains(text(), 'My Health')]")
    tab_visitSummaries = (By.PARTIAL_LINK_TEXT, "Visit Summaries")
    tab_appointments = (By.PARTIAL_LINK_TEXT, "My Appointments")
    tab_medical_history = (By.PARTIAL_LINK_TEXT, "Medical History")
    tab_allergies = (By.PARTIAL_LINK_TEXT, "Allergies")

    tab_medications = (By.PARTIAL_LINK_TEXT, "Medications")

    @Test(tab_medications)
    def click_on_medications_tab(self):
        self.element(*self.tab_medications).click()
        return self

    @Test(tab_allergies)
    def click_on_allergies_tab(self):
        self.element(*self.tab_allergies).click()
        return self

    @Test(tab_medical_history)
    def click_on_medical_history_tab(self):
        self.element(*self.tab_medical_history).click()
        return self

    def focus_on_tab(self, tab_name):
        tab = (By.XPATH, "//ul[@class='nav nav-tabs']//a[text()='{0}']".format(tab_name))
        self.element(*tab).wait_until_present().click_and_wait(2)
        return self

    @Test(("Undefined", "Undefined"))
    def is_tab_active(self, tab_name):
        self.focus_on_tab(tab_name)

        active_tab = (By.XPATH, "//ul[@class='nav nav-tabs']//a[text()='{0}']/ancestor-or-self::li".format(tab_name))
        tab_status = self.element(*active_tab).get_attribute_value("class")

        if "active" == tab_status:
            return True
        else:
            return False


class HealthAction(BasePage):
    @Test(("Undefined", "Undefined"))
    def click_on_update_by_name(self, name):
        item_xpath = "//h4[text()='{0}']/a[text()='Update']".format(name)
        item = (By.XPATH, item_xpath)
        self.element(*item).click()

    @Test(("Undefined", "Undefined"))
    def click_on_add_button_by_name(self, name):
        item_xpath = "//h4[text()='{0}']/ancestor-or-self::div[@class='modal-header']/" \
                     "following-sibling::div[@class='modal-body']//button[@data-bind='click: add']".format(name)
        item = (By.XPATH, item_xpath)
        self.element(*item).click()

    @Test(("Undefined", "Undefined"))
    def click_on_done_by_name(self, name):
        item_xpath = "//h4[text()='{0}']/ancestor-or-self::div[@class='modal-header']/" \
                     "following-sibling::div[@class='modal-footer']//a[text()='Done']".format(name)
        item = (By.XPATH, item_xpath)
        self.element(*item).click_and_wait(3)

    @Test(("Undefined", "Undefined"))
    def check_item_by_text(self, value):
        item_xpath = "//td[contains(text(),'{0}')]/preceding-sibling::td/span".format(value)
        item = (By.XPATH, item_xpath)
        self.element(*item).click_and_wait(1)

    def get_all_item_by_id(self, id):
        list_items = (By.XPATH, "//div[@id='{0}']/following-sibling::ul/li".format(id))
        return self.get_text_values(*list_items)

    @Test(("Undefined", "Undefined"))
    def enter_text_filed_by_label(self, value, label):
        input_field = (By.XPATH, "//label[text()='{0}']/following-sibling::div/input".format(label))
        self.element(*input_field).type(value)
        return self


class PatientMedicationPage(HealthAction):
    def get_current_medications(self):
        return self.get_all_item_by_id("Current MedicationsList")

    def fill_medication(self, value):
        self.enter_text_filed_by_label(value, "Name of Medication")
        return self

    def uncheck_medications(self, value):
        self.check_item_by_text(value)
        return self

    def click_on_update_button(self):
        self.click_on_update_by_name("Current Medications")
        return self

    def click_on_add_button(self):
        self.click_on_add_button_by_name("Current Medications")
        return self

    def click_on_done(self):
        self.click_on_done_by_name("Current Medications")
        return self


class PatientAllergiePage(HealthAction):
    drug_field = (By.XPATH, "//label[.='Name of Drug']/following-sibling::div/div/div/input")

    def get_allergies(self):
        return self.get_all_item_by_id("AllergiesList")

    @Test(drug_field)
    def fill_allergy(self, value):
        self.element(*self.drug_field).wait_until_visible() \
            .highlight_element().click().type(value).type(Keys.ENTER)
        return self

    def uncheck_allergy(self, value):
        self.check_item_by_text(value)
        return self

    def click_on_update_button(self):
        self.click_on_update_by_name("Allergies")
        return self

    def click_on_add_button(self):
        self.click_on_add_button_by_name("Allergies")
        return self

    def click_on_done(self):
        self.click_on_done_by_name("Allergies")
        return self


class PatientMedicalHistoryPage(HealthAction):
    # Past Medical History
    def get_past_medical_history(self):
        return self.get_all_item_by_id("Past Medical HistoryList")

    def fill_other_conditions(self, value):
        self.enter_text_filed_by_label(value, "Other Conditions")
        return self

    def uncheck_or_check_disease(self, value):
        self.check_item_by_text(value)
        return self

    def click_on_update_past_medical_history(self):
        self.click_on_update_by_name("Past Medical History")

    def click_on_add_past_medical_history(self):
        self.click_on_add_button_by_name("Past Medical History")
        return self

    def click_on_done_past_medical_history(self):
        self.click_on_done_by_name("Past Medical History")
        return self

    # Past Surgeries
    def check_surgeries_item(self, value):
        self.check_item_by_text(value)
        return self

    def click_on_add_past_surgeries(self):
        self.click_on_add_button_by_name("Past Surgeries")
        return self

    def click_on_done_past_surgeries(self):
        self.click_on_done_by_name("Past Surgeries")
        return self

    def click_on_update_past_surgeries(self):
        self.click_on_update_by_name("Past Surgeries")

    def change_surgeries(self, value):
        self.check_item_by_text(value)
        return self

    def fill_procedure(self, value):
        self.enter_text_filed_by_label(value, "Name of Procedure")
        return self

    # Family Medical History

    def click_on_update_family_medical_history(self):
        self.click_on_update_by_name("Family Medical History")
        return self

    def click_on_done_family_medical_history(self):
        self.click_on_done_by_name("Family Medical History")
        return self

    @Test(("Undefined", "Undefined"))
    def choose_diseases(self, person, value):
        item_xpath = "//label[text()='{0}']/following-sibling::div//input[@value='{1}']".format(value, person)
        item = (By.XPATH, item_xpath)
        self.element(*item).click()

    def choose_diseases_for_mother(self, value):
        self.choose_diseases("Mother", value)
        return self

    def choose_diseases_for_father(self, value):
        self.choose_diseases("Father", value)
        return self

    def choose_diseases_for_siblings(self, value):
        self.choose_diseases("Siblings", value)
        return self

    def choose_diseases_for_maternal_grandparents(self, value):
        self.choose_diseases("Maternal grandparents", value)
        return self

    def choose_diseases_for_paternal_grandparents(self, value):
        self.choose_diseases("Paternal grandparents", value)
        return self

    def get_family_medical_history(self):
        return self.get_all_item_by_id("Family Medical HistoryList")

    # Social History
    def click_on_update_social_history(self):
        self.click_on_update_by_name("Social History")
        return self

    def click_on_done_social_history(self):
        self.click_on_done_by_name("Social History")
        return self

    martial_status = (By.XPATH, "//label[text()='Marital Status']/following-sibling::input")
    education_text = (By.XPATH, "//label[text()='Highest Level of Education']/following-sibling::input")
    occupation_text = (By.NAME, "occupation")
    children_text = (By.NAME, "num_kids")

    @Test(martial_status)
    def enter_martial_status(self, name):
        self.element(*self.martial_status).click()
        self.element(*self.martial_status).type_and_wait(name, 1) \
            .type(Keys.ENTER).type_and_wait(Keys.TAB, 3)
        return self

    @Test(education_text)
    def enter_highest_level_of_education(self, name):
        self.element(*self.education_text).click()
        self.element(*self.education_text).type_and_wait(name, 1) \
            .type(Keys.ENTER).type_and_wait(Keys.TAB, 3)
        return self

    @Test(occupation_text)
    def enter_occupation(self, value):
        self.element(*self.occupation_text).type(value)
        return self

    @Test(children_text)
    def enter_number_of_children(self, value):
        self.element(*self.children_text).type(value)
        return self

    def get_social_history(self):
        return self.get_all_item_by_id("Social HistoryList")

    # Health Habits
    def click_on_update_health_habits(self):
        self.click_on_update_by_name("Health Habits")
        return self

    def click_on_done_health_habits(self):
        self.click_on_done_by_name("Health Habits")
        return self

    def get_health_habits(self):
        return self.get_all_item_by_id("Health HabitsList")

    smoking_frequency = (By.NAME, "smoking")
    alcohol_frequency = (By.NAME, "alcohol")
    drugs_frequency = (By.NAME, "drugs")
    exercise_frequency = (By.NAME, "exercise")

    @Test(smoking_frequency)
    def select_smoking_frequency(self, frequency):
        self.element(*self.smoking_frequency).select_option_by_text(frequency)
        return self

    @Test(alcohol_frequency)
    def select_alcohol_frequency(self, frequency):
        self.element(*self.alcohol_frequency).select_option_by_text(frequency)
        return self

    @Test(drugs_frequency)
    def enter_street_drugs_used(self, drug):
        self.element(*self.drugs_frequency).type(drug)
        return self

    @Test(exercise_frequency)
    def select_exercise_frequency(self, frequency):
        self.element(*self.exercise_frequency).select_option_by_text(frequency)
        return self
