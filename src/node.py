class Node:
    def __init__(self, name):
        self.name = name

        self.P = None

        self.pipes_in = []
        self.pipes_out = []

    def set_pressure(self, P):
        self.P = P

