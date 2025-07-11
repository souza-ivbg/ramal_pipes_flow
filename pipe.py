import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

class Pipe:
    def __init__(self, diameter, length, f, k, d_unit='m'):
        self.diameter = diameter
        self.length = length
        self.f = f
        self.k = k
        self.d_unit = d_unit

        if self.d_unit == 'mm':
            self.diameter = diameter / 1000
        elif self.d_unit == 'pol':
            self.diameter = diameter* 0.0508

    def calculate_pressure(self, mass_flow, position=None):
        if position is None:
            position = self.length
        pass

    def calculate_flow(self):
        pass



