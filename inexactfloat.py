class InexactFloat(float):
    def __eq__(self, other):
        try:
            return abs(self.real - other) / (0.5 * (abs(self.real) + abs(other))) < 0.0001
        except ZeroDivisionError:
            # Could do another inexact comparison here, this is just an example:
            return self.real == other

    def __ne__(self, other):
        return not self.__eq__(other)