"""Wrapper of Twitter API

A simple wrapper of Twitter API.
This supports
* authorize
* tweet(with pictures)
* upload pictures
"""


from rauth import OAuth1Service
from rauth import OAuth1Session
import os.path as path


class Twitter:
    """
    Wrapper class of Twitter API
    """

    def __init__(self, keys):
        """
        :param Dict keys: a Dict instance contains consumer keys
        """

        if "consumer_key" not in keys or "consumer_secret" not in keys:
            raise KeyError("consumer_key and consumer_secret are necessary.")

        self.__request = OAuth1Service(
            name="twitter",
            consumer_key=keys["consumer_key"],
            consumer_secret=keys["consumer_secret"],
            request_token_url="https://api.twitter.com/oauth/request_token",
            access_token_url="https://api.twitter.com/oauth/access_token",
            authorize_url="https://api.twitter.com/oauth/authorize",
            base_url="https://api.twitter.com/1.1/")

        # when already authorized
        if "access_token" in keys and "access_token_secret" in keys:
            self.__session = OAuth1Session(
                consumer_key=keys["consumer_key"],
                consumer_secret=keys["consumer_secret"],
                access_token=keys["access_token"],
                access_token_secret=keys["access_token_secret"],
                service=self.__request)
        else:
            self.__session = None

    def authorize(self):
        """
        :rtype: (str, str)
        :return: taple of access token and token secret.

        Authorize Twitter App.
        """
        if self.__session is not None:
            return (self.__session.access_token,
                    self.__session.access_token_secret)

        (request_token,
         request_token_secret) = self.__request.get_request_token()
        authorize_url = self.__request.get_authorize_url(
            request_token)

        print("Please get a PIN and enter it!")
        print("Access below URL in your Browser.")
        print(authorize_url, "\n")
        print("Enter PIN: ", end="")
        pin = input()

        self.__session = self.__request.get_auth_session(
            request_token, request_token_secret,
            method="POST", data={"oauth_verifier": pin})

        return (self.__session.access_token,
                self.__session.access_token_secret)

    def tweet(self, text):
        """
        :param str text: content of tweet

        Tweet only text.
        """

        if self.__session is None:
            return False

        return self.__session.post(
            "statuses/update.json",
            data={"status": text}).json()

    def __uploadPictures(self, filePaths):
        """
        :type filepaths: list[str]
        :param filepaths: list of path of picture
        :rtype: list
        :return: list of media_id(success) or None(failure)

        Upload Pictures.
        """
        result = []
        MAX_SIZE = 5 * 1024 * 1024  # bytes = 5MiB

        for filePath in filePaths:
            if not path.exists(filePath):
                result.append(None)
                continue

            if path.getsize(filePath) > MAX_SIZE:
                result.append(None)
                continue

            image = open(filePath, "rb")
            media = {"media": image.read()}

            responce = self.__session.post(
                "https://upload.twitter.com/1.1/media/upload.json",
                files=media).json()

            image.close()

            result.append(responce.get("media_id", None))

        return result

    def tweetWithPictures(self, text, filePaths):
        """
        :param str text: content of tweet
        :type filepaths: list[str]
        :param filepaths: list of path of picture
        :return: json(Dict, success) or False(failure)

        Tweet with pictures.
        You can upload up to 4 pictures at once
        """

        if self.__session is None:
            return False

        if len(filePaths) > 4:
            filePaths = filePaths[:4]

        uploaded = self.__uploadPictures(filePaths)
        uploaded = [x for x in uploaded if x is not None]

        if len(uploaded) == 0:
            return False

        return self.__session.post(
            "statuses/update.json",
            data={"status": text, "media_ids": uploaded}).json()

    def postPictures(self, filePaths):
        """
        :type filepaths: list[str]
        :param filepaths: list of path of picture
        :return: json(Dict, success) or False(failure)

        Tweet only pictures.
        You can upload up to 4 pictures at once
        """

        return self.tweetWithPictures("", filePaths)
