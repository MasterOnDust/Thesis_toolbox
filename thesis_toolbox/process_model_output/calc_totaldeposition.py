import xarray as xr
import time

def get_total_depostion(drydep, wetdep):
    ds_tot=drydep['drydep']+wetdep['wetdep']
    ds_tot.attrs=drydep.attrs
    ds_tot.attrs['long_name']='Total deposition'
    ds_tot=ds_tot.to_dataset(name='total_deposition')
    ds_tot.attrs=drydep.drydep.attrs
    ds_tot.attrs.pop('ind_source', None)
    ds_tot.attrs.pop('ind_receptor', None)
    ds_tot.attrs.pop('filename',None)

    ds_tot.attrs['varName'] = 'total_deposition'
    ds_tot['RELLAT1']=drydep['RELLAT1']
    ds_tot['RELLNG1']=drydep['RELLNG1']
    
    return ds_tot