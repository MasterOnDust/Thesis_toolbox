from fpcluster import get_distance_circles
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from fpcluster.adaptive_kmeans import center_of_mass_trajectory
from dust.plot.maps import map_terrain_china, map_china
import numpy as np
import cartopy.crs as ccrs
import fpcluster as fc
from fpcluster.plot_trajectories import dist_from_center

def plot_center_spread_trajectory(ds,weights=None, ax=None, mapping='terrain', color='red', method='std', plot_spread=True,
                                   add_trajectory_marks=False,mark_size=1,color_markers='#F01846',trajectory_marker='D',
                                   alpha_spread=.5,receptor_marker_color=None,
                                   scatter_kwargs=dict(edgecolors='black',linewidth=1, s=70), **kwargs):
    """
    plot center trajectory with spread, ds is a dataset containing the trajectories. 
    """
    
    xcenter,ycenter = center_of_mass_trajectory(ds.lons.values,ds.lats.values, weights=weights)
    
    
    height = np.average(ds.height.values-ds.mean_topo.values,weights=weights,axis=1)
    
    

    if ax == None:
        ax = plt.gca()
    
    fc.plot_trajectories.plot_center_trajectory(xcenter,ycenter, height=height,
                                  p0=[ds.lon0,ds.lat0],ax=ax, receptor_marker_color=receptor_marker_color, 
                                  scatter_kwargs=scatter_kwargs)
    if add_trajectory_marks:
        ax.scatter(xcenter[::4][1:],ycenter[::4][1:],  marker=trajectory_marker, color=color_markers, zorder=2000,s=mark_size, edgecolors='black')
    if plot_spread:
        
        geoms = get_distance_circles(ds.lons,ds.lats,xcenter, ycenter, method=method, weight=weights)

        ax.add_geometries(geoms, crs=ccrs.PlateCarree(), facecolor=color, edgecolor='none', 
        linewidth=4, alpha=alpha_spread)
    if mapping == 'terrain':
        map_terrain_china(ax)
    elif mapping == 'plain':
        map_china(ax)
    elif mapping == 'none' :
        pass
    else:
        raise(ValueError(f'{mapping} is invalid use either terrain or plain'))