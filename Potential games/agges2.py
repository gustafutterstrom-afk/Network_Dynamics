import numpy as np
from scipy.linalg import null_space

# Generator (your Lambda matrix)
Lambda = np.array([
    [0,   2/5, 1/5, 0,   0],
    [0,   0,   3/4, 1/4, 0],
    [1/2, 0,   0,   1/2, 0],
    [0,   0,   1/3, 0,   2/3],
    [0,   1/3, 0,   1/3, 0]
])

# Exit rates ω
omega = np.sum(Lambda, axis=1)

# Laplacian: L = diag(ω) - Λ
L = np.diag(omega) - Lambda

# Solve L^T π = 0
ns = null_space(L.T)

# Extract stationary vector and normalize
pi = ns[:, 0]
pi = pi / np.sum(pi)

print("Stationary distribution π:")
print(pi)