"""Twitter Application for pristella

An Implementation of App.
This app tweet with pictures that webcam takes.
"""


from .app import App
from .twitter import Twitter
import subprocess
import os


class TwitterApp(App):
    """
    An Subclass of App specialized Twitter.
    """

    def __init__(self, config):
        """
        :type config: ConfigLoader
        :param config: instance that loaded settings.json
        """

        self.__config = config

        if self.__config.data is None:
            self.__settings = self.__config.load()
        else:
            self.__settings = self.__config.data

        self.__twitter = Twitter(self.__settings)
        if "access_token" not in self.__settings \
                or "access_token_secret" not in self.__settings:
            (at, ats) = self.__twitter.authorize()
            self.__settings["access_token"] = at
            self.__settings["access_token_secret"] = ats
            self.__config.save()

        dir = os.path.abspath(
            os.path.expanduser(
                os.path.dirname(self.__settings["photo_path"])))
        if not os.path.exists(dir):
            os.makedirs(dir)

    def do(self):
        """
        :return: json(Dict, success) or False(failure)

        Take photo by webcam and post Twitter.
        """
        return self.__post()

    def __post(self):
        cmd = self.__settings["webcam_command"].strip().split(" ")
        cmd.extend([self.__settings["photo_path"].strip()])

        ret = subprocess.call(cmd,
                              stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)

        if ret is not 0:
            raise Exception("cannot take photo")

        return self.__twitter.postPictures([self.__settings["photo_path"]])
