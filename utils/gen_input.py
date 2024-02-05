#!/usr/bin/env python3


def get_xyz(atoms, coords):
    """Generates string with structure in format suitable for Molpro."""
    xyz = f"{len(atoms)}\n\n"
    for atom in list(zip(atoms, coords)):
        xyz += f"{atom[0]} {atom[1][0]} {atom[1][1]} {atom[1][2]}\n"
    return xyz[:-1]


def input_text(
    geometry, oep_basis, orbital_basis="aug-cc-pwCV5Z", spin=0, charge=0, space_sym=False, spin_sym=False
):
    """Generate input text for Molpro."""
    if spin == 0:
        method1 = "df-hf"
        method2 = "scexx"
    else:
        method1 = "df-uhf"
        method2 = "uscexx"
    sym_ = ""
    if space_sym is True:
        sym_ += ",thr_sym=1d-10,vhoep=1"
    if spin_sym is True:
        sym_ += ",oepsav=1"
    return f"""basis={{
default,{orbital_basis}
set,oep;{oep_basis}
}}

symmetry,nosym

angstrom
geometry={{
{geometry}
}}

spin={spin}
charge={charge}

{method1},maxit=0,df_basis=aug-cc-pwCV5Z/mp2fit
{{cfit,basis_coul=aug-cc-pwCV5Z/mp2fit,basis_exch=aug-cc-pwCV5Z/mp2fit}}

acfd;{method2},dfit=1,thr_fai_oep=5d-3{sym_}
"""
