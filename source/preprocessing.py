def plot3D(sim,xrange:list=None,yrange:list=None,zrange:list=None,color_scale=["rgba(240,250,35,0)","rgba(247,149,65,0.2)","rgba(201,70,122,0.3)","rgba(122,5,166,0.4)","rgba(13,8,135,0.5)"]):
    import plotly.express as px
    import plotly.graph_objects as go
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
    ccs=color_scale
    #plot
    fig = go.Figure(data=go.Volume(
    x=view['x'],
    y=view['y'],
    z=view['z'],
    value=view['epsilon'],
    colorscale=ccs,
    slices_y=dict(show=True, locations=[view['y'][-1]/2]),
    slices_x=dict(show=True, locations=[view['x'][-1]/2]),
    surface=dict(show=False),
    spaceframe=dict(fill=1,show=True),
    caps= dict(x_show=False, y_show=False, z_show=False),
    ))
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0),
                      scene = dict(xaxis = dict(range=xrange,),yaxis = dict(range=yrange,),zaxis = dict(range=zrange,)),
                      width=600)
    fig.update_scenes(aspectmode='data')
    fig.show()
    return fig