import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from .tools import map_large_scale, add_colorbar
import numpy as np
import xarray as xr


def plot_500hPa_composite(ds,ax=None, label='', colorbar=True, x_qk=0.93, y_qk=0.9, receptor_loc=None
                            ,receptor_name=None,vector_scale=1, angles='xy',hatches='xx', hatch_color='gray', 
                            forcing='era5', q_density=22,xticks =[20,40,60,80,100,120,140,160,180], yticks=[0,30,60,90],
                            receptor_color='black',receptor_marker_s=135):
    if ax==None:
        ax = plt.gca()
    map_large_scale(ax, xticks = xticks, yticks= yticks)
    extent = ax.get_extent()
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

    if forcing == 'merra2':
        ds = ds.sel(lon=slice(extent[0],extent[1]),lat=slice(extent[2],extent[3]))
        lon = 'lon'
        lat = 'lat'
    else:
        ds = ds.sel(longitude=slice(extent[0],extent[1]),latitude=slice(extent[3],extent[2]))
        lon = 'longitude'
        lat = 'latitude'
    im = ds[hws].plot.contourf(transform=ccrs.PlateCarree(),  levels= np.linspace(-7.5,7.5,16),
                                                    cmap='bwr', add_colorbar=False, ax=ax)
    CS = ds[Z].plot.contour(transform=ccrs.PlateCarree(), ax=ax,colors='black', linewidths=1, 
                       add_labels=False, alpha=1,  vmin=-6, vmax=6, levels=7)
    CS.collections[3].set_linewidth(2)
    ax.text( x=0.03,y=0.94, s=label, fontsize=16, transform=ax.transAxes)
    cs=ds[Z+'_significance_map_005'].where(ds[hws+'_significance_map_005'] !=0, drop=True).plot.contourf(ax=ax,colors='none',hatches=[hatches, None],
                 add_colorbar=False)
    for i, collection in enumerate(cs.collections):
        collection.set_edgecolor(hatch_color)
        collection.set_linewidth(0.)

    Q = ax.quiver(ds[lon][::q_density], ds[lat][::q_density], ds[u][::q_density,::q_density], 
                   ds[v][::q_density,::q_density],transform=ccrs.PlateCarree(),color='saddlebrown', 
              units='xy', zorder=1002, minlength=2, pivot='middle', scale=vector_scale,angles=angles)
    # ax.clabel(CS, fmt='%d', colors='black', fontsize=12, inline=1, zorder=1030)
    qk=ax.quiverkey(Q, x_qk,y_qk, U=2, label='2 m/s', labelpos='E', coordinates='axes', color='black')
    qk.text.set_backgroundcolor('w')
    ax.set_xlabel('')
    ax.set_ylabel('')
    
    if colorbar:
        add_colorbar(im,im.levels, label='Composite difference 500hPa winds [m/s] \n  (strong years - weak years)')
    if receptor_loc and isinstance(receptor_loc,list):
                ax.scatter(receptor_loc[0], receptor_loc[1], color=receptor_color, marker='*', 
                    zorder=2000, edgecolors='black',linewidth=1, s=receptor_marker_s)

def plot_200hPa_composite(ds,ax=None, label='', colorbar=True, receptor_loc=None,  x_qk=0.93, y_qk=0.9,
                            receptor_name=None,vector_scale=1, angles='xy',vmin=-6, vmax=6,hatches='xx', hatch_color='gray',
                            xticks =[20,40,60,80,100,120,140,160,180], yticks=[0,30,60,90]):
    if ax==None:
        ax = plt.gca()
    map_large_scale(ax, xticks = xticks, yticks= yticks)

    extent = ax.get_extent()
    ds = ds.sel(longitude=slice(extent[0],extent[1]),latitude=slice(extent[3],extent[2]))
    if receptor_name and isinstance(receptor_name,str):
        Z = receptor_name+'_Z'

        hws = receptor_name+'_hws'
    else:
        Z='Z'
        hws = 'hws'
    im = ds[hws].plot.contourf(transform=ccrs.PlateCarree(),
                                        cmap='bwr', add_colorbar=False, ax=ax, levels=np.linspace(-9,9, 16))
    ax.text( x=0.03,y=0.94, s=label, fontsize=16, transform=ax.transAxes)
    ax.set_xlabel('')
    ax.set_ylabel('')
    CS = ds[Z].plot.contour(transform=ccrs.PlateCarree(), ax=ax,colors='black', linewidths=1, add_labels=False, alpha=1, 
                           vmin=vmin, vmax=vmax, levels=13)
    CS.collections[6].set_linewidth(3)

    ax.clabel(CS, fmt='%d', colors='black', fontsize=12, inline=1, zorder=1030)
    cs=ds[Z+'_significance_map_005'].where(ds[Z+'_significance_map_005'] !=0, drop=True).plot.contourf(ax=ax,colors='none',hatches=[hatches, None],
                 add_colorbar=False)
    for i, collection in enumerate(cs.collections):
        collection.set_edgecolor(hatch_color)
        collection.set_linewidth(0.)
    if colorbar:
        add_colorbar(im,im.levels, label='Composite difference 200hPa winds [m/s] \n  (strong years - weak years)')
    if receptor_loc and isinstance(receptor_loc,list):
        ax.scatter(receptor_loc[0], receptor_loc[1], color='black', marker='*')
    return im
        
def plot_mslp_850hpa_composite(ds, 
oro='/mnt/acam-ns2806k/ovewh/tracing_the_winds/Master_thesis_UiO_workflow/Master_thesis_UiO_workflow/downloads/ERA5_orography.nc' 
                                ,ax=None, x_qk=0.93, y_qk=0.9, label='', colorbar=True, title='', receptor_loc=None,
                                receptor_name=None, vector_scale=1, angles='xy',U=2, q_label='',
                                vmin=-6, vmax=6, significance_mask=True,hatches='xx', hatch_color='gray', forcing='era5',
                                q_density=22, xticks =[20,40,60,80,100,120,140,160,180], yticks=[0,30,60,90],
                                receptor_color='black',receptor_marker_s=135):
    if ax==None:
        ax = plt.gca()
    map_large_scale(ax, xticks = xticks, yticks= yticks)
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
    extent = ax.get_extent()
    if forcing == 'merra2':
        ds = ds.sel(lon=slice(extent[0],extent[1]),lat=slice(extent[2],extent[3]))
        lon = 'lon'
        lat = 'lat'
    else:
        ds = ds.sel(longitude=slice(extent[0],extent[1]),latitude=slice(extent[3],extent[2]))
        lon = 'longitude'
        lat = 'latitude'
    im = ds[msl].plot.contourf(transform=ccrs.PlateCarree(),levels=16, vmin=vmin, vmax=vmax,
                                                               cmap='bwr', add_colorbar=False, ax=ax)
    if significance_mask:
        cs=ds[msl+'_significance_map_005'].where(ds[msl+'_significance_map_005'] !=0, drop=True).plot.contourf(ax=ax,colors='none',hatches=[hatches, None],
                    add_colorbar=False)
        for i, collection in enumerate(cs.collections):
            collection.set_edgecolor(hatch_color)
            collection.set_linewidth(0.)
    # cs.collections[0].set_edgecolor('gainsboro')
    if q_label == '':
        q_label = f'{U} m/s'
    Q = ax.quiver(ds[lon][::q_density], ds[lat][::q_density], ds[u][::q_density,::q_density], 
                   ds[v][::q_density,::q_density],transform=ccrs.PlateCarree(),color='saddlebrown', 
              units='xy', zorder=1002, minlength=2, pivot='middle', scale=vector_scale, angles = angles)
    qk=ax.quiverkey(Q, x_qk,y_qk, U=U, label=q_label, labelpos='E', coordinates='axes', color='black')
    qk.text.set_backgroundcolor('w')
    oro.z.where(oro.z > 33000,drop=True).plot.contourf(transform=ccrs.PlateCarree(),
                                                       levels=2, colors='lightgrey'
                                                        , add_colorbar=False,ax =ax, zorder=1100, hatches='/')
    if colorbar:
        add_colorbar(im,im.levels, label='Mean Sea Level Pressure \n  (strong years - weak years)')
    if receptor_loc and isinstance(receptor_loc,list):
        ax.scatter(receptor_loc[0], receptor_loc[1], color=receptor_color, marker='*', 
                    zorder=2000, edgecolors='black',linewidth=1, s=receptor_marker_s)

    ax.text( x=0.03,y=0.94, s=label, fontsize=14, transform=ax.transAxes)
    
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_title(title)
    return im

def plot_which_years_composited(composite_ds,ax=None, xlabelsize=8,locs=None,**scatter_kwargs):
    if ax==None:
        ax = plt.gca()
    ax.cla()
    ax.set_xticks(range(1999,2020))
    ax.set_xlim(1998,2020)
    ax.set_xticklabels(ax.get_xticks(), rotation = 45,)
    ax.yaxis.tick_right()
    
    ax.set_yticks(range(1,8))
    variable = list(composite_ds.data_vars)[0].split('_')[-1]
    n = 1
    if locs==None:
        locs = composite_ds.attrs['locations']

    for loc in locs:
        ax.scatter((composite_ds[loc+'_'+variable].strong_years),
                [n for i in range(len(composite_ds[loc+'_'+variable].strong_years))],color='deeppink', **scatter_kwargs)
        ax.scatter((composite_ds[loc+'_'+variable].weak_years),
                [n for i in range(len(composite_ds[loc+'_'+variable].weak_years))], color='slateblue', **scatter_kwargs)
        
        n=n+1
    if locs[4] == 'BADOE':
        locs[4] = 'BAODE'

    ax.set_yticklabels(locs)
    ax.set_ylim(0,9)
    ax.tick_params(axis='x', which='major', labelsize=xlabelsize)
    ax.legend(['Strong years','Weak Years'],mode='expand', ncol=2, frameon=False)