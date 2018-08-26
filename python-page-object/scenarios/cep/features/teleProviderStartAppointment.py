__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif
from resource import ODTC
from util.date_time import get_current_datetime

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.font_end.provider.dashboard import DashBoardSteps
from steps.font_end.provider.control_panel import ControlPanelSteps
from steps.font_end.provider.visit_note import VisitNoteSteps
from steps.install_steps import InstallSteps
from steps.web_chat import WebChatSteps
from steps.navigate_steps import NavigateSteps
from steps.font_end.provider.my_patient import MyPatientSteps
from steps.font_end.provider.my_patient import AllVisitSteps

testID = sys.argv[1]  # test case ID
bType = sys.argv[2]  # type of browser
osType = sys.argv[3]  # type of platform
userID = int(sys.argv[4])  # userID
src = sys.argv[5]  # Local VM ID
dst = sys.argv[6]  # Remote VM ID
is_install = int(sys.argv[7])  # Install VSee client if equal to 1
installFlagMem = int(sys.argv[8])  # Wait for Member installation
editPMHx = int(sys.argv[9])  # if 1 then Provider will edit the PMHx info of patient
checkSurveyFlag = int(sys.argv[10])  # if 1 then Check Provider Post Visit Survey will be on
endFlag = int(sys.argv[11])  # Local ends the call


# Tester thread
def nurse_start_visit():
    _actor = LoginSteps()
    _dashboard = DashBoardSteps()
    _control_panel = ControlPanelSteps()
    _install = InstallSteps()
    _visit_note = VisitNoteSteps()
    _webchat = WebChatSteps()

    _navigate = NavigateSteps()
    _my_patient = MyPatientSteps()
    _all_visit = AllVisitSteps()

    index = 1

    odtc = ODTC()
    provider_name = odtc.get_fullname_provider(env='tele', index=index)

    patients = odtc.get_tele_patient()
    f_name = patients[0].split(",")[1]
    l_name = patients[0].split(",")[2]
    email = patients[0].split(",")[0]

    full_name = f_name + " " + l_name

    try:
        _actor\
            .visit_telepsych() \
            .signin_as_provider(env='tele', index=3)

        _webchat\
            .wait_for_message_from_sender("How are you going?") \
            .reply_message("Thanks, I am doing well") \
            .wait_for_message_from_sender("I have an appointment today.") \
            .reply_message("Yes, Please wait for in a while.") \
            .reply_message("Dr. " + provider_name + " will call now") \
            .close_web_chat()

        _actor\
            .logout() \
            .visit_telepsych() \
            .signin_as_provider(env='tele', index=index)

        _dashboard.select_patient_in_lounge(env='tele')

        # provider start Visit
        _control_panel.make_video_call()

        if is_install:
            _install.install_vsee()
        _install.launch_vsee(is_install)
        _install.accept_privacy_and_term_GDPR()

        _control_panel\
            .visit("chat_in_call.png")\
            .end_call(testID, src, dst, endFlag)

        if editPMHx:
            _visit_note\
                .edit_intake_information(encounter_number='88888888',
                                         medical_number='66666666',
                                         insurance_type='',
                                         information_to_provider='') \
                .should_see_intake_information(encounter_number='88888888',
                                               medical_number='66666666',
                                               insurance_type='',
                                               files_uploaded_for_this_visit='No file uploaded')
            _visit_note\
                .consult_type('Follow-up telepsychiatric assessment') \
                .history_of_present_illness("Pain") \
                .past_psychiatric_history("feel am going mad") \
                .suicidal_attempts("no, sometime stress") \
                .violence_or_aggression("sounding") \
                .in_outpatient_history("Outpatient history") \
                .ECT("Treatment-resistant depression") \
                .recovery_program("Daily activities you need to do to stay well/healthy") \
                .provider_edit_chief_complaint("Suicidal Ideation", env='tele', index=index) \
                .provider_edit_past_medical_history("Thyroid problem,Asthma", env='tele', index=index) \
                .provider_edit_allergies("Apresoline,Moxifloxacin", env='tele', index=index) \
                .provider_edit_medications("Hypertension,Metoprolol", env='tele', index=index)

            _visit_note\
                .provider_write_comment_plan_or_care_instructions("NOT eat meat, fish, milk, egg") \
                .what_was_the_disposition_of_the_patient("Recommend admission to inpatient psychiatric care.") \
                .complete__and_sent_visit_to_patient() \
                .feedback_on_patient(env='tele') \
                .submit() \
                .should_see_back_to_lounge()
            _navigate.goto_patient_page()

            _my_patient \
                .select_tab("My Patients") \
                .search_patient_by(full_name) \
                .should_see_name_patient(full_name) \
                .should_see_gender_patient("Male") \
                .should_see_age_patient("35") \
                .should_see_email_patient(email) \
                .should_see_last_visit_patient(get_current_datetime())

            _actor \
                .logout() \
                .access_waiting_room(env='tele') \
                .signin_as_nurse(env='tele')

            _navigate \
                .goto_my_patients() \
                .re_type_password()

            _my_patient \
                .select_tab("All Visits")
            _all_visit \
                .search_history_visit_by(value=email) \
                .should_see_the_status_visit("Completed")
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
    nurse_start_visit()


main()
