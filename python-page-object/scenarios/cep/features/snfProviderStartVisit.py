__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif
from resource import ODTC
from util.date_time import calculate_age


sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.font_end.provider.dashboard import DashBoardSteps
from steps.font_end.provider.control_panel import ControlPanelSteps
from steps.font_end.provider.visit_note import VisitNoteSteps
from steps.install_steps import InstallSteps
from steps.web_chat import WebChatSteps
from steps.font_end.provider.my_patient import MyPatientSteps
from steps.font_end.provider.my_patient import AllVisitSteps
from steps.navigate_steps import NavigateSteps

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
    _my_patient = MyPatientSteps()
    _all_visit = AllVisitSteps()
    _navigate = NavigateSteps()


    odtc = ODTC()
    patient_index = 0
    patients = odtc.get_snf_patient()
    f_name = patients[patient_index].split(",")[0]
    l_name = patients[patient_index].split(",")[1]
    dob = patients[patient_index].split(",")[2]
    full_name = f_name + " " + l_name

    room = odtc.get_snf_room()
    room_name = room[0].split(",")[3]

    try:
        _actor\
            .visit_snf() \
            .signin_as_provider(env='snf')

        _dashboard\
            .wait_for_patient_getting_ready() \
            .should_see_vsee_status_is_offline(full_name) \
            .wait_for_patient_on_dashboard(name=full_name) \
            .should_see_the_patient_info(full_name=full_name,
                                         room=room_name,
                                         gender="Male",
                                         reason="Vomiting") \
            .should_see_vsee_status_is_online(full_name)

        _dashboard\
            .select_patient_to_view(full_name)

        _control_panel.open_webchat()

        _webchat.send_a_message("Dear, Mr. " + full_name) \
            .send_a_message("How are you going?") \
            .wait_for_message_from_sender("Thanks Doctor, I am doing well") \
            .send_a_message("Do you exercise everyday?") \
            .wait_for_message_from_sender("Yes, Walking and Running 7km everyday") \
            .send_a_message("That sounds great. Keep moving!") \
            .send_a_message("Please, Should not eat fish, meat, butter") \
            .wait_for_message_from_sender("Thank you for your advices.") \
            .close_web_chat().should_not_see_web_chat_of(full_name)

        _control_panel \
            .should_see_vsee_status_is_online()

            # provider start Visit
        _control_panel.make_video_call()

        if is_install:
            _install.install_vsee()
        _install.launch_vsee(is_install)
        _install.accept_privacy_and_term_GDPR()

        _control_panel\
            .should_see_vsee_status_in_a_call()

        _navigate.goto_patient_page()

        _my_patient \
            .select_tab("All Visits")
        _all_visit \
            .search_history_visit_by(value=full_name) \
            .should_see_the_status_visit("In Progress") \
            #.view()

        _navigate\
            .goto_dashboard()

        _dashboard \
            .wait_for_patient_in_progress() \
            .should_see_vsee_status_is_incall(full_name)\
            .resume(full_name)

        # SNF-12

        if editPMHx:
            # Put also the Editing Chief Complaint here to test as well
            _visit_note \
                .should_see_intake_information(chief_complaint='Vomiting',
                                               hr='99 BPM',
                                               bp='180/120 mmHg',
                                               temp='38 C',
                                               rr='99 BPM',
                                               SpO2='53%',
                                               glucose='120 mg/dL',
                                               date_admission='2017-11-22' ,
                                               first_name=f_name,
                                               last_name=l_name,
                                               dob=dob,
                                               gender='Male') \
                .should_see_the_reason_for_visit_that_sent_by_patient("Vomiting") \
                .provider_edit_chief_complaint("Rash,Fever", env='snf') \
                .should_see_the_reason_for_visit_that_sent_by_patient("Vomiting,Rash,Fever") \
                .should_see_the_past_medical_history_that_sent_by_patient("CHF,COPD") \
                .provider_edit_past_medical_history("Irregular heart beat,Asthma", env='snf') \
                .should_see_the_allergies_that_sent_by_patient('5HT1 agonist,12 Hour Nasal') \
                .provider_edit_allergies("Apresoline,Moxifloxacin", env='snf') \
                .should_see_the_allergies_that_sent_by_patient('5HT1 agonist,12 Hour Nasal,Apresoline,Moxifloxacin') \
                .provider_edit_medications("Hypertension,Metoprolol", env='snf')\
                .should_see_the_medications_that_sent_by_patient("Hypertension,Metoprolol")

        _visit_note.provider_write_comment_plan_or_discharge_instructions("NOT eat meat, fish, milk, egg") \
            .complete__and_sent_visit_to_patient() \
            .feedback_on_patient().submit().should_see_back_to_lounge()

        _control_panel \
            .end_call(testID, src, dst, endFlag)

        _navigate.goto_patient_page()

        _my_patient \
            .select_tab("All Visits")
        _all_visit \
            .search_history_visit_by(value=full_name) \
            .should_see_the_status_visit("Completed") \
            .view() \
            .has_tab("Demographics")

        """
        _visit_note \
            .complete_without_notification() \
            .feedback_on_patient(env='snf').submit()
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
    nurse_start_visit()


main()
