import xarray as xr
from .create_composites import create_composite, calculate_climatology
import numpy as np

def mslp_wind_composite(mslp, u_wind, v_wind, weak_years, strong_years, plevel,
                               season='', location='', kind='', lon0=None, lat0=None,lon1=None,lat1=None):
    composite_ds = xr.Dataset()
    composite_ds['msl'] = create_composite(mslp['msl'], weak_years,strong_years)
    composite_ds = composite_ds.assign(msl=composite_ds.msl/100)
    composite_ds['msl'].attrs['units'] = 'hPa' 
    composite_ds['u'] = create_composite(u_wind['u'], weak_years, strong_years)
    composite_ds['v'] = create_composite(v_wind['v'], weak_years, strong_years)
    composite_ds.attrs['title'] = "Composites of Mslp and windspeed at "+ plevel + " hPa"
    composite_ds.attrs['season'] = season
    composite_ds.attrs['source'] = 'ERA5 reanalysis'
    composite_ds.attrs['location'] = location
    composite_ds.attrs['kind'] = kind
    
    return composite_ds


def geopot_wind_composite(geopot, u_wind, v_wind, weak_years, strong_years, plevel, 
                         season='', location='', kind='',lon0=None, lat0=None,lon1=None,lat1=None):
    """Create composite dataset of geopotential height, windspeed and windvectors"""
    
    composite_ds = xr.Dataset()
    composite_ds['Z'] = create_composite(geopot['Z'], weak_years, strong_years)
    composite_ds['u'] = create_composite(u_wind['u'], weak_years, strong_years)
    composite_ds['v'] = create_composite(v_wind['v'], weak_years, strong_years)
    windspeed=np.sqrt(u_wind['u']**2 + v_wind['v']**2)
    windspeed.attrs['varName']='hws'
    windspeed.attrs['units'] = 'm/s'
    windspeed.attrs['long_name'] = 'wind speed'
    composite_ds['hws'] = create_composite(windspeed, weak_years, strong_years)
    composite_ds.attrs['title'] = "Composites of geopotential height and windspeed at " + str(plevel)
    composite_ds.attrs['season'] = season
    composite_ds.attrs['source'] = 'ERA5 reanalysis'
    composite_ds.attrs['location'] = location
    composite_ds.attrs['kind'] = kind
    return composite_ds
    

def geopot_wind_climatology(geopot, u_wind, v_wind, plevel,start_year=None, end_year=None, season=''):
    clim_ds=xr.Dataset()
    clim_ds['Z'] = calculate_climatology(geopot['Z'], start_year=start_year, end_year=end_year)
    clim_ds['u'] = calculate_climatology(u_wind['u'],  start_year=start_year, end_year=end_year)
    clim_ds['v'] = calculate_climatology(v_wind['v'],  start_year=start_year, end_year=end_year)
    windspeed=np.sqrt(u_wind['u']**2 + v_wind['v']**2)
    windspeed.attrs['varName']='hws'
    windspeed.attrs['units'] = 'm/s'
    windspeed.attrs['long_name'] = 'wind speed'
    clim_ds['hws'] = calculate_climatology(windspeed, start_year, end_year)
    clim_ds.attrs['title'] = "Climatology of geopotential height and windspeed at " + str(plevel)
    clim_ds.attrs['season'] = season
    clim_ds.attrs['source'] = 'ERA5 reanalysis'
    return clim_ds

