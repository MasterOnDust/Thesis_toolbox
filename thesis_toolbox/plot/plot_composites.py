import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from .tools import map_large_scale, add_colorbar
import numpy as np
import xarray as xr


def plot_500hPa_composite(ds,ax=None, label='', colorbar=True, x_qk=0.93, y_qk=0.9, receptor_loc=None
                            ,receptor_name=None,vector_scale=1, angles='xy'):
    if ax==None:
        ax = plt.gca()
    map_large_scale(ax)
    extent = ax.get_extent()
    ds = ds.sel(longitude=slice(extent[0],extent[1]),latitude=slice(extent[3],extent[2]))
    if receptor_name and isinstance(receptor_name,str):
        Z = receptor_name+'_Z'
        u = receptor_name+'_u'
        v = receptor_name+'_v'
        hws = receptor_name+'_hws'
    else:
        Z='Z'
        u = 'u'
        v = 'v'
        hws = 'hws'
    im = ds[hws].plot.contourf(transform=ccrs.PlateCarree(),  levels= np.linspace(-7.5,7.5,16),
                                                    cmap='bwr', add_colorbar=False, ax=ax)
    CS = ds[Z].plot.contour(transform=ccrs.PlateCarree(), ax=ax,colors='black', linewidths=1, 
                       add_labels=False, alpha=1,  vmin=-6, vmax=6, levels=13)
#     print(CS.levels)
    CS.collections[6].set_linewidth(3)
    ax.text( x=0.03,y=0.94, s=label, fontsize=16, transform=ax.transAxes)

    Q = ax.quiver(ds.longitude[::22], ds.latitude[::22], ds[u][::22,::22], 
                   ds[v][::22,::22],transform=ccrs.PlateCarree(),color='saddlebrown', 
              units='xy', zorder=1002, minlength=2, pivot='middle', scale=vector_scale,angles=angles)
    # ax.clabel(CS, fmt='%d', colors='black', fontsize=12, inline=1, zorder=1030)
    qk=ax.quiverkey(Q, x_qk,y_qk, U=2, label='2 m/s', labelpos='E', coordinates='axes', color='black')
    qk.text.set_backgroundcolor('w')
    ax.set_xlabel('')
    ax.set_ylabel('')
    
    if colorbar:
        add_colorbar(im,im.levels, label='Composite difference 500hPa winds [m/s] \n  (strong years - weak years)')
    if receptor_loc and isinstance(receptor_loc,list):
        ax.scatter(receptor_loc[0], receptor_loc[1], color='black', marker='*')

def plot_200hPa_composite(ds,ax=None, label='', colorbar=True, receptor_loc=None):
    if ax==None:
        ax = plt.gca()
    map_large_scale(ax)
    extent = ax.get_extent()
    ds = ds.sel(longitude=slice(extent[0],extent[1]),latitude=slice(extent[3],extent[2]))
    im = ds.hws.plot.contourf(transform=ccrs.PlateCarree(),
                                        cmap='bwr', add_colorbar=False, ax=ax, levels=np.linspace(-9,9, 16))
    ax.text( x=0.03,y=0.94, s=label, fontsize=16, transform=ax.transAxes)
    ax.set_xlabel('')
    ax.set_ylabel('')
    CS = ds.Z.plot.contour(transform=ccrs.PlateCarree(), ax=ax,colors='black', linewidths=1, add_labels=False, alpha=1, 
                           vmin=-6, vmax=6, levels=13)
    CS.collections[6].set_linewidth(3)
    ax.clabel(CS, fmt='%d', colors='black', fontsize=12, inline=1, zorder=1030)
    if colorbar:
        add_colorbar(im,im.levels, label='Composite difference 200hPa winds [m/s] \n  (strong years - weak years)')
    if receptor_loc and isinstance(receptor_loc,list):
        ax.scatter(receptor_loc[0], receptor_loc[1], color='black', marker='*')

        
def plot_mslp_850hpa_composite(ds, 
oro='/mnt/acam-ns2806k/ovewh/tracing_the_winds/Master_thesis_UiO_workflow/Master_thesis_UiO_workflow/downloads/ERA5_orography.nc' 
                                ,ax=None, x_qk=0.93, y_qk=0.9, label='', colorbar=True, title='', receptor_loc=None,
                                receptor_name=None, vector_scale=1, angles='xy'):
    oro = xr.open_dataset(oro)
    oro = oro.sel(longitude=slice(69,105), latitude=slice(40,27)).isel(time=0)
    if receptor_name and isinstance(receptor_name,str):
        msl = receptor_name+'_msl'
        u = receptor_name+'_u'
        v = receptor_name+'_v'
    else:
        msl='msl'
        u = 'u'
        v = 'v'
    if ax==None:
        ax = plt.gca()
    map_large_scale(ax)
    extent = ax.get_extent()
    ds = ds.sel(longitude=slice(extent[0],extent[1]),latitude=slice(extent[3],extent[2]))
    im = ds[msl].plot.contourf(transform=ccrs.PlateCarree(),levels=16, vmin=-6, vmax=6,
                                                                cmap='bwr', add_colorbar=False, ax=ax)
    Q = ax.quiver(ds.longitude[::22], ds.latitude[::22], ds[u][::22,::22], 
                   ds[v][::22,::22],transform=ccrs.PlateCarree(),color='saddlebrown', 
              units='xy', zorder=1002, minlength=2, pivot='middle', scale=vector_scale, angles = angles)
    qk=ax.quiverkey(Q, x_qk,y_qk, U=2, label='2 m/s', labelpos='E', coordinates='axes', color='black')
    qk.text.set_backgroundcolor('w')
    oro.z.where(oro.z > 33000,drop=True).plot.contourf(transform=ccrs.PlateCarree(),
                                                       levels=2, colors='lightgrey'
                                                        , add_colorbar=False,ax =ax, zorder=1100, hatches='/')
    if colorbar:
        add_colorbar(im,im.levels, label='Mean Sea Level Pressure \n  (strong years - weak years)')
    if receptor_loc and isinstance(receptor_loc,list):
        ax.scatter(receptor_loc[0], receptor_loc[1], color='black', marker='*')

    ax.text( x=0.03,y=0.94, s=label, fontsize=16, transform=ax.transAxes)
    
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_title(title)

def plot_which_years_composited(composite_ds,ax=None):
    if ax==None:
        ax = plt.gca()
    ax.cla()
    ax.set_xticks(range(1999,2020))
    ax.set_xlim(1998,2020)
    ax.set_xticklabels(ax.get_xticks(), rotation = 45)
    ax.yaxis.tick_right()
    ax.set_yticklabels(composite_ds.attrs['locations'])
    ax.set_yticks(range(1,9))
    variable = list(composite_ds.data_vars)[0].split('_')[-1]
    n = 1
    for loc in composite_ds.attrs['locations']:
        ax.scatter((composite_ds[loc+'_'+variable].strong_years),[n for i in range(len(composite_ds[loc+'_'+variable].strong_years))],color='deeppink')
        ax.scatter((composite_ds[loc+'_'+variable].weak_years),[n for i in range(len(composite_ds[loc+'_'+variable].weak_years))], color='slateblue')
        
        n=n+1
    ax.set_ylim(0,9)
    ax.legend(['Strong years','Weak Years'],mode='expand', ncol=2, frameon=False)