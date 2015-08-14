import pytest
import sys
import os.path as path
sys.path.append("..")
from pristella.config_loader import ConfigLoader
from pristella.twitter import Twitter


cfgLoader = ConfigLoader("../config/settings.json")
keys = cfgLoader.load()
twitter = Twitter(keys)


class TestClass(object):
    def test_1(self):
        res = twitter.tweet("This is test.\n日本語 あいうえお")

        assert res is not False

    def test_2(self):
        res = twitter.tweetWithPictures(
            "Tweet with Picture.",
            [path.abspath(path.join(path.dirname(__file__), "test.png"))])

        assert res is not False
