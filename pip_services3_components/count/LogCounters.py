# -*- coding: utf-8 -*-
"""
    pip_services3_components.counters.LogCounters
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Log counters implementation
    
    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""

from .CachedCounters import CachedCounters
from .CounterType import CounterType
from ..log.CompositeLogger import CompositeLogger
from pip_services3_commons.convert.StringConverter import StringConverter
from pip_services3_commons.refer.IReferenceable import IReferenceable

class LogCounters(CachedCounters, IReferenceable):
    """
    Performance counters that periodically dumps counters measurements to logger.

    ### Configuration parameters ###

        - options:
            - interval:          interval in milliseconds to save current counters measurements (default: 5 mins)
            - reset_timeout:     timeout in milliseconds to reset the counters. 0 disables the reset (default: 0)

    ### References ###
        - *:logger:*:*:1.0           [[ILogger]] components to dump the captured counters
        - *:context-info:*:*:1.0     (optional) [[ContextInfo]] to detect the context id and specify counters source

    Example:
        counters = LogCounters()
        counters.set_references(References.from_tuples(
                    Descriptor("pip-services", "logger", "console", "default", "1.0"), ConsoleLogger()))

        counters.increment("mycomponent.mymethod.calls")
        timing = counters.begin_timing("mycomponent.mymethod.exec_time")
        ...
        timing.endTiming()
    """
    _logger = None

    def __init__(self):
        """
        Creates a new instance of the counters.
        """
        super(LogCounters, self).__init__()
        self._logger = CompositeLogger() 

    #
    # def get_descriptor(self):
    #     return LogCountersDescriptor


    def set_references(self, references):
        """
        Sets references to dependent components.

        :param references: references to locate the component dependencies.
        """
        self._logger.set_references(references)


    def _counter_to_string(self, counter):
        result = "Counter " + counter.name + " { "
        result += "\"type\": " + str(counter.type)
        if counter.last != None:
            result += ", \"last\": " + StringConverter.to_string(counter.last)
        if counter.count != None:
            result += ", \"count\": " + StringConverter.to_string(counter.count)
        if counter.min != None:
            result += ", \"min\": " + StringConverter.to_string(counter.min)
        if counter.max != None:
            result += ", \"max\": " + StringConverter.to_string(counter.max)
        if counter.average != None:
            result += ", \"avg\": " + StringConverter.to_string(counter.average)
        if counter.time != None:
            result += ", \"time\": " + StringConverter.to_string(counter.time)
        result += " }"
        return result

    @staticmethod
    def _get_counter_name(counter):
        return counter.name

    def _save(self, counters):
        """
        Saves the current counters measurements.

        :param counters: current counters measurements to be saves.
        """
        if self._logger == None:
            return
        if len(counters) == 0:
            return

        # Sort counters by name
        counters = sorted(counters, key=LogCounters._get_counter_name)

        for counter in counters:
            self._logger.info("counters", self._counter_to_string(counter))
