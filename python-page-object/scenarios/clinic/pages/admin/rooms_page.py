'''
Created on Jun 4, 2018

@author: Thang Nguyen
Including locators for Rooms page on admin
Including actions 
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


class RoomsPage(ClinicPage):
    def __init__(self, ClinicPage):
        self.set_attribute(ClinicPage)
    
    rooms_link = (By.PARTIAL_LINK_TEXT, "Rooms")
    rooms_datatable = (By.XPATH, ".//*[@id='room-table']//tr")
    rooms_new_room_button = (By.XPATH, "//a[contains(string(), 'New Room')]")
    rooms_new_room_modal = (By.ID, "AddRoomForm")
    rooms_create_a_new_room_success = (By.XPATH, "//div[@class='alert alert-success fade in' and contains(string(), 'Room created successfully.')]")
    rooms_update_a_new_room_success = (By.XPATH, "//div[@class='alert alert-success fade in' and contains(string(), 'Room updated successfully.')]")
    rooms_delete_success = (By.XPATH, "//div[@class='alert alert-success fade in' and contains(string(), 'Room deleted successfully')]")
    rooms_search_field = (By.XPATH, ".//*[@id='room-table_filter']//input")
    rooms_edit_room_icon = (By.CSS_SELECTOR, "i.fa.fa-pencil")
    rooms_delete_room_icon = (By.CSS_SELECTOR, "i.fa.fa-trash-o")
    
    @Test(rooms_link)
    def click_rooms_link(self):
        self.element(*self.rooms_link) \
        .wait_until_clickable() \
        .click()
    
    @Test(rooms_datatable)
    def wait_for_rooms_datatable(self):
        wait(lambda: self.check_datatable_is_loaded(self.rooms_datatable), waiting_for='Wait for rooms data table is loaded',
             timeout_seconds=20)
    
    @Test(rooms_datatable)
    def wait_for_number_of_rooms_on_datatable(self, number_of_result):
        wait(lambda: self.check_number_of_results_on_datatable(self.rooms_datatable, number_of_result), 
             waiting_for='Wait for rooms data table returns {0} result(s)'.format(str(number_of_result)),
             timeout_seconds=20) 
    
    @Test(rooms_new_room_button)
    def click_into_new_room_button(self):
        self.element(*self.rooms_new_room_button) \
        .wait_until_clickable() \
        .click()
    
    @Test(rooms_new_room_modal)
    def wait_new_room_modal_shows_up(self):
        self.element(*self.rooms_new_room_modal) \
        .wait_until_visible()
    
    @Test(rooms_create_a_new_room_success)
    def wait_for_create_room_success_text(self):
        self.element(*self.rooms_create_a_new_room_success) \
        .wait_until_visible()
    
    @Test(rooms_update_a_new_room_success)
    def wait_for_update_room_success_text(self):
        self.element(*self.rooms_update_a_new_room_success) \
        .wait_until_visible()
    
    @Test(rooms_delete_success)
    def wait_for_delete_room_success_text(self):
        self.element(*self.rooms_delete_success) \
        .wait_until_visible()
    
    @Test(rooms_search_field)
    def search_rooms(self, value):
        self.element(*self.rooms_search_field) \
        .wait_until_clickable() \
        .type(value)
    
    # Assume that room we want to edit is the first result
    @Test(rooms_edit_room_icon)
    def click_into_edit_room(self):
        self.element(*self.rooms_edit_room_icon) \
        .wait_until_clickable() \
        .click()
    
    @Test(rooms_delete_room_icon)
    def click_into_delete_room(self):
        self.element(*self.rooms_delete_room_icon) \
        .wait_until_clickable() \
        .click()
    
    @Test()
    def accept_delete_room_alert(self):
        self._driver.switch_to.alert.accept()
    
    # New room modal
    create_a_room_domain = (By.ID, "jsonform-1-elt-domain")
    create_a_room_slug = (By.ID, "jsonform-1-elt-slug")
    create_a_room_name = (By.ID, "jsonform-1-elt-name")
    create_a_room_code = (By.ID, "jsonform-1-elt-code")
    create_a_room_assignment = (By.XPATH, "//*[contains(@id, 's2id_autogen')]")
    create_a_room_submit_button = (By.XPATH, "//button[@type='submit']")
    
    @Test(create_a_room_domain)
    def enter_room_domain(self, domain):
        self.element(*self.create_a_room_domain) \
        .wait_until_clickable() \
        .type(domain)
    
    @Test(create_a_room_slug)
    def enter_room_slug(self, slug):
        self.element(*self.create_a_room_slug) \
        .type(slug)
    
    @Test(create_a_room_name)
    def enter_room_name(self, name):
        self.element(*self.create_a_room_name) \
        .type(name)
    
    @Test(create_a_room_code)
    def enter_room_code(self, code):
        self.element(*self.create_a_room_code) \
        .type(code)
    
    @Test(create_a_room_assignment)
    def assign_provider_to_room(self, provider_email):
        self.element(*self.create_a_room_assignment) \
        .wait_until_clickable() \
        .click()
        sleep(0.5)
        self.send_keys_active_elem(provider_email)
        sleep(3)
        self.send_keys_active_elem(Keys.ENTER)
    
    @Test(create_a_room_submit_button)
    def click_on_submit_button(self):
        self.element(*self.create_a_room_submit_button) \
        .wait_until_clickable() \
        .click()
