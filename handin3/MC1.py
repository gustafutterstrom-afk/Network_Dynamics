import numpy as np

# States: 0=o, 1=a, 2=b, 3=c, 4=d
# a) 
Lambda = np.array([
    [0,   2/5, 1/5, 0,   0],
    [0,   0,   3/4, 1/4, 0],
    [1/2, 0,   0,   1/2, 0],
    [0,   0,   1/3, 0,   2/3],
    [0,   1/3, 0,   1/3, 0]
])

<<<<<<< HEAD
def simulate_return_time():
    state = 0      # start in node a
=======
def simulate_return_time(start,stop):
    state = start     # start in node a
>>>>>>> 831216b3067e48ce722e176842fd5cb1cb6c7fda
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
<<<<<<< HEAD
        if state == 4:
            return t
=======
        if state == stop:
            return t 
>>>>>>> 831216b3067e48ce722e176842fd5cb1cb6c7fda

#simulate_return_time(start=1,stop=1)
N = 100000
<<<<<<< HEAD
#times = [simulate_return_time() for _ in range(N)]

#print("Average return time:", np.mean(times))

#P = Lambda = np.array([
 #   [0,   2/5, 1/5, 0,   0],
 #   [0,   0,   3/4, 1/4, 0],
  #  [1/2, 0,   0,   1/2, 0],
  #  [0,   0,   1/3, 0,   2/3],
  #  [0,   1/3, 0,   1/3, 0]
#])

#D = np.sum(P, axis=1)
#print(D)
#D = np.diag(D)
#P=np.linalg.inv(D)@P
#print(P)
import numpy as np

# Lambda matrix (given)
Lambda = np.array([
    [0,   2/5, 1/5, 0,   0],
    [0,   0,   3/4, 1/4, 0],
    [1/2, 0,   0,   1/2, 0],
    [0,   0,   1/3, 0,   2/3],
    [0,   1/3, 0,   1/3, 0]
])

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
=======
#times = [simulate_return_time(1,1) for _ in range(N)]
#print("Average return time:", np.mean(times))
# used in b) kind of
w = np.sum(Lambda, axis=1)
P = np.linalg.inv(np.diag(w))@Lambda
print(P)

#c) 
simulate_return_time(0,4)
N = 100000
times = [simulate_return_time(0,4) for _ in range(N)]
print("Average return time:", np.mean(times))
>>>>>>> 831216b3067e48ce722e176842fd5cb1cb6c7fda
