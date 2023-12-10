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
    return cmd == "DIR" or cmd == "DELETE" or cmd == "COPY" or cmd == "EXECUTE" or request == "TAKE SCREENSHOT" or request == "PHOTO SEND" or request == "EXIT"


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.connect((IP, PORT))
        response = ""
        while response != "done with the work":
            request = input("enter the request: ")
            logging.debug("the request was: " + request)
            if checking_the_request(request):
                protocol_length_request_or_respond(my_socket, request)
                response = protocol_decryption_request(my_socket)
                logging.debug("the response was: " + response)
                if request != 'PHOTO SEND' or response == "the screenshot wasn't sent successfully":
                    print(response)
                else:
                    with open('image.png', 'wb') as f:
                        f.write(eval(response))
            else:
                logging.debug("The request: " + request + " didn't return any data info")
                print(INVALID_COMMAND)
    except socket.error as err:
        print('received socket error ' + str(err))
    finally:
        my_socket.close()


if __name__ == '__main__':
    """
    checking
    """
    main()