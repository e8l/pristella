import pytest
import sys
sys.path.append("..")
from pristella.config_loader import ConfigLoader
from pristella.twitter_app import TwitterApp


class TestClass(object):
    def test_1(self):
        cfgLoader = ConfigLoader("../config/settings.json")
        twitter = TwitterApp(cfgLoader)

        assert twitter.do() is not False
