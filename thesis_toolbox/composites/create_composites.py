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
from scipy import stats

def detrend_timeseries(timeseries):
    """
    Detrend time series,
    input: xarray.DataArray (1D)
    """
    
    detrended = detrend(timeseries)

    return detrended

def select_years_according_to_rank(timeseries, c):
    """
    DESCRIPTION:
    ============
        Chooses which years to be included in the composite based on rank. 

    ARGUMENTS:
    ==========
        timeseries either a xarray.dataarray.DataArray or pandas.core.series.Series
        c how many to include in the composite, eg. c=3 would take the 3 strongest and 3 weakest years. 

    RETURN:

        weak_years, strong_years

    """

    
    if isinstance(timeseries, xr.core.dataarray.DataArray):
        if 'time' in timeseries.dims:
            tdim = 'time'
        elif 'year' in timeseries.dims:
            tdim='year'
        elif 'T' in timeseries.attrs.keys():
            tdim = timeseries.attrs['T']
        else:
            raise(ValueError('''Time dimmension not found, make sure that time dimension is either 
                                called time or year or that dataarray has an attribute called T'''))
        n_weakest = timeseries.argsort()[:c].values
        weak_years = timeseries.isel({tdim:n_weakest})[tdim]
        
        n_strongest = timeseries.argsort()[-c:].values
        strong_years = timeseries.isel({tdim:n_strongest})[tdim]

        if isinstance(strong_years.values[0], np.datetime64):
            strong_years = strong_years.dt.year.values
            weak_years = weak_years.dt.year.values
        else:
            strong_years = strong_years.values
            weak_years = weak_years.values


    elif isinstance(timeseries, pd.core.series.Series):
        if not isinstance(timeseries.index, pd.DatetimeIndex):
            sorted_indices = timeseries.sort_values().index
            weak_years = timeseries.loc[sorted_indices[:c]].index.values
            sorted_indices = timeseries.sort_values().index
            strong_years = timeseries.loc[sorted_indices[-c:]].index.values 
        else:
            raise(NotImplementedError('Not implemented yet, but will be if i find a use'))
    else:
        raise(ValueError(f'{type(timeseries)} is not supported, provided either a xarray DataArray or pandas series'))

    return weak_years, strong_years

def select_years_according_to_std(timeseries,c=1):
    std = c*timeseries.std()
    mean = timeseries.mean()

        
    if isinstance(timeseries, xr.core.dataarray.DataArray):
        if 'time' in timeseries.dims:
            timeseries = timeseries.assign_coords(time=timeseries.time.dt.year)
            timeseries = timeseries.rename(time='year')
        if 'year' in timeseries.dims:
            strong_years =timeseries.where(timeseries > (mean+std), drop=True).year.values
            weak_years=timeseries.where(timeseries < (mean-std), drop=True).year.values
        else:
            strong_years = timeseries.where(timeseries > (mean+std), drop=True).time.dt.year.values
            weak_years = timeseries.where(timeseries < (mean-std), drop=True).time.dt.year.values
    elif isinstance(timeseries,pd.core.series.Series):
        if isinstance(timeseries.index, pd.DatetimeIndex):
            strong_years = timeseries.where(timeseries > (mean+std)).dropna().index.year.values
            weak_years = timeseries.where(timeseries < (mean-std)).dropna().index.year.values
        else:
            strong_years = timeseries.where(timeseries > (mean+std)).dropna().index.values
            weak_years = timeseries.where(timeseries < (mean-std)).dropna().index.values
        
    else:
        raise(ValueError(f'Invalid datatype provided {type(timeseries)}'))



    return weak_years,strong_years

def select_years_to_composite(timeseries,c,criterion='rank'):
    """
    DESCRIPTION:
    ===========
        Chooses which years to be included in the composites, the selection criterion can 
        either be 2, 1 or 0.5 standard devivation around the mean.
    
    USAGE:
    ======
        weak_years, strong_years = select_years_to_composite(timeseries, criterion='1-std')
    
    PARAMETERS:
    ==========
        timeseries : either xarray DataArray or pandas.series
        criterion : valid values '0.5-std', '1-std' and '2-std'
        
    """
    if criterion == 'rank':
        weak_years, strong_years = select_years_according_to_rank(timeseries,c)
    elif criterion == 'std':
        weak_years, strong_years = select_years_according_to_std(timeseries,c)
    else:
        raise(ValueError('Invalid criterion provided: {}'.format(criterion)))
    
    return weak_years, strong_years




    
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
    da = da.assign_coords(time=da.time.dt.year)
    weak_years_composite_avg,weak_years_composite_std = _calc_composite_statistics(weak_years, da)
    strong_years_composite_avg, strong_years_composite_std = _calc_composite_statistics(strong_years, da)
    n1 = len(strong_years)
    n2 = len(weak_years)
    s_p = np.sqrt(((n1-1)*strong_years_composite_std**2-(n2-1)*weak_years_composite_std**2)/(n1+n2-2))
    s_p = xr.where(s_p>0, s_p, np.nan)
    t_values=np.abs((strong_years_composite_avg-weak_years_composite_avg)/(s_p*np.sqrt(1/n1+1/n2)))
    t_dist = stats.t.ppf(1-0.05/2, n1+n2-2)
       
    significance_mask_005 = (t_values > t_dist).astype(int)
    # t_values, p_values = ttest_ind(strong_years_composite_avg, weak_years_composite_avg)
    composite_difference = strong_years_composite_avg - weak_years_composite_avg
    significance_mask_005.attrs['long_name'] = 'Gridcell with significant change'
    significance_mask_005.attrs['alpha']=0.05
    composite_difference.attrs = da.attrs
    composite_difference.attrs['weak_years']=weak_years
    composite_difference.attrs['strong_years']=strong_years
    return composite_difference, significance_mask_005  
    
        
def _calc_composite_statistics(years_to_composite,data):
    """averages the composite years"""
    if len(years_to_composite) ==1:
        mean = data.sel(time=years_to_composite)
        std = 0
    else:
        std = data.sel(time=years_to_composite).std(dim='time',keep_attrs=True)
        mean = data.sel(time=years_to_composite).mean(dim='time',keep_attrs=True)
    return mean,std


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