# coding: utf-8

__author__ = "Juliano Fischer Naves"


class Event:
    def __init__(self, from_node, to_node, time, is_opening):
        self.from_node = from_node
        self.to_node = to_node
        self.time = time
        self.is_opening = is_opening

    def opening_status(self):
        return "up" if self.is_opening else "down"

    def __str__(self):
        return "event [%d,%d,%d,%s]" % (self.time, self.from_node, self.to_node, self.opening_status())


class Connection:
    def __init__(self, upevent, downevent):
        self.from_node = upevent.from_node
        self.to_node = upevent.to_node
        self.init_time = upevent.time
        self.end_time = downevent.time

    def duration(self):
        assert self.end_time, "end_time was not set - unable to compute duration"
        return self.end_time - self.init_time

    def get_id(self):
        return str(min(self.from_node, self.to_node)) + ":"+str(max(self.from_node, self.to_node))

    def is_same_connection(self, c):
        return (c.from_node == self.from_node and self.to_node == c.to_node) or (
            c.from_node == self.to_node and c.to_node == self.from_node)

    def __str__(self):
        end = self.end_time if self.end_time is not None else -1
        return "connection [%d, %d, %d, %d]" % (self.init_time, self.from_node, self.to_node, end)
