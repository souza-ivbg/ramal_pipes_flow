'''
Essa é uma seção de teste

a principio o codigo ira funcionar da seguinte forma

inicia os nós
inicia-se as tubulações

inicia a rede
resolve o sistema de equaçoes


'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

from node import Node
from pipe import Pipe
from pipe_system import PipeSystem

# Prop. dos fluidos
ρ = 999 # [kg/m^3]
μ = 1.002e-3 # [Pa s]

g = 9.81 # [m/s^2]
P_1 = 200e3 # [kPa], pressao manometrica
P_2 = 100e3 # [kPa], pressao manometrica
D1 = 1.5e-2 # [m]
D2 = 3e-2 # [m]
z_2 = 2.0 # [m]
z_3 = 1.0 # [m]

# Material cobre
e = 1.5e-6 # Valor tabelado - Checa Cap.8 Fox ou Cengel
e_D1 = e / D1
e_D2 = e / D2

L_a = 5.0 # [m]
L_b = 4.0 # [m]
L_c = 2.0 # [m]
L_d = 1.0  # [m]

node_1 = Node()
node_1.set_pressure(P_1)
node_2 = Node()
node_2.set_pressure(P_2)
node_3 = Node()
node_3.set_pressure(P_2)

pipe_1 = Pipe(
    node_in = node_1,
    node_out = node_2,
    diameter = D1,
    length = L_a,
    wall_roughness = e,
    rho = ρ,
    mu = μ)

pipe_2 = Pipe(
    node_in = node_2,
    node_out = node_3,
    diameter = D1,
    length = L_a,
    wall_roughness = e,
    rho = ρ,
    mu = μ)

pipe_3 = Pipe(
    node_in = node_2,
    node_out = node_3,
    diameter = D2,
    length = L_a,
    wall_roughness = e,
    rho = ρ,
    mu = μ)

pipe_sys = PipeSystem()
pipe_sys.add_pipe(pipe_1)
pipe_sys.add_pipe(pipe_2)
pipe_sys.add_pipe(pipe_3)
pipe_sys.add_nodes(node_1)
pipe_sys.add_nodes(node_2)
pipe_sys.add_nodes(node_3)

pipe_sys.initialize()
pipe_sys.solve()


