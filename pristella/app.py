"""The interface of app_class

This file defines an interface
'app_class' class must implement
"""

from abc import ABCMeta, abstractmethod


class App(object, metaclass=ABCMeta):
    """
    Interface 'app_class' class must implement.
    In pristella_daemon.py, daemon first check
    if assigned 'app_class' class implements
    This interface. if not, daemon is stopped.
    """

    @abstractmethod
    def __init__(self, config):
        """
        :type config: ConfigLoader
        :param config: instance that loaded settings.json
        """
        pass

    @abstractmethod
    def do(self):
        """
        do anything you want to do
        """
        raise NotImplementedError()
