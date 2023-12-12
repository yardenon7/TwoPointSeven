"""
author: Yarden Hadas
Date: 11/12
Description: The functions that return what the client ask for. The options for the possible actions it can do are
explained in the server
"""
import glob
import os
import shutil
import subprocess
from PIL import ImageGrab

FAILED_DIR = "the dir has failed"
UNFINED_FOLDER_DIR = "the folder you asked for doesn't exist in this computer"
SUCCEED_DELETE = "the file was deleted successfully"
UNFINED_FILE_DELETE = "the file doesn't exist"
FAILED_DELETE = "the file wasn't deleted successfully"
SUCCEED_COPY = "the file was copied successfully"
FAILED_COPY = "the file wasn't copied successfully"
SUCCEED_EXECUTE = "the software was opened successfully"
FAILED_EXECUTE = "the software wasn't opened successfully"
SUCCEED_SCREENSHOT = "the screenshot was taken successfully"
FAILED_SCREENSHOT = "the screenshot wasn't taken successfully"
FAILED_PHOTO_SEND = "the screenshot wasn't sent successfully"


def ask_for_dir(request):
    """
    :param request: the request the client want to ask the server. DIR ....
    :return: a list of the files, if the directory doesn't exist return a matching response.
    """
    try:
        name_of_tikia = request[4:] + "/*.*"
        if os.path.isdir(request[4:]):
            files_list = glob.glob(name_of_tikia)
            return files_list
        else:
            return UNFINED_FOLDER_DIR

    except Exception:
        return FAILED_DIR


def ask_for_remove(request):
    """
    :param request: the request the client want to ask the server. Delete a file. DELETE ....
    :return: return a message that says if the file was deleted successfully or not.
     Will return the file doesn't exist if the file wasn't existing at first
    """
    try:
        name_of_file = request[7:]
        if os.path.isfile(request[7:]):
            os.remove(name_of_file)
            return SUCCEED_DELETE
        else:
            return UNFINED_FILE_DELETE
    except Exception:
        return FAILED_DELETE


def ask_for_copy(request):
    """
    :param request: the request the client want to ask the server. Copy one file to a directory. COPY ....
    :return: return a message that says if the file was copied successfully or not.
    Note: between the file and the directory THE CLIENT NEED TO PUT '$' SIGNAL.
    """
    try:
        copy_files = request[5:]
        index_of_space = copy_files.find('$')
        the_copied_file = copy_files[0:index_of_space]
        index_of_space = index_of_space + 1
        to_where_is_copied = copy_files[index_of_space:]
        shutil.copy(the_copied_file, to_where_is_copied)
        return SUCCEED_COPY
    except Exception:
        return FAILED_COPY


def ask_for_execute(request):
    """
    :param request: the request the client want to ask the server. Start a software. EXECUTE ....
    :return: return a message that says if the software was opened successfully or not.
    """
    try:
        name_of_software = request[8:]
        subprocess.call(name_of_software)
        return SUCCEED_EXECUTE
    except Exception:
        return FAILED_EXECUTE


def ask_for_take_screenshot(request):
    """
    :param request: the request the client want to ask the server. Takes a screenshot. TAKE SCREENSHOT
    :return: return a message that says if the screenshot was taken successfully or not. Put the image in a file called
    my_image.png
    """
    try:
        filepath = 'my_image.png'
        screenshot = ImageGrab.grab()
        screenshot.save(filepath, 'PNG')
        return SUCCEED_SCREENSHOT
    except Exception:
        return FAILED_SCREENSHOT


def ask_for_photo_send(request):
    """
    :param request: the request the client want to ask the server. Send the photo to the client. PHOTO SEND
    :return: return a message that says if the image wasn't sent successfully or the image doesn't exist. If the image was sent, return the image
     in bytes
    """
    try:
        with open(r'my_image.png', "rb") as f:
            image = f.read()
        return image
    except Exception as err:
        return FAILED_PHOTO_SEND
