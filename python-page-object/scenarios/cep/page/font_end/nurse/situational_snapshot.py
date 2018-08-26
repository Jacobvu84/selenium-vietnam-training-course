__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webium.base_page import BasePage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.logger import Test


class SituationalPage(BasePage):
    reason_for_visit = (By.XPATH, "//*[text()='Reason for visit']/following-sibling::input")
    patientinby_name = (By.NAME, 'patientinby_name')
    patientinby_phone = (By.NAME, 'patientinby_phone')
    patientinby_relationship = (By.NAME, 'patientinby_relationship')

    @Test(reason_for_visit)
    def enter_reason_for_visit(self, reasons):
        symptoms = reasons.split(",")
        for symptom in symptoms:
            self.element(*self.reason_for_visit).wait_until_clickable() \
                .highlight_element().type(symptom.strip()).type(Keys.ENTER).type(Keys.TAB)
        return self

    @Test(patientinby_name)
    def enter_patientinby_name(self, name):
        self.element(*self.patientinby_name).type(name)
        return self

    @Test(patientinby_phone)
    def enter_patientinby_phone(self, phone):
        self.element(*self.patientinby_phone).type(phone)
        return self

    @Test(patientinby_relationship)
    def enter_relationship_to_patient(self, name):
        self.element(*self.patientinby_relationship).type(name)
        return self

    des_txt = (By.NAME, 'witness_text')

    @Test(des_txt)
    def enter_description(self, description):
        self.element(*self.des_txt).type(description)
        return self

    @Test()
    def choose_threaten_violence(self, option):
        witness_radio = (By.XPATH,
                         "//label[contains(text(),'Did the patient threaten violence, or act violently?')]"
                         "/following-sibling::div//input[@name='witness_violence' and @value='{0}']".format(option))
        self.element(*witness_radio).click()
        return self

    witness_drugs = (By.NAME, 'witness_drugs_who')
    witness_violence = (By.NAME, 'witness_violence_who')

    @Test(witness_drugs)
    def enter_who_witnessed_this(self, person_witnessed):
        self.element(*self.witness_drugs).type(person_witnessed)
        self.element(*self.witness_violence).type(person_witnessed)
        return self

    @Test()
    def choose_overdose(self, option):
        label = "Did the patient take drugs or overdose, or claim to have take drugs or overdose?"
        overdose_radio = (By.XPATH,
                          "//label[contains(text(),'{0}')]"
                          "/following-sibling::div//input[@name='witness_drugs' and @value='{1}']".format(label, option))
        self.element(*overdose_radio).click()
        return self

    @Test()
    def choose_involuntary_psychiatric(self, answer):
        radio = (By.XPATH,
                 "//label[contains(text(),'Is this patient on an involuntary psychiatric hold?')]"
                 "/following-sibling::div//input[@name='patient_hold' and @value='{0}']".format(answer))
        self.element(*radio).click()
        return self

    @Test()
    def choose_criminal_justrice_system(self, answer):
        radio = (By.XPATH,
                 "//input[@name='patient_criminal' and @value='{0}']".format(answer))
        self.element(*radio).click()
        return self

    @Test()
    def choose_influence_of_drug_or_alcohol(self, answer, relevant_test_results):
        radio = (By.XPATH,
                 "//label[contains(text(),'Does the patient appear to be under the influence of drug or alcohol?')]"
                 "/following-sibling::div//input[@name='patient_drug' and @value='{0}']".format(answer))
        self.element(*radio).click()
        if 'Yes' == answer:
            result = (By.NAME, 'patient_drug_testresults')
            self.element(*result).type(relevant_test_results)
        return self
