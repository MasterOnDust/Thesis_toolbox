from fpcluster.adaptive_kmeans import Adaptive_KMeans
import numpy as np
from fpcluster.read_trajectories import load_trajectories, read_trajectories
import pandas as pd
from thesis_toolbox.utils import get_trajectory_paths, get_path_source_contribution
import xarray as xr

def get_dust_trajectories(path0,years,kind,loc,psize,threshold=1e-3, 
                          std_treshold=None, use_dask=True,chunks={'time':1}):
    """
    DESCRIPTON:
    ===========
        Filter out only dust carrying trajectories

    args:
        path0: path to top directory
        years: which years to cluster
        kind: wetdep / drydep
        loc: which location
        psize: 20micron/2micron
        threshold: minimum depostion of dust loading trajectory 
        std_treshold: use standard deviation as treshold instead
        use_dask : whether to use dask or not (will consume less memory)
        chunks : how to chunk the dask array

    return:
        xarray.Dataset containing dust carrying trajectories. 

    """


    paths_trajecs = get_trajectory_paths(path0,years,kind,loc, psize)
    paths_source_contrib = get_path_source_contribution(path0+'/source_contribution',years,kind,loc,psize)
    time_stamps = []
    ddep = []
    for path in paths_source_contrib:
        if use_dask:
            ds = xr.open_dataset(path,chunks=chunks)
        else: 
            ds = xr.open_dataset(path)
        ds = ds.drydep.sum(dim=['btime','lon','lat'])
        ddep.append(ds.values)
        time_stamps.append(ds.time.values)
    ddep = np.concatenate(ddep)
    time_stamps = np.concatenate(time_stamps)
    if std_treshold:
        treshold = std_treshold*ddep.std()
    time_stamps = time_stamps[ddep >= threshold]
    ddep = ddep[ddep >= threshold]
    ds = read_trajectories(paths_trajecs,kind=kind,timestamps=time_stamps)
    da = xr.DataArray(data=ddep, dims=['time'], coords={'time':time_stamps})
    da = da[~da.get_index("time").duplicated()] #avoid duplicate indices?
    ds = ds.sel(time=ds.time[~ds.get_index("time").duplicated()])
    ds = ds.assign({kind:da})
    ds.attrs['varName'] = kind
    return ds