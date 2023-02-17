import xarray as xr 
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import glob
from thesis_toolbox.utils import get_locations_CLP
from thesis_toolbox.plot.tools import add_letter
from dust.plot.plotting import mpl_base_map_plot_xr,plot_log_anomaly
from dust.plot.maps import map_terrain_china, map_china
from dust.plot.utils import _gen_flexpart_colormap,_add_colorbar
from matplotlib.colors import LogNorm
import numpy as np


def depositon_facet_plot( total_depo,wet_depo=None,dry_depo=None,ylabel_bar_plot=None,ylim=None,
                        figsize=(8.3,11.7),fontsize_title=14,hspace=0.5,wspace=None, ax = None,
                        no_tick_labels=False, title=True, **mesh_kwargs):
    locations_df = get_locations_CLP()
    
    if isinstance(ax, np.ndarray) == False:
        fig, ax = plt.subplots(nrows=4, ncols=2, figsize=figsize, subplot_kw={'projection':ccrs.PlateCarree()})
    

    plt.subplots_adjust(hspace=hspace, wspace=wspace)
    axes = ax.ravel()
    for i,dvar in enumerate(total_depo.data_vars):
        map_terrain_china(axes[i])
        mpl_base_map_plot_xr(total_depo[dvar], ax=axes[i], extend='max', **mesh_kwargs)
        if total_depo.locations[i] == 'BADOE':
            loc_name = 'BAODE'
        else:
            loc_name = total_depo.locations[i]
        if title:
            axes[i].set_title(loc_name, fontsize=fontsize_title)
        axes[i].scatter(locations_df.loc[total_depo.locations[i],:][0],
                        locations_df.loc[total_depo.locations[i],:][1],marker='*', color='black', zorder=1300)
        if no_tick_labels:
            axes[i].yaxis.set_ticklabels([])
            axes[i].xaxis.set_ticklabels([])

        elif i in (1,3,5):
            axes[i].yaxis.set_ticklabels([])
    if wet_depo and dry_depo:
    
        ax1 = fig.add_subplot(4,2,8)
        ax[3,1] = ax1
        add_letter(ax,y=0.87)
        deposition_bar_plot(wet_depo,dry_depo, y_axis_label=ylabel_bar_plot,ax=ax1,ylim=ylim)


def composite_depositon_facet_plot(total_depo,lin_tresh,vmin,vmax,wet_depo=None,dry_depo=None,ax=None,figsize=(8.3,11.7),
                                lower_bound=-5e-8,upper_bound=5e-8,fontsize_title=14,hspace=0.5,wspace=None, add_site_name=True,
                                no_tick_labels=False,
                                **mesh_kwargs):
    locations_df = get_locations_CLP()

    if isinstance(ax, np.ndarray) == False:
        fig, ax = plt.subplots(nrows=4, ncols=2, figsize=figsize, subplot_kw={'projection':ccrs.PlateCarree()})
    
    # plt.subplots_adjust(hspace=hspace, wspace=wspace)
    axes = ax.ravel()
    for i,dvar in enumerate(total_depo.data_vars):
        map_terrain_china(axes[i])
        plot_log_anomaly(total_depo[dvar], lin_tresh,vmin,vmax,ax=axes[i], cmap='bwr', lower_bound=lower_bound,upper_bound=upper_bound, **mesh_kwargs)
        if total_depo.locations[i] == 'BADOE':
            loc_name = 'BAODE'
        else:
            loc_name = total_depo.locations[i]
        if add_site_name:
            axes[i].set_title(loc_name, fontsize=fontsize_title)
        axes[i].scatter(locations_df.loc[total_depo.locations[i],:][0],
                        locations_df.loc[total_depo.locations[i],:][1],marker='*', color='black', zorder=1300)
        if no_tick_labels:
            axes[i].yaxis.set_ticklabels([])
            axes[i].xaxis.set_ticklabels([])
        
        elif i in (1,3,5):
            axes[i].yaxis.set_ticklabels([])
    if wet_depo and dry_depo:        
        ax1 = fig.add_subplot(4,2,8)
        ax[3,1] = ax1
        add_letter(ax,y=0.87)

        deposition_bar_plot(wet_depo,dry_depo,  ax=ax1,
        y_axis_label='Deposition rate [$\mathrm{g/m}^2$] \n (Strong years - weak yeak)')

def deposition_bar_plot(wet_dep,dry_dep,ax=None, y_axis_label=None, ylim=None):
    if ax == None:
        ax = plt.gca()
    ax.yaxis.tick_right()
    wet_dep = wet_dep.sum(dim=['lon','lat'])
    dry_dep = dry_dep.sum(dim=['lon','lat'])
    locs = wet_dep.locations
    if locs[4] =='BADOE':
        locs[4] = 'BAODE'

    if y_axis_label:
        ax.set_ylabel(y_axis_label)
    else:
        ax.set_ylabel('Average Depostion [$\mathrm{g/m}^2$]')
    ax.bar(range(1,len(locs)+1),[wet_dep[dvar].values for dvar in wet_dep.data_vars],
           color='lightseagreen', label='Wet Depositon' )
    ax.bar(range(1,len(locs)+1),[dry_dep[dvar].values for dvar in dry_dep.data_vars],
           bottom=[wet_dep[dvar].values for dvar in wet_dep.data_vars],color='darkgoldenrod', label='Dry Depostion')
    ax.set_xticks(range(1,len(locs)+1))
    ax.set_xticklabels(locs,rotation = 90)
    ax.yaxis.set_label_position("right")
    if ylim:
        ax.set_ylim(ylim)
    ax.legend(fontsize='small')      