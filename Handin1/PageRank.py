import networkx as nx
import numpy as np 
from scipy.sparse import coo_matrix, csr_matrix
import scipy.io
from scipy.sparse import diags
import matplotlib.pyplot as plt

### This is the in built method in network X. Only used for validation####
def func1():
    twitterD = np.loadtxt('twitter.mat')
    users = np.loadtxt('users.mat')
    graph = nx.DiGraph()

    for i,j,w in twitterD: 
        graph.add_edge(int(i), int(j), weight=w)

    pagerank = nx.pagerank(graph)
    top5_index = sorted(pagerank, key = pagerank.get, reverse=True)[:5]
    print(top5_index)
    print("user-ID:", {n: users[n] for n in top5_index})
    print("centrality:", {n: pagerank[n] for n in top5_index})

func1()


def func11(beta):

    twitter_table = np.loadtxt("twitter.mat") # Loading the data
    users = np.loadtxt('users.mat')# Loading the data
    rows = twitter_table[:, 0].astype(int)   # 0-based indexing in Python
    cols = twitter_table[:, 1].astype(int) # 0-based indexing in Python
    data = twitter_table[:, 2]# 0-based indexing in Python
    n_nodes = max(rows.max(), cols.max()) + 1  # total number of nodes
    W = coo_matrix((data, (rows, cols)), shape=(n_nodes, n_nodes)).tocsr()  # CSR format - sparse matrix 
    row_sums = np.array(W.sum(axis=1)).flatten() # Right format
    row_sums[row_sums == 0] = 1 # handel the 0
    D_inv = diags(1/row_sums)  # diagonal matrix with 1 / row_sum
    P = D_inv @ W  # row-normalized matrix
    Q = (1-beta)*P.T # according to formula 
    #n_nodes = P.shape[0]
    mu = np.ones((n_nodes,1))
    lamb = beta*mu/n_nodes # Accordig to formula 
    z = np.ones((n_nodes,1)) # initial values 

    for i in range (0,100):
        z = Q @z + lamb

    top_nodes_idx = np.argsort(z.flatten())[-5:][::-1] # Sort top 5
    print("Top 3 node indices:", top_nodes_idx) # Correct zero idex
    print(z[top_nodes_idx])
    print(users[1])


beta = 0.15
func11(beta)

def func2():
    twitter_table = np.loadtxt("twitter.mat")
    rows = twitter_table[:, 0].astype(int) - 1  # 0-based indexing in Python
    cols = twitter_table[:, 1].astype(int) - 1
    data = twitter_table[:, 2]
    n_nodes = max(rows.max(), cols.max()) + 1  # total number of nodes
    W = coo_matrix((data, (rows, cols)), shape=(n_nodes, n_nodes)).tocsr()  # CSR format

    row_sums = np.array(W.sum(axis=1)).flatten()
    dangeling = (row_sums==0)
    W[dangeling,dangeling] = 1
    row_sums[row_sums == 0] = 1
    D_inv = diags(1/row_sums)  # diagonal matrix with 1 / row_sum
    P = D_inv @ W  # row-normalized matrix
    n_nodes = P.shape[0]
    z = 0.5*np.ones((n_nodes,1))

    s1 = 8 # set the stubborn nodes 
    s2 = 25
    z[s1]=0
    z[s2]=1

    # history for plotting
    tracked_nodes = [s1, s2,112,5001,6001]  # example nodes to plot
    history = [z[tracked_nodes].flatten()]

    for i in range (0,1000):
        z = P @z 
        z[s1]=0 # Correct the stubborn nodes 
        z[s2]=1
        history.append(z[tracked_nodes].flatten())
    history = np.array(history)

    # Plot opinions over time
    for i, node in enumerate(tracked_nodes):
        plt.plot(history[:,i], label=f'Node {node+1}')
    plt.xlabel("Time step")
    plt.ylabel("Opinion")
    plt.title("Discrete-time consensus with two stubborn nodes")
    plt.legend()
    plt.show()

func2()
