__author__ = 'jacob@vsee.com'

import sys, os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from page.account_page import PatientProfilePage
from page.account_page import ProviderProfilePage
from util.assertions import Assert


class PatientProfileSteps(Assert):
    on_profile_page = PatientProfilePage()

    def should_see_profile_information(self, password, email, first_name, last_name, gender, dob,
                                             street_address, city, state, zipcode, phone_number, timezone,
                                             primary_care_physician_name, primary_care_physician_phone):
        self.verifyEquals(password, self.on_profile_page.get_profile_information_by_text(label="Password"))
        self.verifyEquals(email, self.on_profile_page.get_profile_information_by_text(label="Email"))
        self.verifyEquals(first_name, self.on_profile_page.get_profile_information_by_text(label="First Name"))
        self.verifyEquals(last_name, self.on_profile_page.get_profile_information_by_text(label="Last Name"))
        self.verifyEquals(gender, self.on_profile_page.get_profile_information_by_text(label="Gender"))
        self.verifyEquals(dob, self.on_profile_page.get_profile_information_by_text(label="Date of Birth"))
        self.verifyEquals(street_address, self.on_profile_page.get_profile_information_by_text(label="Street Address"))
        self.verifyEquals(city, self.on_profile_page.get_profile_information_by_text(label="City"))
        self.verifyEquals(state, self.on_profile_page.get_profile_information_by_text(label="State"))
        self.verifyEquals(zipcode, self.on_profile_page.get_profile_information_by_text(label="Zip Code"))
        self.verifyEquals(phone_number, self.on_profile_page.get_profile_information_by_text(label="Phone Number"))
        self.verifyEquals(timezone, self.on_profile_page.get_profile_information_by_text(label="Timezone"))
        self.verifyEquals(primary_care_physician_name,
                          self.on_profile_page.get_profile_information_by_text(label="Primary Care Physician Name"))
        self.verifyEquals(primary_care_physician_phone,
                          self.on_profile_page.get_profile_information_by_text(label="Primary Care Physician Phone"))

    def edit_profile(self, first_name, last_name, gender, dob,
                           street_address, city, state, zipcode, phone_number, timezone,
                           primary_care_physician_name, primary_care_physician_phone, photo):
        self.on_profile_page.click_on_edit_button()
        if "none" != first_name:
            self.on_profile_page.edit_information_by_text(label="First Name", value=first_name)
        if "none" != last_name:
            self.on_profile_page.edit_information_by_text(label="Last Name", value=last_name)
        if "none" != gender:
            self.on_profile_page.edit_information_by_option(label="Gender", option=gender)
        if "none" != dob:
            self.on_profile_page.edit_bod_information(label="Date of Birth", option=dob)
        self.on_profile_page.edit_information_by_text(label="Street Address", value=street_address)
        self.on_profile_page.edit_information_by_text(label="City", value=city)
        self.on_profile_page.edit_information_by_option(label="State", option=state)
        self.on_profile_page.edit_information_by_text(label="Zip Code", value=zipcode)
        self.on_profile_page.edit_information_by_text(label="Phone Number", value=phone_number)
        self.on_profile_page.edit_information_by_option(label="Timezone", option=timezone)
        self.on_profile_page.edit_information_by_text(label="Primary Care Physician Name",
                                                      value=primary_care_physician_name)
        self.on_profile_page.edit_information_by_text(label="Primary Care Physician Phone",
                                                      value=primary_care_physician_phone)
        self.on_profile_page.upload_photo(upload=photo, path_file="VSeeLogo.png")
        self.on_profile_page.click_on_update()


class ProviderProfileSteps(Assert):
    on_profile_page = ProviderProfilePage()

    def should_see_profile_information(self, email, first_name, last_name, short_bio,
                                             street_address, city, state, zipcode, phone_number, timezone, DEA, NPI,
                                             educational_training, professional_interests, personal_interests):
        self.verifyEquals(email, self.on_profile_page.get_profile_information_by_text(label="Email"))
        self.verifyEquals(first_name, self.on_profile_page.get_profile_information_by_text(label="First Name"))
        self.verifyEquals(last_name, self.on_profile_page.get_profile_information_by_text(label="Last Name"))
        self.verifyEquals(short_bio, self.on_profile_page.get_profile_information_by_text(label="Short Bio"))
        self.verifyEquals(street_address, self.on_profile_page.get_profile_information_by_text(label="Street Address"))
        self.verifyEquals(city, self.on_profile_page.get_profile_information_by_text(label="City"))
        self.verifyEquals(state, self.on_profile_page.get_profile_information_by_text(label="State"))
        self.verifyEquals(zipcode, self.on_profile_page.get_profile_information_by_text(label="Zip Code"))
        self.verifyEquals(phone_number, self.on_profile_page.get_profile_information_by_text(label="Phone Number"))
        self.verifyEquals(timezone, self.on_profile_page.get_profile_information_by_text(label="Timezone"))
        if "none" != DEA:
            self.verifyEquals(DEA, self.on_profile_page.get_profile_information_by_text(label="DEA"))
        if "none" != NPI:
            self.verifyEquals(NPI, self.on_profile_page.get_profile_information_by_text(label="NPI"))
        self.verifyEquals(educational_training,
                          self.on_profile_page.get_profile_information_by_text(label="Educational and Training"))
        self.verifyEquals(professional_interests,
                          self.on_profile_page.get_profile_information_by_text(label="Professional Interests"))
        self.verifyEquals(personal_interests,
                          self.on_profile_page.get_profile_information_by_text(label="Personal Interests"))

    def edit_profile(self, first_name, last_name, short_bio, street_address, city, state, zipcode, phone_number,
                           timezone, DEA, NPI, educational_training, professional_interests, personal_interests, photo):
        self.on_profile_page.click_on_edit_button()
        if "none" != first_name:
            self.on_profile_page.edit_information_by_text(label="First Name", value=first_name)
        if "none" != last_name:
            self.on_profile_page.edit_information_by_text(label="Last Name", value=last_name)
        self.on_profile_page.edit_information_by_textarea(label="Short Bio", value=short_bio)

        self.on_profile_page.edit_information_by_text(label="Street Address", value=street_address)
        self.on_profile_page.edit_information_by_text(label="City", value=city)
        self.on_profile_page.edit_information_by_option(label="State", option=state)
        self.on_profile_page.edit_information_by_text(label="Zip Code", value=zipcode)
        self.on_profile_page.edit_information_by_text(label="Phone Number", value=phone_number)
        self.on_profile_page.edit_information_by_option(label="Timezone", option=timezone)
        if "none" != DEA:
            self.on_profile_page.edit_information_by_text(label="DEA", value=DEA)
        if "none" != NPI:
            self.on_profile_page.edit_information_by_text(label="NPI", value=NPI)
        self.on_profile_page.edit_information_by_textarea(label="Educational and Training", value=educational_training)
        self.on_profile_page.edit_information_by_textarea(label="Professional Interests", value=professional_interests)
        self.on_profile_page.edit_information_by_textarea(label="Personal Interests", value=personal_interests)
        self.on_profile_page.upload_photo(upload=photo, path_file="VSeeLogo.png")
        self.on_profile_page.click_on_update()
        # workaround to make test case pass:
        # https://app.asana.com/0/0/687718364965038/f
        self.on_profile_page.click_on_cancel()
