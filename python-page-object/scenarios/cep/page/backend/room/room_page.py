__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webium.base_page import BasePage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.logger import Test


class RoomPage(BasePage):
    new_button = (By.XPATH, "//a[@data-action='Rooms.add']")
    domain_txt = (By.NAME, "domain")
    slug_txt = (By.NAME, "slug")
    name_txt = (By.NAME, "name")
    code_txt = (By.NAME, "code")
    assignments_txt = (By.XPATH, "//label[text()='Assignments']/following-sibling::input")
    active_check = (By.NAME, "active")
    submit_btn = (By.XPATH, "//button[@type='submit']")
    search_txt = (By.XPATH, "//*[@id='room-table_filter']/label/input")
    del_button = (By.XPATH, "//a[@data-action='Rooms.delete']")
    edit_button = (By.XPATH, "//a[@data-action='Rooms.edit']")
    no_record = (By.XPATH, "//*[@id='room-table']//*[@class='dataTables_empty']")
    col_xpath = "//table[@id='room-table']/tbody/tr/td[count(//table[@id='room-table']/thead/tr/th[text()='{0}']" \
                "/preceding-sibling::*)+1]"

    @Test(new_button)
    def click_on_new_room(self):
        self.element(*self.new_button).wait_until_visible().click()
        return self

    @Test(domain_txt)
    def enter_domain(self, domain):
        self.element(*self.domain_txt).highlight_element() \
            .type(domain)
        return self

    @Test(slug_txt)
    def enter_slug(self, slug):
        self.element(*self.slug_txt).highlight_element() \
            .type(slug)
        return self

    @Test(name_txt)
    def enter_name(self, name):
        self.element(*self.name_txt).highlight_element() \
            .type(name)
        return self

    @Test(code_txt)
    def enter_code(self, code):
        self.element(*self.code_txt).highlight_element() \
            .type(code)
        return self

    @Test(assignments_txt)
    def enter_assignments(self, assignments):
        if type(assignments) is list:
            for assignment in assignments:
                self.element(*self.assignments_txt).highlight_element() \
                    .type(assignment)
                self.wait_a_bit(3)
                self.element(*self.assignments_txt).type(Keys.ENTER).type(Keys.TAB)
        else:
            self.element(*self.assignments_txt).highlight_element() \
                .type(assignments)
            self.wait_a_bit(3)
            self.element(*self.assignments_txt).type(Keys.ENTER).type(Keys.TAB)
        return self

    @Test(active_check)
    def set_active(self):
        status = self.element(*self.active_check).highlight_element().is_checked()
        if status is None:
            self.element(*self.active_check).check()
        return self

    @Test(submit_btn)
    def process(self):
        self.element(*self.submit_btn).highlight_element() \
            .click_and_wait(2)
        return self

    @Test(search_txt)
    def enter_search_box(self, name):
        self.element(*self.search_txt).highlight_element().clear() \
            .type(name).type_and_wait(Keys.TAB, 2)
        return self

    @Test(del_button)
    def click_on_delete_button(self):
        self.element(*self.del_button).wait_until_clickable() \
            .highlight_element().click().accept_alert()
        return self

    @Test(edit_button)
    def click_on_edit_button(self):
        self.element(*self.edit_button).wait_until_clickable() \
            .highlight_element().click_and_wait(2)
        return self

    @Test(no_record)
    def get_text_in_the_empty_data_table(self):
        return self.element(*self.no_record).wait_for_text_to_appear('No matching records found').get_text_value()

    # Get information on the table room
    @Test(("Undefine", "Undefine"))
    def get_text_by_col_name(self, name):
        domain_col = (By.XPATH, self.col_xpath.format(name))
        return self.element(*domain_col).get_text_value()

    def get_domain(self):
        return self.get_text_by_col_name("Domain")

    def get_slug(self):
        return self.get_text_by_col_name("Slug")

    def get_name(self):
        return self.get_text_by_col_name("Name")

    def get_code(self):
        return self.get_text_by_col_name("Code")

    def get_room_status(self):
        return self.get_text_by_col_name("Status")

    def get_assignments(self):
        more = (By.XPATH, '//a[text()="more..."]')
        # If have many provider in the room, the more link will be appear
        if self.element(*more).is_present():
           self.element(*more).wait_until_clickable().highlight_element().click_and_wait(2)
        return self.get_text_by_col_name("Providers")
