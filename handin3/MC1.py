import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random
# States: 0=o, 1=a, 2=b, 3=c, 4=d
# a) 
Lambda = np.array([
    [0,   2/5, 1/5, 0,   0],
    [0,   0,   3/4, 1/4, 0],
    [1/2, 0,   0,   1/2, 0],
    [0,   0,   1/3, 0,   2/3],
    [0,   1/3, 0,   1/3, 0]
])

def simulate_return_time(start,stop):
    state = start     # start in node a
    t = 0.0

    # first jump out of a
    while True:

        rates = Lambda[state]
        r = np.sum(rates)

        # waiting time
        dt = -np.log(np.random.rand()) / r
        t += dt

        # choose next state
        probs = rates / r
        state = np.random.choice(5, p=probs)

        # stop when we return to a
        if state == stop:
            return t

#simulate_return_time(start=1,stop=1)
#N = 100000
#times = [simulate_return_time(1,1) for _ in range(N)]
#print("Average return time:", np.mean(times))

#c) 
#simulate_return_time(start=0,stop=4)
N = 100000
#times = [simulate_return_time(0,4) for _ in range(N)]
#print("Average return time:", np.mean(times))

#d)
n = 5
target = 4  # d

# compute omega (exit rates)
omega = Lambda.sum(axis=1)

# build linear system A x = b
A = np.zeros((n, n))
b = np.zeros(n)

for i in range(n):
    if i == target:
        A[i, i] = 1
        b[i] = 0
    else:
        A[i, i] = omega[i]
        for j in range(n):
            A[i, j] -= Lambda[i, j]
        b[i] = 1

E = np.linalg.solve(A, b)

print("E_o[T_d] =", E[0])


N = 10                  # Number of nodes
T = 1000                # Maximum simulation time

# Colors, 0 = red,1 = green
X = np.zeros(N, dtype=int)

# Graph
G = nx.path_graph(N)

# Adjacency matrix
W = nx.to_numpy_array(G)

# Store potential values
U = []

# Node positions for plotting
#pos = {i: (i, 0) for i in range(N)}

# =========================
# Simulation
# =========================
plt.figure(figsize=(10, 6))

for t in range(1, T + 1):

    # Inverse noise parameter
    eta = t / 100

    # Random node wakes up
    i = random.randint(0, N - 1)

    # Find neighbors
    neighbors = list(G.neighbors(i))

    # -------------------------
    # Compute costs
    # -------------------------
    cost_red = 0
    cost_green = 0

    for j in neighbors:

        # Cost if node i chooses red
        if X[j] == 0:
            cost_red += 1

        # Cost if node i chooses green
        if X[j] == 1:
            cost_green += 1

    # -------------------------
    # Gibbs probabilities
    # -------------------------
    p_red = np.exp(-eta * cost_red)
    p_green = np.exp(-eta * cost_green)

    Z = p_red + p_green

    p_red /= Z
    p_green /= Z

    # -------------------------
    # Sample new color
    # -------------------------
    r = random.random()

    if r < p_red:
        X[i] = 0
    else:
        X[i] = 1

    # =========================
    # Compute potential
    # =========================
    potential = 0

    for (u, v) in G.edges():
        if X[u] == X[v]:
            potential += 1

    U.append(potential)

    # =========================
    # Animation
    # =========================
    plt.clf()

    # ---- Graph plot ----
    plt.subplot(2, 1, 1)

    node_colors = ['red' if c == 0 else 'green' for c in X]

    nx.draw(
        G,
        #pos,
        with_labels=True,
        node_color=node_colors,
        node_size=700,
        font_color='white'
    )

    plt.title(f"Distributed Graph Coloring (t = {t})")

    # ---- Potential plot ----
    plt.subplot(2, 1, 2)

    plt.plot(U, linewidth=2)

    plt.xlabel("Time")
    plt.ylabel("Potential U(t)")
    plt.title("Potential Function")
    plt.grid(True)

    plt.tight_layout()
    plt.pause(0.02)

    # Stop if solution found
    if potential == 0:
        print(f"Solution found at t = {t}")
        break

plt.show()