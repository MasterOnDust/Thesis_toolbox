import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from .tools import map_large_scale
import numpy as np

def plot_500hPa_composite(ds,ax=None, label='', add_colorbar=True):
    if ax==None:
        ax = plt.gca()
    map_large_scale(ax)
    im = ds.hws.plot.contourf(transform=ccrs.PlateCarree(),  levels= np.linspace(-7.5,7.5,16),
                                                    cmap='bwr', add_colorbar=False, ax=ax)
    CS = ds.Z.plot.contour(transform=ccrs.PlateCarree(), ax=ax,colors='black', linewidths=1, 
                       add_labels=False, alpha=1,  vmin=-6, vmax=6, levels=13)
#     print(CS.levels)
    CS.collections[6].set_linewidth(3)
    ax.text( x=0.03,y=0.94, s=label, fontsize=16, transform=ax.transAxes)

    Q = ax.quiver(ds.longitude[::22], ds.latitude[::22], ds.u[::22,::22], 
                   ds.v[::22,::22],transform=ccrs.PlateCarree(),color='saddlebrown', 
              scale_units='xy', zorder=1002, minlength=2, pivot='middle')
    ax.clabel(CS, fmt='%d', colors='black', fontsize=12, inline=1, zorder=1030)
    qk=ax.quiverkey(Q, 0.92,0.95, U=2, label='2 m/s', labelpos='E', coordinates='axes', color='black')
    qk.text.set_backgroundcolor('w')
    ax.set_xlabel('')
    ax.set_ylabel('')
    
    if add_colorbar:
        fig =plt.gcf()
        fig.colorbar(im, ax=ax, label='Composite difference 500hPa winds [m/s] \n  (strong years - weak years)',
            ticks=im.levels, pad=0.01)


def plot_200hPa_composite(ds,ax=None, label='', add_colorbar=True):
    if ax==None:
        ax = plt.gca()
    map_large_scale(ax)
    im = ds.hws.plot.contourf(transform=ccrs.PlateCarree(),
                                        cmap='bwr', add_colorbar=False, ax=ax, levels=np.linspace(-9,9, 16))
    ax.text( x=0.03,y=0.94, s=label, fontsize=16, transform=ax.transAxes)
    ax.set_xlabel('')
    ax.set_ylabel('')
    CS = ds.Z.plot.contour(transform=ccrs.PlateCarree(), ax=ax,colors='black', linewidths=1, add_labels=False, alpha=1, 
                           vmin=-6, vmax=6, levels=13)
    CS.collections[6].set_linewidth(3)
    ax.clabel(CS, fmt='%d', colors='black', fontsize=12, inline=1, zorder=1030)
    if add_colorbar:
        fig =plt.gcf()
        fig.colorbar(im, ax=ax, label='Composite difference 200hPa winds [m/s] \n  (strong years - weak years)',
            ticks=im.levels, pad=0.01)

        
def plot_mslp_850hpa_composite(ds, oro ,ax=None, label='', add_colorbar=True, title=''):
    oro = oro.sel(longitude=slice(69,105), latitude=slice(40,27)).isel(time=0)
    if ax==None:
        ax = plt.gca()
    im = ds.msl.plot.contourf(transform=ccrs.PlateCarree(),levels=16, vmin=-6, vmax=6,
                                                                cmap='bwr', add_colorbar=False, ax=ax)
    Q = ax.quiver(ds.longitude[::22], ds.latitude[::22], ds.u[::22,::22], 
                   ds.v[::22,::22],transform=ccrs.PlateCarree(),color='saddlebrown', 
              scale_units='xy', zorder=1002, minlength=2, pivot='middle')
    qk=ax.quiverkey(Q, 0.93,0.96, U=2, label='2 m/s', labelpos='E', coordinates='axes', color='black')
    qk.text.set_backgroundcolor('w')
    oro.z.where(oro.z > 33000,drop=True).plot.contourf(transform=ccrs.PlateCarree(),
                                                       levels=2, colors='lightgrey'
                                                        , add_colorbar=False,ax =ax, zorder=1100, hatches='/')
    if add_colorbar:
        fig=plt.gcf()
        fig.colorbar(im, ax=ax, 
             label='Mean Sea Level Pressure \n  (strong years - weak years)',
            ticks=im.levels, pad=0.01)
    ax.text( x=0.03,y=0.94, s=label, fontsize=16, transform=ax.transAxes)
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_title(title)