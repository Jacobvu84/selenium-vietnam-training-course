__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif
from util import date_time
from resource import ODTC

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.font_end.provider.new_visit import NewVisitSteps
from steps.font_end.nurse.nurse_steps import NurseSteps
from steps.install_steps import InstallSteps
from steps.web_chat import WebChatSteps
from steps.navigate_steps import NavigateSteps
from steps.font_end.provider.my_patient import MyPatientSteps
from steps.font_end.provider.my_patient import AllVisitSteps
from steps.font_end.provider.dashboard import DashBoardSteps

testID = sys.argv[1]  # test case ID
bType = sys.argv[2]  # type of browser
osType = sys.argv[3]  # type of platform
userID = int(sys.argv[4])  # userID
src = sys.argv[5]  # Local VM ID
dst = sys.argv[6]  # Remote VM ID
is_install = int(sys.argv[7])  # Install VSee client if equal to 1


def clinic_admin_new_visit():
    _actor = LoginSteps()
    _new_visit = NewVisitSteps()
    _nurse = NurseSteps()
    _install = InstallSteps()
    _webchat = WebChatSteps()
    _navigate = NavigateSteps()
    _my_patient = MyPatientSteps()
    _all_visit = AllVisitSteps()
    _dashboard = DashBoardSteps()

    index = 3
    odtc = ODTC()
    room_name = odtc.get_room_name_by(env='tele')
    date_app = date_time.get_current_datetime()
    clinic_name = odtc.get_fullname_provider(env='tele', index=index)
    clinic_id = odtc.get_email_provider(env='tele', index=index)

    provider_name = odtc.get_fullname_provider(env='tele', index=1)
    provider_id = odtc.get_email_provider(env='tele', index=1)

    patients = odtc.get_tele_patient()
    f_name = patients[0].split(",")[1]
    l_name = patients[0].split(",")[2]
    email = patients[0].split(",")[0]

    full_name = f_name + " " + l_name

    try:
        # CA/SA will create visit/appointment
        _actor\
            .visit_telepsych() \
            .signin_as_provider(env='tele', index=index)
        _new_visit\
            .open_new_visit_form() \
            .should_see_visit_type("Video (Other), Phone, Video (VSee)") \
            .should_see_visit_type_focus_on("Video (Other)") \
            .should_see_date_and_time_type("Now, Schedule for a later time") \
            .should_see_date_and_time_focus_on("Now") \
            .create_visit_with_new_patient(room=room_name,
                                           first_name=f_name,
                                           last_name = l_name,
                                           email= email,
                                           gender = 'Male',
                                           dob = '1982-11-17',
                                           visit_type='Video (VSee)',
                                           visit_option='30-min Consultation',
                                           date_time='Now') \
            .should_see_visit_details(visit_type='Video (VSee)',
                                      visit_option='30-min Consultation',
                                      date_time="Now (" + date_app,
                                      patient_name=full_name)\
            .go_to_visit_detail_page('Are you going to review this visit now?', 'no')

        # Nurse starts to enter the WR for patient
        _actor \
            .logout() \
            .visit_telepsych() \
            .signin_as_nurse(env='tele')
        _dashboard \
            .start_appointment_for(full_name)


        # VM is installed the first time
        if is_install:
            _install.install_vsee()
        _install.launch_vsee(is_install)
        _install.accept_privacy_and_term_GDPR()

        _nurse \
            .should_see_the_chat_button(clinic_id, clinic_name) \
            .should_see_the_exit_button() \
            .start_to_chat_with(clinic_id, clinic_name)

        _webchat.send_a_message("Dear, Mr. " + clinic_name) \
            .send_a_message("How are you going?") \
            .wait_for_message_from_sender("Thanks, I am doing well") \
            .send_a_message("I have an appointment today.") \
            .wait_for_message_from_sender("Dr. " + provider_name + " will call now") \
            .close_web_chat().should_not_see_web_chat_of(clinic_name)

        _nurse \
            .wait_doctor_visit(testID, src, dst) \
            .start_to_chat_with(provider_id, provider_name)

        _webchat\
            .send_a_message("Dear, Dr. " + provider_name)\
            .send_a_message("I've been waiting for someone like you")
        _nurse \
            .wait_doctor_complete_visit(testID, src) \
            .end_visit()

        _navigate\
            .goto_my_patients()\
            .re_type_password()

        _my_patient\
            .select_tab("My Patients") \
            .should_see_my_patient_table_with_title("Name,Gender,Age,Email,Phone Number,Date of Last Visit") \
            .should_see_no_data_available_in_table()

        _my_patient\
            .select_tab("All Visits")
        _all_visit \
            .search_history_visit_by(value=email) \
            .should_see_the_status_visit("In Progress") \

        """
        _visit_note\
            .download_visit_note() \
            .should_see_the_file("summary.pdf")
        """
        print "[PASSED]: TEST PASSED"
    except Exception as e:
        print type(e)
        print e.args
        print e
        print "[FAILED]: TEST FAILED"

    finally:
        _actor.quit()
        create_gif()


def main():
    start_test()
    clinic_admin_new_visit()


main()
