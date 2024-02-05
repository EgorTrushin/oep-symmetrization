#!/usr/bin/env python3

import os
from utils.gen_input import get_xyz, input_text
from utils.slurm_text import slurm_text
from utils.oep_basis import get_oep_basis
from sets import W4_11


class Config:
    """Config for generation of inputs."""

    output_dir = "FULL_SYM"
    molpro_path = "/home/trushin/Molpro/molpro-vhoep2/bin"
    space_sym = True
    spin_sym = True


os.mkdir(Config.output_dir)

for system in W4_11.systems:
    coords = W4_11.systems[system]["coords"]
    atoms = W4_11.systems[system]["atoms"]
    spin = W4_11.systems[system]["spin"]
    charge = W4_11.systems[system]["charge"]

    subdir = os.path.join(Config.output_dir, system)
    os.mkdir(subdir)

    molpro_input = os.path.join(subdir, "input")
    with open(molpro_input, "w", encoding="utf8") as file_obj:
        print(
            input_text(
                get_xyz(atoms, coords),
                get_oep_basis(atoms),
                spin=spin,
                charge=charge,
                space_sym=Config.space_sym,
                spin_sym=Config.spin_sym,
            ),
            file=file_obj,
        )

    slurm_input = os.path.join(subdir, "run.sh")
    with open(slurm_input, "w", encoding="utf8") as file_obj:
        print(slurm_text(Config.molpro_path), file=file_obj)
