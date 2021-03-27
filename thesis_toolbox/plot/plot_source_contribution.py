import xarray as xr 
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import glob
from thesis_toolbox.utils import get_locations_CLP
from thesis_toolbox.plot.tools import add_letter
from DUST.plot.plotting import mpl_base_map_plot_xr,plot_log_anomaly
from DUST.plot.maps import map_terrain_china, map_china
from DUST.plot.utils import _gen_flexpart_colormap,_add_colorbar
from matplotlib.colors import LogNorm
import numpy as np


def depositon_facet_plot( total_depo,wet_depo,dry_depo,locs=None,**mesh_kwargs):
    if locs == None:
        locs = get_locations_CLP()
    
    fig, ax = plt.subplots(nrows=4, ncols=2, figsize=(13,15), subplot_kw={'projection':ccrs.PlateCarree()})
    
    plt.subplots_adjust(hspace=0.0)
    axes = ax.ravel()
    for i,dvar in enumerate(total_depo.data_vars):
        map_terrain_china(axes[i])
        mpl_base_map_plot_xr(total_depo[dvar], colorbar=True,ax=axes[i], extend='max', **mesh_kwargs)
        axes[i].set_title(total_depo.locations[i])
        axes[i].scatter(locs.loc[total_depo.locations[i],:][0],
                        locs.loc[total_depo.locations[i],:][1],marker='*', color='black', zorder=1300)
    ax1 = fig.add_subplot(4,2,8)
    ax[3,1] = ax1
    add_letter(ax)
    deposition_bar_plot(wet_depo,dry_depo, locs=locs.index, ax=ax1)


def composite_depositon_facet_plot(total_depo,wet_depo,dry_depo,lin_tresh,vmin,vmax,locs=None,lower_bound=-5e-8,upper_bound=5e-8,**mesh_kwargs):
    if isinstance(locs,np.ndarray):
        locs=locs
    else:
        locs = get_locations_CLP()
    
    fig, ax = plt.subplots(nrows=4, ncols=2, figsize=(13,15), subplot_kw={'projection':ccrs.PlateCarree()})
    
    plt.subplots_adjust(hspace=0.0)
    axes = ax.ravel()
    for i,dvar in enumerate(total_depo.data_vars):
        map_terrain_china(axes[i])
        plot_log_anomaly(total_depo[dvar], lin_tresh,vmin,vmax,ax=axes[i], cmap='bwr', lower_bound=lower_bound,upper_bound=upper_bound, **mesh_kwargs)
        axes[i].set_title(total_depo.locations[i])
        axes[i].scatter(locs.loc[total_depo.locations[i],:][0],
                        locs.loc[total_depo.locations[i],:][1],marker='*', color='black', zorder=1300)
    ax1 = fig.add_subplot(4,2,8)
    ax[3,1] = ax1
    add_letter(ax)
    deposition_bar_plot(wet_depo,dry_depo, locs=locs.index, ax=ax1,y_axis_label='Deposition rate difference [g\m^2 s] \n (Strong years - weak yeak)')

def deposition_bar_plot(wet_dep,dry_dep,locs,ax=None, units=None, n_days=87, y_axis_label=None):
    if ax == None:
        ax = plt.gca()
    ax.yaxis.tick_right()
    if units=='kg':
        wet_dep = wet_dep.sum(dim=['lon','lat'])*n_days*24*60*60/1000
        dry_dep = dry_dep.sum(dim=['lon','lat'])*n_days*24*60*60/1000
        if y_axis_label:
            ax.set_ylabel(y_axis_label)
        else:
            ax.set_ylabel('Average Depostion [kg/m2]')
    else:
        wet_dep = wet_dep.sum(dim=['lon','lat'])
        dry_dep = dry_dep.sum(dim=['lon','lat'])
        if y_axis_label:
            ax.set_ylabel(y_axis_label)
        else:
            ax.set_ylabel('Average Depostion rate [g/m^2 s]')
    ax.bar(range(1,len(locs)+1),[wet_dep[dvar].values for dvar in wet_dep.data_vars],
           color='lightseagreen', label='Wet Depositon' )
    ax.bar(range(1,len(locs)+1),[dry_dep[dvar].values for dvar in dry_dep.data_vars],
           bottom=[wet_dep[dvar].values for dvar in wet_dep.data_vars],color='darkgoldenrod', label='Dry Depostion')
    ax.set_xticks(range(1,len(locs)+1))
    ax.set_xticklabels(locs,rotation = 90)
    ax.yaxis.set_label_position("right")
    ax.legend()      