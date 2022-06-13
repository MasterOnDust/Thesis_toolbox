import xarray as xr
import numpy as np
from .create_composites import create_composite

def merra2_mslp_wind_composite(ds, weak_years, strong_years, plevel, season, location, kind):
    """Create composites of MSLP and windvector from MERRA2 reanalysis"""
    composite_ds = xr.Dataset()
    ds = ds.sel(lev=plevel)
    slp = ds['SLP'].where(ds['SLP']>0,drop=True)/100
    composite_ds['msl'], composite_ds['msl_significance_map_005']= create_composite(slp, weak_years,strong_years)
    composite_ds['msl'].attrs['units'] = 'hPa' 

    composite_ds['u'], composite_ds['u_significance_map_005'] = create_composite(ds['U'], weak_years, strong_years)
    composite_ds['v'], composite_ds['v_significance_map_005'] = create_composite(ds['V'], weak_years, strong_years)
    composite_ds.attrs['title'] = "Composites of Mslp and windspeed at {} hPa".format(plevel)
    composite_ds.attrs['season'] = season
    composite_ds.attrs['source'] = 'MERRA2 reanalysis'
    composite_ds.attrs['location'] = location
    composite_ds.attrs['kind'] = kind
    return composite_ds

def merra2_geopot_wind_composite(ds, weak_years, strong_years,plevel, season, location, kind):
    """Create composite anomaly dataset of geopotential height windspeed and windvectors from MERRA2 """
    composite_ds = xr.Dataset()
    ds = ds.sel(lev=plevel)
    Z = ds['H']/10
    Z.attrs['units'] = 'dam'
    composite_ds['Z'], composite_ds['Z_significance_map_005'] = create_composite(Z, weak_years, strong_years)
    composite_ds['u'],composite_ds['u_significance_map_005'] = create_composite(ds['U'], weak_years, strong_years)
    composite_ds['v'],composite_ds['v_significance_map_005'] = create_composite(ds['V'], weak_years, strong_years)
    windspeed=np.sqrt(ds['U']**2 + ds['V']**2)
    windspeed.attrs['varName']='hws'
    windspeed.attrs['units'] = 'm/s'
    windspeed.attrs['long_name'] = 'wind speed'
    composite_ds['hws'], composite_ds['hws_significance_map_005'] = create_composite(windspeed, weak_years, strong_years)
    composite_ds.attrs['title'] = "Composites of geopotential height and windspeed at {} hPa".format(plevel)
    composite_ds.attrs['season'] = season
    composite_ds.attrs['source'] = 'MERRA2 reanalysis'
    composite_ds.attrs['location'] = location
    composite_ds.attrs['kind'] = kind
    return composite_ds