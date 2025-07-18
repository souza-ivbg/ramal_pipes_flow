import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import os
from scipy.optimize import fsolve, root


class PipeSystem:
    def __init__(self):
        self.pipes = []
        self.nodes = []
        self.x0 = []

        self.system_equation = None
        self.system_solution = None

    def add_nodes(self, nodes):
        self.nodes.append(nodes)

    def add_pipe(self, pipe):
        self.pipes.append(pipe)

    def initialize(self):
        # Clean the previous indexes to permit more than one initialization
        self.node_internal_indexes = []

        for i, node in enumerate(self.nodes):
            if node.P is None:
                self.node_internal_indexes.append(i)

        def system_equation(x):
            equations = []

            Q = x[:len(self.pipes)]
            P_internal = x[len(self.pipes):]

            P = []
            internal_counter = 0
            for node in self.nodes:
                if node.P is not None:
                    P.append(node.P)
                else:
                    P.append(P_internal[internal_counter])
                    internal_counter += 1

            # Energy conservation equation (1 per pipe)
            for i, pipe in enumerate(self.pipes):
                P_in = P[self.nodes.index(pipe.node_in)]
                P_out = P[self.nodes.index(pipe.node_out)]

                P_i_residual = pipe.pressure_equation(P_in, P_out, Q[i])
                equations.append(P_i_residual)

            # Continuity Equations (1 per intern node)
            for node_index in self.node_internal_indexes:
                node = self.nodes[node_index]
                Q_eq = 0
                for j, pipe in enumerate(self.pipes):
                    if pipe in node.pipes_in:
                        Q_eq += Q[j]
                    if pipe in node.pipes_out:
                        Q_eq -= Q[j]
                equations.append(Q_eq)

            return equations

        self.system_equation = system_equation

    def solve(self, Q0=0.028, P0=1e5):

        Q0_ref = np.ones(len(self.pipes)) * Q0

        known_pressures = [node.P for node in self.nodes if node.P is not None]
        if known_pressures:
            avg_P = np.mean(known_pressures)
        else:
            avg_P = P0
        P0_ref = np.ones(len(self.node_internal_indexes)) * avg_P

        x0 = np.concatenate((Q0_ref, P0_ref))

        sol = root(self.system_equation, x0, method='lm', options={'xtol': 1e-9, 'maxiter': 100000})

        if not sol.success:
            print("Solver failed to converge!")
            print(sol.message)
            return

        self.system_solution = sol

        x = sol.x

        Q_solved = x[:len(self.pipes)]
        P_internal_solved = x[len(self.pipes):]

        for i, pipe in enumerate(self.pipes):
            pipe.Q = Q_solved[i]

        internal_counter = 0
        for i in self.node_internal_indexes:
            self.nodes[i].P = P_internal_solved[internal_counter]
            internal_counter += 1


    def save_results(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

        node_data = []
        for node in self.nodes:
            node_data.append({
                'Node': node.name,
                'Pressure [Pa]': node.P
            })

        df_nodes = pd.DataFrame(node_data)
        df_nodes.to_csv(os.path.join(path, 'nodes.csv'), index=False)

        pipe_data = []
        for pipe in self.pipes:
            pipe_data.append({
                'Pipe': pipe.name,
                'Flow rate [m3/s]': pipe.Q,
                'Diameter [m]': pipe.diameter,
                'Length [m]': pipe.length
            })

        df_pipes = pd.DataFrame(pipe_data)
        df_pipes.to_csv(os.path.join(path, 'pipes.csv'), index=False)