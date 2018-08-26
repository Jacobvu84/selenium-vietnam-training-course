__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.navigate_steps import NavigateSteps
from steps.backend.room.room_steps import RoomSteps

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif
from resource import ODTC

testID = sys.argv[1]  # test case ID


def add_visit_option_room():
    # Objects
    _actor = LoginSteps()
    _navigate = NavigateSteps()
    _room = RoomSteps()
    odtc = ODTC()

    try:

        room = odtc.get_snf_room()

        """[TEST] ADD NURSE TO ROOM"""
        _actor.visit_snf().login_as(username="admin", password="Evc0nnect=")
        _navigate.goto_room_screen()
        for index in range(0,2):
            code = room[0].split(",")[2]
            _room.edit_room(code)
            _room.assign_to(odtc.get_nurse_by("snf", index))

        print "[PASSED]: TEST PASSED"
    # Catch any exception from test failure
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
    add_visit_option_room()


main()
