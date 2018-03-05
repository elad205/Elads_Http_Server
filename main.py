from Server import *

"""
Description     : Http server
Author          : Elad Cynamon
Exercise Number : 4.4
File Name       : main.py
Date            : 05.03.2018
Version         : 1.0
"""


def main(debug):
    new_server = Server("Elads server", "127.0.0.1", 8007, debug)
    if debug:
        print(new_server)
    if debug and new_server.get_server_socket() is None:
        print("the connection is not available- couldn't create a server "
              "socket")
    if new_server.get_server_socket() is None:
        exit(1)

    while True:
        #  first request from client
        while True:
            if debug:
                print("iterating over send loop")
            new_server.bind_connection(0)
            new_server.get_handler().receive_request(new_server.
                                                     get_client_socket(), 2100)

        print("closed connection")


if __name__ == '__main__':
    main(False)
