import xarray as xr
from .create_composites import create_composite
import numpy as np

def mslp_850hpa_wind_composite(mslp, u_wind_850, v_wind_850,strong_years, weak_years, 
                               season='', location='', kind=''):
    composite_ds = xr.Dataset()
    composite_ds['msl'] = create_composite(mslp['msl'], weak_years,strong_years)
    composite_ds = composite_ds.assign(msl=composite_ds.msl/100)
    composite_ds['msl'].attrs['units'] = 'hPa' 
    composite_ds['u'] = create_composite(u_wind_850['u'], weak_years, strong_years)
    composite_ds['v'] = create_composite(v_wind_850['v'], weak_years, strong_years)
    windspeed=np.sqrt(u_wind_850['u']**2 + v_wind_850['v']**2)
    windspeed.attrs['varName']='hws'
    windspeed.attrs['units'] = 'm/s'
    windspeed.attrs['long_name'] = 'wind speed'
    composite_ds['hws'] = create_composite(windspeed, weak_years, strong_years)
    composite_ds.attrs['title'] = "Composites of Mslp and windspeed at 850hPa"
    composite_ds.attrs['season'] = season
    composite_ds.attrs['source'] = 'ERA5 reanalysis'
    composite_ds.attrs['location'] = location
    composite_ds.attrs['kind'] = kind
    
    return composite_ds


def geopot_wind_composite(geopot, u_wind, v_vind, weak_years, strong_years, plevel, 
                         season='', location='', kind=''):
    """Create composite dataset of geopotential height, windspeed and windvectors"""
    
    composite_ds = xr.Dataset()
    composite_ds['Z'] = create_composite(geopot['Z'], weak_years,strong_years)
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
    

