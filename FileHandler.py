import os
import re

"""
Description     : Http server- File handler class file
Author          : Elad Cynamon
Exercise Number : 4.4
File Name       : FileHandler.py
Date            : 05.03.2018
Version         : 1.0
"""


class FileHandler(object):

    START_CONST = "index.html"
    # this dictionary contains all the files that were moved to another
    # location
    # for example: "{0}js{0}box.js".format(os.sep): "{0}imgs{0}box.js".
    # format(os.sep)
    moved_files = {}

    def __init__(self, filename, debug):
        super(FileHandler, self).__init__()
        self.__file_name = self.validate_file_request(filename)
        self.__debug = debug
        if self.__debug:
            print("file name = {}".format(self.__file_name))

    @staticmethod
    def validate_file_request(filename):
        """
        this function gets a relative filename from the client and checks
        if it exists and if so gets the full path that is needed in order
        to open the file
        :param filename: a relative path that was gotten from the server
        :return: a full path or an error code if the path is invalid
        """
        #  if the request is for the root file
        if filename == "/" and os.path.isfile(FileHandler.START_CONST):
            return FileHandler.START_CONST
        # if there was not a file name
        elif filename is None:
            return None
        # check if the file name exists
        else:
            # fix abspath for windows
            if os.name == 'nt':
                filename = "." + filename
            filename2 = os.path.abspath(
                filename.replace("{}".format(os.sep), "", 1))
        if os.path.isfile(filename2):
            return filename2
        elif filename in FileHandler.moved_files:
            FileHandler.moved_files["moved"] = \
                FileHandler.moved_files[filename]
            return "moved"
        else:
            return "Not Found"

    def prepare_file(self):
        """
        this function takes the file,opens him and turns him into a string-
        so it could be sent
        :return:
        """
        if self.__file_name and self.__file_name != "Not Found" and self\
                .__file_name != "moved":
            with open(self.__file_name, 'rb') as file1:
                data = file1.read()
        else:
            data = None

        return data

    def set_filename(self, new_file):
        self.__file_name = self.validate_file_request(new_file)

    def get_filename(self):
        return self.__file_name

    @staticmethod
    def extract_file_name(string):
        """
        filters the filename from the valid http request and returns the-
        raw filename
        :param string: the valid http request
        :return: the filename and if not found then None.
        """
        file_name = re.search("\A.*?\sHTTP", string)
        if file_name:
            file_name = file_name.group(0)
            file_name = file_name.replace("GET", "", 1)
            file_name = file_name.replace("HTTP", "", 1)
            file_name = file_name.strip()
            return file_name
        else:
            return "Not Found"

    @staticmethod
    def get_only_name(string):
        """
        this function gets only the name of the string
        :param string:
        :return:
        """
        name = re.search("'{0}'.[^'{0}']*?$".format(os.sep), string)
        if name:
            return name.group(0)
        else:
            return ""
