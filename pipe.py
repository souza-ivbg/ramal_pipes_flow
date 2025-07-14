'''
calculo do Q é feito no node
calculo da pressão é feito no pipe
tem que fazer a comunicação node <-> pipe

'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

class Pipe:
    def __init__(self, node_in, node_out, diameter, length, wall_roughness, rho, mu, d_unit='m'):
        self.node_in = node_in
        self.node_out = node_out

        node_in.pipes_out.append(self)
        node_out.pipes_in.append(self)

        self.diameter = diameter
        self.length = length

        self.P = None
        self.Q = None

        self.rho = rho
        self.mu = mu

        self.wall_roughness = wall_roughness
        self.d_unit = d_unit


        if self.d_unit == 'mm':
            self.diameter = diameter / 1000
        elif self.d_unit == 'pol':
            self.diameter = diameter* 0.0508

    def set_flow(self, Q):
        self.Q = Q

    def churchill_correlation(self,Re):
        eq_1 = 0.27 * self.wall_roughness
        eq_2 = np.power(7 / Re, 0.9)
        eq_3 = -2.457 * np.log(eq_1 + eq_2)
        A = np.power(eq_3, 16)
        B = np.power(37530 / Re, 16)
        eq_A = np.power(8 / Re, 12)
        eq_B = np.power(A + B, -1.5)

        return 8 * np.power(eq_A + eq_B, 1 / 12)


    def pressure_equation(self, P_in, Q, position=None):
        if position is None:
            position = self.length

        v = (4 * Q)/(np.pi * (self.diameter**2))
        Re = (self.diameter * v * self.rho)/self.mu
        f = self.churchill_correlation(Re)
        h_M = f * (self.length / self.diameter) * ((v**2)/2*9.81)

        return P_in - h_M * (self.rho*9.81)




