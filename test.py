""""
This code exemplifies the use of the pipe system solver. The case used to exemplify is the example 8.11 from the 7ed of the fluid mechanic book (Fox and McDonalds)
"""

from src.node import Node
from src.pipe import Pipe
from src.pipe_system import PipeSystem

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


node_1 = Node('node_1')
node_1.set_pressure(P_in)

node_5 = Node('node_5')
node_5.set_pressure(P_out)

node_2 = Node('node_2')
node_3 = Node('node_3')
node_4 = Node('node_4')
node_6 = Node('node_6')
node_7 = Node('node_7')


pipe_A = Pipe(name='pipe_A', node_in=node_1, node_out=node_2, diameter=D['A'], length=L['A'], wall_roughness=e, rho=rho, mu=mu)
pipe_B = Pipe(name='pipe_B', node_in=node_2, node_out=node_3, diameter=D['B'], length=L['B'], wall_roughness=e, rho=rho, mu=mu)
pipe_C = Pipe(name='pipe_C', node_in=node_3, node_out=node_4, diameter=D['C'], length=L['C'], wall_roughness=e, rho=rho, mu=mu)
pipe_D = Pipe(name='pipe_D', node_in=node_4, node_out=node_5, diameter=D['D'], length=L['D'], wall_roughness=e, rho=rho, mu=mu)
pipe_E = Pipe(name='pipe_E', node_in=node_2, node_out=node_6, diameter=D['E'], length=L['E'], wall_roughness=e, rho=rho, mu=mu)
pipe_F = Pipe(name='pipe_F', node_in=node_6, node_out=node_7, diameter=D['F'], length=L['F'], wall_roughness=e, rho=rho, mu=mu)
pipe_G = Pipe(name='pipe_G', node_in=node_6, node_out=node_7, diameter=D['G'], length=L['G'], wall_roughness=e, rho=rho, mu=mu)
pipe_H = Pipe(name='pipe_H', node_in=node_7, node_out=node_3, diameter=D['H'], length=L['H'], wall_roughness=e, rho=rho, mu=mu)

pipe_sys = PipeSystem()

for pipe in [pipe_A, pipe_B, pipe_C, pipe_D, pipe_E, pipe_F, pipe_G, pipe_H]:
    pipe_sys.add_pipe(pipe)

for node in [node_1, node_2, node_3, node_4, node_5, node_6, node_7]:
    pipe_sys.add_nodes(node)


pipe_sys.initialize()
pipe_sys.solve()

pipe_sys.save_results("results")


