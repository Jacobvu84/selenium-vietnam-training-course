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

    index = 0
    telep = 'tele'

    odtc = ODTC()
    patient_index = 1
    patients = odtc.get_tele_patient()
    f_name = patients[patient_index].split(",")[1]
    l_name = patients[patient_index].split(",")[2]
    gender = patients[patient_index].split(",")[6]
    dob = patients[patient_index].split(",")[3]
    name = f_name + " " + l_name

    room = odtc.get_tele_room()
    room_name = room[0].split(",")[3]

    try:
        _actor\
            .visit_telepsych() \
            .signin_as_provider(env=telep, index=index)

        _dashboard\
            .wait_for_patient_on_dashboard(name=f_name) \
            .should_see_the_patient_info(full_name=name,
                                         gender=gender,
                                         dob=str(calculate_age(dob))+' years',
                                         room=room_name,
                                         reason="Agitation,Paranoia") \
            .should_see_vsee_status_is_online(name)

        _webchat\
            .wait_for_message_from_sender("How are you going?") \
            .reply_message("Thanks, I am doing well") \
            .wait_for_message_from_sender("Can you please give me a call ?") \
            .reply_message("Yes, Of course.") \
            .reply_message("I am calling...") \
            .close_web_chat()

        _dashboard\
            .should_see_the_intake_attachment_file("patient_record.png")\
            .select_patient_to_view(f_name)

        # provider start Visit
        _control_panel.make_video_call()

        if is_install:
            _install.install_vsee()
        _install.launch_vsee(is_install)
        _install.accept_privacy_and_term_GDPR()

        _control_panel\
            .visit("chat_in_call.png")\
            .should_see_vsee_status_in_a_call() \
            .end_call(testID, src, dst, endFlag)

        if editPMHx:
            status = 'The patient is voluntary and has consented to a telepsychiatry evaluation.'

            _visit_note\
                .should_see_intake_information(chief_complaint='Agitation,Paranoia',
                                               hr='99 BPM',
                                               bp='180/120 mmHg',
                                               temp='38 C',
                                               rr='99 BPM',
                                               first_name=f_name,
                                               dob=dob,
                                               gender='Male',
                                               encounter_number='VSEE99912347',
                                               medical_number='VSEE658974',
                                               insurance_type='',
                                               legal_status=status,
                                               files_uploaded_for_this_visit='patient_record.png') \
                .edit_intake_information(encounter_number='VSEE8888',
                                         medical_number='VSEE6666',
                                         insurance_type='',
                                         information_to_provider='') \
                .should_see_intake_information(chief_complaint='Agitation,Paranoia',
                                               hr='99 BPM',
                                               bp='180/120 mmHg',
                                               temp='38 C',
                                               rr='99 BPM',
                                               first_name=f_name,
                                               dob=dob,
                                               gender='Male',
                                               encounter_number='VSEE8888',
                                               medical_number='VSEE6666',
                                               insurance_type='',
                                               legal_status=status,
                                               files_uploaded_for_this_visit='patient_record.png')
            _visit_note\
                .consult_type('Follow-up telepsychiatric assessment') \
                .history_of_present_illness("Pain") \
                .past_psychiatric_history("feel am going mad") \
                .suicidal_attempts("no, sometime stress") \
                .violence_or_aggression("sounding") \
                .in_outpatient_history("Outpatient history") \
                .ECT("Treatment-resistant depression") \
                .recovery_program("Daily activities you need to do to stay well/healthy") \
                .should_see_the_reason_for_visit_that_sent_by_patient('Agitation,Paranoia') \
                .provider_edit_chief_complaint("Suicidal Ideation", env='tele') \
                .provider_remove_chief_complaint("Paranoia") \
                .should_see_the_past_medical_history_that_sent_by_patient('Depression,Diabetes') \
                .provider_edit_past_medical_history("Thyroid problem,Asthma", env='tele') \
                .should_see_the_allergies_that_sent_by_patient("5HT1 agonist,12 Hour Nasal") \
                .provider_edit_allergies("Apresoline,Moxifloxacin", env='tele') \
                .should_see_the_medications_that_sent_by_patient('Headaches, Depression') \
                .provider_edit_medications("Hypertension,Metoprolol", env='tele')

            _visit_note\
                .provider_write_comment_plan_or_care_instructions("NOT eat meat, fish, milk, egg") \
                .what_was_the_disposition_of_the_patient("Recommend admission to inpatient psychiatric care.") \
                .complete__and_sent_visit_to_patient() \
                .feedback_on_patient(env='tele').submit() \
                .should_see_back_to_lounge()

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
