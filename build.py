import math
import meep as mp
from meep import mpb
import matplotlib.pyplot as plt
import sys

def log_file(fuct,out_file='./temp.log'):
    current = sys.stdout
    f = open(out_file, 'w+')
    sys.stdout = f
    fuct
    sys.stdout = current
    
def tri_rods(out_file,a=50,k=0.25,num_bands=8):
    k_points = [mp.Vector3(),          # Gamma
                mp.Vector3(y=0.5),       # M
                mp.Vector3(-1/3, 1/3),  # K
                mp.Vector3()]          # Gamma
    k_points = mp.interpolate(8, k_points)

    geometry = [mp.Cylinder(k*a, material=mp.Medium(epsilon=1.999146519**2))]
    geometry_lattice = mp.Lattice(basis1=mp.Vector3(math.sqrt(3)/2,0.5),
                                basis2=mp.Vector3(math.sqrt(3)/2,-0.5),
                                basis3=mp.Vector3(0,0,1),
                                basis_size=mp.Vector3(a, a, a),size=mp.Vector3(1, 1))

    resolution = 32
    ms = mpb.ModeSolver(num_bands=num_bands,
                        k_points=k_points,
                        geometry=geometry,
                        geometry_lattice=geometry_lattice,
                        resolution=resolution)

    '''Hexagonal lattice of rods: all bands'''

    current = sys.stdout
    f = open(out_file, 'w+')
    sys.stdout = f
    ms.run_tm()
    sys.stdout = current

    md = mpb.MPBData(rectify=True, periods=3, resolution=32)
    eps = ms.get_epsilon()
    converted_eps = md.convert(eps)
    plt.imshow(converted_eps.T, interpolation='spline36', cmap='binary')
    plt.axis('off')
    plt.show()