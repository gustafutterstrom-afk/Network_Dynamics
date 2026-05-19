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
    state = start 
    t = 0.0

    while True:

        rates = Lambda[state]
        r = np.sum(rates)

        # waiting time
        dt = -np.log(np.random.rand()) / r
        t += dt

        # choose next state
        probs = rates / r
        state = np.random.choice(5, p=probs)

        # stop when we return to stop
        if state == stop:
            return t

simulate_return_time(start=1,stop=1)
N = 100000
times = [simulate_return_time(1,1) for _ in range(N)]
print("Average return time:", np.mean(times))

#c) 
#simulate_return_time(start=0,stop=4)
#times = [simulate_return_time(0,4) for _ in range(N)]
#print("Average return time:", np.mean(times))

#d)
def theoretical():
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

def nodes10():
    N = 10  # number of nodes
    T = 1000 # simulation time

    #colors, 0 = red,1 = green
    X = np.zeros(N, dtype=int)
    # graph
    G = nx.path_graph(N)

    # Store potential values
    U = []

    # needed for plotting 
    pos = {i: (i, 0) for i in range(N)}

    plt.figure(figsize=(10, 6))

    for t in range(1, T):
        # noise
        n = t / 100

        # node wakes up
        i = random.randint(0, N - 1)

        # neighbors
        neighbors = list(G.neighbors(i))

        # Costs 
        cost_red = 0
        cost_green = 0

        for j in neighbors:
            # Cost if node i chooses red
            if X[j] == 0:
                cost_red += 1
            #Cost if node i chooses green
            if X[j] == 1:
                cost_green += 1

        # probability 
        p_red = np.exp(-n * cost_red)
        p_green = np.exp(-n * cost_green)

        Z = p_red + p_green # Normalization term
        p_red /= Z
        p_green /= Z

        # pick a r.v between 0,1
        r = random.random()

        # doing the simulation 
        if r < p_red:
            X[i] = 0
        else:
            X[i] = 1
        # Potential function 
        potential = 0

        for (u, v) in G.edges(): # looping over each node-pair
            if X[u] == X[v]:
                potential += 1 # each edges is calcualted one time

        U.append(potential)

        # Animation 
        plt.clf() # just plotting one window  
        plt.subplot(2, 1, 1)
        node_colors = ['red' if c == 0 else 'green' for c in X]

        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color=node_colors,
            node_size=700,
            font_color='white'
        )

        plt.title(f"Distributed Graph Coloring (t = {t})")
        #Potential 
        plt.subplot(2, 1, 2)
        plt.plot(U, linewidth=2)
        plt.xlabel("Time")
        plt.ylabel("Potential U(t)")
        plt.title("Potential Function")
        plt.grid(True)
        plt.tight_layout()
        plt.pause(0.02)

        # stop 
        if potential == 0:
            print(f"Solution found at t = {t}")
            break

<<<<<<< HEAD
    plt.show()


#b) 
W = np.loadtxt('handin3/data/wifi.mat')
def wifi():
    N = 100  # number of nodes
    T = 1000 # simulation time

    #colors
    X = np.zeros(N, dtype=int)
    # graph
   
    coord = np.loadtxt('handin3/data/coord.mat')
    G = nx.from_numpy_array(W)

    # Store potential values
    U = []

    # needed for plotting 
    pos = {i: (coord[i,0],coord[i,1]) for i in range(N)}

    plt.figure(figsize=(15, 12))

    for t in range(1, T):
        # noise
        n = t**2/100

        # node wakes up
        i = random.randint(0, N - 1)

        # neighbors
        neighbors = list(G.neighbors(i))

        # Costs 
        num_colors = 8
        costs = np.zeros(num_colors)
        for s in range(num_colors):
            for j in neighbors:
            # Cost if node i chooses red
                if X[j] == s:
                    costs[s] += 2
            #Cost if node i chooses green
                elif np.abs(X[j]-s) == 1:
                    costs[s] += 1
                
                
        # probability 
        prob = np.exp(-n * costs)
        prob /= np.sum(prob)

        # pick a r.v between 0,1
        r = random.random()

        # doing the simulation
        prob_cum = np.zeros(len(prob))
        prob_cum[0]=prob[0]
        for m in range(1,len(prob)):
            prob_cum[m]=prob[m]+prob_cum[m-1]
        for s in range(len(prob_cum)):
            if r < prob_cum[s]:
                X[i] = s
                break

        # Potential function 
        potential = 0

        for (u, v) in G.edges(): # looping over each node-pair
            if X[u] == X[v]:
                potential += 2
            elif abs(X[u] - X[v]) == 1:
                potential += 1

        U.append(potential)

        # Animation 
        plt.clf() # just plotting one window  
        plt.subplot(2, 1, 1)
        color_map = ['red', 'green', 'blue', 'yellow',
                'magenta', 'cyan', 'white', 'black']

        node_colors = [color_map[c] for c in X]

        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color=node_colors,
            node_size=700,
            font_color='orange'
        )

        plt.title(f"Distributed Graph Coloring (t = {t}), with η(t)=t^2/100")
        #Potential 
        plt.subplot(2, 1, 2)
        plt.plot(U, linewidth=2)
        plt.xlabel("Time")
        plt.ylabel("Potential U(t)")
        plt.title("Potential Function")
        plt.grid(True)
        plt.tight_layout()
        plt.pause(0.02)

        # stop 
        if potential == 0:
            print(f"Solution found at t = {t}")
            break

    plt.show()
#wifi()

row_sum = W.sum(axis=1)
print(np.where(row_sum>8))
=======
plt.show()
print(potential)

W0 = np.load('handin3/data/wifi.mat')
W = nx.Graph(W0)
>>>>>>> refs/remotes/origin/main
