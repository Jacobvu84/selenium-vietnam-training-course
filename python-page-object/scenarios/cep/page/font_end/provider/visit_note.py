__author__ = 'jacob@vsee.com'

import os, sys
from waiting import wait

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../../../")
from webium.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../../")
from util.logger import Test
from util.rand import feedback_on_patient


class VisitNotePage(BasePage):
    auto_refresh = (By.XPATH, "//button[text()='Save']/following-sibling::button[text()='Saved']")
    search_history = (By.XPATH, "//h4[text()='Visit History']"
                                "/following-sibling::div/div[@id='pastVisits_filter']/label/input")
    edit_visit = (By.XPATH, "//div[@id='visitNotesNav']//a[@data-action='Visit.edit']")

    @Test(auto_refresh)
    def refresh(self):
        self.element(*self.complete_chart).scroll_element_into_view()
        display = self.element(*self.auto_refresh).wait_until_present().size()
        if 1 == display:
            return True

    def wait_refresh_completed(self):
        wait(lambda: self.refresh(), waiting_for='Wait For Refresh complete',
             timeout_seconds=30)

    def scroll_down_page(self):
        self.evaluate_javascript("window.scrollTo(0, document.body.scrollHeight)")
        return self

    @Test(search_history)
    def search_visit_history(self, value):
        self.element(*self.search_history).type(value)
        view_visit = (By.XPATH, "//table[@id='pastVisits']//a[text()='View']")
        self.element(*view_visit).wait_until_clickable().click_and_wait(2)
        return self

    @Test(edit_visit)
    def click_on_edit_visit_note(self):
        # self.element(*self.edit_visit).waitUntilClickable().clickAndWait(5) not work
        self.element(*self.edit_visit).click_and_wait(5)
        return self

    # Chief Complaint
    chief_edit = (By.XPATH, "//strong[text()='Chief Complaint']/following-sibling::a[@title='Edit']")
    desc_text = (By.XPATH, "//label[text()='Choose symptom(s) that best describe the situation']"
                           "/following-sibling::input")
    done_btn = (By.XPATH, "//h4[text()='Chief Complaint']/ancestor-or-self::div[@class='modal-header']"
                          "/following-sibling::div/a")
    chief_update_time = (By.XPATH, "//div[@id='Chief ComplaintList']/span/span[1]")
    chief_update_by = (By.XPATH, "//div[@id='Chief ComplaintList']/span/span[2]")

    checkedItems = (By.XPATH, "//div[@id='Chief ComplaintList']/following-sibling::ul/li")

    @Test(checkedItems)
    def get_chief_complaint(self):
        data = []
        # self.wait_refresh_completed()
        items = self.element(*self.checkedItems).get_text_value().split(",")
        for item in items:
            data.append(item.strip())
        return data

    @Test(chief_edit)
    def edit_chief_complaint(self, names):
        self.element(*self.chief_edit).wait_until_clickable()\
            .scroll_element_into_view() \
            .highlight_element().click()

        values = names.split(",")

        for value in values:
            self.element(*self.desc_text).highlight_element().click().type(value) \
                .type(Keys.ENTER).type_and_wait(Keys.TAB, 1)

        self.element(*self.done_btn) \
            .highlight_element().click_and_wait(1)
        return self

    @Test(chief_edit)
    def remove_chief_complaint(self, value):
        self.element(*self.chief_edit) \
            .scroll_element_into_view() \
            .highlight_element().click()

        remove_items = (By.XPATH, "//div[text()='{0}']/following-sibling::a".format(value))
        self.element(*remove_items).wait_until_clickable().click()

        self.element(*self.done_btn) \
            .highlight_element().click_and_wait(1)
        return self

    @Test(chief_update_time)
    def get_last_update_date_time(self):
        return self.element(*self.chief_update_time).highlight_element().get_text_value()

    @Test(chief_update_by)
    def get_last_update_by(self):
        return self.element(*self.chief_update_by).get_text_value()

    # Past Medical History
    pmh_edit = (By.XPATH, "//strong[text()='Past Medical History']"
                          "/following-sibling::a[@title='Edit']")
    condition_text = (By.XPATH, "//input[@name='condition']"
                                "/following-sibling::div/div/input")
    pmh_add_btn = (By.XPATH, "//label[text()='Other Conditions']"
                             "/ancestor-or-self::form/div//button[text()='Add']")
    pmh_done_btn = (By.XPATH, "//label[text()='Other Conditions']/"
                              "ancestor-or-self::div[@class='modal-body']"
                              "/following-sibling::div[@class='modal-footer']/a[text()='Done']")
    pmh_update_time = (By.XPATH, "//div[@id='Past Medical HistoryList']/span/span[1]")
    pmh_update_by = (By.XPATH, "//div[@id='Past Medical HistoryList']/span/span[3]")

    @Test(pmh_edit)
    def edit_past_medical_history(self, names):
        self.element(*self.pmh_edit).wait_until_clickable().scroll_element_into_view() \
            .highlight_element().click()

        values = names.split(",")

        for value in values:
            self.element(*self.condition_text).wait_until_clickable().highlight_element().click().type(value) \
                .type_and_wait(Keys.ENTER, 1)
            self.element(*self.pmh_add_btn).click()

        self.element(*self.pmh_done_btn) \
            .highlight_element().click_and_wait(1)
        return self

    @Test(pmh_update_time)
    def get_last_update_date_time_of_pmh(self):
        return self.element(*self.pmh_update_time).get_text_value()

    @Test(pmh_update_by)
    def get_last_update_by_of_pmh(self):
        return self.element(*self.pmh_update_by).get_text_value()

    @Test()
    def get_past_medical_history(self):
        """
        Condition:
            //strong[text()='Past Medical History']
            /ancestor::div[@class='table-list-component']
            /following-sibling::div[1]/div[row_index]/div[1]
        By:
            //strong[text()='Past Medical History']
            /ancestor::div[@class='table-list-component']
            /following-sibling::div[1]/div[row_index]/div[2]
        Date Time Update:
            //strong[text()='Past Medical History']
            /ancestor::div[@class='table-list-component']
            /following-sibling::div[1]/div[row_index]/div[3]
        :return:
        """
        root_xpath = "//strong[text()='Past Medical History']" \
                     "/ancestor::div[@class='table-list-component']/following-sibling::div[1]/div"
        xpath_item = (By.XPATH, root_xpath)
        data = []
        items = self.element(*xpath_item).size()
        for item in range(items):
            item = item + 1
            phm_item = (By.XPATH,
                        "{0}[{1}]/div[1]".format(root_xpath, item))
            # self.wait_refresh_completed()
            value = self.element(*phm_item).get_text_value()
            data.append(value)
        return data

    # Allergies
    allergies_edit = (By.XPATH, "//strong[text()='Allergies']/following-sibling::a[@title='Edit']")
    drug_name_text = (By.XPATH, "//input[@name='substance']/following-sibling::div/div/input")
    allergies_add_btn = (By.XPATH, "//label[text()='Name of Drug']/ancestor-or-self::form/div//button[text()='Add']")
    allergies_done_btn = (By.XPATH, "//label[text()='Name of Drug']/"
                                    "ancestor-or-self::div[@class='modal-body']/"
                                    "following-sibling::div[@class='modal-footer']/a[text()='Done']")
    allergies_update_time = (By.XPATH, "//div[@id='AllergiesList']/span/span[1]")
    allergies_update_by = (By.XPATH, "//div[@id='AllergiesList']/span/span[3]")

    @Test(drug_name_text)
    def add_more_allergies(self, value):
        self.element(*self.drug_name_text).wait_until_clickable().highlight_element().click().type(value) \
            .type_and_wait(Keys.ENTER, 1)
        self.element(*self.allergies_add_btn).click()

    @Test(allergies_edit)
    def edit_allergies(self, names):
        self.element(*self.allergies_edit).scroll_element_into_view() \
            .highlight_element().click_and_wait(2)

        values = names.split(",")

        for value in values:
            self.add_more_allergies(value)

        self.element(*self.allergies_done_btn) \
            .highlight_element().click_and_wait(1)
        return self

    @Test(allergies_update_time)
    def get_last_update_date_time_of_allergies(self):
        return self.element(*self.allergies_update_time).wait_a_bit(3).get_text_value()

    @Test(allergies_update_by)
    def get_last_update_by_of_allergies(self):
        return self.element(*self.allergies_update_by).get_text_value()

    @Test()
    def get_allergies(self):
        """
        Condition:
            //strong[text()='Allergies']
            /ancestor::div[@class='table-list-component']
            /following-sibling::div[1]/div[row_index]/div[1]
        By:
            //strong[text()='Allergies']
            /ancestor::div[@class='table-list-component']
            /following-sibling::div[1]/div[row_index]/div[2]
        Date Time Update:
            //strong[text()='Allergies']
            /ancestor::div[@class='table-list-component']
            following-sibling::div[1]/div[row_index]/div[3]
        :return:
        """

        root_xpath = "//strong[text()='Allergies']" \
                     "/ancestor::div[@class='table-list-component']" \
                     "/following-sibling::div[1]/div"
        xpath_item = (By.XPATH, root_xpath)
        data = []
        items = self.element(*xpath_item).size() + 1
        for item in range(1, items):
            allergies_item = (By.XPATH,
                              "{0}[{1}]/div[1]".format(root_xpath, item))
            # self.wait_refresh_completed()
            value = self.element(*allergies_item).get_text_value()
            data.append(value)
        return data

    # Medications
    medications_edit = (By.XPATH, "//strong[text()='Medications']/following-sibling::a[@title='Edit']")
    medications_name_text = (By.XPATH, "//input[@name='name']")
    medications_add_btn = (
        By.XPATH, "//label[text()='Name of Medication']/ancestor-or-self::form/div//button[text()='Add']")
    medications_done_btn = (By.XPATH, "//label[text()='Name of Medication']/"
                                      "ancestor-or-self::div[@class='modal-body']/"
                                      "following-sibling::div[@class='modal-footer']/a[text()='Done']")
    medications_update_time = (By.XPATH, "//div[@id='MedicationsList']/span/span[1]")
    medications_update_by = (By.XPATH, "//div[@id='MedicationsList']/span/span[3]")

    @Test(medications_edit)
    def edit_medications(self, names):
        self.element(*self.medications_edit).scroll_element_into_view() \
            .highlight_element().click()

        values = names.split(",")

        for value in values:
            self.element(*self.medications_name_text).wait_until_clickable().highlight_element().click().type(value) \
                .type_and_wait(Keys.ENTER, 1)
            self.element(*self.medications_add_btn).click()

        self.element(*self.medications_done_btn) \
            .highlight_element().click_and_wait(1)
        return self

    @Test(medications_update_time)
    def get_last_update_date_time_of_medications(self):
        return self.element(*self.medications_update_time).get_text_value()

    @Test(medications_update_by)
    def get_last_update_by_of_medications(self):
        return self.element(*self.medications_update_by).get_text_value()

    @Test()
    def get_medications(self):
        """
        Condition:
            //strong[text()='Medications']
            /ancestor::div[@class='table-list-component']
            /following-sibling::div[1]/div[row_index]/div[1]
        By:
            //strong[text()='Medications']
            /ancestor::div[@class='table-list-component']
            /following-sibling::div[1]/div[row_index]/div[2]
        Date Time Update:
            //strong[text()='Medications']
            /ancestor::div[@class='table-list-component']
            /following-sibling::div[1]/div[row_index]/div[3]
        :return:
        """

        root_xpath = "//strong[text()='Medications']" \
                     "/ancestor::div[@class='table-list-component']" \
                     "/following-sibling::div[1]/div"
        xpath_item = (By.XPATH, root_xpath)
        data = []
        items = self.element(*xpath_item).size()
        for item in range(items):
            item = item + 1
            allergies_item = (By.XPATH,
                              "{0}[{1}]/div[1]".format(root_xpath, item))
            # self.wait_refresh_completed()
            value = self.element(*allergies_item).get_text_value()
            data.append(value)
        return data

    complete_chart = (By.XPATH, "//button[.='Complete chart, sign and send to patient']")

    @Test(complete_chart)
    def click_on_complete_chart(self):
        """The button at bottom-right corner"""
        self.element(*self.complete_chart) \
            .highlight_element().click_and_wait(5)
        return self

    @Test()
    def click_on_completed_visit(self):
        complete_visit = (By.XPATH, "//*[@data-action='Visit.complete_without_notification']")
        self.element(*complete_visit) \
            .highlight_element().click()
        return self

    @Test()
    def click_on_complete_confirm(self):
        complete_confirm = (By.XPATH, "//*[@id='CompleteVisitConfirmationModal']//*[.='Complete without signing']")
        self.element(*complete_confirm) \
            .highlight_element().click()
        return self

    @Test()
    def were_you_comfortable_addressing_the_patients_needs_through_this_platform(self):
        answer = feedback_on_patient(1)
        answer_check = (By.XPATH, "//*[text()='{0}']/preceding-sibling::"
                                  "input[@name='where_you_comfortable']".format(answer))
        status = self.element(*answer_check).wait_until_visible().is_checked()
        if status == None:
            self.element(*answer_check).check().wait_a_bit(1)
        return self

    @Test()
    def did_you_refer_the_patient_for_in_person_care(self):
        answer = feedback_on_patient(2)
        answer_check = (By.XPATH, "//*[text()='{0}']/preceding-sibling::input[@name='did_you_refer']".format(answer))
        status = self.element(*answer_check).wait_until_visible().is_checked()
        if status == None:
            self.element(*answer_check).check().wait_a_bit(1)
            if answer == 'Yes':
                self.why_did_you_refer_for_in_person_patient_care_via_telehealth()
        return self

    @Test()
    def did_you_feel_telehealth_was_an_effective_care_delivery_method_for_this_patient(self):
        answer = feedback_on_patient(2)
        answer_check = (By.XPATH,
            "//label[contains(text(),'Did you feel telehealth was an effective care delivery method for this patient?')]"
            "/following-sibling::div//input[@value='{0}']".format(answer))
        self.element(*answer_check).check().wait_a_bit(1)
        return self

    @Test()
    def was_the_audio_and_video_quality_high(self):
        answer = feedback_on_patient(2)
        answer_check = (By.XPATH,
            "//label[contains(text(),'Was the audio and video quality high?')]"
            "/following-sibling::div//input[@value='{0}']".format(answer))
        self.element(*answer_check).check().wait_a_bit(1)
        return self

    @Test()
    def what_disposition_did_you_recommend_for_this_patient(self, value):
        answer_check = (By.XPATH,
            "//label[contains(text(),'What disposition did you recommend for this patient?')]"
            "/following-sibling::div//input[@value='{0}']".format(value))
        self.element(*answer_check).check().wait_a_bit(1)
        return self

    @Test()
    def was_this_patient_on_a_psychiatric_hold_when_they_were_seen(self):
        answer = feedback_on_patient(2)
        answer_check = (By.XPATH,
                        "//label[contains(text(),'Was this patient on a psychiatric hold when they were seen?')]"
                        "/following-sibling::div//input[@value='{0}']".format(answer))
        self.element(*answer_check).check().wait_a_bit(1)
        if 'Yes' == answer:
            answer = feedback_on_patient(2)
            yes_ch = (By.XPATH,
                            "//label[contains(text(),'If yes, did you recommend the hold be dropped?')]"
                            "/following-sibling::div//input[@value='{0}']".format(answer))
            self.element(*yes_ch).check().wait_a_bit(1)
        else:
            answer = feedback_on_patient(2)
            no_ch = (By.XPATH,
                      "//label[contains(text(),'If no, did you recommend a hold be placed?')]"
                      "/following-sibling::div//input[@value='{0}']".format(answer))
            self.element(*no_ch).check().wait_a_bit(1)
        return self

    @Test()
    def thinking_about_all_aspects_of_this_consult(self, value):
        opinion = (
            By.XPATH,
            "//label[contains(text(),'Thinking about all aspects of this consult')]"
            "/following-sibling::div//input[@name='your_opinion']")
        self.element(*opinion).type(value)
        return self

    def disposition_recommendation(self, value):
        element = (By.XPATH, "//*[text()='Disposition recommendation']"
                             "/following-sibling::input")
        self.element(*element).wait_until_clickable()\
            .highlight_element()\
            .click().type(value) \
            .type_and_wait(Keys.ENTER, 1)
        return self

    @Test()
    def why_did_you_refer_for_in_person_patient_care_via_telehealth(self):
        answer = feedback_on_patient(3)
        answer_check = (By.XPATH, "//*[text()='{0}']/preceding-sibling::"
                                  "input[contains(@name,'what_component_not_adequate')]".format(answer))
        status = self.element(*answer_check).wait_until_visible().is_checked()
        if status == None:
            self.element(*answer_check).check().wait_a_bit(1)
        return self

    @Test()
    def click_on_submit(self):
        submit_btn = (By.XPATH, "//*[@id='ProviderVisitSurvey']//a[text()='Submit']")
        self.element(*submit_btn) \
            .highlight_element().click_and_wait(5)
        return self

    editor_area = (
        By.XPATH, "//label[text()='Plan / Discharge Instructions']"
                  "/following-sibling::div//*[text()='Write a comment']")

    plan_care = (
        By.XPATH, "//label[text()='Plan/Care Instructions']"
                  "/following-sibling::div//*[text()='Write a comment']")

    @Test(editor_area)
    def write_comment_into_editor(self, comment):
        self.element(*self.editor_area).highlight_element().click().wait_a_bit(5)
        self.evaluate_javascript("window.scrollTo(0, document.body.scrollHeight)")
        if 'firefox' == self.get_driver().name:
            self.get_driver().find_element_by_tag_name('body').send_keys(comment)
            self.wait_a_bit(5)
        else:
            self.get_driver().switch_to.active_element.send_keys(comment)
            self.wait_a_bit(5)
        return self

    def active_plan_care_editor_area(self):
        self.element(*self.plan_care).highlight_element().click().wait_a_bit(5)
        return self

    def enter_into_editor(self, value):
        self.evaluate_javascript("window.scrollTo(0, document.body.scrollHeight)")
        if 'firefox' == self.get_driver().name:
            self.get_driver().find_element_by_tag_name('body').send_keys(value)
            self.wait_a_bit(5)
        else:
            self.get_driver().switch_to.active_element.send_keys(value)
            self.wait_a_bit(5)
        return self

    editor_edit = (
        By.XPATH,
        "//label[text()='Plan / Discharge Instructions']"
        "/following-sibling::div//div[@class='note-editing-area']")

    @Test(editor_edit)
    def edit_comment_into_editor(self, comment):
        self.element(*self.editor_edit).highlight_element().click().wait_a_bit(5)
        self.enter_into_editor(comment)
        return self

    header_lounge = (By.XPATH, "//div[@id='ProviderDashboard']//h3[contains(.,'Currently in the Waiting Room')]")

    @Test(header_lounge)
    def is_waiting_room(self):
        return self.element(*self.header_lounge).wait_until_visible().is_present()

    def get_intake_information_by_label(self, label='xxx',label2='xxx'):
        intake_item = (By.XPATH, "//div[@id='examroom-info']//b[contains(text(),'{0}') or contains(text(),'{1}')]"
                                 "/following-sibling::span".format(label, label2))
        return self.element(*intake_item).wait_until_present().get_text_value()

    def get_chief_complaint_intake(self):
        return self.get_intake_information_by_label('Chief Complaint')

    def get_hr_intake(self):
        return self.get_intake_information_by_label('Patient vitals: HR', 'Vital / HR (BPM):')

    def get_bp_intake(self):
        return self.get_intake_information_by_label('Patient vitals: BP', 'Vital / BP (mmHg/mmHg):')

    def get_temp_intake(self):
        return self.get_intake_information_by_label('Patient vitals: Temp', 'Vital / Temp (degree):')

    def get_rr_intake(self):
        return self.get_intake_information_by_label('Patient vitals: RR', 'Vital / RR (BPM)')

    def get_first_name_intake(self):
        return self.get_intake_information_by_label('First Name')

    def get_last_name_intake(self):
        return self.get_intake_information_by_label('Last Name')

    def get_dob_intake(self):
        return self.get_intake_information_by_label('Date of Birth')

    def get_gender_intake(self):
        return self.get_intake_information_by_label('Gender')

    def get_encounter_number_intake(self):
        return self.get_intake_information_by_label('Encounter number (Chart number)')

    def get_medical_number_intake(self):
        return self.get_intake_information_by_label('Medical Record Number')

    def get_insurance_type_intake(self):
        return self.get_intake_information_by_label('Insurance type')

    def get_legal_status_intake(self):
        return self.get_intake_information_by_label('Legal Status')

    def get_SpO2_intake(self):
        return self.get_intake_information_by_label('Vital / SpO2 (%)')

    def get_glucose(self):
        return self.get_intake_information_by_label('Vital / Glucose (mg/dL)')

    def get_date_admission(self):
        return self.get_intake_information_by_label('Date of most recent admission')

    def get_via_telemedicine(self):
        return self.get_intake_information_by_label('This patient has consented to be seen via telemedicine')

    def get_files_uploaded_intake(self):
        intake_item = (By.XPATH, "//div[@id='examroom-info']//b[contains(text(),'Files uploaded for this visit')]"
                                 "/following-sibling::a")
        if self.element(*intake_item).is_present():
            return self.element(*intake_item).wait_until_present().get_text_value()
        else:
            return "No file uploaded"

    def edit_encounter_number(self, value):
        element = (By.XPATH, "//label[text()='Encounter number (Chart number)']/following-sibling::div/input")
        self.element(*element).highlight_element().clear().type(value)
        return self

    def edit_medical_number(self, value):
        element = (By.XPATH, "//label[text()='Medical record number']/following-sibling::div/input")
        self.element(*element).highlight_element().clear().type(value)
        return self

    def edit_insurance_type(self, value):
        element = (By.XPATH, "//label[text()='Insurance type']/following-sibling::div/select")
        self.element(*element).highlight_element().select_option_by_text(value)
        return self

    def edit_csr_input(self, value):
        element = (By.XPATH, "//label[text()='Information for Provider']/following-sibling::div/textarea")
        self.element(*element).highlight_element().type(value)
        return self

    def click_done_button_on_intake(self):
        element = (By.XPATH,
                   "//h4[contains(text(),'Edit Intake')]/ancestor-or-self::div[@class='modal-content']/div[@class='modal-footer']/a")
        self.element(*element).highlight_element().click_and_wait(10)
        return self

    def click_on_edit_button(self):
        element = (By.XPATH, '//div[@id="examroom-info"]/input[@value="Edit"]')
        self.element(*element).highlight_element().click_and_wait(2)
        return self

    @Test()
    def update_intake_information(self, encounter_number, medical_number, information_to_provider="", insurance_type="" ):
        self.click_on_edit_button()
        self.edit_encounter_number(encounter_number)
        self.edit_medical_number(medical_number)
        if "" != insurance_type:
            self.edit_insurance_type(insurance_type)
        if "" != information_to_provider:
            self.edit_csr_input(information_to_provider)
        self.click_done_button_on_intake()
        return self

    @Test()
    def select_consult_type(self,value):
        element = (By.XPATH, "//span[.='{0}']/preceding-sibling::input".format(value))
        self.element(*element).highlight_element().click()
        return self

    history_illness = (By.XPATH,
                       "//*[text()='History of Present Illness']"
                       "/following-sibling::div//div[@class='note-editing-area']")

    @Test(history_illness)
    def enter_history_of_present_illness(self, comment):
        self.element(*self.history_illness).highlight_element().click().wait_a_bit(5)
        self.enter_into_editor(comment)
        return self

    psychiatric_history = (By.XPATH, "//*[text()='Past Psychiatric History']/following-sibling::div//textarea")

    @Test(history_illness)
    def enter_past_psychiatric_history(self, value):
        self.element(*self.psychiatric_history).highlight_element().type(value)
        return self

    def type_by_label(self,label, value):
        element = (By.XPATH, "//*[text()='{0}']/following-sibling::div//input".format(label))
        self.element(*element).highlight_element().type(value)
        return self

    @Test()
    def enter_suicidal_attempts(self, value):
        self.type_by_label('Suicidal Attempts', value)
        return self

    @Test()
    def enter_violence_or_aggression(self, value):
        self.type_by_label('Violence / aggression', value)
        return self

    @Test()
    def enter_in_outpatient_history(self, value):
        self.type_by_label('In / Outpatient history', value)
        return self

    @Test()
    def enter_ect(self, value):
        self.type_by_label('ECT', value)
        return self

    @Test()
    def enter_recovery_program(self, value):
        self.type_by_label('Recovery program', value)
        return self

    @Test()
    def enter_disposition_of_the_patient(self, value):
        element = (By.XPATH, "//*[text()='What was the disposition of the patient?']"
                             "/following-sibling::input")
        self.element(*element).wait_until_clickable()\
            .highlight_element()\
            .click().type(value) \
            .type_and_wait(Keys.ENTER, 1)
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

    def focus_on_tab(self, tab_name):
        tab = (By.XPATH, "//ul[@class='nav nav-tabs']//a[text()='{0}']".format(tab_name))
        self.element(*tab).wait_until_present().click_and_wait(2)
        return self

    def click_on_complete(self):
        complete = (By.XPATH, "//a[@data-action='Visit.complete_without_notification']")
        self.element(*complete).wait_until_present().click_and_wait(2)
        return self

    def confirm_complete_without_notification(self):
        element = (By.XPATH, "//button[@data-bind='click: completeVisitWithoutNotification']")
        self.element(*element).wait_until_present().click_and_wait(2)
        return self