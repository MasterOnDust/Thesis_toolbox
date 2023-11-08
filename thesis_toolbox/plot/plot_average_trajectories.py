import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from dust.plot.maps import map_terrain_china, map_china
from thesis_toolbox.plot.trajectory_plotting import plot_center_spread_trajectory
from thesis_toolbox.utils import get_locations_CLP
import numpy as np
import matplotlib.cm as cm
import matplotlib
import pandas as pd

def plot_trajectories_all_locs(dsets,kind='drydep',vmin=0,vmax=5000, axes=None, 
                                        add_colorbar=True,add_letters=True, locs=None, colors=None
                                         ,join_trajec_to_receptor=False):
    if isinstance(locs, pd.core.indexes.base.Index) or isinstance(locs, type([])) or isinstance(locs, np.ndarray):
        locs = locs
    else:
        locs = get_locations_CLP().index
    if colors:
        colors=colors
    else:
        colors = ['tab:blue', 'tab:orange','tab:green','tab:red','tab:purple','tab:brown','tab:pink','tab:gray','tab:olive','tab:cyan']
    if axes == None:
        fig,(ax,ax1) = plt.subplots(ncols=2,subplot_kw={'projection':ccrs.PlateCarree()}, figsize=(12,5))
    else:
        ax = axes[0]
        ax1 = axes[1]
    map_terrain_china(ax)
    for i,location in enumerate(locs):
        ds = dsets[f'dust_loading_traj_{kind}_2micron_{location}']
        plot_center_spread_trajectory(ds, ax =ax,mapping='none',
                                     weights=ds[kind], plot_spread=False,vmin=vmin,vmax=vmax, 
                                      add_trajectory_marks=True, mark_size=2, receptor_marker_color=colors[i],
                                      join_trajec_to_receptor=join_trajec_to_receptor)
    map_terrain_china(ax1)
    for i,location in enumerate(locs):
        ds = dsets[f'dust_loading_traj_{kind}_20micron_{location}']
        plot_center_spread_trajectory(ds, ax =ax1,mapping='none',
                                     weights=ds[kind], plot_spread=False,vmin=vmin,vmax=vmax, 
                                      add_trajectory_marks=True, mark_size=2,receptor_marker_color=colors[i],
                                     join_trajec_to_receptor=join_trajec_to_receptor)
        
    
    if add_letters:
        add_letter(np.array((ax,ax1)),y=0.87)
    if add_colorbar:
        fig = plt.gcf()
        cbar_ax = fig.add_axes([0.15,0.01, 0.7,0.07])
        fig.colorbar(cm.ScalarMappable(norm=matplotlib.colors.Normalize(vmin=vmin,vmax=vmax)), 
                 label='Height above ground [m]',orientation='horizontal',cax=cbar_ax)


def plot_trajectory_height_all_locs(dsets,kind='drydep',vmin=0,vmax=5000, axes=None, 
                                    add_letters=True, btime_limit=72, locs=None, colors=None):
    if isinstance(locs, pd.core.indexes.base.Index) or isinstance(locs, type([])) or isinstance(locs, np.ndarray):
        locs = locs
    else:
        locs = get_locations_CLP().index
    if axes == None:
        fig,(ax,ax1) = plt.subplots(ncols=2,subplot_kw={'projection':ccrs.PlateCarree()}, figsize=(12,5))
    else:
        ax = axes[0]
        ax1 = axes[1]
    for i,location in enumerate(locs):
        ds = dsets[f'dust_loading_traj_{kind}_2micron_{location}'].sel(btime=slice(0,-btime_limit*3600))
        height = ds.height - ds.mean_topo
        height = np.average(height,weights=ds[kind],axis=1)
        time = np.abs(ds.btime/3600)
        ax.set_xticks(np.arange(0,btime_limit+12,12))
        if colors:
            ax.plot(time , height, label=location, color=colors[i])
        else:
            ax.plot(time , height, label=location)

    for i,location in enumerate(locs):
        ds = dsets[f'dust_loading_traj_{kind}_20micron_{location}'].sel(btime=slice(0,-btime_limit*3600))
        height = ds.height - ds.mean_topo
        height = np.average(height,weights=ds[kind],axis=1)
        ax1.set_xticks(np.arange(0,btime_limit+12,12))
        time = np.abs(ds.btime/3600)
        
        if colors:
            ax1.plot(time , height, label=location, color=colors[i])
        else:
            ax1.plot(time , height, label=location)
    
    if add_letters:
        add_letter(np.array((ax,ax1)),y=0.87)