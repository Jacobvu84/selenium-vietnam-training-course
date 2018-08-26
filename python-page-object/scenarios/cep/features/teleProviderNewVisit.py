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
from steps.font_end.provider.dashboard import DashBoardSteps
from steps.font_end.provider.visit_note import VisitNoteSteps
from steps.font_end.nurse.nurse_steps import NurseSteps


testID = sys.argv[1]  # test case ID


def provider_new_visit():
    _actor = LoginSteps()
    _new_visit = NewVisitSteps()
    _dashboard = DashBoardSteps()
    _visit_detail = VisitNoteSteps()
    _nurse = NurseSteps()

    index = 1
    patient_index = 1
    odtc = ODTC()
    room_name = odtc.get_room_name_by(env='tele')
    not_now = date_time.get_next_date()
    full_name = odtc.get_fullname_patient(env='tele', index=patient_index)

    try:
        _actor\
            .visit_telepsych() \
            .signin_as_provider(env='tele', index=index)

        _new_visit\
            .open_new_visit_form() \
            .should_see_visit_type("Video (Other), Phone, Video (VSee)") \
            .should_see_visit_type_focus_on("Video (Other)") \
            .should_see_date_and_time_type("Now, Schedule for a later time") \
            .should_see_date_and_time_focus_on("Now") \
            .create_new_visit(room=room_name,
                              patient_name=full_name,
                              visit_type='Phone',
                              visit_option='30-min Consultation',
                              date_time='Schedule for a later time', date=not_now, time='10:15 AM') \
            .should_see_visit_details(visit_type='Phone',
                                      visit_option='30-min Consultation',
                                      date_time=not_now + " 10:15 AM",
                                      patient_name=full_name)\
            .go_to_visit_detail_page('Are you going to review this visit now?', 'no')
        _dashboard\
            .should_see_section("Currently in the Waiting Room")\
            .should_see_today_schedule_section()\
            .should_see_create_new_visit_option()

        _new_visit\
            .open_new_visit_form() \
            .should_see_visit_type("Video (Other), Phone, Video (VSee)") \
            .should_see_visit_type_focus_on("Video (Other)") \
            .should_see_date_and_time_type("Now, Schedule for a later time") \
            .should_see_date_and_time_focus_on("Now") \
            .create_new_visit(room=room_name,
                              patient_name=full_name,
                              visit_type='Video (VSee)',
                              visit_option='15-min Consultation',
                              date_time='Schedule for a later time', date=not_now, time='11:00 AM')\
            .should_see_visit_details(visit_type='Video (VSee)',
                                      visit_option='15-min Consultation',
                                      date_time=not_now + " 11:00 AM",
                                      patient_name=full_name)\
            .go_to_visit_detail_page('Are you going to review this visit now?', 'yes')\

        _visit_detail \
            .has_tab("Visit Notes") \
            .has_tab("Medical History")
        _nurse \
            .should_see_the_past_medical_history_is_updated('Depression, Diabetes, Stroke, Thyroid problem') \
            .should_see_the_past_surgeries_is_updated('Heart valve replaced, Hernia repair, Joint replacement')
        _visit_detail \
            .has_tab("Allergies")
        _nurse \
            .should_see_the_allergies_is_updated('5HT1 agonist,12 Hour Nasal, Vsee Clinic')
        _visit_detail \
            .has_tab("Medications") \
            .has_tab("Documents") \
            .has_tab("Demographics")

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
    provider_new_visit()


main()
