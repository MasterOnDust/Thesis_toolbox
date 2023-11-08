import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.cm as cm
import matplotlib as mpl
import matplotlib.ticker as mticker
import xarray as xr
from .tools import map_large_scale


def plot_large_scale_correlation_map(r: xr.DataArray, ax=None, p_vals=None, p_val_treshold=0.1,vcenter=None, contourf=False, **kwargs):
    
    plt.rcParams['hatch.color'] = 'cyan'
    if ax==None:
        fig,ax = plt.subplots(subplot_kw={'projection':ccrs.PlateCarree()}, figsize=(10,8))
    else:
        ax=ax
        
    if vcenter:
        norm = mpl.colors.CenteredNorm(vcenter)
    else:
        norm=mpl.colors.CenteredNorm()
    map_large_scale(ax)
    cmap= kwargs.pop('cmap',cm.get_cmap('bwr',11))
    if contourf:
        r.plot.contourf(ax=ax, transform = ccrs.PlateCarree(), cmap=cmap, norm=norm,**kwargs)
    else:
        r.plot(ax=ax, transform = ccrs.PlateCarree(), cmap=cmap, norm=norm,**kwargs)
    if p_vals is not None:
        p_vals.where(p_vals < p_val_treshold,drop=True).plot.contourf(ax=ax,transform=ccrs.PlateCarree(),
                                                                      hatches=[" ","..."],add_colorbar=False,alpha=0, levels=2)

def plot_polar_correlation_map(r: xr.DataArray, ax=None, p_vals=None, p_val_treshold=0.1,vcenter=None, **kwargs):
    
    plt.rcParams['hatch.color'] = 'cyan'
    if ax==None:
        fig,ax = plt.subplots(subplot_kw={'projection':ccrs.Orthographic(90, 90)}, figsize=(10,8))
    else:
        ax=ax
    ax.coastlines(zorder=3) 
    if vcenter:
        norm = mpl.colors.CenteredNorm(vcenter)
    else:
        norm=mpl.colors.CenteredNorm()
    cmap= kwargs.pop('cmap',cm.get_cmap('bwr',11))
    r.plot(ax=ax, transform = ccrs.PlateCarree(), cmap=cmap, norm=norm,**kwargs)
    
    
    if p_vals is not None:
        p_vals.where(p_vals < p_val_treshold,drop=True).plot.contourf(ax=ax,transform=ccrs.PlateCarree(),hatches=[" ","..."],add_colorbar=False,alpha=0, levels=2)
    # p.where(p < 0.05,drop=True).plot.scatter(ax=ax,transform=ccrs.PlateCarree())
    gl=ax.gridlines(draw_labels=True)
    ax.set_extent([-180,180,50,90],crs=ccrs.PlateCarree(135))
    gl.xlocator=mticker.FixedLocator([0,-30,-60,-90,-120,-150,30,60,90,120,150,180])
    gl.y_inline = True
    gl.ylabel_style = {'size': 15, 'color': 'gray'}
    # gl.ylocator=