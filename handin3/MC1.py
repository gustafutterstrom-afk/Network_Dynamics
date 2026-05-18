import numpy as np

# States: 0=o, 1=a, 2=b, 3=c, 4=d

Lambda = np.array([
    [0,   2/5, 1/5, 0,   0],
    [0,   0,   3/4, 1/4, 0],
    [1/2, 0,   0,   1/2, 0],
    [0,   0,   1/3, 0,   2/3],
    [0,   1/3, 0,   1/3, 0]
])

def simulate_return_time():
    state = 1      # start in node a
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
        if state == 1:
            return t

N = 100000
times = [simulate_return_time() for _ in range(N)]

print("Average return time:", np.mean(times))