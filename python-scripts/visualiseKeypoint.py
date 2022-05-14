import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

#load data points
lms = np.genfromtxt('../tests/datapoints.csv', delimiter=',')

#unnomalised landmarks
lms_ = lms[0]

xs = lms_[::3]
ys = lms_[1::3]
zs = lms_[2::3]

ax.scatter(xs, ys, zs, marker='s')


#translation invariant landmarks
lms_norm0 = lms[1]

x0s = lms_norm0[::3]
y0s = lms_norm0[1::3]
z0s = lms_norm0[2::3]

ax.scatter(x0s, y0s, z0s, marker='^')


# #translation and scale invariant landmarks
# lms_norm1 = lms[2]

# x1s = lms_norm1[::3]
# y1s = lms_norm1[1::3]
# z1s = lms_norm1[2::3]

# ax.scatter(x1s, y1s, z1s, marker='o')

# ax.set_xlabel('X Label')
# ax.set_ylabel('Y Label')
# ax.set_zlabel('Z Label')

plt.show()