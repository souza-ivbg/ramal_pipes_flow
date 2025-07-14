import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve


class PipeSystem:
    def __init__(self):
        self.pipes = []
        self.nodes = []
        self.equations = []
        self.x0 = []

    def add_nodes(self, nodes):
        self.nodes.append(nodes)

    def add_pipe(self, pipe):
        self.pipes.append(pipe)

    def initialize(self):
        Q0_ref = 1
        P0_ref = 1

        for pipe in self.pipes:
            if pipe.Q is not None:
                Q0_ref = pipe.Q
                break

        for node in self.nodes:
            if node.P is not None:
                P0_ref = node.P
                break

        for node in self.nodes:
            self.x0.append(Q0_ref)
            self.equations.append(lambda x, n=node: n.flow_equation(x))

        for pipe in self.pipes:
            self.x0.append(P0_ref)
            self.equations.append(lambda x, p=pipe: p.pressure_equation(x))

    def solve(self):
        def system_equations(x):
            return np.array([eq(x) for eq in self.equations])
        return fsolve(system_equations, self.x0)

