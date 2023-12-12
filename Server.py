"""
author: Yarden Hadas
Date: 11/12
Description: The server. The computer that the engineer ask data from. The engineer can ask for DIR, EXECUTE, DELETE, CO
PY, TAKE SCREENSHOT, PHOTO SEND OR EXIT
"""
import socket
import logging
from ServerFunction import *
from Protocol import *

logging.basicConfig(filename="log_server.log", level="DEBUG")
QUEUE_LEN = 1
IP = '0.0.0.0'
PORT = 1729
MAX_PACKET = 1024
EXIT = "EXIT"
LAST_MASSAGE = "done with the work"


def send_request(request, client_socket):
    """
    :param request: the request the client want to ask the server. client_socket:
    """
    cmd = request.split(' ')[0]
    if cmd == "DIR":
        protocol_length_request_or_respond(client_socket, ask_for_dir(request))
    elif cmd == "DELETE":
        protocol_length_request_or_respond(client_socket, ask_for_remove(request))
    elif cmd == "COPY":
        protocol_length_request_or_respond(client_socket, ask_for_copy(request))
    elif cmd == "EXECUTE":
        protocol_length_request_or_respond(client_socket, ask_for_execute(request))
    elif request == "TAKE SCREENSHOT":
        protocol_length_request_or_respond(client_socket, ask_for_take_screenshot(request))
    elif request == "PHOTO SEND":
        protocol_length_request_or_respond(client_socket, ask_for_photo_send(request))
    else:
        protocol_length_request_or_respond(client_socket, "invalid commands")


def main():
    socketi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        socketi.bind((IP, PORT))
        socketi.listen(QUEUE_LEN)
        while True:
            client_socket, client_address = socketi.accept()
            try:
                request = protocol_decryption_request(client_socket)
                logging.debug("the request was: " + request)
                while request != EXIT:
                    send_request(request, client_socket)
                    # protocol_length_request_or_respond(client_socket, request)
                    request = protocol_decryption_request(client_socket)
                    logging.debug("the request was: " + request)
            except socket.error as err:
                print('received socket error on client socket' + str(err))
            finally:
                protocol_length_request_or_respond(client_socket, LAST_MASSAGE)
                client_socket.close()
                logging.debug("the server has done connecting with the client")
    except socket.error as err:
        print('received socket error on server socket' + str(err))
    finally:
        socketi.close()


# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    """
    checking
    """
    assert ask_for_dir("DIR something") == "the folder you asked for doesn't exist in this computer"
    assert ask_for_remove("DELETE something") == "the file doesn't exist"
    assert ask_for_copy("COPY something") == "the file wasn't copied successfully"
    assert ask_for_execute("EXECUTE some") == "the software wasn't opened successfully"
    assert ask_for_take_screenshot("TAKE SCREENSHOT") == "the screenshot was taken successfully" or "the screenshot wasn't taken successfully"

    main()
