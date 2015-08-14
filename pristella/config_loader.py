"""Read/Write JSON File

Wrapper of JSON access.
"""

import os.path as path
import json


class ConfigLoader(object):
    """
    Wrapper class of json
    """

    def __init__(self, path):
        """
        :param str path: path of json
        """

        self.__configPath = path
        self.__check_path(self.__configPath)

        self.data = None

    def __check_path(self, pathStr):
        """
        :param str pathStr: path that will be checked

        Check if file exists
        """

        if not path.exists(pathStr):
            raise Exception("File not found: %s" % pathStr)

    def load(self):
        """
        :rtype: json(dict or list)
        :return: loaded JSON data

        load JSON data
        """

        configFile = open(self.__configPath, "r", encoding="utf-8")

        self.data = json.load(configFile)

        configFile.close()

        return self.data

    def save(self):
        """
        :return: True(success)

        save JSON data
        """

        configFile = open(self.__configPath, "w", encoding="utf-8")

        json.dump(self.data, configFile, sort_keys=True, indent=2)

        configFile.close()

        return True
