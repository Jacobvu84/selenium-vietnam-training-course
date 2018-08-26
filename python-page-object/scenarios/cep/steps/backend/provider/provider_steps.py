__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from page.backend.provider.provider_page import ProviderPage
from page.backend.provider.provider_page import SubTypePage
from page.backend.provider.provider_page import DemographicsPage
from page.backend.provider.provider_page import LicensePage
from page.backend.provider.provider_page import ProfilePage
from page.backend.provider.provider_page import AssignmentPage
from page.backend.provider.provider_page import RolePage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.assertions import Assert


class SubTypeSteps(Assert):
    on_subtype_page = SubTypePage()

    def select_sub_type(self, provider):
        self.on_subtype_page \
            .select_subtype(provider.subtype.subtype)
        return self


class DemographicsSteps(Assert):
    on_demographics_page = DemographicsPage()

    def enter_demographics_information(self, provider):
        self.on_demographics_page \
            .fill_first_name(provider.demographics.firstname) \
            .fill_last_name(provider.demographics.lastname) \
            .fill_email(provider.demographics.email) \
            .fill_username(provider.demographics.username) \
            .fill_password(provider.demographics.password) \
            .fill_confirm_password(provider.demographics.confirm_pwd) \
            .fill_title(provider.demographics.title) \
            .fill_suffix(provider.demographics.suffix) \
            .fill_phone(provider.demographics.phone) \
            .fill_address(provider.demographics.street) \
            .fill_city(provider.demographics.city) \
            .fill_state(provider.demographics.state) \
            .fill_zipcode(provider.demographics.zip).process_demographics()
        return self


class LicenseSteps(Assert):
    on_license_page = LicensePage()

    def enter_license_information(self, provider):
        self.on_license_page \
            .fill_dea(provider.license.dea) \
            .fill_npi(provider.license.npi) \
            .fill_specialties(provider.license.specialties) \
            .fill_states_licensed(provider.license.statesLicensed) \
            .fill_states_serviced(provider.license.statesLicensed).process_license()
        return self


class ProfileSteps(Assert):
    on_profile_page = ProfilePage()

    def enter_profile_information(self, provider):
        self.on_profile_page \
            .fill_medical_school(provider.profile.medicalSchool) \
            .fill_internship(provider.profile.internship) \
            .fill_residency(provider.profile.residency) \
            .fill_language(provider.profile.language) \
            .fill_bio(provider.profile.shortBio) \
            .upload_image_profile(provider.profile.picture).process_profile()
        return self


class AssignmentSteps(Assert):
    on_assignment_page = AssignmentPage()

    def enter_assignment_information(self, provider):
        if provider.assignment.values is not None:
            self.on_assignment_page \
                .select_assignment(provider.assignment.byClinics) \
                .assign_to(provider.assignment.values)
        self.on_assignment_page.save()
        return self


class RoleSteps(Assert):
    on_role_page = RolePage()

    def should_see_provider_information(self, provider):
        self.verifyEquals(self.on_role_page.get_first_name(), provider.demographics.firstname)
        self.verifyEquals(self.on_role_page.get_last_name(), provider.demographics.lastname)
        self.verifyEquals(self.on_role_page.get_email(), provider.demographics.email)
        return self

    def assign_role(self, provider):
        if "" != provider.role:
            self.on_role_page \
                .select_role(provider.role)\
                .click_on_save()
        return self


class ProviderSteps(SubTypeSteps, DemographicsSteps, LicenseSteps, ProfileSteps, AssignmentSteps, RoleSteps):
    on_provider_page = ProviderPage()

    # Add new provider
    def create_new(self):
        self.on_provider_page \
            .create_a_one()
        return self

    def search_user(self, provider):
        self.on_provider_page \
            .search_provider(provider.demographics.email) \
            .click_on_manage_permession()
        return self

    def should_see_that_provider_table_contain(self, email):
        self.on_provider_page \
            .search_provider(email)

        self.verifyEquals(self.on_provider_page.provider_found(), email)
        return self

    def logout(self):
        self.on_provider_page \
            .user_logout()

    subtitle_mail = on_provider_page.get_project_name()

    def set_password(self, pwd):
        self.on_provider_page.reset_password(pwd)
        return self

    def should_see_alert_message(self, msg):
        assert msg in self.on_provider_page.get_source_html(), msg + " doesn't contains."
        return self
