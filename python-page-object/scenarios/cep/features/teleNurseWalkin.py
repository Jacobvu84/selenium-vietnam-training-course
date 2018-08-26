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

from steps.web_chat import WebChatSteps

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
    _webchat = WebChatSteps()
    _dashboard = DashBoardSteps()

    odtc = ODTC()

    index = 0
    patient_index = 1

    provider_name = odtc.get_fullname_provider(env='tele', index=index)
    vsee_id = odtc.get_email_provider(env='tele', index=index)

    patients = odtc.get_tele_patient()
    f_name = patients[patient_index].split(",")[1]
    l_name = patients[patient_index].split(",")[2]
    dob = patients[patient_index].split(",")[3]
    name = f_name + " " + l_name

    try:
        with MailBox(patient_gmail, password_gmail) as mbox:
            mbox.delete_all()
        # WHEN: Nurse creates the visit
        _actor \
            .visit_telepsych() \
            .signin_as_nurse(env='tele')

        _nurse \
            .enter_patient_information(first_name=f_name,
                                       last_name=l_name,
                                       dob=dob,
                                       gender="Male",
                                       encounter_no="VSEE99912347",
                                       medical_record_no="VSEE658974",
                                       insurance_type="") \
            .account_lookup(patient='new') \
            .create_new_patient_record(
                            legal_status="The patient is voluntary and has consented to a telepsychiatry evaluation.") \
            .add_contact_information(ED_facility=odtc.get_room_name_by(env='tele'),
                                     facility_phone_number="650-390-6971",
                                     person_requesting_the_call=odtc.get_nurse_full_name(env='tele'),
                                     nurse_phone_number="650.390.6970",
                                     emergency_room_doctor="Dr. Jacob",
                                     doctor_phone_number="650-390-6972") \
            .reason_for_visit("Agitation, Paranoia") \
            .who_brought_the_patient_in(name="Bella",
                                        phone="650-390-6973",
                                        relationship="wife") \
            .what_did_the_person_witness(description="witness",
                                         threaten_violence="Yes",
                                         overdose="No",
                                         person_witnessed="Valencia") \
            .is_this_patient_on_an_involuntary_psychiatric_hold(answer='Yes') \
            .is_this_patient_currently_in_the_criminal_justrice_system(answer='Yes') \
            .does_the_patient_appear_to_be_under_the_influence_of_drug_or_alcohol(answer='Yes',
                                                                                  relevant_test_results='some text') \
            .click_to_continue() \
            .patient_vitals(hr='99 BPM',
                            bp='180/120 mmHg',
                            temp='38 C',
                            rr='99 BPM',
                            height='60 Inches',
                            weight='80 lb',
                            upload='no') \
            .past_medical_history(conditions='Depression, Diabetes') \
            .should_see_the_past_medical_history_is_updated('Depression, Diabetes') \
            .past_surgeries(procedures='Heart valve replaced, Hernia repair') \
            .should_see_the_past_surgeries_is_updated('Heart valve replaced, Hernia repair') \
            .medications(names='Headaches, Depression') \
            .should_see_the_medications_is_updated('Headaches, Depression') \
            .allergies(drug_name='5HT1 agonist,12 Hour Nasal') \
            .should_see_the_allergies_is_updated('5HT1 agonist,12 Hour Nasal') \
            .click_to_continue() \
            .please_select_a_visit_option(visit_option='45-min Consultation') \
            .select_the_psychiatrist_to_see_availability(1) \
            .pick_an_available_time_slot()

        _dashboard \
            .start_appointment_for(f_name)

        # VM is installed the first time
        if is_install:
            _install.install_vsee()
        _install.launch_vsee(is_install)
        _install.accept_privacy_and_term_GDPR()

        # Launch VM if already installed
        _nurse \
            .should_see_the_chat_button(vsee_id, provider_name) \
            .should_see_the_exit_button() \
            .should_see_notify('Your provider will be with you shortly.') \
            .upload_intake_attachment_file() \
            .start_to_chat_with(vsee_id, provider_name)

        _webchat.send_a_message("Dear, Mr. " + provider_name + ". Today, you have an appointment with" + name) \
            .send_a_message("How are you going?") \
            .wait_for_message_from_sender("Thanks, I am doing well") \
            .send_a_message("I sent the intake attachment file") \
            .send_a_message("Please, Review it!") \
            .send_a_message("Can you please give me a call ?") \
            .wait_for_message_from_sender("I am calling...") \
            .close_web_chat().should_not_see_web_chat_of(provider_name)

        _nurse \
            .wait_doctor_visit(testID, src, dst) \
            .wait_doctor_complete_visit(testID, src) \
            .should_see_visit_status('Visit with Dr. '+provider_name+', Ph.D is in progress') \
            .end_visit()
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
