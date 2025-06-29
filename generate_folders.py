from os import popen
N=0
supercell_positions = str()
number_of_atoms = int()
def from_STRUCT(filename):
    global number_of_atoms
    with open(f"{filename}", 'r') as f: s=f.read().split('\n')
    cell = s[0:3]
    cell = [list(map(float, cell[i].strip().split())) for i in range(3)]
    for i in range(4): s.pop(0)
    if s[-1]==str(): s.pop(-1)
    pos= [list(map(float, s[i].strip().split())) for i in range(len(s))]
    species = [int(pos[i][0]) for i in range(len(pos))]
    atoms = [int(pos[i][1]) for i in range(len(pos))]
    number_of_atoms = len(atoms)
    pos = [pos[i][2:] for i in range(len(pos))]
    supercell_positions = str()
    for i in range(len(pos)): supercell_positions+=f"{pos[i][0]:14.8f}{pos[i][1]:14.8f}{pos[i][2]:14.8f}{species[i]:4d}{i+1:8d}  {'C' if atoms[i]==6 else 'H'}\n"
    return cell, supercell_positions

def position_file(cell, comment=str()):
    global N, supercell_positions, number_of_atoms
    return f"""#{comment}
NumberOfAtoms {number_of_atoms}
NumberOfSpecies 2

%block Chemical_Species_label
  1   1   H
  2   6   C
%endblock Chemical_Species_label

LatticeConstant 1.000 Ang

%block LatticeVectors
{cell[0][0]:21.9f}{cell[0][1]:18.9f}{cell[0][2]:18.9f}
{cell[1][0]:21.9f}{cell[1][1]:18.9f}{cell[1][2]:18.9f}
{cell[2][0]:21.9f}{cell[2][1]:18.9f}{cell[2][2]:18.9f}
%endblock LatticeVectors

#..............................................
#         Atomic coordinates
#..............................................
AtomicCoordinatesFormat  Fractional
%block AtomicCoordinatesAndAtomicSpecies
{supercell_positions}
%endblock AtomicCoordinatesAndAtomicSpecies
"""
def create_dir(foldername, cell, xy=str(), comment=str()):
    global N
    print(popen(f"mkdir {foldername}").read())
    print(popen(f"cp C.psf {foldername}").read())
    print(popen(f"cp H.psf {foldername}").read())
    if xy=='x': print(popen(f"cat G_x.fdf > ./{foldername}/G.fdf").read())
    if xy=='y': print(popen(f"cat G_y.fdf > ./{foldername}/G.fdf").read())
    if xy=='xy': print(popen(f"cat G_xy.fdf > ./{foldername}/G.fdf").read())
    with open(f"./{foldername}/positions.fdf", 'w+') as f: f.write(position_file(cell, comment=comment))
    N+=1
    return;
#       usefull bash commands
#       grep "Etot" G.out | awk '{print $4}'
#       awk '/Stress tensor \(total\)/ {print; count=3; next} count > 0 {print; count--}' G.out
#       

cell,supercell_positions = from_STRUCT('G.STRUCT_OUT')

#..............................................
#                   XY
#..............................................
for i in range(-5, 41, 1):
    alpha=1+i/100
    x=[alpha*cell[0][j] for j in range(3)]
    y=[alpha*cell[1][j] for j in range(3)]
    c = [x, y, cell[2]]
    create_dir(f"mec{N:03d}", cell=c, comment=f"XY: {i}%\n", xy='xy')
#..............................................
#                   X
#..............................................

for i in range(-5, 41, 1):
    alpha=1+i/100
    x=[alpha*cell[0][j] for j in range(3)]
    c = [x, cell[1], cell[2]]
    create_dir(f"mec{N:03d}", cell=c, comment=f"X: {i}%\n", xy='x')
#..............................................
#                   Y
#..............................................

for i in range(-5, 41, 1):
    alpha=1+i/100
    y=[alpha*cell[1][j] for j in range(3)]
    c = [cell[0], y, cell[2]]
    create_dir(f"mec{N:03d}", cell=c, comment=f"Y: {i}%\n", xy='y')
