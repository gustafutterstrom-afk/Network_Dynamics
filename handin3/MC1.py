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
N = 100000
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