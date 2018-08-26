__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from page.patient_page import PatientHomePage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.assertions import Assert
from resource import ODTC
from util.logger import Test
from util import date_time


class PatientHomeSteps(Assert):
    on_patient_home_page = PatientHomePage()

    time = ""
    today = date_time.today_in_slot()

    odtc = ODTC()

    @Test(("Group Steps", ""))
    def schedule_appointment(self, index=0):
        patients = self.odtc.get_cep_patient()
        first_name = patients[index].split(",")[1]

        self.on_patient_home_page \
            .click_on_schedule_appointment() \
            .select_who_visit_for(first_name)

        self.what_is_your_health_concern_today(symptom="Difficulty breathing",
                                               temperature="39.5",
                                               heart_rate="124 bpm",
                                               blood_pressure="180/120mmHg",
                                               upload="Yes")

        self.please_verify_and_update_the_following_information(phone_number="0977525625",
                                                                location="California",
                                                                medical_conditions="High blood pressure (HTN)",
                                                                others_medical_conditions="Deadache",
                                                                allergies="1000 BC",
                                                                medications="Vitamin E")
        self.time = self.get_time_lost()
        self.pick_an_available_time_slot_for_your_appointment(time=self.time)
        self.your_input_is_valuable_to_help_us_improve_our_services(i_would="Ask a friend or family member what to do",
                                                                    i_want="To feel better so I can go to work/school",
                                                                    other="Hard working")
        self.should_see_start_appointment_in_dashboard(day="Today")
        return self

    @Test(("Group Steps", ""))
    def schedule_appointment_quickly(self, index=0):
        patients = self.odtc.get_cep_patient()
        first_name = patients[index].split(",")[1]

        self.on_patient_home_page \
            .click_on_schedule_appointment() \
            .select_who_visit_for(first_name)
        self.what_is_your_health_concern_today(symptom="Seasonal allergies")
        self.please_verify_and_update_the_following_information(phone_number="0977525625")

        self.time = self.get_time_lost()
        self.pick_an_available_time_slot_for_your_appointment(time=self.time)
        self.your_input_is_valuable_to_help_us_improve_our_services(other="schedule appointment quickly")
        self.should_see_start_appointment_in_dashboard(day="Today")
        return self

    @Test(("Group Steps", ""))
    def select_a_doctor_and_book_an_appointment_quickly(self, provider, patient):
        doctors = self.odtc.get_cep_provider()
        provider_name = doctors[provider].split(",")[1]

        patients = self.odtc.get_cep_patient()
        patient_name = patients[patient].split(",")[1]

        self.on_patient_home_page \
            .select_a_doctor(provider_name) \
            .click_book_an_appointment() \
            .select_who_visit_for(patient_name)

        self.what_is_your_health_concern_today(symptom="Seasonal allergies")
        self.please_verify_and_update_the_following_information(phone_number="0977525625")

        self.time = self.get_time_lost()
        self.pick_an_available_time_slot_for_your_appointment(time=self.time)
        self.your_input_is_valuable_to_help_us_improve_our_services(
                                                            other="Book an appointment quickly with special doctor")
        return self

    @Test(("Group Steps", ""))
    def select_a_doctor_and_book_an_appointment(self, index):
        doctors = self.odtc.get_cep_provider()
        provider_name = doctors[index].split(",")[1]

        patients = self.odtc.get_cep_patient()
        patient_name = patients[0].split(",")[1]

        self.on_patient_home_page \
            .select_a_doctor(provider_name) \
            .click_book_an_appointment() \
            .select_who_visit_for(patient_name)

        self.what_is_your_health_concern_today(symptom="Difficulty breathing",
                                               temperature="39.5",
                                               heart_rate="124 bpm",
                                               blood_pressure="180/120mmHg",
                                               upload="Yes")

        self.please_verify_and_update_the_following_information(phone_number="0977525625",
                                                                location="California",
                                                                medical_conditions="High blood pressure (HTN)",
                                                                others_medical_conditions="Deadache",
                                                                allergies="1000 BC",
                                                                medications="Vitamin E")
        self.time = self.get_time_lost()
        self.pick_an_available_time_slot_for_your_appointment(time=self.time)

        self.your_input_is_valuable_to_help_us_improve_our_services(i_would="Ask a friend or family member what to do",
                                                                    i_want="To feel better so I can go to work/school",
                                                                    other="Work-hard")
        return self

    @Test(("Group Steps", ""))
    def should_see_start_appointment_in_dashboard(self, day):
        if day == date_time.next_day_in_slot():
            date_app = date_time.get_next_date()
        else:
            date_app = "Today"

        self.on_patient_home_page.should_see_start_appointment_in_upcoming_appointments(day=date_app, time=self.time)
        return self

    @Test(("Group Steps", ""))
    def see_a_doctor_in_room_quickly(self, visit_option):
        """
        Short Steps: Only fill mandatory fields
        """
        patients = self.odtc.get_cep_patient()
        first_name = patients[0].split(",")[1]

        self.on_patient_home_page \
            .click_on_see_a_doctor_now() \
            .select_who_visit_for(first_name)

        self.what_is_your_health_concern_today(symptom="Back pain,Chest pain")

        self.please_verify_and_update_the_following_information(phone_number="0984303104")
        self.choose_pharmacy("no")
        if "no" != visit_option:
            self.please_select_a_visit_option(consultation_type=visit_option)
        self.your_input_is_valuable_to_help_us_improve_our_services(other="see a doctor quickly")
        return self

    @Test(("Group Steps", ""))
    def see_a_doctor_in_room(self, visit_option):
        """
        Full Steps
        Convention for sub steps:
            * method_name_() is mandatory steps/fields
            * method without underscore ending, it can ignore if needed
        Remarks: Should not change data test because they are using to verify in cepProviderStartVisit.py
        """
        patients = self.odtc.get_cep_patient()
        first_name = patients[0].split(",")[1]

        self.on_patient_home_page \
            .click_on_see_a_doctor_now() \
            .select_who_visit_for(first_name)

        self.what_is_your_health_concern_today(symptom="Back pain,Chest pain",
                                               temperature="39",
                                               heart_rate="99 bpm",
                                               blood_pressure="140/90mmHg",
                                               upload="Yes")

        self.please_verify_and_update_the_following_information(phone_number="0984303104",
                                                                location="California",
                                                                medical_conditions="Depression,Heart burn (GERD),"
                                                                                   "Headaches (Migraines)",
                                                                others_medical_conditions="Headaches (Migraines),"
                                                                                          "Anorexia and Bulimia",
                                                                allergies="5HT1 agonist,12 Hour Nasal",
                                                                medications="Amoxicillin,Paracetamol")
        # self.choose_pharmacy("Downtown Center Pharmacy")
        self.choose_pharmacy("no")
        if "no" != visit_option:
            self.please_select_a_visit_option(consultation_type=visit_option)
        self.your_input_is_valuable_to_help_us_improve_our_services(i_would="See my primary care doctor",
                                                                    i_want="To know that I don't have a dangerous condition",
                                                                    other="Testing")
        return self

    @Test(("Group Steps", ""))
    def what_is_your_health_concern_today(self, symptom, temperature="", heart_rate="",
                                                blood_pressure="", upload="yes"):
        self.on_patient_home_page \
            .give_question_that("WHAT IS YOUR HEALTH CONCERN TODAY?") \
            .then_answers_are() \
            .choose_symptom_that_best_describe_situation_(symptom) \
            .temperature(temperature) \
            .heart_rate(heart_rate) \
            .blood_pressure(blood_pressure) \
            .upload_relevant_information(upload, path_file="patient_record.png") \
            .agreed_to_the_terms_('yes')
        return self

    @Test(("Group Steps", ""))
    def please_verify_and_update_the_following_information(self, phone_number, location="California",
                                                                 medical_conditions="", others_medical_conditions="",
                                                                 allergies="", medications=""):
        self.on_patient_home_page.then("PLEASE VERIFY AND UPDATE THE FOLLOWING INFORMATION") \
            .phone_number_can_reach_you_today_(phone_number) \
            .current_location(location) \
            .update_past_and_current_medical_conditions(medical_conditions) \
            .add_others_medical_conditions(others_medical_conditions) \
            .update_allergies(allergies) \
            .update_current_medications(medications) \
            .next_screen_()
        return self

    @Test(("Group Steps", ""))
    def choose_pharmacy(self, name="no"):
        self.on_patient_home_page.then("SELECT PHARMACY") \
            .select_pharmacy(name) \
            .continues_()
        return self

    @Test(("Group Steps", ""))
    def your_input_is_valuable_to_help_us_improve_our_services(self, i_would="", i_want="", other=""):
        self.on_patient_home_page \
            .then("YOUR INPUT IS VALUABLE TO HELP US IMPROVE OUR SERVICE.") \
            .then("PLEASE TAKE A MOMENT TO ANSWER THE FOLLOWING QUESTIONS.") \
            .give_question_that("If this telehealth service was not available to me, I would:") \
            .then_answers_are() \
            .answer_random(1).select_answer(i_would) \
            .give_question_that("I want the following from my telehealth visit today:") \
            .then_answers_are() \
            .answer_random(2).select_answer(i_want) \
            .other_answer(other) \
            .submit_()
        return self

    @Test(("Group Steps", ""))
    def pick_an_available_time_slot_for_your_appointment(self, day=today, time=0):
        date_app = ""
        # .select_slot_at(session,time)\
        if day == date_time.next_day_in_slot():
            date_app = date_time.get_next_date()
        else:
            date_app = date_time.get_current_datetime()

        self.on_patient_home_page.then("Pick an available time slot for your appointment") \
            .select_first_available_time_lost(day) \
            .should_see_the_message("Please confirm your appointment", date_app, time) \
            .click_on_confirm()
        return self

    def get_time_lost(self, day=today):
        return self.on_patient_home_page \
            .get_first_available_time_lost(day)

    # Should update new UI
    def patient_rate_and_end_visit(self):
        self.on_patient_home_page \
            .click_on_5_star() \
            .click_end_visit()
        return self

    def end_visit(self):
        self.on_patient_home_page \
            .click_end_visit()
        return self

    # Wait for starting call [eVisitLib.waitCall]
    def wait_doctor_visit(self, testID, src, dst):
        """
        :param
            - src: vm id, example: vm6.
                   Check hostConfig var in setting/installConfig.py
        """
        self.on_patient_home_page.wait_for_call_from_provider(testID, src, dst)
        return self

    @Test(("Group Steps", ""))
    def wait_doctor_complete_visit(self, testID, src):
        self.on_patient_home_page.wait_for_endcall(testID, src)
        return self

    @Test(("Group Steps", ""))
    def start_his_appointment(self):
        self.on_patient_home_page.click_on_start_appointment()
        self.please_verify_and_update_the_following_information(phone_number="0984303104")
        self.choose_pharmacy("no")
        return self

    def just_exit_appointment(self):
        self.on_patient_home_page.click_on_just_exit()
        return self

    @Test(("Group Steps", ""))
    def should_see_end_call(self, testID, src):
        self.on_patient_home_page.wait_for_endcall(testID, src)
        return self

    @Test(("Group Steps", ""))
    def please_select_a_visit_option(self, consultation_type):
        """
        - consultation_type: config in the setting room
        """
        self.on_patient_home_page \
            .then("PLEASE SELECT A VISIT OPTION.") \
            .give_question_that("Visit Option") \
            .then_answers_are() \
            .select_visit_option(consultation_type) \
            .next_to_continue()
        return self

    @Test(("Group Steps", ""))
    def do_you_want_to_cancel_this_upcoming_appointment(self, answer):
        if "no" == answer:
            self.on_patient_home_page.click_on_cancel_button().say_no()
        else:
            self.on_patient_home_page.click_on_cancel_button().say_yes()
            self.verifyEquals(
                self.on_patient_home_page.should_see_message_cancel_appointment(), "Success! Appointment is canceled")

        return self

    def reschedule_appointment(self, other_day):
        self.on_patient_home_page.click_on_exist_and_schedule_appointment()

        self.time = self.get_time_lost(other_day)
        self.pick_an_available_time_slot_for_your_appointment(other_day, self.time)
        return self
