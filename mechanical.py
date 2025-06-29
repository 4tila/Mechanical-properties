import numpy as np
from os import popen
cte = 1.602176634e1 # convert between eV/ang^2 to J/m^2=N/m
STRUCT_OUT = 'X'
ls = popen('ls -d mec*').read().split()

E_xy, E_x, E_y = list(), list(), list() # energy curves for each type of strain
strain_x, strain_y = list(), list() # list of pairs of (strain applied to fixed x axis, strain on y axis) and
                                    # (strain applied to fixed y axis, starin on x axis)
A = list(map(float, popen(f'sed -n 1p ./{STRUCT_OUT}').read().strip().split() ))
B = list(map(float, popen(f'sed -n 2p ./{STRUCT_OUT}').read().strip().split() ))
A_0 = A[0]*B[1]-A[1]*B[0] # modulus of cross product equals the area and A[2]=B[2]=0

norm_A = float(np.linalg.norm(A))
norm_B = float(np.linalg.norm(B))

for mec in ls:
    with open(f'./{mec}/positions.fdf', 'r') as f: comment = f.readline().strip().split()
    N = int(comment[1][:-1])
    E = float(popen("""grep "Etot" ./%s/G.out | tail -1 | awk '{print $4}'"""%(mec)).read())
    if '#XY:'==comment[0]:
        E_xy.append((N, E))
    if '#X:'==comment[0]:
        E_x.append((N, E))
        y = np.linalg.norm(list(map(float, popen('sed -n 2p ./%s/G.STRUCT_OUT'%(mec)).read().strip().split() ))) # norm of vector y of the lattice
        y=float(y) #np.float64 to float
        strain_x.append((N, y/norm_B-1))
        
    if '#Y:'==comment[0]:
        E_y.append((N, E))
        x = np.linalg.norm(list(map(float, popen('sed -n 1p ./%s/G.STRUCT_OUT'%(mec)).read().strip().split() ))) # norm of vector y of the lattice
        x = float(x)
        strain_y.append((N, x/norm_A-1))
threshold = 5 # in percentage 

#..............................................
#                   XY
#..............................................

A = [(1+E_xy[i][0]/100)**2 for i in range(len(E_xy)) if abs(E_xy[i][0])<=threshold] # area strain
E = [E_xy[i][1] for i in range(len(E_xy)) if abs(E_xy[i][0])<=threshold]
p = np.polyfit(A, E, 2)
bulk_modulus = 2*p[0]*cte/A_0
print(f"bulk modulus = {bulk_modulus} J/m^2")

#..............................................
#                   X
#..............................................

epsx= [E_x[i][0]/100 for i in range(len(E_x)) if abs(E_x[i][0])<=threshold] # area strain
E = [E_x[i][1] for i in range(len(E_x)) if abs(E_x[i][0])<=threshold]
p = np.polyfit(epsx, E, 2)
Y2D_x = 2*p[0]*cte/A_0
print(f"2D Young modulus with x fixed= {Y2D_x} J/m^2")
eps1 = [strain_x[i][0]/100 for i in range(len(strain_x)) if abs(strain_x[i][0])<=threshold]
eps2 = [strain_x[i][1] for i in range(len(strain_x)) if abs(strain_x[i][0])<=threshold]
p=np.polyfit(eps1, eps2, 1)
poisson_x = -p[0]
print(f"poisson coefficient with x fixed = {poisson_x}")
pred_bulk = Y2D_x/(2*(1-poisson_x))
print(f"Expected bulk modulus of {pred_bulk:.4f} with error of {100*abs(pred_bulk/bulk_modulus-1):.4f}% with relation to computed bulk modulus")

#..............................................
#                   Y
#..............................................

epsx= [E_y[i][0]/100 for i in range(len(E_y)) if abs(E_y[i][0])<=threshold] # area strain
E = [E_y[i][1] for i in range(len(E_y)) if abs(E_y[i][0])<=threshold]
p = np.polyfit(epsx, E, 2)
Y2D_y = 2*p[0]*cte/A_0
print(f"2D Young modulus with y fixed= {Y2D_y} J/m^2")
eps1 = [strain_y[i][0]/100 for i in range(len(strain_y)) if abs(strain_y[i][0])<=threshold]
eps2 = [strain_y[i][1] for i in range(len(strain_y)) if abs(strain_y[i][0])<=threshold]
p=np.polyfit(eps1, eps2, 1)
poisson_y = -p[0]
print(f"poisson coefficient with x fixed = {poisson_y}")
pred_bulk = Y2D_y/(2*(1-poisson_y))
print(f"Expected bulk modulus of {pred_bulk:.4f} with error of {100*abs(pred_bulk/bulk_modulus-1):.4f}% with relation to computed bulk modulus")
