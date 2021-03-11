import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import .tools import map_large_scale
import numpy as np

def plot_climatology_500hpa(ds, ax=None, label='', title='', add_colorbar=True):
    if ax == None:
        ax = plt.gca()
    map_large_scale(ax)
    im = ds.hws.where(ds.hws_clim > 10, drop=True).plot.contourf(transform=ccrs.PlateCarree(), levels=np.arange(12,33,3), 
                                                            cmap='viridis_r', extend='neither', add_colorbar=False,ax =ax)
    CS = ds.Z.plot.contour(transform=ccrs.PlateCarree(), ax=ax,colors='black', linewidths=.7, levels=np.arange(510,592,4), add_labels=False, alpha=1)
    CS.collenctions[2].set_linewidth(3)
    ax.clabel(CS, fmt='%d', colors='black', fontsize=12, inline=1, zorder=1030)
    Q = ax.quiver(ds.longitude[::22], ds.latitude[::22], ds.u_clim[::22,::22], ds.v_clim[::22,::22],transform=ccrs.PlateCarree(),color='saddlebrown', 
              scale_units='xy', zorder=1002, minlength=2, pivot='middle')
    ax.quiverkey(Q, 0.9,0.8, U=20, label='20 m/s', labelpos='E')
    ax.set_xlabel('')
    ax.set_ylabel('')
    if add_colorbar:
        fig.plt.gcf()
        fig.colorbar(im, ax=ax, ticks=im.levels, pad=0.01, label='500hPa windspeed [m/s]')

        
