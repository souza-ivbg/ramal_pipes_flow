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

D = {
    'A': 0.038,
    'B': 0.038,
    'C': 0.050,
    'D': 0.038,
    'E': 0.050,
    'F': 0.025,
    'G': 0.038,
    'H': 0.050
}

L = {
    'A': 3,
    'B': 6,
    'C': 3,
    'D': 3,
    'E': 3,
    'F': 1,
    'G': 3,
    'H': 1.5
}

P_in = 4e5
P_out = 1e5

rho = 1000
mu = 0.0001
e = 0.00026


# === Criação dos nodes ===

node_1 = Node()
node_1.set_pressure(P_in)

node_5 = Node()
node_5.set_pressure(P_out)

# Exemplo: criar nodes intermediários (adapte conforme seu layout real)
# Aqui, node_2, node_3, ..., são placeholders para conectar os pipes conforme o seu esquema hidráulico.

node_2 = Node()
node_3 = Node()
node_4 = Node()
node_6 = Node()
node_7 = Node()

# === Criação dos pipes ===

pipe_A = Pipe(node_in=node_1, node_out=node_2, diameter=D['A'], length=L['A'], wall_roughness=e, rho=rho, mu=mu)
pipe_B = Pipe(node_in=node_2, node_out=node_3, diameter=D['B'], length=L['B'], wall_roughness=e, rho=rho, mu=mu)
pipe_C = Pipe(node_in=node_3, node_out=node_4, diameter=D['C'], length=L['C'], wall_roughness=e, rho=rho, mu=mu)
pipe_D = Pipe(node_in=node_4, node_out=node_5, diameter=D['D'], length=L['D'], wall_roughness=e, rho=rho, mu=mu)
pipe_E = Pipe(node_in=node_2, node_out=node_6, diameter=D['E'], length=L['E'], wall_roughness=e, rho=rho, mu=mu)
pipe_F = Pipe(node_in=node_6, node_out=node_7, diameter=D['F'], length=L['F'], wall_roughness=e, rho=rho, mu=mu)
pipe_G = Pipe(node_in=node_6, node_out=node_7, diameter=D['G'], length=L['G'], wall_roughness=e, rho=rho, mu=mu)
pipe_H = Pipe(node_in=node_7, node_out=node_3, diameter=D['H'], length=L['H'], wall_roughness=e, rho=rho, mu=mu)

# === Sistema de pipes ===

pipe_sys = PipeSystem()

# Adiciona pipes
for pipe in [pipe_A, pipe_B, pipe_C, pipe_D, pipe_E, pipe_F, pipe_G, pipe_H]:
    pipe_sys.add_pipe(pipe)

# Adiciona nodes
for node in [node_1, node_2, node_3, node_4, node_5, node_6, node_7]:
    pipe_sys.add_nodes(node)


pipe_sys.initialize()
pipe_sys.solve()

print(pipe_A.Q * 1000*60)
print(pipe_B.Q * 1000*60)
print(pipe_C.Q * 1000*60)
print(pipe_D.Q * 1000*60)
print(pipe_E.Q * 1000*60)
print(pipe_F.Q * 1000*60)
print(pipe_G.Q * 1000*60)
print(pipe_H.Q * 1000*60)

# print(pipe_sys.system_solution.fun[0] )
# print(pipe_sys.system_solution.fun[1] )
# print(pipe_sys.system_solution.fun[2] )
# print(pipe_sys.system_solution.fun[3] )
# print(pipe_sys.system_solution.fun[4] )
# print(pipe_sys.system_solution.fun[5] )
# print(pipe_sys.system_solution.fun[6] )
# print(pipe_sys.system_solution.fun[7] )


