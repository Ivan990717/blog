import numpy as np

interval = 0.05
p1 = np.array([1.922,17.169])
p2 = np.array([4.292,13.691])

length = np.linalg.norm(p2-p1)
num_points = int(np.ceil(length/interval)) + 1
t = np.linspace(0,1,num_points)
points = np.outer(t,p2-p1) + p1
