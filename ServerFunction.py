import socket
import logging
import glob
import os
import shutil
import subprocess
from PIL import Image, ImageGrab



def ask_for_dir(request):
    try:
        name_of_tikia = request[4:] + "/*.*"
        files_list = glob.glob(name_of_tikia)
        return files_list
    except Exception as err:
        return "the dir has failed"


def ask_for_remove(request):
    try:
        name_of_file = request[7:]
        os.remove(name_of_file)
        return "the file was deleted successfully"
    except Exception as err:
        return "the file wasn't deleted successfully"

def ask_for_copy(request):
    try:
        copy_files = request[5:]
        index_of_space = copy_files.find('$')
        the_copied_file = copy_files[0:index_of_space]
        index_of_space = index_of_space + 1
        to_where_is_copied = copy_files[index_of_space:]
        shutil.copy(the_copied_file, to_where_is_copied)
        return "the file was copied successfully"
    except Exception as err:
        return "the file wasn't copied successfully"

def ask_for_execute(request):
    try:
        name_of_software = request[8:]
        print(name_of_software)
        subprocess.call(name_of_software)
        return "the software was opened successfully"
    except Exception as err:
        return "the software wasn't opened successfully"


def ask_for_take_screenshot(request):
    try:
        filepath = 'my_image.png'
        screenshot = ImageGrab.grab()
        screenshot.save(filepath, 'PNG')
        return "the screenshot was taken successfully"
    except Exception as err:
        return "the screenshot wasn't taken successfully"


def ask_for_photo_send(request):
    try:
        with open(r'my_image.png', "rb") as f:
            image = f.read()
        return image
    except Exception as err:
        return "the screenshot wasn't sent successfully"

