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
rho = 1000
mu = 0.0001
e = 0.00026

def system_equations(Q):
    # Q = [Qa, Qb, Qc, Qd, Qe, Qf, Qg, Qh]
    # Q = [0,  1,  2,  3,  4,  5,  6,  7]
    hf = []
    for i, sec in enumerate(['A','B','C','D','E','F','G','H']):
        hf_i = calculate_head_loss(Q[i], D[sec], L[sec], rho, mu, e)
        hf.append(hf_i)

    eqs = []

    # === Equações de continuidade ===
    # Nó 2: Qa = Qb + Qe
    eqs.append(Q[0] - Q[1] - Q[4])
    # Nó 3: Qa = Qc
    eqs.append(Q[0] - Q[2])
    # Nó 4: Qa = Qd
    eqs.append(Q[0] - Q[3])
    # Nó 6: Qe = Qf + Qg
    eqs.append(Q[4] - Q[5] - Q[6])
    # Nó 7: Qe = Qh
    eqs.append(Q[4] - Q[7])


    # === Equações de energia nos loops ===
    # h = ha + hb + hc + hd
    eqs.append(P_in - P_out - (hf[0] + hf[1] + hf[2] + hf[3]) * rho * 9.81)
    # hb = he + hf + hh
    eqs.append(hf[1] - hf[4] - hf[5] - hf[7])
    eqs.append(hf[1] - hf[4] - hf[6] - hf[7])
    # hf = hg
    eqs.append(hf[5] - hf[6])



    return eqs
#
# from scipy.optimize import show_options
# show_options(solver="minimize")

# Chute inicial: 1 L/min = 0.0167 kg/s / rho ≈ 0.0000167 m³/s
Q0 = np.ones(8) * 2.8e-3  # 1 L/s para cada trecho como chute inicial

# Resolver
sol = root(system_equations, Q0, method='lm', options={'xtol': 1e-12 ,'maxiter': 100000})


# Mostrar resultados
if sol.success:
    for i, sec in enumerate(['A','B','C','D','E','F','G','H']):
        print(f"Vazão em {sec}: {sol.x[i]*1000*60:.2f} L/min;")
    for i, sec in enumerate(['A','B','C','D','E','F','G','H']):
        print(f"Função: {sol.fun[i]} ")
else:
    print("Solução não convergiu:", sol.message)
