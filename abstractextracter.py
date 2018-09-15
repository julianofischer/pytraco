import abc


class Extracter(abc.ABC):
    @abc.abstractmethod
    def extract_events(self, line):
        pass
