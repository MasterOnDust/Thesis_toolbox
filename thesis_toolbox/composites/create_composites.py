################################################################################
# Created by Ove Haugvaldstad                                                  #
# 23.02.2021                                                                   #
#                                                                              #
################################################################################

import pandas as pd
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from statsmodels.tsa.tsatools import detrend


def detrend_timeseries(timeseries):
    """
    Detrend time series,
    input: xarray.DataArray (1D)
    """
    
    detrended = detrend(timeseries)

    return detrended
 
def select_years_to_composite(timeseries,criterion='1-std'):
    """
    DESCRIPTION:
    ===========
        Chooses which years to be included in the composites, the selection criterion can 
        either be 2, 1 or 0.5 standard devivation around the mean.
    
    USAGE:
    ======
        weak_years, strong_years = select_years_to_composite(timeseires, criterion='1-std')
    
    PARAMETERS:
    ==========
        timeseries : either xarray DataArray or pandas.series
        criterion : valid values '0.5-std', '1-std' and '2-std'
        
    """
    
    if criterion == '05-std':
        c = 0.5
    elif criterion == '1-std':
        c = 1
    elif criterion == '2-std':
        c = 2
    else:
        raise(ValueError('Invalid criterion provided: {}'.format(criterion)))
    
    std = c*timeseries.std()
    mean = timeseries.mean()
    
    if isinstance(timeseries, xr.core.dataarray.DataArray):
        if 'year' in timeseries.dims:
            strong_years =timeseries.where(timeseries > (mean+std), drop=True).year.values
            weak_years=timeseries.where(timeseries < (mean-std), drop=True).year.values
        else:
            strong_years = timeseries.where(timeseries > (mean+std), drop=True).time.dt.year.values
            weak_years = timeseries.where(timeseries < (mean-std), drop=True).time.dt.year.values
    elif isinstance(timeseries,pd.core.series.Series):
        strong_years = timeseries.where(timeseries > (mean+std)).dropna.index.year.values
        weak_years = timesereis.where(timeseries < (mean-std)).dropna.index.year.values
    else:
        raise(ValueError('Invalid datatype provided'))
    return weak_years,strong_years

    
def create_composite(da,weak_years,strong_years):
    """
    DESCRIPTION:
    ===========
        Creates a composite difference from one array of weak years and strong years. 
        Return dataset containing composite difference , depending on wether the data is provided as contour_f, 
        contour or quiver, determine how the comopsite data will interface with the plotting functions.  
    
    USAGE:
    ======
        composite_data = create_composite([2005,2007,2009], contour_f=temperature_data, quiver=winds)
    
    PARAMETERS:
    ==========
        da : dataset containing variable
        weak_years : list/array of weak years make composite of
        strong_years : list/array of strong years to make composite of 

    RETURNS:
    =======
        xarray Dataset containing the calculated composit, with interface ready for plotting
    """

    
    if len(weak_years)==0:
        raise(ValueError('Years to composite cannot be of 0 size'))
    da['time'] = da.time.dt.year
    weak_years_composite = _average_composite(weak_years, da)
    strong_years_composite = _average_composite(strong_years, da)
    composite_difference = strong_years_composite - weak_years_composite
    composite_difference.attrs = da.attrs
    composite_difference.attrs['weak_years']=weak_years
    composite_difference.attrs['strong_years']=strong_years
    

    return composite_difference     
        
def _average_composite(years_to_composite,data):
    """averages the composite years"""
    if len(years_to_composite) ==1:
        data = data.sel(time=years_to_composite)
    else:
        data = data.sel(time=years_to_composite).mean(dim='time',keep_attrs=True)
    return data


def calculate_climatology(data, start_year=None, end_year=None):
    if start_year == None:
        if isinstance(data.time[0].values,np.datetime64):
            start_year = str(data.time[0].dt.year.values)
        else:
            start_year = int(data.time[0].values)
    if end_year == None:
        if isinstance(data.time[0].values,np.datetime64):
            end_year = str(data.time[-1].dt.year.values)
        else:
            end_year = int(data.time[-1].values)
    data=data.sel(time=slice(start_year,end_year)).mean(dim='time', keep_attrs=True)
    data.attrs['start_year'] = start_year
    data.attrs['end_year'] = end_year
    return data        