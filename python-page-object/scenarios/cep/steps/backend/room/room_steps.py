__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from page.backend.room.room_page import RoomPage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.assertions import Assert


class RoomSteps(Assert):
    on_room_page = RoomPage()

    # Add new provider
    def add_new_room(self, room):
        self.room = room
        self.on_room_page.click_on_new_room() \
            .enter_domain(room.domain.lower()) \
            .enter_slug(room.slug) \
            .enter_name(room.name) \
            .enter_code(room.code) \
            .enter_assignments(room.assignments) \
            .set_active().process()
        return self

    def search_room(self, value):
        self.on_room_page.enter_search_box(value)
        return self

    def should_see_the_room_in_room_table(self):
        self.search_room(self.room.code)
        self.verifyEquals(self.on_room_page.get_domain(), self.room.domain.lower())
        self.verifyEquals(self.on_room_page.get_slug(), self.room.slug)
        self.verifyEquals(self.on_room_page.get_name(), self.room.name)
        self.verifyEquals(self.on_room_page.get_code(), self.room.code)
        for assignment in self.room.assignments:
            self.verifyContainsString(assignment, self.on_room_page.get_assignments())
        self.verifyEquals(self.on_room_page.get_room_status(), 'Active')
        return self

    def delete_room(self, value):
        self.search_room(value)
        self.on_room_page.click_on_delete_button()
        return self

    def edit_room(self, value):
        self.search_room(value)
        self.on_room_page.click_on_edit_button()
        return self

    def should_see_the_room_is_delete(self):
        self.verifyEquals(
            self.on_room_page.get_text_in_the_empty_data_table(), 'No matching records found')
        return self

    def assign_to(self, provider):
        self.on_room_page \
            .enter_assignments(provider) \
            .set_active().process()
