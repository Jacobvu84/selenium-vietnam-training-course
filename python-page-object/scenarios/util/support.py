__author__ = 'jacob@vsee.com'

import platform
import os
import sys
import errno
import subprocess
from waiting import wait
import time
from setting import _empty_log
from setting import _record_screen


sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from webium.core.robot.pyrobot import Robot, Keyboard

testID = sys.argv[1]  # test case ID

# Windows evn on VM
TEMP_DIR_WIN = "C:\\tempdir\\"
DOWNLOAD_DIR_WIN = "C:\\Users\\vsee\\downloads\\"
WORKING_DIR_WIN = "C:\\tempFiles\\"  # vsee.exe and webdrivers are in here
TEMP_DIR_MAC = "/Users/vsee/Documents/tempDIR/"  # save screen shot and others here
TARGET = TEMP_DIR_WIN + testID + "\\"


def capture_screenshot(img_name):
    path_pic = TARGET + img_name
    # create an instance of the class
    robot = Robot()
    im = robot.take_screenshot()
    # Save the PIL Image to disk
    im.save(path_pic, 'png')
    return True

def capture_screenshot_browser(img_name, _driver):
    try:
        path_pic = TARGET + img_name
        _driver.save_screenshot(path_pic)
        return True
    except:
        return False


def create_gif(filenames=TARGET, duration=0.4):
    print "This feauture is implementing"
    print _record_screen
    """
    import imageio
    if 'TURN_ON' == record_screen:
        print "This feauture is implementing"
        
       images = []
        for filename in os.listdir(filenames):
            img = TARGET+filename
            if img.endswith(".png"):
                images.append(imageio.imread(img))
        output_file = TARGET + 'Gif-%s.gif' % str(datetime.datetime.now()).replace("-", "").replace(" ", "").replace(":", "")
        imageio.mimsave(output_file, images, duration=duration)
    """


def check_file():
    """
    Verify the file is existed in the folder
    """
    time.sleep(5)
    path, dirs, files = os.walk(DOWNLOAD_DIR_WIN).next()
    file_count = len(files)
    print file_count
    print files
    if file_count == 2:  # desktop.ini and vsee*.exe
        for filename in os.listdir(DOWNLOAD_DIR_WIN):
            root, ext = os.path.splitext(filename)
            if root.startswith('vsee') and ext.endswith('.exe'):
                return True


def wait_for_vsee_downloaded():
    """
    Wait for downloading is completed with special time out
    """
    wait(lambda: check_file(), waiting_for='Wait For VSee Installer download',
         timeout_seconds=300)


def execute_file():
    """
    Execute vseeXXXX.exe to install VM on the device
    Need to sikuli support to process installing.
    Click on OK in popup: Complete installation
    """
    for file_exe in os.listdir(DOWNLOAD_DIR_WIN):
        if "vsee" in file_exe:
            vsee_installer = DOWNLOAD_DIR_WIN + file_exe
            subprocess.Popen(vsee_installer, stdout=subprocess.PIPE, shell=True)
    time.sleep(10)


def get_platform():
    """
    :return:
        - Linux: Linux
        - Mac: Darwin
        - Windows: Windows
    """
    return platform.system()


def empty_dir(dir_path):
    """
    Delete all of liles in the folder
    """
    if ("Windows" in get_platform()):
        command = "cmd.exe /c del /f /q {0}".format(dir_path)
        subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)


def empty_dir_download():
    """
    Delete all of liles in the download folder in the Windows
    """
    empty_dir(DOWNLOAD_DIR_WIN)


def empty_dir_target():
    """
    Delete all of liles in the target folder in the Windows
    """
    if 'YES' == _empty_log:
        empty_dir(TARGET)


def mkdir(folder):
    """
    :param folder:
        - is test case ID
    :return:
        - made dir to contains image log test
    """
    new_folder = ""
    try:
        if 'Darwin' in get_platform():
            new_folder = TEMP_DIR_MAC + folder
            if not os.path.isdir(TEMP_DIR_MAC):
                # shutil.rmtree(new_folder)
                os.mkdir(TEMP_DIR_MAC)
        else:
            new_folder = TEMP_DIR_WIN + folder
            # os.rmdir(new_folder)
        mkdir_command = "mkdir " + new_folder
        os.system(mkdir_command)
        return new_folder
    except (IOError, WindowsError) as e:
        print "The system cannot find the file specified {}".format(new_folder)


def mkdir_by_path(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as error:
            if error.errno != errno.EEXIST:
                raise
    return path
