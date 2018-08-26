__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif
from util.mailbox import MailBox
from resource import ODTC

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.font_end.nurse.nurse_steps import NurseSteps
from steps.install_steps import InstallSteps
from steps.font_end.provider.dashboard import DashBoardSteps
from steps.navigate_steps import NavigateSteps
from steps.font_end.provider.my_patient import AllVisitSteps
from steps.font_end.provider.my_patient import MyPatientSteps
from steps.font_end.provider.visit_note import VisitNoteSteps

from model.patient import patient_gmail
from model.patient import password_gmail

testID = sys.argv[1]  # test case ID
bType = sys.argv[2]  # type of browser
osType = sys.argv[3]  # type of platform
userID = int(sys.argv[4])  # userID
src = sys.argv[5]  # Local VM ID
dst = sys.argv[6]  # Remote VM ID
is_install = int(sys.argv[7])  # Install VSee client if equal to 1


def nurse_walk_in():
    # Objects
    _actor = LoginSteps()
    _nurse = NurseSteps()
    _install = InstallSteps()
    _dashboard = DashBoardSteps()
    _navigate = NavigateSteps()
    _all_visit = AllVisitSteps()
    _my_patient = MyPatientSteps()
    _visit_note = VisitNoteSteps()

    patient_index = 0

    odtc = ODTC()
    patients = odtc.get_snf_patient()
    f_name = patients[patient_index].split(",")[0]
    l_name = patients[patient_index].split(",")[1]
    dob = patients[patient_index].split(",")[2]

    full_name = f_name + " " + l_name

    provider_full_name = odtc.get_fullname_provider(env='snf')
    provider2 = odtc.get_fullname_provider(env='snf', index=1)
    room_name = odtc.get_room_name_by(env='snf')

    try:
        with MailBox(patient_gmail, password_gmail) as mbox:
            mbox.delete_all()
        # WHEN: Nurse creates the visit
        _actor\
            .visit_snf() \
            .signin_as_nurse(env='snf', index=1)

        _navigate \
            .goto_patient_page() \
            .re_type_password()

        _all_visit \
            .search_history_visit_by(value=full_name) \
            .should_see_the_status_visit("Completed")\
            .should_see_the_patient_name(full_name)\
            .should_see_the_provider_name(provider_full_name)\
            .should_see_the_waiting_room(room_name)

        _navigate \
            .goto_dashboard()
        _nurse \
            .enter_patient_information(first_name=f_name,
                                       last_name=l_name,
                                       dob=dob,
                                       gender="Male") \
            .account_lookup(patient=f_name + " " + l_name+ ", " + dob) \
            .add_more_patient_information(date_of_most_recent_admission="2017-12-22",
                                          principal_diagnosis_upon_admission_to_the_facility='Hip fracture',
                                          reason_for_visit='Vomiting') \
            .click_to_continue() \
            .patient_vitals(hr='99 BPM',
                            bp='180/120 mmHg',
                            temp='38 C',
                            rr='99 BPM',
                            SpO2='53%',
                            glucose='120 mg/dL',
                            upload='no') \
            .should_see_the_past_medical_history_is_updated('CHF, COPD, Asthma, Irregular heart beat') \
            .should_see_the_past_surgeries_is_updated('Heart valve replaced, Hernia repair') \
            .should_see_the_allergies_is_updated('Moxifloxacin,Apresoline,5HT1 agonist,12 Hour Nasal') \
            .click_to_continue() \
            .please_help_us_improve_our_service_by_answering_the_followin(
                option='Call 911 to take patient to the emergency department')

        # VM is installed the first time
        if is_install:
            _install.install_vsee()
        _install\
            .launch_vsee(is_install) \
            .accept_privacy_and_term_GDPR()\
            .close_the_video_conference(testID, src)\
            .relaunch_video()\
            .should_see_the_video_relaunch(testID, src)

        # Launch VM if already installed
        _nurse.wait_doctor_visit(testID, src, dst) \
            .wait_doctor_complete_visit(testID, src) \
            .patient_rate_and_end_visit()

        _navigate\
            .goto_patient_page() \
            .re_type_password()
        # All Visit is default
        _my_patient \
            .should_see_the_all_visit_history_table_with_columns("Visit Time,Patient,Waiting Room,Provider,"
                                                                 "Gender,Age,Email,Visit Status,Action")
        _all_visit \
            .search_history_visit_by(value=full_name) \
            .should_see_the_status_visit("Completed")\
            .should_see_the_patient_name(full_name)\
            .should_see_the_provider_name(provider2)\
            .should_see_the_waiting_room(room_name)

# Nurse can view the completed visit in All Visits tab and see the notes of visit
        _visit_note \
            .should_see_intake_information(chief_complaint='Vomiting',
                                           hr='99 BPM',
                                           bp='180/120 mmHg',
                                           temp='38 C',
                                           rr='99 BPM',
                                           SpO2='53%',
                                           glucose='120 mg/dL',
                                           date_admission='2017-11-22',
                                           first_name=f_name,
                                           last_name=l_name,
                                           dob=dob,
                                           gender='Male') \
            .should_see_the_reason_for_visit_that_sent_by_patient("Vomiting,Rash,Fever") \
            .should_see_the_past_medical_history_that_sent_by_patient("CHF,COPD") \
            .should_see_the_allergies_that_sent_by_patient('5HT1 agonist,12 Hour Nasal,Apresoline,Moxifloxacin') \
            .should_see_the_medications_that_sent_by_patient("Hypertension,Metoprolol")

        _nurse\
            .download_the_visit_summary()\
            .upload_file_in_document_tab()\
            .update_patient_profile_in_demogranphics()\
            .should_not_see_edit_button()

        print "[PASSED]: TEST PASSED"

    except Exception as e:
        print type(e)
        print e.args
        print e
        print "[INFO]: TEST FAILED"
    finally:
        _actor.quit()
        create_gif()


def main():
    start_test()
    nurse_walk_in()


main()
