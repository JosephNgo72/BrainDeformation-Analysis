from simple_slurm import Slurm

job_def = Slurm(
    t='1:0:0',  # one hour
    c=1,  # one CPU
    mem_per_cpu='500M'  # 500MB memory per CPU
)


def main():
    job_def.sbatch("DSET = mps.dataset.hdf5 singularity exec sbatch analysis1.bat python3 data_analysis.py ")
    job_def.sbatch("DSET = mps.dataset.hdf5 singularity exec sbatch --depend=afterok: analysis2.bat python3 data_analysis.py")
    job_def.sbatch("DSET = mps.dataset.hdf5 singularity exec swarm -f swarmfile --module blast --depend=afterok: analysis3.bat python3 data_analysis.py")


if __name__ == '__main__':
    main()
