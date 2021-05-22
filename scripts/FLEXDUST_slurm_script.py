#!/usr/bin/env python
import os
import argparse as ap
import pandas as pd
import shutil


def submit_to_slurm(output_dir, flexdust_src, wall_time='04:00:00', memory_limit='24GB'):
    job_name = output_dir.split('/')[-1]
    with open(output_dir + 'run_FLEXDUST.sh', 'w') as js:
        js.writelines("#!/bin/bash\n")
        js.writelines("#SBATCH --account=nn2806k\n")
        js.writelines("#SBATCH --time={}\n".format(wall_time))
        js.writelines("#SBATCH --job-name=FLEXDUST_{}\n".format(job_name))
        js.writelines("#SBATCH --ntasks=1\n")
        js.writelines("#SBATCH --mem-per-cpu={}\n".format(memory_limit))
        js.writelines("#SBATCH --mail-type=FAIL\n")
        js.writelines("#SBATCH --mail-user=ovewh@student.geo.uio.no\n")
        js.writelines('set -o errexit\n')
        js.writelines('set -o nounset\n')
        js.writelines('module --quiet purge\n')
        js.writelines('module load ecCodes/2.9.2-intel-2018b\n')
        js.writelines('module load netCDF-Fortran/4.4.4-intel-2018b\n')
        js.writelines('export PATH={}:$PATH\n'.format(flexdust_src))
        js.writelines('cd {}\n'.format(output_dir))
        js.writelines("time FLEXDUST\n")
        js.writelines("exit 0")
#    os.system('sbatch {}run_FLEXDUST.sh'.format(output_dir))
def create_command_file(output_dir, settings):
    with open(output_dir + 'COMMAND_FLEXDUST','w') as cf:
        cf.writelines('&COMMAND_FLEXDUST\n')
        for option, setting in settings.items():
            if option == 'OUTPUT_DIRECTORY':
                cf.writelines(' ' + option + '=  \'{}\',\n'.format(setting))
            else:
                cf.writelines(' ' + option + '= {},\n'.format(setting))
        cf.writelines(' /')

if __name__ == '__main__':
    parser = ap.ArgumentParser(description='Creates FLEXDUST COMMAND file and submit to job queue')
    parser.add_argument('month',  help='Start month of FLEXDUST simulation',  type=int)
    parser.add_argument('day',  help='Start day of FLEXDUST simulation', type=int)
    parser.add_argument('years', nargs = '+', help='Number concurent years to simulate, start from sdate',type=int)
    parser.add_argument('--ndays', '-nd', help='Number of days to simulate starting from sdate', default=91)
    parser.add_argument('--wall_time', '-wt', help='Time of each job submission', default='04:00:00')
    parser.add_argument('--memory_limit', '-ml', help='memory_limit of slurm job', default='24GB')
    parser.add_argument('--outpath', '-op', help='path to where simulation output should be stored', default='/cluster/work/users/ovewh/')
    parser.add_argument('--flexdust_src', '-fs', help='path to FLEXDUST src',
                       default='/cluster/projects/nn2806k/ovewh/flexdust/flexdust/src')
    args = parser.parse_args()
    month = args.month
    day = args.day
    years = args.years
    ndays = args.ndays
    memory_limit = args.memory_limit
    outpath = args.outpath
    wall_time = args.wall_time
    flexdust_src = args.flexdust_src

    options = {}
    options['RELEASEDAYS'] = ndays
    p_dir = outpath + 'FLEXDUST{}_{}'.format(years[0], years[-1])
    try:
        os.mkdir(p_dir)
    except:
        shutil.rmtree(p_dir)
        os.mkdir(p_dir)
    for year in years:
        output_dir = p_dir + '/' + str(year) + '/'
        os.mkdir(output_dir)
        dateI = pd.Timestamp(year,month,day)
        sdate = dateI.strftime('%Y%m%d')
        edate = dateI + pd.Timedelta(ndays, unit='d')
        options['OUTPUT_DIRECTORY'] = output_dir
        options['START_DATE_DAY'] = sdate
        options['NC_FILE_NAME'] = 'FLEXDUST_{}_{}.nc'.format(sdate, edate.strftime('%Y%m%d'))
        create_command_file(output_dir, options)
        submit_to_slurm(output_dir, flexdust_src, wall_time, memory_limit)





