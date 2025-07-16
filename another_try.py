import numpy as np
from scipy.optimize import root

def churchill_correlation(Re, eD):
    if Re < 2300:
        return 64 / Re
    else:
        A = (-2.457 * np.log((7/Re)**0.9 + 0.27*eD))**16
        B = (37530 / Re)**16
        f = 8 * ((8/Re)**12 + 1/(A+B)**1.5)**(1/12)
        return f

def calculate_head_loss(Q, D, L, rho, mu, e):
    A = np.pi * (D/2)**2
    v = Q / A
    Re = rho * v * D / mu
    eD = e / D
    f = churchill_correlation(Re, eD)
    hf = f * (L/D) * (v**2 / (2 * 9.81))
    return hf

# === Dados do problema ===
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

# Condições de Contorno
P_in = 4e5
P_out = 1e5

# Propriedades
rho = 986
mu = 0.001
e = 0.00026

res = []
Q_old = 0
def system_equations(Q):

    h =  calculate_head_loss(Q, D["A"], L["A"], rho, mu, e) + calculate_head_loss(Q, D["B"], L["B"], rho, mu, e) + (
        calculate_head_loss(Q, D["C"], L["C"], rho, mu, e) + calculate_head_loss(Q, D["D"], L["D"], rho, mu, e)  )

    return P_in - P_out - (h * rho * 9.81)
x0 = 2.8e-3

sol = root(system_equations, x0, method='lm', options={'xtol': 1e-12 ,'maxiter': 100000})

print(f"Vazão em A: {sol.x[0] * 1000 * 60:.2f} L/min;")
print(f"Função em A: {sol.fun[0]}")
