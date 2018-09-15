# coding: utf-8
__author__ = "Juliano Fischer Naves"

from connections import Event
from abstractextracter import Extracter


class HyccupsExtracter(Extracter):

    def extract_events(self, line):
        events = []
        from_node, to_node, init, duration = [int(i) for i in line.split(',')]
        from_node -= 1
        to_node -= 1

        # ONE time is given in seconds
        init = init//1000
        duration = duration//1000

        upevent = Event(from_node, to_node, init, is_opening=True)
        downevent = Event(from_node, to_node, init + duration, is_opening=False)
        events.append(upevent)
        events.append(downevent)
        return events


