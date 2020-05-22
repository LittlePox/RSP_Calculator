import random as rnd
import numpy as np

N = 1000000
ctrl_mean = 353.6

a = np.zeros(N)
b = np.zeros(N)

level_adj = 0
for i in range(0, N):
    if level_adj > 0:
        level_adj = level_adj - 1
    elif level_adj < 0:
        level_adj = level_adj + 1

    r = rnd.random()
    if r < 0.03:
        b[i] = 1080
        level_adj = level_adj + 3
    elif r < 0.15:
        b[i] = 720
        level_adj = level_adj + 2
    elif r < 0.3:
        b[i] += 480
        level_adj = level_adj + 1
    elif r < 0.7:
        b[i] = 320
        level_adj = level_adj
    elif r < 0.85:
        b[i] = 160
        level_adj = level_adj - 1
    elif r < 0.97:
        b[i] = 80
        level_adj = level_adj - 2
    else:
        b[i] = 40
        level_adj = level_adj - 3

    level_adj = min(3, max(level_adj, -3))
    if level_adj == -3:
        a[i] = 1080
    elif level_adj == -2:
        a[i] = 720
    elif level_adj == -1:
        a[i] = 480
    elif level_adj == 0:
        a[i] = 320
    elif level_adj == 1:
        a[i] = 160
    elif level_adj == 2:
        a[i] = 80
    else:
        a[i] = 40

print("mean of adjusted: ", np.mean(a))
print("std of adjusted:", np.std(a, ddof=1))

print("mean of unadjusted: ", np.mean(b))
print("std of unadjusted:", np.std(b, ddof=1))
