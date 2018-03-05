from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
from FileHandler import *

"""
Description     : Http server- response handler class file
Author          : Elad Cynamon
Exercise Number : 4.4
File Name       : ResponseHandler.py
Date            : 05.03.2018
Version         : 1.0
"""


class ResponseHandler(object):
    """
    this class handles everything that belongs to making the response for
    the client
    """
    # this is a dictionary of all the file expansions that the server can-
    # support.
    EXTENSION_DICT = {".js": "Content-Type: text/javascript; charset=UTF-8",
                      ".css": "Content-Type: text/css", ".jpg":
                          "Content-Type: image/jpeg", ".txt": "Content-Type: "
                                                              "text/html; "
                                                              "charset=utf-8",
                      ".html": "Content-Type: text/html; charset=utf-8",
                      ".ico": "Content-Type: image/x-icon"}
    # this is a dictionary of all the errors that the server can support
    STATUS_CODES = {None: "500 Internal Server Error",
                    "Not Found": "404 Not Found",
                    "forbidden": "403 Forbidden", "moved": "302 Found",
                    "ok": "200 OK"}

    # this list contains all the files that the client cant access
    # for example put \box.js in the list to make the file unavailable
    FORBIDDEN_FILES = []

    def __init__(self, raw_data, name, filename):
        super(ResponseHandler, self).__init__()
        self.__raw_data = raw_data
        self.__server_name = name
        self.__file_name = filename
        self.__response = self.coat_header()

    def coat_header(self):
        """
        this function assembles the header according to the http1.1 protocol
        and takes in place all the errors and parameters in order to make
        the header.
        :return: a fully working header according to the http1.1 protocol
        """
        # check which status coed is active
        if self.__raw_data and FileHandler.get_only_name(self.__file_name) \
                not in self.FORBIDDEN_FILES:
            #  if everything is ok
            key = "ok"
            length = len(self.__raw_data) + 1
            html_type = None
        else:
            # if there is some kind of error check which error is it.
            if FileHandler.get_only_name(self.__file_name) in \
                    self.FORBIDDEN_FILES:
                self.__file_name = "forbidden"
            key = self.__file_name
            # assemble a response page with the correct error
            html_type = "<!doctype html><body>{}<body>".\
                format(self.STATUS_CODES[self.__file_name])
            length = len(html_type.encode())
            if self.__file_name == "moved":
                length = 0
        now = datetime.now()
        stamp = mktime(now.timetuple())
        stamp = format_date_time(stamp)
        # make the header
        temp_packge = "HTTP/1.1 {3}\r\nDate: {0}\r\nServer: {1}" \
                      "\r\nContent-Length: {2} \r\n".format(stamp,
                                                            self.__server_name,
                                                            length, self.
                                                            STATUS_CODES[key])
        if key == "ok":
            extension = re.search("\..[^.]*?$", self.__file_name)
            if extension:
                extension = extension.group(0)
                return temp_packge + ResponseHandler.EXTENSION_DICT[extension]\
                    + " \r\n\r\n"
        elif self.__file_name == "moved":
            # make a new file location to the server for error 302
            a = temp_packge + "Location: {} \r\n\r\n".format(
                FileHandler.moved_files["moved"])
            FileHandler.moved_files.__delitem__("moved")
            return a
        else:
            return temp_packge + "\r\n" + html_type

    def send_response(self, client_socket):
        """
        this function sends the complete response to the client
        :param client_socket: the client to send the information to
        :return: True
        """
        if self.__raw_data:
            self.__response = self.__response.encode() + self.__raw_data + \
                              b'\n\r'
        else:
            self.__response = self.__response.encode()
        client_socket.send(self.__response)
        return True

    def set_file_name(self, file):
        self.__file_name = file

    def set_data(self, data):
        self.__raw_data = data

    def set_response(self):
        self.__response = self.coat_header()
