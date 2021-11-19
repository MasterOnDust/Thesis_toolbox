import xarray as xr
import numpy as np

def merra2_mslp_wind_composite(ds, weak_years, strong_years, plevel):
    """Create composites of MSLP and windvector from MERRA2 reanalysis"""
    composite_ds = xr.Dataset()
    ds = ds.sel(lev=plevel)
    composite_ds['msl'], composite_ds['msl_significance_map_005']= create_composite(ds['SLP']/100, weak_years,strong_years)
    composite_ds['msl'].attrs['units'] = 'hPa' 

    composite_ds['u'], composite_ds['u_significance_map_005'] = create_composite(ds['U'], weak_years, strong_years)
    composite_ds['v'], composite_ds['v_significance_map_005'] = create_composite(ds['V'], weak_years, strong_years)
    composite_ds.attrs['title'] = "Composites of Mslp and windspeed at "+ plevel + " hPa"
    composite_ds.attrs['season'] = season
    composite_ds.attrs['source'] = 'MERRA2 reanalysis'
    composite_ds.attrs['location'] = location
    composite_ds.attrs['kind'] = kind
    return composite_ds

def merra2_geopot_wind_composite(ds, weak_years, strong_years,plevel):
    """Create composite anomaly dataset of geopotential height windspeed and windvectors from MERRA2 """
    composite_ds = xr.Dataset()
    ds = ds.sel(lev=plevel)
    omposite_ds['Z'], composite_ds['Z_significance_map_005'] = create_composite(ds['H'], weak_years, strong_years)
    composite_ds['u'],composite_ds['u_significance_map_005'] = create_composite(ds['u'], weak_years, strong_years)
    composite_ds['v'],composite_ds['v_significance_map_005'] = create_composite(ds['v'], weak_years, strong_years)

    windspeed=np.sqrt(ds['u']**2 + ds['v']**2)
    windspeed.attrs['varName']='hws'
    windspeed.attrs['units'] = 'm/s'
    windspeed.attrs['long_name'] = 'wind speed'
    composite_ds['hws'], composite_ds['hws_significance_map_005'] = create_composite(windspeed, weak_years, strong_years)
    composite_ds.attrs['title'] = "Composites of geopotential height and windspeed at " + str(plevel)
    composite_ds.attrs['season'] = season
    composite_ds.attrs['source'] = 'MERRA2 reanalysis'
    composite_ds.attrs['location'] = location
    composite_ds.attrs['kind'] = kind
    return composite_ds