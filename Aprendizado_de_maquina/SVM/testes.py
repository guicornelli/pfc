import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10.8, 7.2), dpi=100)
ax = fig.add_subplot(111, projection='3d')
ax.scatter(val1SemOut20, val2SemOut20, val3SemOut20)

ax.set_xlabel('Gen NCS Temp')
ax.set_ylabel('Gen Speed')
ax.set_zlabel('Curr Grid')

# ou

fig = plt.figure(figsize=(10.8, 7.2), dpi=100)
ax = fig.add_subplot(111, projection='3d')
ax.scatter(errorsV120, errorsV220, errorsV320)

ax.set_xlabel('Gen NCS Temp - 10 min')
ax.set_ylabel('Gen Speed - 10 min')
ax.set_zlabel('Curr Grid - 10 min')

# ou

x1 = df_analogic1['GenNCSBearingTemp'][df_analogic1['Labels'] == 1]
y1 = df_analogic1['GenSpeed'][df_analogic1['Labels'] == 1]
z1 = df_analogic1['GridCurrent'][df_analogic1['Labels'] == 1]

x0 = df_analogic1['GenNCSBearingTemp'][df_analogic1['Labels'] == 0]
y0 = df_analogic1['GenSpeed'][df_analogic1['Labels'] == 0]
z0 = df_analogic1['GridCurrent'][df_analogic1['Labels'] == 0]

fig = plt.figure(figsize=(10.8, 7.2), dpi=100)
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x1, y1, z1, c='r', marker='^')
ax.scatter(x0, y0, z0)

ax.set_xlabel('Gen NCS Temp A20')
ax.set_ylabel('Gen Speed A20')
ax.set_zlabel('Curr Grid A20')


