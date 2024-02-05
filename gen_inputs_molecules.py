#!/usr/bin/env python3

import os

class Config:
    """Config for generation of inputs."""

    MOL_DATA = "mol_data/"
    molecules = ["no", "of", "sif", "sih", "clo", "hs", "ch", "cf"]
    light_atoms = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne"]
    methods = {
        "Standard": "plot_x=1,plot_y=1,plot_z=1",
        "VH": "vhoep=1,thr_sym=-1d0,,plot_x=1,plot_y=1,plot_z=1",
        "SS": "vhoep=1,thr_sym=1d-10,plot_x=1,plot_y=1,plot_z=1",
        "SA": "vhoep=1,thr_sym=-1d0,oepsav=1,plot_x=1,plot_y=1,plot_z=1",
        "SS+SA": "vhoep=1,thr_sym=1d-10,oepsav=1,plot_x=1,plot_y=1,plot_z=1",
    }
    output_dir = "MOLECULES"

def input_text(geometry, method, oep_basis, orbital_basis="aug-cc-pwCV5Z", thr_fai_oep="5d-3"):
    """Generate input text for Molpro."""
    return f"""basis={{
default,{orbital_basis}
set,oep
{oep_basis}
}}

symmetry,nosym

angstrom
geometry={{
{geometry}
}}

spin=1

uhf,maxit=0

acfd;uscexx,dfit=0,thr_fai_oep={thr_fai_oep},{method}
"""

def slurm_text(partition="mem256"):
    """Generate input text for Slurm script."""
    if partition == "mem256":
        cpu_per_task = 16
        mem = 20000
    return f"""#!/bin/bash -l
#
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task={cpu_per_task}
#SBATCH --job-name=testjob
#SBATCH --partition={partition}
#SBATCH --mail-user=egor.trushin@fau.de

export I_MPI_DEBUG=5
export I_MPI_PMI_LIBRARY=/usr/lib64/libpmi.so.0

MOLPRO=/home/trushin/Molpro/molpro-vhoep2/bin/

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export MKL_NUM_THREADS=$SLURM_CPUS_PER_TASK
export OMP_STACKSIZE=3000M
ulimit -s unlimited
export MV2_CPU_MAPPING=0-$(( ${{num}} - 1))

cd $SLURM_SUBMIT_DIR
echo $SLURM_JOB_NODELIST > $SLURM_SUBMIT_DIR/machines_jobid

TMPDIR=/scratch/trushin/${{SLURM_JOBID}}

$MOLPRO/molpro -t {cpu_per_task} -m {mem} --no-xml-output --no-helper-server -d $TMPDIR < input 1> $SLURM_SUBMIT_DIR/output 2> $SLURM_SUBMIT_DIR/error

rm *.wfu *vxdiff machines_jobid
scp $TMPDIR/* tcsv020:$SLURM_SUBMIT_DIR
cd $SLURM_SUBMIT_DIR
"""


os.mkdir(Config.output_dir)

for mol in Config.molecules:
    xyz_file = os.path.join(Config.MOL_DATA, mol+".xyz")
    with open(xyz_file, 'r') as file_obj:
        xyz = file_obj.read()[:-1]
    atoms = [xyz.splitlines()[2].split()[0], xyz.splitlines()[3].split()[0]]
    if atoms[0] in Config.light_atoms:
        oep_basis=atoms[0]+'=aug-cc-pVDZ/mp2fit\n'
    else:
        oep_basis=atoms[0]+'=aug-cc-pVTZ/mp2fit\n'
    if atoms[1] in Config.light_atoms:
        oep_basis+=atoms[1]+'=aug-cc-pVDZ/mp2fit'
    else:
        oep_basis+=atoms[1]+'=aug-cc-pVTZ/mp2fit'
    for mthd in Config.methods:
        subdir = os.path.join(Config.output_dir, mol + '_' + mthd)
        os.mkdir(subdir)
        molpro_input = os.path.join(subdir, "input")
        with open(molpro_input, "w", encoding="utf8") as file_obj:
            print(
                input_text(
                    xyz,
                    Config.methods[mthd],
                    oep_basis,
                ),
                file=file_obj,
            )
        slurm_input = os.path.join(subdir, "run.sh")
        with open(slurm_input, "w", encoding="utf8") as file_obj:
            print(slurm_text(), file=file_obj)
