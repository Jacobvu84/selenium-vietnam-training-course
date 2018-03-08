__author__ = 'jacob@vsee.com'

import os,sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from page.provider_page import ProviderPage

class ProviderSteps():

    on_provider_page = ProviderPage()

    # Add new provider
    def create_new(self, first_name, last_name, jobTitle,
                   vsee_id, active, department):
        self.on_provider_page.click_on_new_button()
        self.on_provider_page.type_first_name(first_name)
        self.on_provider_page.type_last_name(last_name)
        self.on_provider_page.type_job_title(jobTitle)
        self.on_provider_page.type_vsee_id(vsee_id)
        self.on_provider_page.active(active)
        self.on_provider_page.select_department(department)
        self.on_provider_page.click_on_create_button()

    def search_provider_by_email(self, email):
        self.on_provider_page.search_provider(email)

    def should_see_the_email_matches(self, email):
        if email == self.on_provider_page.provider_found():
            return True

    def delete_provider_by_email(self):
        self.on_provider_page.delete_provider()

    def should_see_no_results_found(self):
        return self.on_provider_page.provider_not_found()

