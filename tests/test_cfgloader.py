import pytest
import copy
import sys
sys.path.append("..")
from pristella.config_loader import ConfigLoader


class TestClass(object):
    def test_1(self):
        """Load Config File and json check
        """
        json = ConfigLoader("../config/test.json")
        json.load()

        assert json.data["hoge"] == "fuga"
        assert json.data["foo"] == "bar"
        assert json.data["baz"] == 123

    def test_2(self):
        """Save Config File
        """
        json = ConfigLoader("../config/test.json")
        json.load()

        json.data["added"] = "done"

        assert json.save()

        json2 = ConfigLoader("../config/test.json")
        json2.load()

        assert json2.data["added"] == "done"

        del json2.data["added"]
        assert json2.save()

        json3 = ConfigLoader("../config/test.json")
        json3.load()

        assert "added" not in json3.data

