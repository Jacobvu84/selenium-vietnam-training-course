'''
Created on Jun 10, 2018

@author: Thang Nguyen
'''

import sys, os
from time import sleep
import datetime
import re

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from webium.clinic_page import ClinicPage
from clinic.pages.provider.dashboard_page import DashboardPage
from clinic.pages.provider.calendar_page import CalendarPage


class CalendarSteps(ClinicPage):
    def __init__(self, ClinicPage):
        self.on_next_week = False
        self.set_attribute(ClinicPage)
        
        self.calendar_page = CalendarPage(ClinicPage)
    
    def open_calendar_page(self):
        self.calendar_page.click_into_calendar_link()
        self.calendar_page.wait_visible_of_calendar_title()
    
    def is_date_on_next_week(self, date_time):
        date = datetime.date.today()
        start_week = date - datetime.timedelta(date.weekday())
        end_week = start_week + datetime.timedelta(7)
        
        date_time = datetime.datetime.strptime(date_time, "%m/%d/%Y").date()
        
        return end_week < date_time
    
    def click_into_created_slot(self, start_date, start_time, end_time, provider_name, clinic_name):
        if self.is_date_on_next_week(start_date):   # Should click to next week incase create slot on next week
            self.calendar_page.move_to_next_week()
            self.on_next_week = True
            
        # Get slot duration. If 15 mins then single cell
        duration = (datetime.datetime.strptime(end_time, "%I:%M %p") - datetime.datetime.strptime(start_time, "%I:%M %p")).seconds/60
        # slot_info = ["07", "30", "08", "15"]
        slot_info = re.findall(r'\d+', start_time + end_time)
        if duration == 15:
            self.info("Click into slot on {0} at {1}".format(start_date, start_time))
            self.calendar_page.click_into_created_single_cell_slot(slot_info, provider_name, clinic_name)
        else:
            self.info("Click into slot on {0} at {1} - {2}".format(start_date, start_time, end_time))
            self.calendar_page.click_into_created_multi_cell_slot(slot_info, provider_name, clinic_name)
        
        self.calendar_page.wait_visible_of_slot_view_modal()
        self.calendar_page.verify_slot_date(start_date)
        
        # Add leading zero to verify slot time
        slot_time = "%02d" % int(start_time.split(":")[0]) + ":" + start_time.split(":")[1] + \
                    " - " + "%02d" % int(end_time.split(":")[0]) + ":" + end_time.split(":")[1]
        self.calendar_page.verify_slot_time(slot_time)
    
    def click_into_created_slot_without_slot_info(self):
        self.calendar_page.click_into_created_slot_on_calendar()
        self.calendar_page.wait_visible_of_slot_view_modal()
    
    def click_into_confirmed_appointment(self, appointment_date, appointment_start, appointment_end, duration, patient_name):
        # slot_info = ["07", "30", "08", "15"]
        slot_info = re.findall(r'\d+', appointment_start + appointment_end)
        if duration == 15:
            self.info("Click into appointment on {0} at {1} of {2}".format(appointment_date, 
                                                                                  appointment_start, 
                                                                                  patient_name))
            self.calendar_page.click_into_single_cell_appointment(slot_info, patient_name)
        else:
            self.info("Click into appointment on {0} at {1} - {2} of {3}".format(appointment_date, 
                                                                                  appointment_start, 
                                                                                  appointment_end,
                                                                                  patient_name))
            self.calendar_page.click_into_multi_cell_appointment(slot_info, patient_name)
        self.calendar_page.wait_visible_of_appointment_details_modal()
        #TODO: appointment details here
    
    def wait_new_created_slot_on_calendar(self, start_time, end_time, provider_name, clinic_name):
        # Get slot duration. If 15 mins then single cell
        duration = (datetime.datetime.strptime(end_time, "%I:%M %p") - datetime.datetime.strptime(start_time, "%I:%M %p")).seconds/60
        # slot_info = ["07", "30", "08", "15"]
        slot_info = re.findall(r'\d+', start_time + end_time)
        if duration == 15:
            self.calendar_page.wait_until_single_cell_slot_on_calendar(slot_info, provider_name, clinic_name)
        else:
            self.calendar_page.wait_until_multi_cell_slot_on_calendar(slot_info, provider_name, clinic_name)
    
    def wait_new_scheduled_appointment_on_calendar(self, appointment_start, appointment_end, duration, patient_name):
        # slot_info = ["07", "30", "08", "15"]
        slot_info = re.findall(r'\d+', appointment_start + appointment_end)
        if duration == 15:
            self.calendar_page.wait_until_single_cell_appointment_on_calendar(slot_info, patient_name)
        else:
            self.calendar_page.wait_until_multiple_cell_appointment_on_calendar(slot_info, patient_name)
    
    # Start on calendar
    def create_slot(self, start_date, start_time, end_time, provider_name, clinic_name, repeat=False, end_date=""):
        self.calendar_page.click_into_a_single_cell()
        self.calendar_page.wait_visible_of_action_type_modal()
        self.calendar_page.click_into_create_slot_button()
        self.calendar_page.wait_visible_of_create_slot_modal()
        self.calendar_page.type_slot_date(start_date)
        self.calendar_page.select_start_time(start_time)
        self.calendar_page.select_end_time(end_time)
        self.calendar_page.click_into_confirm_new_slot()
        self.calendar_page.wait_visible_of_slot_created_success_text()
        
        if self.is_date_on_next_week(start_date):   # Should click to next week incase create slot on next week
            self.calendar_page.move_to_next_week()
            self.on_next_week = True
        
        self.wait_new_created_slot_on_calendar(start_time, end_time, provider_name, clinic_name)
    
    # On view slot modal
    def update_slot(self, start_date, start_time, end_time, provider_name, clinic_name, repeat=False, end_date=""):
        self.calendar_page.click_into_edit_slot_button()
        self.calendar_page.wait_visible_of_update_slot_title()
        self.calendar_page.type_slot_date(start_date)
        self.calendar_page.select_start_time(start_time)
        self.calendar_page.select_end_time(end_time)
        self.calendar_page.click_into_update_slot_button()
        
        self.calendar_page.wait_visible_of_slot_update_success_text()
        
        # Should move to next week if updated slot is on next week and calendar is on current week
        if self.is_date_on_next_week(start_date) and not self.on_next_week:
            self.calendar_page.move_to_next_week()
            self.on_next_week = True
        # Should move to previous week if updated slot is on current week and calendar is on next week
        elif not self.is_date_on_next_week(start_date) and self.on_next_week:
            self.calendar_page.move_to_previous_week()
            self.on_next_week = False
            
        self.wait_new_created_slot_on_calendar(start_time, end_time, provider_name, clinic_name)
    
    # On view slot modal
    def delete_slot(self, start_date, start_time, end_time, provider_name, clinic_name, repeat=False):
        self.calendar_page.click_into_edit_slot_button()
        self.calendar_page.wait_visible_of_update_slot_title()
        if repeat:
            self.calendar_page.click_into_delete_slot_dropdown()
            self.calendar_page.click_into_delete_all_slots_in_this_series()
            self.calendar_page.wait_visible_of_slot_delete_all_series_success_text()
        else:
            self.calendar_page.click_into_delete_slot_button()
            self.calendar_page.wait_visible_of_slot_delete_success_text()
            # Get slot duration. If 15 mins then single cell
            duration = (datetime.datetime.strptime(end_time, "%I:%M %p") - datetime.datetime.strptime(start_time, "%I:%M %p")).seconds/60
            # slot_info = ["07", "30", "08", "15"]
            slot_info = re.findall(r'\d+', start_time + end_time)
            if duration == 15:
                self.calendar_page.wait_deleted_single_cell_slot_is_removed(slot_info, provider_name, clinic_name)
            else:
                self.calendar_page.wait_deleted_multi_cell_slot_is_removed(slot_info, provider_name, clinic_name)
    
    def delete_slot_without_info(self):
        self.calendar_page.click_into_edit_slot_button()
        self.calendar_page.wait_visible_of_update_slot_title()
        self.calendar_page.click_into_delete_slot_button()
        self.calendar_page.wait_visible_of_slot_delete_success_text()
        
    # On calendar
    def open_new_appointment_modal(self):
        self.calendar_page.click_into_a_single_cell()
        self.calendar_page.wait_visible_of_action_type_modal()
        self.calendar_page.click_into_schedule_appointment_button()
        self.calendar_page.wait_visible_of_new_appointment_title()
        
    # On visit details modal
    def cancel_appointment(self, appointment_start, appointment_end, duration, patient_name):
        self.calendar_page.click_into_cancel_appointment_button()
        self.calendar_page.accept_cancel_appointment_alert()
        
        # slot_info = ["07", "30", "08", "15"]
        slot_info = re.findall(r'\d+', appointment_start + appointment_end)
        if duration == 15:
            self.calendar_page.wait_until_canceled_single_cell_appointment_is_removed(slot_info, patient_name)
        else:
            self.calendar_page.wait_until_canceled_multiple_cell_appointment_is_removed(slot_info, patient_name)
