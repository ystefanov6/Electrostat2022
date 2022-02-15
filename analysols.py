import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# Function to plot an anasol. Steps is how many how many x, y pairs we will have,
# llimit is different depending on the solution, in the case of the coaxial cylinders
# it is the radius of the smaller cylinder and for the two plates it the radius
# of the grounded cylinder. ulimit depends on the solution as well, for the coaxial
# it is the radius of the larger cylinder and for the plates it is L. Finally
# func is simply the function we wish to graph.
def heatmap(steps, llimit, ulimit, func):
    x = []
    y = []
    V = []
    i = 0
    while i < 2*ulimit:
        i += (2*ulimit)/steps
        x.append(i)
        y.append(i)
    
    for j in x:
        values = []
        for k in y:
            values.append(func(k-ulimit, j-ulimit, 2, llimit, ulimit))
        V.extend([values[0:]])
    
    plt.imshow(V, cmap='plasma')
    plt.colorbar()
    plt.show()

# Function for the coaxial cylinders. V is the voltage at the outer cylinder. 
# r is the radius from the center at which we want to find the voltage. R1 is 
# the radius of the grounded cylinder and R2 is the radius of the outer 
# cylinder. The boundary conditions are V(R2, theta) = V, and 
# V(r =< R1, theta) = 0
def coaxialcylinders(x, y, V, R1, R2):
    r = np.sqrt((x**2) + (y**2))
    if r < R1:
        return 0
    else:
        part1 = np.log(r/R1)
    if r > R2:
        return 0
    else:
        part2 = np.log(R2/R1)
    return V*(part1/part2)

# Function for the a grounded cylinder between two plates. The first plate is
# located at 0 with a potential of +V, the second plate is located at +2L with
# a potential of -V. The grounded cylinder, with radius R is centered between 
# the two plates at +L. r is the radius from the center of the grounded cylinder
# which we fnd the potential, theta is the angle from the cylinder in radians.
def plates_cylinder(x, y, V, R, L):
    # from our x and y find r
    r = np.sqrt((x**2) + (y**2))
     # check what position we are at
    if x == -L: # At the first plate
        return V
    elif x == L: # At the second plate
        return -V
    elif np.abs(x) > np.abs(L): # outside the plates
        return 0
    elif r < R: # Inside the cylinder
        return 0
    else:
        part1 = (r - ((R**2)/r))
    theta = np.arctan2(y, x)
    dV = V - (-V)
    part2 = ((-dV)/(2*L))*(np.cos(theta))
    return part1 * part2

heatmap(1000, 2, 5, coaxialcylinders)
heatmap(1000, 25, 100, plates_cylinder)