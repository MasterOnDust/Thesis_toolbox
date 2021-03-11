from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt
import cartopy.crs as ccrs 
from matplotlib.ticker import ScalarFormatter,AutoMinorLocator

def map_large_scale(ax):
    ax.set_extent([20,180,0,90], crs=ccrs.PlateCarree())
    ax.set_xticks([20,40,60,80,100,120,140,160,180], crs=ccrs.PlateCarree())
    ax.set_yticks([0,30,60,90], crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
#     ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.set_minor_locator(  AutoMinorLocator(3))
    ax.xaxis.set_minor_locator(  AutoMinorLocator(2))
    ax.coastlines()