#!/usr/bin/env python

# Credit:
# Adapted by Martin Amezcua from Andrea Rizzi's file of the same name which he wrote for SAMPL6
# at https://github.com/samplchallenges/SAMPL6/blob/master/host_guest/Analysis/ExperimentalMeasurements/generate_tables.py
# and for SAMPL7 by David Mobley at https://github.com/samplchallenges/SAMPL7/blob/master/host_guest/Analysis/ExperimentalMeasurements/generate_tables.py . 

# They get the credit..

# =============================================================================
# GLOBAL IMPORTS
# =============================================================================

import os
import math
import csv
import json
from collections import OrderedDict

import numpy as np
from simtk import unit as u


# =============================================================================
# CONSTANTS
# =============================================================================

T = 298 * u.kelvin
R = u.MOLAR_GAS_CONSTANT_R
RELATIVE_TITRANT_CONC_ERROR = 0.03

CB8_GUESTS_SMILES_PATH = '/mnt/c/users/marty/desktop/SAMPL8_test/host_guest/CB8/guest_files/CB8_guest_smiles.txt'
CB8_GUESTS_NAMES_PATH = '/mnt/c/users/marty/desktop/SAMPL8_test/host_guest/CB8/guest_files/CB8_guest_names.txt' 
GDCC_GUESTS_SMILES_PATH = '/mnt/c/users/marty/desktop/SAMPL8_test/host_guest/GDCC/guest_files/guest_smiles.txt'
GDCC_GUESTS_NAMES_PATH = '/mnt/c/users/marty/desktop/SAMPL8_test/host_guest/GDCC/guest_files/guest_names.txt'

# Experimental results as provided by the Gibb and Isaacs groups.
# The error is relative. None means that the error is <1%.
# For CB8-G2, only considering the 1:1 binding data. 
EXPERIMENTAL_DATA = OrderedDict([

    ('CB8-G1', OrderedDict([
        ('Ka', 1.47*(10**5) / u.molar), ('dKa', 0.09*(10**5) / u.molar),
        ('DH', -7.84 * u.kilocalories_per_mole), ('dDH', 0.100 * u.kilocalories_per_mole),
        #('DG', -7.05 * u.kilocalories_per_mole), ('dDG', None * u.kilocalories_per_mole),
        ('TDS', 0.788 * u.kilocalories_per_mole), ('dTDS', None),
        ('n', 1.00)
    ])),
    ('CB8-G2', OrderedDict([
        ('Ka', 1.9*(10**7) / u.molar), ('dKa', 0.09*(10**7) / u.molar),
        ('DH', -10.8 * u.kilocalories_per_mole), ('dDH', 0.06 * u.kilocalories_per_mole),
        #('DG', -9.94 * u.kilocalories_per_mole), ('dDG', None * u.kilocalories_per_mole),
        ('TDS', 0.872 * u.kilocalories_per_mole), ('TDS', None * u.kilocalories_per_mole), 
        ('n', 1.00)
    ])),
    ('CB8-G3', OrderedDict([
        ('Ka', 3.41*(10**8) / u.molar), ('dKa', 0.15*(10**8) / u.molar),
        ('DH', -13.6 * u.kilocalories_per_mole), ('dDH', 0.04 * u.kilocalories_per_mole),
        #('DG', -11.6 * u.kilocalories_per_mole), ('dDG', None * u.kilocalories_per_mole),
        ('TDS', 1.93 * u.kilocalories_per_mole), ('dTDS', None * u.kilocalories_per_mole),
        ('n', 1.00)
    ])),
    ('CB8-G4', OrderedDict([
        ('Ka', 1.7*(10**8) / u.molar), ('dKa', 0.11*(10**8) / u.molar),
        ('DH', -15.8 * u.kilocalories_per_mole), ('dDH', 0.1 * u.kilocalories_per_mole),
        #('DG', -11.2 * u.kilocalories_per_mole), ('dDG', None * u.kilocalories_per_mole),
        ('TDS', 4.54 * u.kilocalories_per_mole), ('dTDS', None * u.kilocalories_per_mole),
        ('n', 1.00)
    ])),
    ('CB8-G5', OrderedDict([
        ('Ka', 1.09*(10**9) / u.molar), ('dKa', 0.07*(10**9) / u.molar),
        ('DH', -17.3 * u.kilocalories_per_mole), ('dDH', 0.16 * u.kilocalories_per_mole),
        #('DG', -12.3 * u.kilocalories_per_mole), ('dDG', None * u.kilocalories_per_mole),
        ('TDS', 5.01 * u.kilocalories_per_mole), ('dTDS', None * u.kilocalories_per_mole),
        ('n', 1.00)
    ])),
    ('CB8-G6', OrderedDict([
        ('Ka', 2.1*(10**10) / u.molar), ('dKa', 0.2*(10**10) / u.molar),
        ('DH', -14.9 * u.kilocalories_per_mole), ('dDH', 0.04 * u.kilocalories_per_mole),
        #('DG', -14.1 * u.kilocalories_per_mole), ('dDG', None * u.kilocalories_per_mole),
        ('TDS', 0.797 * u.kilocalories_per_mole), ('dTDS', None * u.kilocalories_per_mole),
        ('n', 1.00)
    ])),
    ('CB8-G7', OrderedDict([
        ('Ka', 6.45*(10**5) / u.molar), ('dKa', 0.43*(10**5) / u.molar),
        ('DH', -8.26 * u.kilocalories_per_mole), ('dDH', 0.15 * u.kilocalories_per_mole),
        #('DG', -7.93 * u.kilocalories_per_mole), ('dDG', None * u.kilocalories_per_mole),
        ('TDS', 0.37 * u.kilocalories_per_mole), ('dTDS', None * u.kilocalories_per_mole),
        ('n', 1.00)
    ])),
    ('TEMOA-G1', OrderedDict([
	('DG',-29.1 * u.kilojoules_per_mole), ('dDG', 0.2 * u.kilojoules_per_mole),
	('DH',-71.2 * u.kilojoules_per_mole), ('dDH', 5.3 * u.kilojoules_per_mole),
	('TDS',42.1 * u.kilojoules_per_mole), ('dTDS', 5.1 * u.kilojoules_per_mole),
	('n', 1)
    ])),
    ('TEMOA-G2', OrderedDict([
	('DG', -35.2 * u.kilojoules_per_mole), ('dDG', 0.1 * u.kilojoules_per_mole),
	('DH', -65.6 * u.kilojoules_per_mole), ('dDH', 1.0 * u.kilojoules_per_mole),
	('TDS', 30.3 * u.kilojoules_per_mole), ('dTDS', 1.0 * u.kilojoules_per_mole),
	('n', 1)
    ])),
    ('TEMOA-G3', OrderedDict([
	('DG', -24.2 * u.kilojoules_per_mole), ('dDG', 0.1 * u.kilojoules_per_mole),
	('DH', -33.2 * u.kilojoules_per_mole), ('dDH', 1.0 * u.kilojoules_per_mole),
	('TDS', 9.0 * u.kilojoules_per_mole), ('dTDS', 0.8 * u.kilojoules_per_mole),
	('n', 1)
    ])),
    ('TEMOA-G4', OrderedDict([
	('DG', -32.3 * u.kilojoules_per_mole), ('dDG', 0.1 * u.kilojoules_per_mole),
	('DH', -74.1 * u.kilojoules_per_mole), ('dDH', 1.4 * u.kilojoules_per_mole),
	('TDS', 41.8 * u.kilojoules_per_mole), ('dTDS', 1.3 * u.kilojoules_per_mole),
	('n', 1)    
    ])),
    ('TEMOA-G5', OrderedDict([
	('DG', -27.9 * u.kilojoules_per_mole), ('dDG', 0.1 * u.kilojoules_per_mole),
	('DH', -59.6 * u.kilojoules_per_mole), ('dDH', 3.2 * u.kilojoules_per_mole),
	('TDS', 31.7 * u.kilojoules_per_mole), ('dTDS', 3.1 * u.kilojoules_per_mole),
    	('n', 1)
    ])),
    ('TEETOA-G1', OrderedDict([
	('DG', -18.8 * u.kilojoules_per_mole), ('dDG', 0.2 * u.kilojoules_per_mole),
	('DH', -57.1 * u.kilojoules_per_mole), ('dDH', 0.7 * u.kilojoules_per_mole),
	('TDS', 38.3 * u.kilojoules_per_mole), ('dTDS', 0.6 * u.kilojoules_per_mole), 
    	('n', 1)
    ])), 
    ('TEETOA-G2', OrderedDict([
	('DG', -21.6 * u.kilojoules_per_mole), ('dDG', 0.1 * u.kilojoules_per_mole),
	('DH', -48.7 * u.kilojoules_per_mole), ('dDH', 1.2 * u.kilojoules_per_mole),
	('TDS', 27.2 * u.kilojoules_per_mole), ('dTDS', 1.1 * u.kilojoules_per_mole),
    	('n', 1)
    ])),
    ('TEETOA-G3', OrderedDict([
	('DG', 'NaN' ), ('dDG', 'NaN'),
	('DH', 'NaN' ), ('dDH', 'NaN'), 
	('TDS', 'NaN'), ('dTDS', 'NaN'),
    	('n', 1)
    ])),
    ('TEETOA-G4', OrderedDict([
	('DG', -18.7 * u.kilojoules_per_mole), ('dDG', 0.2 * u.kilojoules_per_mole),
	('DH', -54.3 * u.kilojoules_per_mole), ('dDH', 3.6 * u.kilojoules_per_mole),
	('TDS', 35.6 * u.kilojoules_per_mole), ('dTDS', 3.4 * u.kilojoules_per_mole),
    	('n', 1)
    ])),
    ('TEETOA-G5', OrderedDict([
	('DG', -13.9 * u.kilojoules_per_mole), ('dDG', 0.1 * u.kilojoules_per_mole), 
	('DH', 'NaN'), ('dDH', 'NaN'),
	('TDS', 'NaN'), ('dTDS', 'NaN'),
    	('n', 1)
    ])),
])



# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def load_smiles(file_path):
    """Return the list of guests IDs and SMILES."""
    guests = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            smiles, gid = line.split(';', 1)
            guests.append([smiles.strip(), gid.strip()])
    return guests

def load_names(file_path):
    """Return the list of guests IDs and names."""
    guests = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            name, gid = line.split(';', 1)
            guests.append([name.strip(), gid.strip()])
    return guests


def compute_DG(Ka, dKa):
    """Compute the free energy from the association constant.

    Parameters
    ----------
    Ka : simtk.Quantity
        Association constant.
    dKa : simtk.Quantity
        Association constant uncertainty.

    Returns
    -------
    DG : simtk.Quantity
        Binding free energy.
    dDG : simtk.Quantity
        Binding free energy uncertainty.

    """
    concentration_unit = 1 / Ka.unit
    DG = -R * T * np.log(Ka*concentration_unit)
    # Propagate error.
    if dKa is None:
        dDG = None
    else:
        dDGdKa = -R * T / Ka  # Derivative dDG(Ka)/dKa.
        # Have to use u.sqrt to avoid bug with simtk.unit
        dDG = u.sqrt(dDGdKa**2 * dKa**2)
    return DG, dDG

def compute_Ka(DG, dDG):
    """Compute the association constant from the free energy.

    Parameters
    ----------
    DG : simtk.Quantity
        Free energy
    dDG : simtk.Quantity
        Uncertainty in free energy

    Returns
    -------
    Ka : simtk.Quantity
        Association constant.
    dKa : simtk.Quantity
        Association constant uncertainty.

    """
    concentration_unit = u.molar
    Ka = np.exp(-DG/(R*T))*1/concentration_unit
    # Propagate error.
    if dDG is None:
        dKa = None
    else:
        dKadDG = - Ka / (R*T)  # Derivative dKa(DG)/dDG.
        dKa = u.sqrt(dKadDG**2 * dDG**2)

    return Ka, dKa


def compute_TDS(DG, dDG, DH, dDH):
    """Compute the entropy from free energy and enthalpy.

    Parameters
    ----------
    DG : simtk.Quantity
        Free energy.
    dDG : simtk.Quantity
        Free energy uncertainty.
    DH : simtk.Quantity
        Enthalpy.
    dDH : simtk.Quantity
        Enthalpy uncertainty.

    Returns
    -------
    TDS : simtk.Quantity
        Entrop.
    dTDS : simtk.Quantity
        Binding free energy uncertainty.

    """
    TDS = DH - DG
    dTDS = u.sqrt(dDH**2 + dDG**2)
    return TDS, dTDS


def strip_units(quantities):
    for k, v in quantities.items():
        if isinstance(v, u.Quantity):
            # We only have energies and association and dissociation constants.
            if 'Ka' in k:
                quantities[k] = v.value_in_unit(v.unit)
            elif 'Kd' in k:
                quantities[k] = v.value_in_unit(v.unit)
            else:
                quantities[k] = v.value_in_unit(u.kilocalories_per_mole)


def reduce_to_first_significant_digit(quantity, uncertainty):
    # If strings, just return
    if isinstance(quantity, str) or isinstance(uncertainty, str):
        return quantity, uncertainty
    first_significant_digit = math.floor(math.log10(abs(uncertainty)))
    quantity = round(quantity, -first_significant_digit)
    uncertainty = round(uncertainty, -first_significant_digit)
    return quantity, uncertainty


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    # Load names and SMILES of guests.
    molecule_names = {}

    smiles_by_host = {
        'CB8': load_smiles(CB8_GUESTS_SMILES_PATH),
        'TEMOA' : load_smiles(GDCC_GUESTS_SMILES_PATH),
        'TEETOA' : load_smiles(GDCC_GUESTS_SMILES_PATH),
    }

    names_by_host = {
        'CB8': load_names(CB8_GUESTS_NAMES_PATH),
        'TEMOA' : load_names(GDCC_GUESTS_NAMES_PATH),
        'TEETOA' : load_names(GDCC_GUESTS_NAMES_PATH),
    }

    #for host in CD_HOST_NAMES:
    #    smiles_by_host[host] = load_smiles(CD_GUESTS_SMILES_PATH)
    #    names_by_host[host] = load_names(CD_GUESTS_NAMES_PATH)
    
    #Note: eventually will need to add the other hosts here. 
    for host in ['CB8', 'TEMOA', 'TEETOA']:
        molecule_names[host] = {}
        for smi, gid in smiles_by_host[host]:
            for name, gid2 in names_by_host[host]:
                if gid==gid2:
                    molecule_names[host][gid] = smi, name

    output_dict = OrderedDict()
    upper_bound_molecules = dict(Ka=set(), DH=set(), TDS=set())

    for system_name, system_data in EXPERIMENTAL_DATA.items():
        host_name, gid = system_name.split('-')

        # Load SMILES and common name of the molecule.
        molecule_smiles, molecule_name = molecule_names[host_name][gid]

        # Create entry in the output dictionary.
        output_dict[system_name] = OrderedDict([
            ('name', molecule_name),
            ('SMILES', molecule_smiles),
        ])
        output_dict[system_name].update(system_data)
        system_data = output_dict[system_name]  # Shortcut.

        # If this data has two values, combine: First deal with measured values
        # Note that Kd/Ka values should be combined as free energies (since that's the normally distributed quantity)
        for data_type in ['Kd', 'Ka', 'DH']:
            if data_type+'_1' in system_data:
                if 'DH' in data_type: #just take mean
                    final_val = np.mean( [system_data[data_type+'_1'], system_data[data_type+'_2']])
                    system_data[data_type] = final_val

                    # Also compute uncertainty -- the larger of the propagated uncertainty and the standard error in the mean
                    final_unc = u.sqrt( system_data['d'+data_type+'_1']**2 + system_data['d'+data_type+'_2']**2 )
                    std_err = u.sqrt( 0.5*( (system_data[data_type+'_1']-final_val)**2 + (system_data[data_type+'_2']-final_val)**2) )
                    if std_err > final_unc:
                        final_unc = std_err
                    system_data['d'+data_type] = final_unc
                #Otherwise first convert to free energy then take mean
                elif 'Kd' in data_type: #First convert to free energy then take mean
                    # If we have Kd data instead of Ka data, convert
                    if 'Kd_1' in system_data and not 'Ka_1' in system_data:
                        system_data['Ka_1'] = 1./system_data['Kd_1']
                        # Handle uncertainty -- 1/Kd^2 * dKd
                        system_data['dKa_1'] = system_data['dKd_1']/(system_data['Kd_1']**2)
                        system_data['Ka_2'] = 1./system_data['Kd_2']
                        # Handle uncertainty -- 1/Kd^2 * dKd
                        system_data['dKa_2'] = system_data['dKd_2']/(system_data['Kd_2']**2)
                elif 'Ka' in data_type:
                    if 'Ka_1' in system_data and not 'Ka' in system_data:
                        # Now convert to free energy
                        DG_1, dDG_1 = compute_DG(system_data['Ka_1'], system_data['dKa_1'])
                        DG_2, dDG_2 = compute_DG(system_data['Ka_2'], system_data['dKa_2'])
                        # Take mean
                        DG = (DG_1+DG_2)/2.
                        # Compute uncertainty
                        final_unc = u.sqrt( (dDG_1)**2 + (dDG_2)**2)
                        std_err = u.sqrt( 0.5*( (DG_1-DG)**2 + (DG_2-DG)**2) )
                        if std_err > final_unc:
                            final_unc = std_err
                        # Convert back to Ka and store
                        Ka, dKa = compute_Ka( DG, final_unc)
                        system_data['Ka'] = Ka
                        system_data['dKa'] = dKa


        # Incorporate the relative concentration uncertainties into quantities.
        # Skip this for the Gibb data, where concentration errors are already accounted for and we already have free energy
        TDS = None
        dTDS = None
        DG = None
        dDG = None
        if not 'OA' in system_name:
            for k in ['Ka', 'DH']:
                quantity = system_data[k]
                # Compute relative uncertainty
                relative_uncertainty = system_data['d' + k]/quantity
                # Use upper-bound of 1% if <1% is reported. Keep track of these molecules.
                if relative_uncertainty is None:
                    upper_bound_molecules[k].add(system_name)
                    relative_uncertainty = 0.01
                # Incorporate the relative concentration uncertainties into quantities.
                relative_uncertainty = u.sqrt( relative_uncertainty**2 + RELATIVE_TITRANT_CONC_ERROR**2)
                # Convert relative to absolute errors.
                system_data['d' + k] = abs(quantity * relative_uncertainty)

            # Propagate Ka and DH error into DG and TDS.
            DG, dDG = compute_DG(system_data['Ka'], system_data['dKa'])
            system_data['DG'] = DG
            system_data['dDG'] = dDG
            TDS, dTDS = compute_TDS(system_data['DG'], system_data['dDG'],
                                    system_data['DH'], system_data['dDH'])
            system_data['TDS'] = TDS
            system_data['dTDS'] = dTDS

        # If we have a free energy but not a Ka, compute Ka
        if not 'Ka' in system_data:
            try:
                system_data['Ka'], system_data['dKa'] = compute_Ka(system_data['DG'], system_data['dDG'])
            except TypeError:
                if system_data['DG']=='NaN':
                    system_data['Ka']='NaN'
                    system_data['dKa']='NaN'

        # Strip units.
        strip_units(system_data)

        ## Consistency checks.
        #if system_data['TDS']!='NaN' and system_data['DG']!='NaN' and system_data['DH']!='NaN':
        #    assert np.isclose(system_data['DG'], system_data['DH'] - system_data['TDS'], atol=0.10000000000001, rtol=0.0)

        #    if DG is not None:
        #        computed_DG = DG.value_in_unit(u.kilocalories_per_mole)
        #        assert np.isclose(np.around(computed_DG, decimals=2), system_data['DG'], atol=0.0200000000000001, rtol=0.0)
        #    if TDS is not None:
        #        computed_TDS = TDS.value_in_unit(u.kilocalories_per_mole)
        #        assert np.isclose(np.around(computed_TDS, decimals=2), system_data['TDS'], atol=0.0200000000000001, rtol=0.0)


        # Report only error most significant digit.
        for k in ['Ka', 'DH', 'TDS', 'DG']:
            if k in system_data:
                quantity, uncertainty = system_data[k], system_data['d' + k]
                if uncertainty is not None:
                    system_data[k], system_data['d' + k] = reduce_to_first_significant_digit(quantity, uncertainty)

    # Create output JSON file.
    with open('experimental_measurements.json', 'w') as f:
        json.dump(output_dict, f)

    # Create output CSV file.
    # Convert single dict to list of dicts.
    csv_dicts = []
    for system_id, system_data in output_dict.items():
        csv_dict = OrderedDict([('ID', system_id)])
        csv_dict.update(system_data)
        csv_dicts.append(csv_dict)
    with open('experimental_measurements.csv', 'w') as f:
        writer = csv.DictWriter(f, csv_dicts[0].keys(), delimiter=';')
        writer.writeheader()
        writer.writerows(csv_dicts)

   
   # Create a LaTex table.
    os.makedirs('PDFTable', exist_ok=True)
    old_host = ''
    with open('PDFTable/experimental_measurements.tex', 'w', encoding='utf-8') as f:
        f.write('\\documentclass{article}\n'
                '\\usepackage[a4paper,margin=0.4in,tmargin=0.5in,landscape]{geometry}\n'
                '\\usepackage{tabu}\n'
                '\\pagenumbering{gobble}\n'
                '\\begin{document}\n'
                '\\begin{center}\n'
                '\\footnotesize\n'
                '\\begin{tabu}')

       # Cell alignment.
        #field_names = ['ID', 'name', '$K_a$ (M$^{-1}$)', '$\\Delta G$ (kcal/mol) $^{(a)}$', '$\\Delta H$ (kcal/mol)', '$T\\Delta S$ (kcal/mol) $^{(b)}$', '$n$']
        field_names = ['ID', 'name', 'SMILES', '$K_a$ (M$^{-1}$)', 'd$K_a$ (M$^{-1}$)', '$\\Delta H$ (kcal/mol)', '$d\\Delta H$ (kcal/mol)', '$T\\Delta S$ (kcal/mol)', 'd$T\\Delta S$ (kcal/mol)', 'n', '$\\Delta G$ (kcal/mol', 'd$\\Delta G$ (kcal/mol)']
        f.write('{| ' + ' | '.join(['c' for _ in range(len(field_names))]) + ' |}\n')

        # Table header.
        f.write('\\hline\n')
        f.write('\\rowfont{\\bfseries} ' + ' & '.join(field_names) + ' \\\\\n')
        f.write('\\hline\n')

        # Print lines.
        for csv_dict in csv_dicts:

            # Separate hosts with a double horizontal line.
            host_name = csv_dict['ID'].split('-')[0]
            if host_name != old_host:
                f.write('\\hline\n')
                old_host = host_name

           #if csv_dict['ID']=='clip-g10' or 'OA-g5' in csv_dict['ID']:
           #    # One name can't be dealt with; reformat
           #    csv_dict['name'] = "Can't format in LaTeX"




            row = '{ID} & {name}'
            # add a superscript to reflect the different experiments (ITC or NMR) for CB8 and GDCCs
            superscript = ''
            if csv_dict['ID'] == 'CB8-G1' or csv_dict['ID'] == 'CB8-G2' or csv_dict['ID'] == 'CB8-G7':
                superscript += 'c'
            elif csv_dict['ID'] == 'CB8-G3' or csv_dict['ID'] == 'CB8-G4':
                superscript += 'd'
            elif csv_dict['ID'] == 'CB8-G5' or csv_dict['ID'] == 'CB8-G6':
                superscript += 'e'
            elif csv_dict['ID'] == 'TEETOA-G3':
                superscript += 'f'
            elif csv_dict['ID'] == 'TEETOA-G5':
                superscript += 'g'
            if superscript != '':
                row += '$^{{(' + superscript + ')}}$'

            for k in ['Ka', 'DG', 'DH', 'TDS']:
                row += ' & '

                # Report Ka in scientific notation.
                if k == 'Ka':
                    if not isinstance(k, str):
                        first_significant_digit = math.floor(math.log10(abs(csv_dict['d' + k])))
                        csv_dict['d' + k] /= 10**first_significant_digit
                        csv_dict[k] /= 10**first_significant_digit
                        row += '('
                row += '{' + k + '} +- {d' + k + '}'
                if k == 'Ka':
                    if not isinstance(k, str):
                        row += ') $\\times$ 10'
                        if first_significant_digit != 1:
                            row += '$^{{{{{}}}}}$'.format(first_significant_digit)

               # Check if we used the upperbound.
               #superscript = ''
               ## if k != 'DG' and csv_dict['ID'] in upper_bound_molecules[k]:
               ##     superscript += 'a'
               #if k == 'Ka':
               #    if csv_dict['n'] == 0.33:
               #        superscript += 'd'
               #    elif csv_dict['n'] == 0.5 or csv_dict['n'] == 2:
               #        superscript += 'c'
               #if superscript != '':
               #    row += ' $^{{(' + superscript + ')}}$'

            row += (' & {n: .2f} \\\\\n'
                    '\\hline\n')

            row = row.format(**csv_dict)

            # Escape underscores for latex formatting
            row = row.replace('_','\_')

            # Write
            f.write(row)

        f.write('\end{tabu}\end{center}\\vspace{5mm}\n'
                'All quantities are reported as point estimate +- statistical error from the ITC data fitting procedure. '
                'The upper bound ($1\%$) was used for errors reported to be $<1\%$. We also included a 3\% relative '
                'uncertainty in the titrant concentration assuming the stoichiometry coefficient to be fitted to the ITC '
                'data for the Isaacs (CB8) dataset, where concentration error had not been factored in to the original'
                'error estimates. For the TEMOA/TEETOA sets, provided uncertainties already include concentration error.\\\\\n'
                '($^a$) Statistical errors were propagated from the $K_a$ measurements. \\\\\n'
                '($^b$) All experiments were performed at 298 K. \\\\\n'
                '($^c$) Direct ITC titration. \\\\\n'
                '($^d$) Competitive ITC titration with C1. \\\\\n'
                '($^e$) Competitive ITC titration with C2.\\\\\n'
		'($^f$) Binding is too weak to be observed by NMR or ITC. \\\\\n'
		'($^g$) Determined by 1H NMR spectroscopy.\n'
                '\end{document}\n')
