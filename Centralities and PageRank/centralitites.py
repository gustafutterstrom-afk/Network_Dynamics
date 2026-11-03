from scipy.io import loadmat
import numpy as np
import networkx as nx 
data = loadmat("IOdownload.mat")
econ = data["econ"].squeeze()
name = data["name"].squeeze()
io = data["io"]
#print(econ[18]) # Idn2000 - just trying 
#print(econ[33]) # Swe2000

mat= []  # Two countries 
matT =[] # Two countries 
lst =io[0]
mat.append( lst[0][33])
mat.append( lst [0][18])
matT.append(np.transpose(mat[0]))
matT.append(np.transpose(mat[1]))
lenM = len(mat[0])
    #print (lenM) # 47
    #print(lst[0][33][2][3])
    #print(np.shape(lst[0][38]))
def func1():
    row_sumMax =0
    col_sumMax = 0
    listCol= [[], []]
    listRow= [[], []]

    for j in range (len(mat)):
        for i in range (0,lenM):
            row_sum = np.sum(mat[j][i])
            col_sum = np.sum(matT[j][i])
            listCol[j].append(col_sum)
            listRow[j].append(row_sum)

            row_sum = 0
            col_sum = 0


    for i in range (0,2):
        top3_indexR = np.argsort(listRow[i])[-3:][::-1] # Sort so that the biggest is last, acending order, and get the indexes of this elements, -1 makes the largest first 
        top3_Rval = np.array(listRow[i])[top3_indexR] # Make a array to find the values by using the indexes 
        top3_indexC = np.argsort(listCol[i])[-3:][::-1]
        top3_Cval = np.array(listCol[i])[top3_indexC]

        if i==0:
            print(econ[33]) 
        if i==1:
            print(econ[18]) 
        
    
        print("Top 3 Out-degree:", top3_Rval)
        print("Out indices:", top3_indexR)
        print("Top 3 in-degree:", top3_Cval)
        print("In indices:", top3_indexC)
        print('out-degree')
        print (name[top3_indexR]) # Out degree
        print('in-degree')
        print(name[top3_indexC]) # in degree

#func()

# 1.b 
def func2():
    #swe = np.array (lst[0][33])
    #idn = np.array(lst[18])
    

    for i in range(len(mat)):

        # Graph
        G = nx.from_numpy_array(mat[i], create_using=nx.DiGraph)

        #  strongly connected component
        largest_comp = max(nx.strongly_connected_components(G), key=len)
        G_sub = G.subgraph(largest_comp).copy()
        nodes = list(G_sub.nodes())

    
        A = nx.to_numpy_array(G_sub, nodelist=nodes, weight='weight')


        eigvals, eigvecs = np.linalg.eig(A.T)
        idx = np.argmax(np.abs(eigvals))
        centrality_vec = np.abs(eigvecs[:, idx])
        #centrality_vec /= np.linalg.norm(centrality_vec)
        
        # Top 3 nodes
        top_nodes = [nodes[j] for j in np.argsort(centrality_vec)[-3:][::-1]] # elementen i egnvektorn är nod nummer 
        # Print results
        if i == 0:
            print('Swe2000')
        elif i == 1:
            print('Idn2000')

        cen_dict = {nodes[j]: centrality_vec[j] for j in range(len(nodes))}
        print("Top nodes:", top_nodes)
        print("Centrality values:", {n: cen_dict[n] for n in top_nodes})
        print([name[n] for n in top_nodes])

#func2()

## 1.c 
def funcK(b, mu):
    for i in range (len(mat)):
        A = np.array(mat[i])
        eigenval = np.linalg.eigvals(mat[i])
        lambda_max = np.max(eigenval.real)
        alpha = (1-b)/(lambda_max)
        z= np.linalg.inv((np.eye(A.shape[0]))-alpha*A.T)@(b*mu)
        
        top_nodes_idx =  np.argsort(z)[-3:][::-1] # elementen i egnvektorn är nod nummer 
        top_nodes_names = [name[j] for j in top_nodes_idx]
        # Print results
        if i == 0:
            print('Swe2000')
        elif i == 1:
            print('Idn2000')
        print("Top 3 node indices:", top_nodes_idx)
        print("Katz centrality values:", z[top_nodes_idx])
        print("Top 3 node names:", top_nodes_names)


        
beta = 0.15

mu= np.ones(len(mat[0]))
funcK(beta, mu)

mu2= np.zeros(len(mat[1]))
mu2[30]=1
funcK(beta,mu2)
