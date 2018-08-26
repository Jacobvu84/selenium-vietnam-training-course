'''
Created on Jun 5, 2018

@author: Thang Nguyen
Steps for admin using
'''

import sys, os
from time import sleep

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from clinic.pages.common.login_page import LoginPage
from clinic.pages.admin.users_page import UsersPage
from clinic.pages.admin.rooms_page import RoomsPage
from webium.clinic_page import ClinicPage


class UsersSteps(ClinicPage):
    def __init__(self, ClinicPage):
        self.users_page = UsersPage(ClinicPage)
        self.set_attribute
        
    def open_users_page(self):
        self.users_page.click_users_link()
        self.users_page.wait_visibile_of_all_users_tab()
        self.users_page.wait_visibile_of_all_users_search_field()
        self.users_page.wait_for_all_users_datatable()
    
    def open_patients_tab(self):
        self.users_page.click_patients_tab()
        self.users_page.wait_visibile_of_patients_search_field()
        self.users_page.wait_for_patients_datatable()

    def open_providers_tab(self):
        self.users_page.click_providers_tab()
        self.users_page.wait_visibile_of_providers_search_field()
        self.users_page.wait_for_provider_datatable()
    
    # Should returns only 1 provider because email is unique
    def search_for_a_provider_by_email(self, provider_email):
        self.users_page.enter_provider_email_into_search(provider_email)
        self.users_page.wait_for_number_of_providers_on_datatable(1)
    
    # Should returns only 1 patient because email is unique
    def search_for_a_patient_by_email(self, patient_email):
        self.users_page.enter_patient_email_into_search(patient_email)
        self.users_page.wait_for_number_of_patients_on_datatable(1)

class RoomsSteps(ClinicPage):
    def __init__(self, ClinicPage):
        self.rooms_page = RoomsPage(ClinicPage)
        
    def open_rooms_page(self):
        self.rooms_page.click_rooms_link()
        self.rooms_page.wait_for_rooms_datatable()
    
    # search for a room only
    def search_for_a_room(self, value):
        self.rooms_page.search_rooms(value)
        self.rooms_page.wait_for_number_of_rooms_on_datatable(1)   # Should returns 1 room only
    
    # provider, rmedic, nurse e.t.c...
    def assign_a_provider_to_room(self, provider_email):
        self.rooms_page.click_into_edit_room()
        self.rooms_page.wait_new_room_modal_shows_up()
        self.rooms_page.assign_provider_to_room(provider_email)
        self.rooms_page.click_on_submit_button()
        self.rooms_page.wait_for_update_room_success_text()
    
    def create_new_room(self, domain, slug, name, code, provider_email=""):
        self.rooms_page.click_into_new_room_button()
        self.rooms_page.wait_new_room_modal_shows_up()
        self.rooms_page.enter_room_domain(domain)
        self.rooms_page.enter_room_slug(slug)
        self.rooms_page.enter_room_name(name)
        self.rooms_page.enter_room_code(code)
        if provider_email != "":
            self.rooms_page.assign_provider_to_room(provider_email)
        self.rooms_page.click_on_submit_button()
        self.rooms_page.wait_for_create_room_success_text()
    
    def delete_room(self):
        self.rooms_page.click_into_delete_room()
        sleep(1)
        self.rooms_page.accept_delete_room_alert()
        self.rooms_page.wait_for_delete_room_success_text()
