"""
author: Yarden Hadas
Date: 19/11
Description: The server. Will return the time, random number between 1 and 10 and
the name of the server, depending on what the client asked. Could also end and start a new connection with another
client
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
    elif request == "EXIT":
        protocol_length_request_or_respond(client_socket, request)


def main():
    socketi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        socketi.bind((IP, PORT))
        socketi.listen(QUEUE_LEN)
        while True:
            client_socket, client_address = socketi.accept()
            try:
                request = protocol_decryption_request(client_socket)
                while request != EXIT:
                    send_request(request, client_socket)
                    #protocol_length_request_or_respond(client_socket, request)
                    request = protocol_decryption_request(client_socket)
            except socket.error as err:
                print('received socket error on client socket' + str(err))
            finally:
                protocol_length_request_or_respond(client_socket, LAST_MASSAGE)
                client_socket.close()
    except socket.error as err:
        print('received socket error on server socket' + str(err))
    finally:
        socketi.close()


# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    """
     checking
     """
    main()


