'''
Created on Jun 10, 2018

@author: Thang Nguyen
'''

import os, sys
from waiting import wait
from time import sleep

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from selenium.webdriver.common.by import By
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../../")
from selenium.webdriver.common.keys import Keys
from webium.clinic_page import ClinicPage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from webium.base_page import Test

class CalendarPage(ClinicPage):
    def __init__(self, ClinicPage):
        self.set_attribute(ClinicPage)
        
    calendar_link = (By.PARTIAL_LINK_TEXT, "Calendar")
    my_schedule_title = (By.XPATH, "//h4[text()='My Schedule']")
    calendar_single_cell = (By.XPATH, "//tr[@class='fc-slot1 fc-minor']/td/div")
    calendar_choose_next_week_btn = (By.XPATH, ".//*[@id='calendar']//span[contains(@class, 'fc-button-next')]")
    calendar_choose_previous_week_btn = (By.XPATH, ".//*[@id='calendar']//span[contains(@class, 'fc-button-prev')]")
    calendar_slot_update_success = (By.XPATH, "//div[@class='alert alert-success fade in' and contains(text(), 'Slot updated successfully.')]")
    calendar_slot_delete_success = (By.XPATH, "//div[@class='alert alert-success fade in' and contains(text(), 'Slot has been deleted successfully.')]")
    calendar_slot_this_day_delete_success = (By.XPATH, "//div[@class='alert alert-success fade in' and contains(text(), "\
                                                        + "'This day's slot in this serie have been deleted successfully.')]")
    calendar_slot_all_series_delete_success = (By.XPATH, "//div[@class='alert alert-success fade in' and contains(text(), "\
                                                        + "'All slots in this serie have been deleted successfully.')]")
    calendar_slot_create_success = (By.XPATH, "//div[@class='alert alert-success fade in' and contains(text(), 'Slots created successfully.')]")
    calendar_created_slot = (By.XPATH, "//div[contains(@class, 'slot')]//div[@class='fc-event-time']")
    
    @Test(calendar_link)
    def click_into_calendar_link(self):
        self.element(*self.calendar_link) \
        .wait_until_clickable() \
        .click()
    
    @Test(calendar_link)
    def wait_visible_of_calendar_link(self):
        self.element(*self.calendar_link) \
        .wait_until_visible()
        sleep(1)
    
    @Test(my_schedule_title)
    def wait_visible_of_calendar_title(self):
        self.element(*self.my_schedule_title) \
        .wait_until_visible()
        sleep(1)
    
    @Test(calendar_single_cell)
    def click_into_a_single_cell(self):
        self.element(*self.calendar_single_cell) \
        .wait_until_clickable() \
        .click()
    
    @Test(calendar_choose_next_week_btn)
    def move_to_next_week(self):
        self.element(*self.calendar_choose_next_week_btn) \
        .wait_until_clickable() \
        .click()
    
    @Test(calendar_choose_previous_week_btn)
    def move_to_previous_week(self):
        self.element(*self.calendar_choose_previous_week_btn) \
        .wait_until_clickable() \
        .click()
    
    # slot_info = ["07", "30", "08", "15"] including start time and end time of slot
    @Test()
    def wait_until_single_cell_slot_on_calendar(self, slot_info, provider_name, clinic_name):
        slot_time = str.lstrip(slot_info[0], "0") + ":" + slot_info[1]  # e.g: 7:00
        
        xpath = "//div[contains(text(),'{0} - {1}') and contains(text(), '{2}')]".format(slot_time, provider_name, clinic_name)
        self.info("Wait for element of single cell slot. LOCATOR: XPATH, {0}".format(xpath))
        self.element(By.XPATH, xpath) \
        .wait_until_visible() \
        .scroll_element_into_view()
    
    # slot_info = ["07", "30", "08", "15"] including start time and end time of slot
    @Test()
    def wait_until_multi_cell_slot_on_calendar(self, slot_info, provider_name, clinic_name):
        slot_time = str.lstrip(slot_info[0], "0") + ":" + slot_info[1] + ' - ' \
         + str.lstrip(slot_info[2], "0") + ':' + slot_info[3]  # e.g: 7:00 - 7:45
        
        xpath = "//div[text()='{0}']/following-sibling::div[contains(string(),'{1}') and contains(string(),'{2}')]" \
        .format(slot_time, provider_name, clinic_name)

        self.info("Wait for element of multi cell slot. LOCATOR: XPATH, {0}".format(xpath))
        self.element(By.XPATH, xpath) \
        .wait_until_visible() \
        .scroll_element_into_view()
    
    # slot_info = ["07", "30", "08", "15"] including start time and end time of slot
    @Test()
    def wait_deleted_single_cell_slot_is_removed(self, slot_info, provider_name, clinic_name):
        slot_time = str.lstrip(slot_info[0], "0") + ":" + slot_info[1]  # e.g: 7:00
        
        xpath = "//div[contains(text(),'{0} - {1}') and contains(text(), '{2}')]".format(slot_time, provider_name, clinic_name)
        self.info("Wait for element of single cell slot is removed from calendar. LOCATOR: XPATH, {0}".format(xpath))
        self.element(By.XPATH, xpath) \
        .wait_until_invisible()
    
    # slot_info = ["07", "30", "08", "15"] including start time and end time of slot
    @Test()
    def wait_deleted_multi_cell_slot_is_removed(self, slot_info, provider_name, clinic_name):
        slot_time = str.lstrip(slot_info[0], "0") + ":" + slot_info[1] + ' - ' \
         + str.lstrip(slot_info[2], "0") + ':' + slot_info[3]  # e.g: 7:00 - 7:45
        
        xpath = "//div[text()='{0}']/following-sibling::div[contains(string(),'{1}') and contains(string(),'{2}')]" \
        .format(slot_time, provider_name, clinic_name)

        self.info("Wait for element of multi cell slot is removed from calendar. LOCATOR: XPATH, {0}".format(xpath))
        self.element(By.XPATH, xpath) \
        .wait_until_invisible()
        
    # slot_info = ["07", "30", "08", "15"] including start time and end time of slot
    @Test()
    def click_into_created_single_cell_slot(self, slot_info, provider_name, clinic_name):
        slot_time = str.lstrip(slot_info[0], "0") + ":" + slot_info[1]  # e.g: 7:00
        
        xpath = "//div[contains(text(),'{0} - {1}') and contains(text(), '{2}')]".format(slot_time, provider_name, clinic_name)
        self.info("Click into single cell slot. LOCATOR: XPATH, {0}".format(xpath))
        self.element(By.XPATH, xpath) \
        .wait_until_clickable() \
        .click()
    
    # slot_info = ["07", "30", "08", "15"] including start time and end time of slot
    @Test()
    def click_into_created_multi_cell_slot(self, slot_info, provider_name, clinic_name):
        slot_time = str.lstrip(slot_info[0], "0") + ":" + slot_info[1] + ' - ' \
         + str.lstrip(slot_info[2], "0") + ':' + slot_info[3]  # e.g: 7:00 - 7:45
        
        xpath = "//div[text()='{0}']/following-sibling::div[contains(string(),'{1}') and contains(string(),'{2}')]" \
        .format(slot_time, provider_name, clinic_name)
        self.info("Click into multi cell slot. LOCATOR: XPATH, {0}".format(xpath))
        self.element(By.XPATH, xpath) \
        .wait_until_clickable() \
        .click()
    
    # slot_info = ["07", "30", "08", "15"] including start time and end time of slot
    # 15 mins appointment
    @Test()
    def click_into_single_cell_appointment(self, slot_info, patient_name):
        slot_time = str.lstrip(slot_info[0], "0") + ":" + slot_info[1]  # e.g: 7:00
        
        xpath = "//div[contains(text(),'{0} - {1}')]".format(slot_time, patient_name)
        self.info("Click into appointment. LOCATOR: XPATH, {0}".format(xpath))
        self.element(By.XPATH, xpath) \
        .wait_until_clickable() \
        .click()
    
    # slot_info = ["07", "30", "08", "15"] including start time and end time of slot
    # 15 mins appointment
    @Test()
    def wait_until_single_cell_appointment_on_calendar(self, slot_info, patient_name):
        slot_time = str.lstrip(slot_info[0], "0") + ":" + slot_info[1]  # e.g: 7:00
        
        xpath = "//div[contains(text(),'{0} - {1}')]".format(slot_time, patient_name)
        self.info("Wait for new appointment on calendar. LOCATOR: XPATH, {0}".format(xpath))
        self.element(By.XPATH, xpath) \
        .wait_until_visible() \
        .scroll_element_into_view()
    
    # slot_info = ["07", "30", "08", "15"] including start time and end time of slot
    # 15 mins appointment
    @Test()
    def wait_until_canceled_single_cell_appointment_is_removed(self, slot_info, patient_name):
        slot_time = str.lstrip(slot_info[0], "0") + ":" + slot_info[1]  # e.g: 7:00
        
        xpath = "//div[contains(text(),'{0} - {1}')]".format(slot_time, patient_name)
        self.info("Wait for canceled appointment is removed from calendar. LOCATOR: XPATH, {0}".format(xpath))
        self.element(By.XPATH, xpath) \
        .wait_until_invisible()
        
    # slot_info = ["07", "30", "08", "15"] including start time and end time of slot
    # More than 15 mins appointment
    @Test()
    def click_into_multi_cell_appointment(self, slot_info, patient_name):
        slot_time = str.lstrip(slot_info[0], "0") + ":" + slot_info[1] + ' - ' \
         + str.lstrip(slot_info[2], "0") + ':' + slot_info[3]  # e.g: 7:00 - 7:45
        
        xpath = "//div[text()='{0}']/following-sibling::div[contains(string(),'{1}')]" \
        .format(slot_time, patient_name)
        self.info("Click into appointment. LOCATOR: XPATH, {0}".format(xpath))
        self.element(By.XPATH, xpath) \
        .wait_until_clickable() \
        .click()
    
    # slot_info = ["07", "30", "08", "15"] including start time and end time of slot
    # More than 15 mins appointment
    @Test()
    def wait_until_multiple_cell_appointment_on_calendar(self, slot_info, patient_name):
        slot_time = str.lstrip(slot_info[0], "0") + ":" + slot_info[1] + ' - ' \
         + str.lstrip(slot_info[2], "0") + ':' + slot_info[3]  # e.g: 7:00 - 7:45
        
        xpath = "//div[text()='{0}']/following-sibling::div[contains(string(),'{1}')]" \
        .format(slot_time, patient_name)
        self.info("Wait for new appointment on calendar. LOCATOR: XPATH, {0}".format(xpath))
        self.element(By.XPATH, xpath) \
        .wait_until_visible() \
        .scroll_element_into_view()
    
    # slot_info = ["07", "30", "08", "15"] including start time and end time of slot
    # More than 15 mins appointment
    @Test()
    def wait_until_canceled_multiple_cell_appointment_is_removed(self, slot_info, patient_name):
        slot_time = str.lstrip(slot_info[0], "0") + ":" + slot_info[1] + ' - ' \
         + str.lstrip(slot_info[2], "0") + ':' + slot_info[3]  # e.g: 7:00 - 7:45
        
        xpath = "//div[text()='{0}']/following-sibling::div[contains(string(),'{1}')]" \
        .format(slot_time, patient_name)
        self.info("Wait for canceled appointment is removed from calendar. LOCATOR: XPATH, {0}".format(xpath))
        self.element(By.XPATH, xpath) \
        .wait_until_invisible()
        
    @Test(calendar_slot_create_success)
    def wait_visible_of_slot_created_success_text(self):
        self.element(*self.calendar_slot_create_success) \
        .wait_until_visible()
    
    @Test(calendar_slot_update_success)
    def wait_visible_of_slot_update_success_text(self):
        self.element(*self.calendar_slot_update_success) \
        .wait_until_visible()
    
    @Test(calendar_slot_delete_success)
    def wait_visible_of_slot_delete_success_text(self):
        self.element(*self.calendar_slot_delete_success) \
        .wait_until_visible()
    
    @Test(calendar_slot_this_day_delete_success)
    def wait_visible_of_slot_delete_this_day_success_text(self):
        self.element(*self.calendar_slot_this_day_delete_success) \
        .wait_until_visible()
    
    @Test(calendar_slot_all_series_delete_success)
    def wait_visible_of_slot_delete_all_series_success_text(self):
        self.element(*self.calendar_slot_all_series_delete_success) \
        .wait_until_visible()
    
    @Test(calendar_created_slot)
    def click_into_created_slot_on_calendar(self):
        self.element(*self.calendar_created_slot) \
        .wait_until_clickable() \
        .scroll_element_into_view() \
        .click()
        
    # ActionTypeModel
    action_type_model = (By.ID, "ActionTypeModel")
    action_type_schedule_appt_button = (By.ID, "ActionTypeScheduleAppt")
    action_type_create_slot_button = (By.ID, "ActionTypeCreateSlots")
    
    @Test(action_type_model)
    def wait_visible_of_action_type_modal(self):
        self.element(*self.action_type_model) \
        .wait_until_visible()
        sleep(1)
    
    @Test(action_type_create_slot_button)
    def click_into_create_slot_button(self):
        self.element(*self.action_type_create_slot_button) \
        .wait_until_clickable() \
        .click()
    
    @Test(action_type_schedule_appt_button)
    def click_into_schedule_appointment_button(self):
        self.element(*self.action_type_schedule_appt_button) \
        .wait_until_clickable() \
        .click()
    
    # slot add modal
    create_slot_modal = (By.ID, "SlotAddModal")
    create_slot_when_date = (By.NAME, "slot_date_start")
    create_slot_start_time  = (By.XPATH, "//label[text()='When:']/following-sibling::div[2]//span[@class='select2-arrow']")
    create_slot_end_time = (By.XPATH, "//label[text()='When:']/following-sibling::div[3]//span[@class='select2-arrow']")
    create_slot_add_btn = (By.ID, "SlotAddButton")
    # For editing slot
    edit_slot_update_btn = (By.ID, "SlotUpdateButton")
    edit_slot_delete_btn = (By.ID, "SlotDeleteButton")
    
    @Test(create_slot_modal)
    def wait_visible_of_create_slot_modal(self):
        self.element(*self.create_slot_modal) \
        .wait_until_visible()
        sleep(1)
    
    # slot_date mm/dd/yyyy
    @Test(create_slot_when_date)
    def type_slot_date(self, slot_date):
        self.element(*self.create_slot_when_date) \
        .wait_until_clickable() \
        .click()
        sleep(0.5)
        self.clear()
        sleep(0.5)
        self.type(slot_date + Keys.ENTER)
        sleep(0.5)
    
    @Test(create_slot_start_time)
    def select_start_time(self, start_time):
        self.element(*self.create_slot_start_time) \
        .wait_until_clickable() \
        .click()
        sleep(1)
        self.send_keys_active_elem(start_time + Keys.ENTER)
    
    @Test(create_slot_end_time)
    def select_end_time(self, end_time):
        self.element(*self.create_slot_end_time) \
        .wait_until_clickable() \
        .click()
        sleep(1)
        self.send_keys_active_elem(end_time + Keys.ENTER)
    
    @Test(create_slot_add_btn)
    def click_into_confirm_new_slot(self):
        self.element(*self.create_slot_add_btn) \
        .wait_until_clickable() \
        .click()
    
    @Test(edit_slot_update_btn)
    def click_into_update_button(self):
        self.element(*self.edit_slot_update_btn) \
        .wait_until_clickable() \
        .click()
    
    @Test(edit_slot_delete_btn)
    def click_into_delete_slot_button(self):
        self.element(*self.edit_slot_delete_btn) \
        .wait_until_clickable() \
        .click()
    
    # Slot view modal 
    slot_view_modal = (By.ID, 'SlotViewModal')
    slot_view_date = (By.ID, 'SlotViewDate')
    slot_view_time = (By.ID, "SlotViewTime")
    slot_view_edit_btn = (By.ID, "SlotViewEdit")
    
    @Test(slot_view_modal)
    def wait_visible_of_slot_view_modal(self):
        self.element(*self.slot_view_modal) \
        .wait_until_visible()
        sleep(1)
    
    @Test(slot_view_date)
    def verify_slot_date(self, slot_date):
        element_text = self.element(*self.slot_view_date) \
        .wait_until_visible() \
        .get_text_by_innerhtml()
        if not element_text == slot_date:
            raise
    
    # slot_time = 07:00 AM - 07:15 AM
    @Test(slot_view_time)
    def verify_slot_time(self, slot_time):
        element_text = self.element(*self.slot_view_time) \
        .wait_until_visible() \
        .get_text_by_innerhtml()
        if not element_text == slot_time:
            raise
    
    @Test(slot_view_edit_btn)
    def click_into_edit_slot_button(self):
        self.element(*self.slot_view_edit_btn) \
        .click()
    
    # create new appointment modal
    new_appointment_title = (By.XPATH, "//span[text()='New Appointment']")
    new_appointment_inperson = (By.XPATH, "//label[contains(string(), 'In Person')]")
    new_appointment_phone = (By.XPATH, "//label[contains(string(), 'Phone')]")
    new_appointment_video = (By.XPATH, "//label[contains(string(), 'Video')]")
    new_appointment_now = (By.XPATH, "//label[contains(string(), 'Now')]")
    new_appointment_later = (By.XPATH, "//label[contains(string(), 'later')]")
    new_appointment_date = (By.NAME, "start_date")
    new_appointment_time = (By.XPATH, "//input[contains(@class, 'ScheduleTime')]")
    new_appointment_patient_search_field = (By.CSS_SELECTOR, ".patient-search.form-control")
    new_appointment_patient_search_btn = (By.XPATH, "//div[@id='VisitScheduler']//button[text()='Search']")
    new_appointment_continue_btn = (By.XPATH, "//div[@id='VisitScheduler']//button[contains(text(), 'Continue')]")
    
    @Test(new_appointment_title)
    def wait_visible_of_new_appointment_title(self):
        self.element(*self.new_appointment_title) \
        .wait_until_visible()
        sleep(1)
    
    @Test(new_appointment_inperson)
    def select_visit_type_in_person(self):
        self.element(*self.new_appointment_inperson) \
        .click()
    
    @Test(new_appointment_phone)
    def select_visit_type_phone(self):
        self.element(*self.new_appointment_phone) \
        .click()
    
    @Test(new_appointment_video)
    def select_visit_type_video(self):
        self.element(*self.new_appointment_video) \
        .click()
    
    @Test(new_appointment_now)
    def choose_date_time_now(self):
        self.element(*self.new_appointment_now) \
        .click()
    
    @Test(new_appointment_later)
    def choose_date_time_late(self):
        self.element(*self.new_appointment_later) \
        .click()
    
    @Test()
    def select_visit_option_by_description(self, description):
        xpath = "//span[text()='{0}']/../preceding-sibling::td/input".format(description)
        self.element(By.XPATH, xpath) \
        .wait_until_clickable() \
        .click()
    
    # slot_date mm/dd/yyyy
    @Test(new_appointment_date)
    def type_appointment_date(self, appointment_date):
        self.element(*self.new_appointment_date) \
        .wait_until_clickable() \
        .click()
        sleep(0.5)
        self.clear()
        sleep(0.5)
        self.type(appointment_date + Keys.ENTER)
        sleep(0.5)
    
    @Test(new_appointment_time)
    def type_appointment_time(self, appointment_time):
        self.element(*self.new_appointment_time) \
        .click()
        sleep(0.5)
        self.clear()
        sleep(0.5)
        self.type(appointment_time + Keys.ENTER)
        sleep(0.5)
    
    @Test(new_appointment_patient_search_field)
    def type_patient_email_into_search_field(self, patient_email):
        self.element(*self.new_appointment_patient_search_field) \
        .clear() \
        .type(patient_email)
    
    @Test(new_appointment_patient_search_btn)
    def click_into_search_patient_button(self):
        self.element(*self.new_appointment_patient_search_btn) \
        .click()
    
    @Test()
    def select_patient_by_email(self, patient_email):
        xpath = "//td[text()='{0}']".format(patient_email)
        self.element(By.XPATH, xpath) \
        .wait_until_visible() \
        .click()
    
    @Test()
    def remove_selected_patient(self, patient_email):
        xpath = "//button[contains(@data-bind, 'removeMember') and contains(string(), '{0}')]".format(patient_email)
        self.element(By.XPATH, xpath) \
        .wait_until_visible() \
        .click()
    
    @Test(new_appointment_continue_btn)
    def click_into_continue_button(self):
        self.element(*self.new_appointment_continue_btn) \
        .click()
    
    # confirm new appointment
    confirm_appointment_title = (By.XPATH, "//h4[text()='Confirm New Appointment']")
    confirm_appointment_confirm_btn = (By.XPATH, ".//*[@id='VisitScheduler']//button[contains(text(), 'Confirm')]")
    
    @Test(confirm_appointment_title)
    def wait_visible_of_confirm_new_appointment_title(self):
        self.element(*self.confirm_appointment_title) \
        .wait_until_visible()
        sleep(1)
    
    @Test(confirm_appointment_confirm_btn)
    def click_into_confirm_new_appointment(self):
        self.element(*self.confirm_appointment_confirm_btn) \
        .click()
    
    @Test()
    def verify_new_appointment_details(self, visit_type, description, date_time, patient_name):
        self.info("Verify visit type: {}".format(visit_type))
        xpath = "//div[contains(@class, 'VisitSchedulerConfirmModel')]" \
        + "//*[text()='Visit Type']/following-sibling::dd[text()='{0}']".format(visit_type)
        self.element(By.XPATH, xpath).wait_until_visible()
        
        self.info("Verify visit options: {}".format(description))
        xpath = "//div[contains(@class, 'VisitSchedulerConfirmModel')]" \
        + "//*[text()='Visit Option']/following-sibling::dd[text()='{0}']".format(description)
        self.element(By.XPATH, xpath).wait_until_visible()
        
        self.info("Verify date and time: {0}".format(date_time))
        xpath = "//div[contains(@class, 'VisitSchedulerConfirmModel')]" \
        + "//*[text()='Date & Time']/following-sibling::dd/span[text()='{0}']".format(date_time)
        self.element(By.XPATH, xpath).wait_until_visible()
        
        self.info("Verify patient name: {0}".format(patient_name))
        xpath = "//div[contains(@class, 'VisitSchedulerConfirmModel')]" \
        + "//*[text()='Date & Time']/following-sibling::dd/a[text()='{0}']".format(patient_name)
        self.element(By.XPATH, xpath).wait_until_visible()
    
    @Test()
    def accept_review_new_visit_alert(self):
        self.accept_alert("Are you going to review this visit now?")
    
    @Test()
    def dismiss_review_new_visit_alert(self):
        self.dismiss_alert("Are you going to review this visit now?")
    
    # Appointment details
    appointment_details_modal = (By.ID, "VisitDetailModal")
    appointment_details_cancel_btn = (By.XPATH, ".//*[@id='VisitDetailModal']//button[contains(text(), 'Cancel')]")
    appointment_details_edit_btn = (By.XPATH, ".//*[@id='VisitDetailModal']//button[text()='Edit']")
    
    @Test(appointment_details_modal)
    def wait_visible_of_appointment_details_modal(self):
        self.element(*self.appointment_details_modal) \
        .wait_until_visible()
        sleep(1)
    
    @Test(appointment_details_cancel_btn)
    def click_into_cancel_appointment_button(self):
        self.element(*self.appointment_details_cancel_btn) \
        .click()
    
    @Test()
    def accept_cancel_appointment_alert(self):
        self.accept_alert("Are you sure to cancel?")
    
    @Test(appointment_details_edit_btn)
    def click_into_edit_appointment_button(self):
        self.element(*self.appointment_details_edit_btn) \
        .click()
        
    # Update slot
    update_slot_title = (By.XPATH, "//h4[text()='Update slot']")
    update_slot_update_button = (By.ID, "SlotUpdateButton")
    update_slot_delete_this_slot_button = (By.ID, "SlotDeleteButton")
    update_slot_delete_slot_dropdown = (By.ID, "SlotGroupDeleteButton")
    update_slot_delete_this_day_button = (By.ID, "SlotGroupDeleteTodayButton")
    update_slot_delete_series_button = (By.ID, "SlotGroupDeleteAllButton")
    
    @Test(update_slot_title)
    def wait_visible_of_update_slot_title(self):
        self.element(*self.update_slot_title) \
        .wait_until_visible()
        sleep(1)
    
    @Test(update_slot_delete_this_slot_button)
    def click_into_delete_this_slot_button(self):
        self.element(*self.update_slot_delete_this_slot_button) \
        .click()
    
    @Test(update_slot_update_button)
    def click_into_update_slot_button(self):
        self.element(*self.update_slot_update_button) \
        .click()
    
    @Test(update_slot_delete_slot_dropdown)
    def click_into_delete_slot_dropdown(self):
        self.element(*self.update_slot_delete_slot_dropdown) \
        .click()
    
    @Test(update_slot_delete_this_day_button)
    def click_into_delete_only_this_day_slot(self):
        self.element(*self.update_slot_delete_this_day_button) \
        .wait_until_clickable() \
        .click()
    
    @Test(update_slot_delete_series_button)
    def click_into_delete_all_slots_in_this_series(self):
        self.element(*self.update_slot_delete_series_button) \
        .wait_until_clickable() \
        .click()