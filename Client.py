"""
author: Yarden Hadas
Date: 11/12
Description: The Client. The computer that the engineer works on. Ask the server to do several actions
"""

import socket
import logging
from Protocol import *

logging.basicConfig(filename="log_client.log", level="DEBUG")
MAX_PACKET = 1024
IP = '127.0.0.1'
PORT = 1729
INVALID_COMMAND = "invalid command"


def checking_the_request(request):
    """
    :param request: the request the client want to ask the server
    :return: true of the request is valid and false otherwise
    """
    cmd = request.split(' ')[0]
    return (cmd == "DIR" or cmd == "DELETE" or cmd == "COPY" or cmd == "EXECUTE" or request == "TAKE SCREENSHOT" or
            request == "PHOTO SEND" or request == "EXIT")


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.connect((IP, PORT))
        response = ""
        while response != "done with the work":
            request = input("You can ask the following requests: DIR, DELETE, COPY (in that case, put an '$' between the"
                            " file and the directory, "
                            "EXECUTE, TAKE SCREENSHOT, "
                            "PHOTO SEND or EXIT. Enter the request: ")
            logging.debug("the request was: " + request)
            if checking_the_request(request):
                protocol_length_request_or_respond(my_socket, request)
                response = protocol_decryption_request(my_socket)
                if request != 'PHOTO SEND' or response == "the screenshot wasn't sent successfully":
                    print(response)
                    logging.debug("the response was: " + response)
                else:
                    with open('image.png', 'wb') as f:
                        f.write(eval(response))
                    logging.debug("the response was: the image")
            else:
                logging.debug("The request: " + request + " didn't return any data info")
                print(INVALID_COMMAND)
    except socket.error as err:
        print('received socket error ' + str(err))
    except KeyboardInterrupt:
        protocol_length_request_or_respond(my_socket, "EXIT")
        logging.debug("an error accord")
    finally:
        my_socket.close()


if __name__ == '__main__':
    """
    checking
    """
    assert checking_the_request("DELETE SOMETHING")
    assert checking_the_request("DIR SOMETHING")
    assert checking_the_request("COPY SOMETHING")
    assert checking_the_request("EXECUTE SOMETHING")
    assert checking_the_request("TAKE SCREENSHOT")
    assert checking_the_request("PHOTO SEND")
    assert checking_the_request("EXIT")
    assert not checking_the_request("")
    main()
