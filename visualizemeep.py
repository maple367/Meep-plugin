import meep as mp

def plot3D(sim,xrange:list=None,yrange:list=None,zrange:list=None,alpha=1): 
    import plotly.express as px
    import numpy as np 
    import pandas as pd
    from meep.visualization import box_vertices

    if sim.dimensions < 3:
        raise ValueError("Simulation must have 3 dimensions to visualize 3D")

    xmin, xmax, ymin, ymax, zmin, zmax = box_vertices(sim.geometry_center,sim.cell_size) #get grid

    Nx = int(sim.cell_size.x * sim.resolution) + 1
    Ny = int(sim.cell_size.y * sim.resolution) + 1
    Nz = int(sim.cell_size.z * sim.resolution) + 1

    xtics = np.linspace(xmin, xmax, Nx)
    ytics = np.linspace(ymin, ymax, Ny)
    ztics = np.linspace(zmin, zmax, Nz)

    eps_data = sim.get_epsilon_grid(xtics, ytics, ztics) #get epsilon
    coordinate = np.mgrid[0:eps_data.shape[0],0:eps_data.shape[1],0:eps_data.shape[2]] #define coordinate
    view = {'x':coordinate[0].flatten(),'y':coordinate[1].flatten(),'z':coordinate[2].flatten(),'epsilon':np.real(eps_data.flatten())} #define a 3D 'picture'
    
    #plot
    fig = px.scatter_3d(pd.DataFrame(view),x='x', y='y', z='z',
                    color='epsilon',opacity=alpha,width=700,color_continuous_scale='Plasma_r')
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0),scene = dict(
                     xaxis = dict(range=xrange,),
                     yaxis = dict(range=yrange,),
                     zaxis = dict(range=zrange,)))
    fig.show()
    return fig

# %%
Si = mp.Medium(index=3.45)
dpml = 1.0
pml_layers = [mp.PML(dpml)]
sx = 4
sy = 2
sz = 1
cell = mp.Vector3(sx,sy,sz)
s=1
a = 1.0     # waveguide width/height
xodd = 1
resolution = 10   # pixels/μm

k_point = mp.Vector3(0,0,0.5)
geometry = [mp.Block(center=mp.Vector3(-0.5*(s+a)),
                        size=mp.Vector3(a,a,5),
                        material=Si),
            mp.Block(center=mp.Vector3(0.5*(s+a)),
                        size=mp.Vector3(a,a,5),
                        material=Si)]

symmetries = [mp.Mirror(mp.X, phase=-1 if xodd else 1),
                mp.Mirror(mp.Y, phase=-1)]

sim = mp.Simulation(resolution=resolution,
                    cell_size=cell,
                    geometry=geometry,
                    boundary_layers=pml_layers,
                    symmetries=symmetries,
                    k_point=k_point)
                    
view = plot3D(sim,xrange=None,alpha=1) #make xrang=[30,40] to get a cross view
