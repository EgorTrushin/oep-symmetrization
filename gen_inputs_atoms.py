#!/usr/bin/env python3
"""Generates inputs for Standard, Spin-Averaged and Spin-Averaged + V_H in OEP."""

import json
import os


class Config:
    """Config for generation of inputs."""

    atoms_json = "json/atoms_LKI.json"
    light_atoms = ["H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne"]
    methods = {
        "Standard": "plot_x=1,plot_y=1,plot_z=1",
        "VH": "vhoep=1,thr_sym=-1d0,,plot_x=1,plot_y=1,plot_z=1",
        "SS": "vhoep=1,thr_sym=1d-10,plot_z=1",
        "SA": "vhoep=1,thr_sym=-1d0,oepsav=1,plot_x=1,plot_y=1,plot_z=1",
        "SS+SA": "vhoep=1,thr_sym=1d-10,oepsav=1,plot_z=1",
    }
    output_dir = "ATOMS"


def input_text(atom, spin, orbital_basis, oep_basis, thr_fai_oep, method):
    """Generate input text for Molpro."""
    if spin == 0:
        unr = ""
    else:
        unr = "u"
    return f"""basis={{
default,{orbital_basis}
set,oep;default,{oep_basis}
}}

symmetry,nosym

angstrom
geometry={{
1

{atom} 0 0 0
}}

spin={spin}

{unr}hf,maxit=0

acfd;{unr}scexx,dfit=0,thr_fai_oep={thr_fai_oep},{method}
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


with open(Config.atoms_json, "r", encoding="utf8") as file_obj:
    atoms = json.load(file_obj)

ATOMS = list(atoms.keys())
print(ATOMS)
print(Config.methods)

os.mkdir(Config.output_dir)
for mthd in Config.methods:
    for atm in atoms:
        subdir = os.path.join(Config.output_dir, atm +'_' + mthd)
        os.mkdir(subdir)
        molpro_input = os.path.join(subdir, "input")
        if atm in Config.light_atoms:
            OEP_BAS = "aug-cc-pVDZ/mp2fit"
        else:
            OEP_BAS = "aug-cc-pVTZ/mp2fit"
        with open(molpro_input, "w", encoding="utf8") as file_obj:
            print(
                input_text(
                    atm,
                    atoms[atm]["spin"],
                    "aug-cc-pwCV5Z",
                    OEP_BAS,
                    "5d-3",
                    Config.methods[mthd],
                ),
                file=file_obj,
            )
        slurm_input = os.path.join(subdir, "run.sh")
        with open(slurm_input, "w", encoding="utf8") as file_obj:
            print(
                slurm_text(),
                file=file_obj,
            )
