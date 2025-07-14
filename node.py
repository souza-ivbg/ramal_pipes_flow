import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

class Node:
    def __init__(self):
        self.P = None
        self.Q = None

        self.pipes_in = []
        self.pipes_out = []

    def set_pressure(self, P):
        self.P = P

    def flow_equation(self):
        for pipe in self.pipes_in:
            self.Q += pipe.Q
        for pipe in self.pipes_out:
            self.Q -= pipe.Q

        return self.Q