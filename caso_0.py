import numpy as np
from scipy.optimize import fsolve, root

def churchill_correlation(reynolds, wall_roughness):
    if reynolds <= 0:
        return np.inf

    eq_1 = (reynolds / 7) ** 0.9
    eq_2 = 0.27 * wall_roughness
    a = (-2.457 * np.log(eq_1 + eq_2)) ** 16
    b = (37530 / reynolds) ** 16

    term_a = (8 / reynolds) ** 12
    term_b = 1 / (a + b) ** 1.5

    return 8 * (term_a + term_b) ** (1 / 12)


def calculate_pressure(Q, P_in, P_out, diameter, length, rho, mu, wall_roughness, position=None):
    if position is None:
        position = length

    v = (4 * Q) / (np.pi * (diameter ** 2))
    Re = (diameter * v * rho) / mu
    f = churchill_correlation(Re, wall_roughness)
    # A equação foi ajustada para usar a posição em vez do comprimento total para o cálculo da perda de carga
    h_M = f * (position / diameter) * ((v ** 2) / (2 * 9.81))

    return P_in - h_M * (rho * 9.81) - P_out

def calculate_loss(Q, h_M, diameter, length, rho, mu, wall_roughness, position=None):
    if position is None:
        position = length

    v = (4 * Q) / (np.pi * (diameter ** 2))
    Re = (diameter * v * rho) / mu
    f = churchill_correlation(Re, wall_roughness)
    # A equação foi ajustada para usar a posição em vez do comprimento total para o cálculo da perda de carga
    return f * (position / diameter) * ((v ** 2) / (2 * 9.81)) - h_M

def calculate_flow_balance(pipes_in, pipes_out):
    flow = 0
    for Q in pipes_in:
        flow += Q
    for Q in pipes_out:
        flow -= Q
    return flow

# Prop. dos fluidos
ρ = 999 # [kg/m^3]
μ = 1.002e-3 # [Pa s]

g = 9.81 # [m/s^2]
P_1 = 4e5 # [kPa], pressao manometrica
P_3 = 1e5 # [kPa], pressao manometrica
z_2 = 2.0 # [m]
z_3 = 1.0 # [m]


D1 = 38e-3 # [m]
D2 = 38e-3 # [m]
D3 = 38e-3 # [m]
D4 = 25e-3 # [m]
D5 = 38e-3 # [m]
D6 = 50e-3 # [m]


# Material cobre
e = 1.5e-6 # Valor tabelado - Checa Cap.8 Fox ou Cengel
e_D1 = e / D1
e_D2 = e / D2
e_D3 = e / D3
e_D4 = e / D4
e_D5 = e / D5
e_D6 = e / D6

L_a = 3.0 # [m]
L_b = 6.0 # [m]
L_c = 1.5 # [m]
L_d = 3.0  # [m]
L_e = 3.0  # [m]
L_f = 1.5 # [m]

Q_guess = 1e-3  # chute inicial [m^3/s]

def system_equations(x):
    # === Variáveis ===
    Q_1, Q_2, Q_3, Q_4, Q_5, Q_6, P_2, P_4, P_5 = x

    # === Equações de perda de carga ===
    eq1 = calculate_pressure(Q_1, P_1, P_2, D1, L_a, ρ, μ, e_D1)
    eq2 = calculate_pressure(Q_2, P_2, P_3, D1, L_b, ρ, μ, e_D2)
    eq3 = calculate_pressure(Q_3, P_2, P_4, D1, L_c, ρ, μ, e_D3)
    eq4 = calculate_pressure(Q_4, P_4, P_5, D1, L_d, ρ, μ, e_D4)
    eq5 = calculate_pressure(Q_5, P_4, P_5, D1, L_e, ρ, μ, e_D5)
    eq6 = calculate_pressure(Q_6, P_5, P_3, D1, L_f, ρ, μ, e_D6)

    # === Equações de balanço de fluxo ===
    eq7 = calculate_flow_balance([Q_1], [Q_2, Q_3])
    eq8 = calculate_flow_balance([Q_3], [Q_4, Q_5])
    eq9 = calculate_flow_balance([Q_4, Q_5], [Q_6])

    return [eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9]


x0 = []
for i in range(9):
    if i <= 4:
        x0.append(P_1)
    else:
        x0.append(Q_guess)


raiz= root(system_equations, x0, method='lm')


a=2

