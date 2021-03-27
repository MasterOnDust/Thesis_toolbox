from cartopy.mpl.gridliner import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt
import cartopy.crs as ccrs 
from matplotlib.ticker import ScalarFormatter,AutoMinorLocator
import matplotlib
from string import ascii_lowercase
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib as mpl

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
    
    
class OOMFormatter(matplotlib.ticker.ScalarFormatter):
    """
    https://stackoverflow.com/questions/42656139/set-scientific-notation-with-fixed-exponent-and-significant-digits-for-multiple
    """
    def __init__(self, order=0, fformat="%1.1f", offset=True, mathText=True):
        self.oom = order
        self.fformat = fformat
        matplotlib.ticker.ScalarFormatter.__init__(self,useOffset=offset,useMathText=mathText)
    def _set_orderOfMagnitude(self, nothing=None):
        self.orderOfMagnitude = self.oom
    def _set_format(self, vmin=None, vmax=None):
        self.format = self.fformat
        if self._useMathText:
            self.format = '$%s$' % self.format
            
def add_letter(axes_array):
    """Add letter each axes object"""
    for i,ax in enumerate(axes_array.ravel()):
        ax.text( x=0.03,y=0.93, s='{})'.format(ascii_lowercase[i]), 
        fontsize=16, transform=ax.transAxes)

def add_colorbar(im,cticks,label='', fmt='%d'):
    """Adds Colorbar Nicely to figure"""
    ax = im.axes
    fig = ax.figure
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3.5%", pad=0.05, axes_class=mpl.pyplot.Axes)

    fig.colorbar(im,ax=ax,cax=cax,label=label,shrink=0.9, format=fmt, ticks=cticks)
        
def latex_plot():
    plt.rcParams.update({'figure.autolayout': True})
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.size'] = 18
    plt.rcParams['axes.linewidth'] = 2
    plt.rcParams['legend.frameon'] = False
    plt.rcParams['axes.linewidth'] = 2

    # --- Use latex-style on text in plots
    plt.rcParams['text.usetex'] = False

    # --- Custumize the length of the labels
    plt.rcParams["legend.labelspacing"] = 0.2
    plt.rcParams["legend.handlelength"] = 1.0
    plt.rcParams["legend.borderaxespad"] = 0.01

    plt.rcParams['axes.labelsize'] = 16
    plt.rcParams['axes.titlesize'] = plt.rcParams['font.size']
    plt.rcParams['legend.fontsize'] = plt.rcParams['font.size']
    plt.rcParams['xtick.labelsize'] = 14
    plt.rcParams['ytick.labelsize'] = 14
    
    # --- Ignore warnings for generated plot
    plt.rcParams.update({'figure.max_open_warning': 0})

    plt.linewidth=17.0

