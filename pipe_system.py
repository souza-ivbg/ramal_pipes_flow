import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve, root


class PipeSystem:
    def __init__(self):
        self.pipes = []
        self.nodes = []
        self.node_internal_indices = []
        self.x0 = []

        self.system_equation = None
        self.system_solution = None

    def add_nodes(self, nodes):
        self.nodes.append(nodes)

    def add_pipe(self, pipe):
        self.pipes.append(pipe)

    def initialize(self):
        # Clear previous indices to allow re-initialization
        self.node_internal_indices = []

        # Correctly identify all internal nodes
        for i, node in enumerate(self.nodes):
            if node.P is None:
                self.node_internal_indices.append(i)

        def system_equation(x):
            equations = []

            # Unpack unknown variables from the solver vector 'x'
            Q = x[:len(self.pipes)]
            P_internal = x[len(self.pipes):]

            # Reconstruct the full pressure vector 'P'
            # This part of your logic was already correct
            P = []
            internal_counter = 0
            for node in self.nodes:
                if node.P is not None:
                    P.append(node.P)  # Known boundary pressure
                else:
                    P.append(P_internal[internal_counter])  # Unknown internal pressure
                    internal_counter += 1

            # 1. Energy Equations (one per pipe)
            for i, pipe in enumerate(self.pipes):
                P_in = P[self.nodes.index(pipe.node_in)]
                P_out = P[self.nodes.index(pipe.node_out)]

                # The residual from the pipe's pressure loss equation
                P_i_residual = pipe.pressure_equation(P_in, P_out, Q[i])
                equations.append(P_i_residual)

            # 2. Continuity Equations (one per INTERNAL node)
            for node_index in self.node_internal_indices:
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

    def solve(self):
        # Define initial guesses
        Q0_ref = np.ones(len(self.pipes)) * 0.028  # A small, non-zero initial flow

        # Use a more robust initial guess for pressure
        known_pressures = [node.P for node in self.nodes if node.P is not None]
        if known_pressures:
            avg_P = np.mean(known_pressures)
        else:
            avg_P = 1e5  # A default pressure (e.g., 1 atm) if none are known

        P0_ref = np.ones(len(self.node_internal_indices)) * avg_P

        # Combine guesses into the initial vector x0
        x0 = np.concatenate((Q0_ref, P0_ref))

        # Solve the system
        sol = root(self.system_equation, x0, method='lm', options={'xtol': 1e-9, 'maxiter': 100000})

        if not sol.success:
            print("Solver failed to converge!")
            print(sol.message)
            return

        self.system_solution = sol
        x = sol.x

        # Unpack and save the results
        Q_solved = x[:len(self.pipes)]
        P_internal_solved = x[len(self.pipes):]

        for i, pipe in enumerate(self.pipes):
            pipe.Q = Q_solved[i]

        internal_counter = 0
        for i in self.node_internal_indices:
            self.nodes[i].P = P_internal_solved[internal_counter]
            internal_counter += 1