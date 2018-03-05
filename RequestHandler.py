from ResponseHandler import *
import socket

"""
Description     : Http server- Request Handler class file
Author          : Elad Cynamon
Exercise Number : 4.4
File Name       : RequestHandler.py
Date            : 05.03.2018
Version         : 1.0
"""


class RequestHandler(object):
    """
    this class is a Request handler.
    it takes care of everything that belongs to the request of the client
    """
    def __init__(self, client_socket, server_name, debug=False):
        super(RequestHandler, self).__init__()
        self.__client_socket = client_socket
        self.__server_name = server_name
        self.__debug = debug
        self.__file_handler = None
        self.__response_handler = None

    def receive_request(self, active_socket, size_to_receive):
        """
        gets the http request from the client
        :param active_socket: the client socket that was established
        :type: socket
        :param size_to_receive: the size of data to expect from the client
        :return: the data that was received.
        """
        self.__client_socket = active_socket
        data = None
        if self.__debug:
            print("waiting for information")
        try:
            data = active_socket.recv(size_to_receive).decode()
            if not data:
                return None
        except socket.timeout and ConnectionResetError:
            print("timed out")
            return False
        except KeyboardInterrupt:
            self.__client_socket.close()
            exit(1)

        # debug--------------
        if self.__debug:
            print("the data received: {}".format(data))
        #  ------------------

        answer = self.verify_http_request(data)
        if self.__debug:
            print("verified answer: {}".format(answer))
        if not answer:
            if self.__debug:
                print("got unknown request")
            file_name = None
        else:
            #  if a valid answer was gotten
            answer = answer.group(0)
            file_name = FileHandler.extract_file_name(answer)
            if self.__debug:
                print("file name is: {}".format(file_name))

        if not self.__file_handler:
            # if it is the first time running the server so create handler-
            # objects in order to extract the files needed
            self.__file_handler = FileHandler(file_name, self.__debug)
            raw_file = self.__file_handler.prepare_file()
            self.__response_handler = ResponseHandler(raw_file,
                                                      self.__server_name,
                                                      self.__file_handler.
                                                      get_filename())
            # send the finished response to the client
            return self.__response_handler.send_response(active_socket)
        else:
            # if there is already a handler objects so set all params again
            self.__file_handler.set_filename(file_name)
            raw_file = self.__file_handler.prepare_file()
            self.__response_handler.set_file_name(
                self.__file_handler.get_filename())
            self.__response_handler.set_data(raw_file)
            self.__response_handler.set_response()
            self.__response_handler.send_response(active_socket)

    @staticmethod
    def verify_http_request(req):
        """ 
        checks if the request is valid- is a GET request and follows the
        protocols.
        :param req: the http request
        :return: re object- None if a math wasn't found
        """
        is_http = re.search("GET\s.*\sHTTP/.*\s\s", req)
        return is_http

    def close_client(self):
        #  closes the client socket
        self.__client_socket.close()
