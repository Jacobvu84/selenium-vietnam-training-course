__author__ = 'jacob@vsee.com'

import os
import sys
import logging

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.navigate_steps import NavigateSteps
from steps.backend.room.room_steps import RoomSteps
from steps.backend.room.room_setting import RoomSettingSteps

from model.room import RoomData

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.logger import setup_logger
from util.console import start_test
from util.support import mkdir
from util.support import TEMP_DIR_WIN
from util.support import create_gif
from resource import ODTC

testID = sys.argv[1]  # test case ID


def create_room():
    # Objects
    _actor = LoginSteps()
    _navigate = NavigateSteps()
    _room = RoomSteps()
    data = RoomData()
    _room_setting = RoomSettingSteps()
    odtc = ODTC()

    mkdir("bin")
    setup_logger('room', TEMP_DIR_WIN + 'bin\\neuro_room.log', level=logging.DEBUG)
    log = logging.getLogger('room')

    try:
        _actor \
            .visit_neuro() \
            .login_as(username="admin", password="Evc0nnect=")

        _navigate.goto_room_screen()
        neuro_rooms = data.get_neuro_rooms()

        for room in neuro_rooms[0:2]:
            """[TEST] CREATE A ROOM"""
            log.debug(room.url + "," + room.slug + "," + room.code + "," + room.name + ",[end]")
            _room.add_new_room(room).should_see_the_room_in_room_table()

        room = odtc.get_neuro_room()
        code = room[0].split(",")[2]
        _room.edit_room(code)
        _room_setting.description("Hello, I am Baymax, your personal healthcare companion")

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
    create_room()


main()
