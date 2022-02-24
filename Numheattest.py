import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def make_array(H, L, V):
    return (np.zeros((H, L)) + V)

def make_rectangle(array, y_a, y_b, x_a, x_b, V):
    array[y_a:y_b,x_a:x_b]=(np.zeros((y_b-y_a,x_b-x_a)) + V)
    return array

def make_vline(array, y_a, y_b, x, V):
    array[y_a:y_b,x]=(np.zeros((1,1)) + V)
    return array

def make_hline(array, x_a, x_b, y, V):
    array[y,x_a:x_b]=(np.zeros((1,1)) + V)
    return array

def make_circle(array, y, x, r, V):
    a, b = y/2, x/2
    for i in range(int(x+1)):
        for j in range(int(y+1)):
            if np.abs((j-a)**2 + (i-b)**2 - r**2) <= r**2:
                array[j][i] = V
    return array

#plt.imshow(make_circle(make_array(60, 120, 1), 60, 120, 20, 2.2, 0))
#plt.colorbar()
#plt.show()

def multiwire_chmaber(L, H, V):
    V_arr = make_array(H, L, 1)
    V_arr = make_hline(V_arr, 0, L, 0, -V)
    V_arr = make_hline(V_arr, 0, L, (H-1), -V)
    d = L/6
    for n in range(5):
        V_arr = make_circle(V_arr, 60, (n+1)*(2*d), 5, 0)
    plt.imshow(V_arr, cmap='jet')
    plt.colorbar()
    plt.show()
    
def edge_strip(L, H, V):
    V_arr = make_array(H, L, V*2)
    V_arr = make_hline(V_arr, 0, L, 0, 0)
    V_arr = make_hline(V_arr, 0, L, (H-1), 0)
    b, d = 10, 15
    for n in range(4):
        if (n+1) == 1 or (n+1) == 4:
            V_arr = make_rectangle(V_arr, 27, 34, (n)*b + (n+1)*d, (n)*b + (n+1)*d + b, 0)
        elif (n+1) == 2:
            V_arr = make_rectangle(V_arr, 27, 34, (n)*b + (n+1)*d, (n)*b + (n+1)*d + b, V)
        elif (n+1) == 3:
            V_arr = make_rectangle(V_arr, 27, 34, (n)*b + (n+1)*d, (n)*b + (n+1)*d + b, -V)
    plt.imshow(V_arr, cmap='jet')
    plt.colorbar()
    plt.show()
    
def gas_mult(L, H, V3, V2, V1):
    V_arr = make_array(H, L, 1000)
    V_arr = make_hline(V_arr, 0, L, 0, -V3)
    V_arr = make_hline(V_arr, 0, L, (H-1), 0)
    a, b = 35, 30
    c, d = 50, 70
    V_arr = make_hline(V_arr, 0, c, a, -V2)
    V_arr = make_hline(V_arr, d, L, a, -V2)
    V_arr = make_hline(V_arr, 0, c, b, -V1)
    V_arr = make_hline(V_arr, d, L, b, -V1)
    plt.imshow(V_arr, cmap='jet')
    plt.colorbar()
    plt.show()
    
multiwire_chmaber(120, 60, 1)
edge_strip(120, 60, 1)
gas_mult(120, 60, 1000, 500, 100)