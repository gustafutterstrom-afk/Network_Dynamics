import networkx as nx
import numpy as np
from scipy.io import loadmat
import cvxpy as cv

B = np.loadtxt('traffic.mat', delimiter=',')
print(B.shape)
le = np.loadtxt('traveltime.mat', delimiter=',')
print(le.shape)
cap = np.loadtxt('capacities.mat', delimiter=',')
flo = np.loadtxt('flow.mat', delimiter=',')
#W = np.zeros((B.shape[0], B.shape[0]))
G = nx.DiGraph()
for i in range(B.shape[1]):  
    a = None
    b = None

    for j in range(B.shape[0]): 
        if B[j, i] == 1:
            a = j
        elif B[j, i] == -1:
            b = j

        if a is not None and b is not None:
            #W[a, b] = le[i]
            G.add_edge(a, b, capacity = cap[i], weight=le[i])

#print(W)
#G = nx.DiGraph(W, capacity=cap)
shortestp = nx.shortest_path(G, source=0, target=16, weight='weight')
shortest = nx.shortest_path_length(G, source=0, target=16, weight='weight') #a
print(shortest)
print(shortestp)

mflow, dict = nx.maximum_flow(G, 0, 16) #b
print(mflow)

mu = B@flo
print(mu) #c


v = np.zeros(B.shape[0])
v[0] = mu[0]
v[16] = -mu[0]
fe = cv.Variable(B.shape[1])

constraints = [B @ fe == v, fe >= 0, fe <= cap]

cost = cv.sum(cv.multiply(le * cap, cv.inv_pos(1 - cv.multiply(fe, 1 / cap)) - 1))

objective = cv.Minimize(cost)

problem = cv.Problem(objective, constraints)

#print(problem.solve())
#print(fe.value)
#print(problem.status) #d

fstar=fe.value


f0 = cv.Variable(B.shape[1])

constraints = [B @ f0 == v, f0 >= 0, f0 <= cap]

cost = cv.sum(cv.multiply(cv.multiply(-le,cap),cv.log(1-f0/cap)))

objective = cv.Minimize(cost)

problem = cv.Problem(objective, constraints)

#print(problem.solve())
#print(f0.value)
#print(problem.status) #e

fw = cv.Variable(B.shape[1])

constraints = [B @ fw == v, fw >= 0, fw <= cap]

cost = cv.sum(cv.multiply(cv.multiply(-le,cap),cv.log(1-fw/cap)) + cv.multiply(fw, cv.multiply(fstar, cv.multiply(le, cv.multiply(cv.inv_pos(cap), cv.inv_pos(cv.square(1-cv.multiply(fstar, cv.inv_pos(cap)))))))))

objective = cv.Minimize(cost)

problem = cv.Problem(objective, constraints)

#print(problem.solve())
#print(fw.value)
#print(problem.status) #f


fe2 = cv.Variable(B.shape[1])

constraints = [B @ fe2 == v, fe2 >= 0, fe2 <= cap]

cost = cv.sum(cv.multiply(le * cap, cv.inv_pos(1 - cv.multiply(fe2, 1 / cap)) - 1)-cv.multiply(fe2,le))

objective = cv.Minimize(cost)

problem = cv.Problem(objective, constraints)

print(problem.solve())
print(fe2.value)
print(problem.status) #g

f2star = fe2.value

fw2 = cv.Variable(B.shape[1])

constraints = [B @ fw2 == v, fw2 >= 0, fw2 <= cap]

cost = cv.sum(cv.multiply(cv.multiply(-le,cap),cv.log(1-fw2/cap)) + cv.multiply(fw2, cv.multiply(f2star, cv.multiply(le, cv.multiply(cv.inv_pos(cap), cv.inv_pos(cv.square(1-cv.multiply(f2star, cv.inv_pos(cap))))))))-cv.multiply(fw2,le))

objective = cv.Minimize(cost)

problem = cv.Problem(objective, constraints)

print(problem.solve())
print(fw2.value)
print(problem.status) #g contd





