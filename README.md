# Pipe Network Solver

This repository contains a Python implementation for solving flow and pressure distribution in pipe networks using a node-pipe object-oriented framework.

## ✨ Features

- Object-oriented structure with `Node`, `Pipe`, and `PipeSystem` classes
- Calculates flow rates and pressures in complex networks
- Supports:
  - Multiple pipes and nodes
  - Boundary conditions (pressure-specified nodes)
  - Automatic initial guess generation
  - Solver based on `scipy.optimize.root`
- Output with results saved in organized CSV files for nodes and pipes

## ⚙️ How It Works

The Pipe Network Solver is based on the fundamental principles of **fluid mechanics and network analysis**. Here is an overview of its operation:

1. **Network Definition (Nodes and Pipes)**
   - Each **Node** represents a junction where pipes connect. A node can have a known pressure (boundary condition) or an unknown pressure (to be solved).
   - Each **Pipe** connects two nodes and has properties such as diameter, length, roughness, fluid density, and viscosity.

2. **System of Equations**
   - The solver builds a system of nonlinear equations combining:
     - **Energy equations** (Darcy–Weisbach) for each pipe, relating pressure drop, friction factor, and flow rate.
     - **Continuity equations** for each internal node, enforcing mass conservation (sum of inflows = sum of outflows).

3. **Boundary Conditions**
   - Nodes with known pressure are treated as boundary conditions and excluded from the list of unknowns, but they participate in the system equations to ensure consistency.

4. **Initial Guesses**
   - Reasonable initial guesses for flow rates and unknown pressures are automatically generated to improve convergence.

5. **Numerical Solution**
   - The system is solved using **`scipy.optimize.root`**, which applies the LM method to find the solution vector of flow rates and pressures that satisfies all equations simultaneously.

6. **Results**
   - After solving, each pipe contains its calculated flow rate, and each node has its final pressure. The results can be saved in organized CSV files for further analysis.



