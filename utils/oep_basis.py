#!/usr/bin/env python3

basis_set_oep = {
    "H": "h=aug-cc-pVDZ/mp2fit",
    "He": "he=aug-cc-pVDZ/mp2fit",
    "Be": "be=aug-cc-pVDZ/mp2fit",
    "Li": "li=aug-cc-pVDZ/mp2fit",
    "B": "b=aug-cc-pVDZ/mp2fit",
    "C": "c=aug-cc-pVDZ/mp2fit",
    "N": "n=aug-cc-pVDZ/mp2fit",
    "O": "o=aug-cc-pVDZ/mp2fit",
    "F": "f=aug-cc-pVDZ/mp2fit",
    "Ne": "ne=aug-cc-pVDZ/mp2fit",
    "Na": "na=aug-cc-pVTZ/mp2fit",
    "Mg": "mg=aug-cc-pVTZ/mp2fit",
    "Al": "al=aug-cc-pVTZ/mp2fit",
    "Si": "si=aug-cc-pVTZ/mp2fit",
    "P": "p=aug-cc-pVTZ/mp2fit",
    "S": "s=aug-cc-pVTZ/mp2fit",
    "Ar": "ar=aug-cc-pVTZ/mp2fit",
    "K": "k=def2-QZVPP/mp2fit",
    "Ti": "ti=def2-QZVPP/mp2fit",  # ???
    "Cl": "cl=aug-cc-pVTZ/mp2fit",
    "Ca": "ca=def2-QZVPP/mp2fit",
    "Zn": "zn=aug-cc-pVTZ/mp2fit",
    "Ge": "ge=def2-QZVPP/mp2fit",
    "Cu": "cu=def2-QZVPP/mp2fit",
    "Ga": "ga=aug-cc-pVTZ/mp2fit",
    "As": "as=aug-cc-pVTZ/mp2fit",
    "Se": "se=def2-QZVPP/mp2fit",  # ???
    "Br": "br=aug-cc-pVTZ/mp2fit",
    "Kr": "kr=def2-QZVPP/mp2fit",  # ???
    "Rb": "rb=def2-QZVPP/mp2fit",  # ???
    "Ag": "ag=def2-QZVPP/mp2fit",  # ???
    "I": "i=def2-QZVPP/mp2fit",  # ???
    "Xe": "xe=def2-QZVPP/mp2fit",  # ???
}


def unique(list1):
    """function to get unique values of list"""
    unique_list = list()
    for x in list1:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list


def get_oep_basis(atom_list):
    """creates string with description of oep basis set for all
    atoms of system"""
    oep_basis_str = ""
    for atom in unique(atom_list):
        oep_basis_str += basis_set_oep[atom] + ";"
    return oep_basis_str[:-1]
