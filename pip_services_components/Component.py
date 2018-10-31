# -*- coding: utf-8 -*-
"""
    pip_services_container.Component
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Component implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from pip_services_commons.config import IConfigurable
from pip_services_components.log import CompositeLogger
from pip_services_components.count import CompositeCounters
from pip_services_commons.refer import IReferenceable
from pip_services_commons.refer import DependencyResolver

class Component(IConfigurable, IReferenceable):
    """
    Abstract component that supportes configurable dependencies, logging and performance counters.

    ### Configuration parameters ###

        - dependencies:
            - [dependency name 1]: Dependency 1 locator (descriptor)
            - ...
            - [dependency name N]: Dependency N locator (descriptor)

    ### References ###
        - *:counters:*:*:1.0     (optional) [[ICounters]] components to pass collected measurements
        - *:logger:*:*:1.0       (optional) [[ILogger]] components to pass log messages
        - ...                                    References must match configured dependencies.
    """
    _logger = None
    _counters = None
    _dependency_resolver = None

    def __init__(self):
        self._logger = CompositeLogger()
        self._counters = CompositeCounters()
        self._dependency_resolver = DependencyResolver()

    def configure(self, config):
        """
        Configures component by passing configuration parameters.

        :param config: configuration parameters to be set.
        """
        self._dependency_resolver.configure(config)
        self._logger.configure(config)

    def set_references(self, references):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        self._dependency_resolver.set_references(references)
        self._logger.set_references(references)
        self._counters.set_references(references)
