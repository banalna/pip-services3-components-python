# -*- coding: utf-8 -*-
"""
    pip_services3_components.config.CachedConfigReader
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Cached config reader implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from abc import ABC, abstractmethod

from pybars import Compiler

from pip_services3_commons.config import IConfigurable
from pip_services3_commons.config import ConfigParams
from .IConfigReader import IConfigReader


class ConfigReader(IConfigReader, IConfigurable, ABC):
    """
    Abstract config reader that supports configuration parameterization.

    ### Configuration parameters ###

    parameters:            this entire section is used as template parameters
        - ...
    """
    _parameters = None

    def __init__(self):
        """
        Creates a new instance of the config reader.
        """
        self._parameters = ConfigParams()

    def configure(self, config):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        parameters = config.get_section("parameters")
        if len(parameters) > 0:
            self._parameters = parameters

    @abstractmethod
    def read_config(self, correlation_id, parameters):
        """
        Reads configuration and parameterize it with given values.

        :param correlation_id: (optional) transaction id to trace execution through call chain.

        :param parameters: values to parameters the configuration or null to skip parameterization.

        :return: ConfigParams configuration.
        """
        raise NotImplementedError('Method is abstract and must be overriden')

    def _parameterize(self, config, parameters):
        """
        Parameterized configuration template given as string with dynamic parameters.

        :param config: a string with configuration template to be parameterized

        :param parameters: dynamic parameters to inject into the template

        :return: a parameterized configuration string.
        """
        compiler = Compiler()
        template = compiler.compile(config)
        parameters = self._parameters.override(parameters)
        return template(parameters)
