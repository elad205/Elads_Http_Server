from RequestHandler import *
import socket

"""
Description     : Http server
Author          : Elad Cynamon
Exercise Number : 4.4
File Name       : Server.py
Date            : 05.03.2018
Version         : 1.0
"""


class Server(object):
    """
    this class represents a basic server.
    """
    def __init__(self, name, ip, port, debug_flag=True):
        super(Server, self).__init__()
        self.__name = name
        self.__ip = ip
        self.__port = port
        self.__server_socket = self.establish_connection()
        self.__client_socket = None
        self.__debug = debug_flag
        self.__new_handler = None

    def establish_connection(self):
        """
        this function establishes the socket and binds it with the ip and port.
        :return:  a binded server socket
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:

            server_socket.bind((self.__ip, self.__port))
        except OSError:
            server_socket = None
        return server_socket

    def bind_connection(self, number_of_clients):
        """
        this function creates the connection between the server and the client
        :param number_of_clients: the number of clients to listen for
        :return: if binded or not
        """
        self.__server_socket.settimeout(8)
        client_socket = None
        while not client_socket:
            try:
                print("Try to listen")
                self.__server_socket.listen(number_of_clients)
                client_socket, address = self.__server_socket.accept()
            except KeyboardInterrupt:
                self.exit()
                self.__server_socket.close()
                exit(1)
            except socket.error:
                client_socket = None
        self.__client_socket = client_socket
        #  -----debug--#
        if self.__debug:
            if self.__client_socket:
                print("established connection with: {0}, "
                      .format(self.__client_socket))
            else:
                print("the client socket is set to None")
        #  ---------------

        if client_socket:
            # creates a request handler to take care of the clients requests.
            self.__new_handler = RequestHandler(self.get_client_socket(),
                                                self.__name,
                                                self.__debug)
            return True
        else:
            return False

    def exit(self):
        #  closes the server socket
        self.__server_socket.close()

    def get_client_socket(self):
        return self.__client_socket

    def get_server_socket(self):
        return self.__server_socket

    def get_handler(self):
        return self.__new_handler
