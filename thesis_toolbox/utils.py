import pandas as pd
import xarray as xr
import glob
from thesis_toolbox.composites.create_composites import detrend_timeseries,select_years_to_composite
import numpy as np
import os

def get_locations_CLP():
    df = pd.DataFrame(index = ['SACOL', 'BADOE', 'LANTIAN','SHAPOTOU','YINCHUAN','LUOCHUAN'], columns=['lon','lat'])
    df.loc['SACOL',:] = (104.1370,35.96400)
    df.loc['BADOE',:] = (111.1700,39.00300)
    df.loc['LANTIAN',:] = (109.2560,34.180)
    df.loc['LINGTAI',:] = (107.789,35.710)
    df.loc['SHAPOTOU',:] = (105.0475,37.749)
    df.loc['YINCHUAN',:] = (106.101,38.50)
    df.loc['LUOCHUAN',:] = (109.424,35.710)
    return df

def extract_source_region(region):
    """
    DESCRIPTION:
    ============
        Give the lon/lat of the rectangle defining each source

    ARGUMENTS:
    ==========
        region, currently defined regions are: taklamakan, north_west, mongolia, jungger_basin
                and quaidam_basin

    RETURN:
    ======
        lon0,lon1,lat0,lat1

    """

    if region == 'taklamakan':
        return 75, 90, 36 ,42
    elif region == 'north_west':
        return 100, 110, 37, 42
    elif region == 'mongolia':
        return 95, 110, 43, 50
    elif region == 'jungger_basin':
        return 80, 90, 43, 47
    elif region == 'quaidam_basin':
        return 90, 100, 35, 40
    else:
        raise(ValueError(f'{region} is not defined'))

def read_receptor_composite(locs,path, folder,size,season,region='total',kind='total_deposition',std='05-std'):
    """Read circulation composite data files based on the Master thesis workflow structure"""
    
    ds=xr.Dataset()
    for loc in locs:
        temp_ds = xr.open_dataset(glob.glob(path+'results/composites/{}/*.composite.{}.{}.{}.{}.{}.{}.*.nc'.format(folder,kind,size,season,loc,region,std))[0])
        for ds_var in list(temp_ds.data_vars):
            ds['{}_{}'.format(loc,ds_var)] = temp_ds[ds_var]
    ds.attrs['locations'] = list(locs)
    return ds

def read_depostion_datasets(path,locs, kind,psize, frac=1):
    """Read depostion dataset based on file structure from Master thesis workflow"""
    ds=xr.Dataset()
    if psize =='2micron':
        frac=0.0820
    elif psize=='20micron':
        frac=0.0349
    else:
        frac=frac
    for loc in locs:
        
        ncpath = path+'{}/{}.{}.{}.*.nc'.format(kind,kind,loc,psize)
        print(glob.glob(ncpath))
        temp_ds = xr.open_dataset(glob.glob(ncpath)[0])
        ds['{}_{}'.format(loc,kind)] = temp_ds[kind]*frac
    ds.attrs['locations'] = list(locs)
    return ds

def source_contrib_composite_difference(path, locs,kind, psize,frac=1, norm=True, c=4):
    """Read in depostion time series and source contribution data """
    ds=xr.Dataset()
    if psize =='2micron':
        frac=0.0820
    elif psize=='20micron':
        frac=0.0349
    else:
        frac=frac
    for loc in locs:
        ts = xr.open_dataset(glob.glob(path+'results/model_results/time_series/{}/{}.{}.total.{}.*.nc'.format(kind,kind,loc,psize))[0])
        ts[kind] = detrend_timeseries(ts[kind])
        weak_years,strong_years = select_years_to_composite(ts[kind],c)
        ds_path = glob.glob(path+'results/model_results/{}/{}.{}.{}.*.nc'.format(kind,kind,loc,psize))[0]
        weak_depo_year = xr.open_dataset(ds_path).sel(year=weak_years).mean(dim='year')

        strong_depo_year = xr.open_dataset(ds_path).sel(year=strong_years).mean(dim='year')
        if norm:
            weak_depo_year[kind] = weak_depo_year[kind]/(weak_depo_year[kind].sum(dim=['lon','lat']))
            strong_depo_year[kind] = strong_depo_year[kind]/(strong_depo_year[kind].sum(dim=['lon','lat']))
        varName = '{}_{}'.format(loc,kind)
        ds[varName] = (strong_depo_year[kind]-weak_depo_year[kind])*frac
    ds.attrs['locations'] = list(locs)
    return ds


def get_trajectory_paths(path0,years, kind, location, size):
    paths=[]
    for year in years:
        temp_path=path0+'/'+kind+'/'+size +'/'+str(year)
        for date_tag in ['0331_00','0430_00','0531_00']:
            paths.append(temp_path+'/'+ str(year)+date_tag+location+'/output/trajectories.txt')
    return paths

def get_path_source_contribution(path0, years, kind, loc, psize):
    paths = []
    for year in years:
        paths += glob.glob(f'{path0}/{kind}/{psize}/{year}/*{loc}*.nc')
    return paths

def load_MERRA2_seasonal(path0,location, psize='clay',date_tag='19990101-20201231', season='MAM'):
    """
    DESCRIPTION:
    ===========
        Reads the MERRA2 dust deposition data and resample it into seasonal sums

    ARGUMENTS:
    ==========
        path0: Path to where FLEXPART output is stored.
        location: Name of location, in the file name.
        psize: The size bin to reading (in the file name).
        date_tag: Tag showing the period that the MERRA2 data file covers (in the filename).
        season: which season to select.

    RETURNS:
    ========
        pandas.DataFrame : dataframe containing the seasonal sum of wet , dry and total deposition. 
    """
    out_ds = xr.Dataset()
    sec_in_month=2592000
    for merra_name,kind in zip(['M2TMNXADG_5_12_4_DUWT003','M2TMNXADG_5_12_4_DUDP003'],['wetdep','drydep']):
        ds = xr.open_dataset(os.path.join(path0,f'{kind}.{psize}.{date_tag}.{location}.nc'))
        ds = ds.rename({merra_name:kind})
        
        ds = ds.drop('datamonth')
        ds=ds.resample(time='Q-NOV').sum(keep_attrs=True)
        ds=ds.sel(time=(ds.time.dt.season==season))
        out_ds[f'{kind} {location}'] = ds[kind]*1000*sec_in_month*3
    df = out_ds.to_dataframe()

    df[f'total {location}'] = df[f'drydep {location}'] + df[f'wetdep {location}']

    return df

def create_deposition_timeseries_MERRA2(ds,lon0, lat0,kind='total', sizebins=None):
    """Creatre deposition/emission timeseries from gridded merra 2 data"""
    if sizebins==None:
        sizebins = ['001','002','003','004','005']
    if kind == 'drydep':
        datavars = ['DUDP' + sb for sb in sizebins]
    elif kind == 'wetdep':
        datavars = ['DUWT' + sb for sb in sizebins]
    elif kind == 'emissions':
        datavars = ['DUEM' + sb for sb in sizebins]
    elif kind == 'total':
        pass
    else:
        raise(ValueError(f'Kind is invalid {kind}'))
    ds = ds.sel(lon=lon0,lat=lat0,method='nearest')
    outval=0
    if kind == 'total':
        wetdep_vars = ['DUWT' + sb for sb in sizebins]
        drydep_vars = ['DUDP' + sb for sb in sizebins]
        total_dep = [ds[wd_var] + ds[dd_var] for wd_var, dd_var in zip(wetdep_vars, drydep_vars)]
        
        for val in total_dep:
            outval += val
    else:
        for dvar in datavars:
            outval += ds[dvar]
    return outval
        