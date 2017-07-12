from __future__ import division
import os
from contextlib import contextmanager
import numpy as np
from ase import units
from ase.data import chemical_symbols
from ase.io.aff import affopen
from ase.utils import basestring
#from ase.io.trajectory import read_atoms
from ase.data import atomic_masses
from ase.units import Rydberg
import setup_paths
from nomadcore.unit_conversion.unit_conversion import convert_unit as cu
from nomadcore.local_meta_info import loadJsonFile, InfoKindEl
from nomadcore.parser_backend import JsonParseEventsWriterBackend
from libxc_names import get_libxc_name
from default_parameters import parameters as parms


@contextmanager
def open_section(p, name):
    gid = p.openSection(name)
    yield gid
    p.closeSection(name, gid)


def c(value, unit=None):
    """ Dummy function for unit conversion"""
    return cu(value, unit)


parser_info = {"name": "parser2_gpaw", "version": "1.0"}
path = '../../../../nomad-meta-info/meta_info/nomad_meta_info/' +\
        'gpaw.nomadmetainfo.json'
metaInfoPath = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), path))

metaInfoEnv, warns = loadJsonFile(filePath=metaInfoPath,
                                  dependencyLoader=None,
                                  extraArgsHandling=InfoKindEl.ADD_EXTRA_ARGS,
                                  uri=None)


def parse(filename):
    p = JsonParseEventsWriterBackend(metaInfoEnv)
    o = open_section
    r = affopen(filename) #  Reader(filename)
    p.startedParsingSession(filename, parser_info)
    parms.update(r.parameters.asdict())
    with o(p, 'section_run'):
        p.addValue('program_name', 'GPAW')
        p.addValue('program_version', r.gpaw_version)
        mode = parms['mode']
        if isinstance(mode, basestring):
            mode = {'name': mode}
        if mode['name'] == 'pw':
            p.addValue('program_basis_set_type', 'plane waves')
            with o(p, 'section_basis_set_cell_dependent'):
                p.addValue('basis_set_cell_dependent_name',
                           'PW_%.1f_Ry' % (mode['ecut'] / r.ha * 2))  # in Ry
                p.addRealValue('basis_set_planewave_cutoff',
                               c(mode['ecut'], 'eV'))
        elif mode['name'] == 'fd':
            p.addValue('program_basis_set_type', 'real space grid')
            with o(p, 'section_basis_set_cell_dependent'):
                cell = r.atoms.cell
                ngpts = r.density.density.shape
                h1 = np.linalg.norm(cell[0]) / ngpts[0]
                h2 = np.linalg.norm(cell[1]) / ngpts[1]
                h3 = np.linalg.norm(cell[2]) / ngpts[2]
                h = (h1 + h2 + h3) / 3.0
                p.addValue('basis_set_cell_dependent_name',
                           'GR_%.1f' % (c(h, 'angstrom') * 1.0E15))  # in fm
        elif mode['name'] == 'lcao':
            p.addValue('program_basis_set_type', 'numeric AOs')
            with o(p, 'section_basis_set_atom_centered'):
                p.addValue('basis_set_atom_centered_short_name',
                          parms['basis'])
        with o(p, 'section_system') as system_gid:
            p.addArrayValues('simulation_cell',
                             c(r.atoms.cell, 'angstrom'))
            symbols = np.array([chemical_symbols[z] for z in r.atoms.numbers])
            p.addArrayValues('atom_labels', symbols)
            p.addArrayValues('atom_positions', c(r.atoms.positions, 'angstrom'))
            p.addArrayValues('configuration_periodic_dimensions',
                             np.array(r.atoms.pbc, bool))
            if 'momenta' in r.atoms:
                masses = atomic_masses[r.atoms.numbers]
                velocities = r.atoms.momenta / masses.reshape(-1, 1)
                p.addArrayValues('atom_velocities',
                                c(velocities * units.fs / units.Angstrom,
                                  'angstrom/femtosecond'))
        with o(p, 'section_sampling_method'):
            p.addValue('ensemble_type', 'NVE')
        with o(p, 'section_frame_sequence'):
            pass
        with o(p, 'section_method') as method_gid:
            p.addValue('relativity_method', 'pseudo_scalar_relativistic')
            p.addValue('electronic_structure_method', 'DFT')
            p.addValue('scf_threshold_energy_change',
                       c(parms['convergence']['energy'], 'eV')) # eV / electron
            #if r.FixMagneticMoment:
            #    p.addValue('x_gpaw_fixed_spin_Sz',
            #               r.MagneticMoments.sum() / 2.)
            if parms['occupations'] is None:  # use default values
                if tuple(parms['kpts']) == (1, 1, 1):
                    width = 0.0
                else:
                    width = 0.1
                parms['occupations'] = {'width': width, 'name': 'fermi-dirac'}

            p.addValue('smearing_kind', parms['occupations']['name'])
            p.addRealValue('smearing_width',
                               c(parms['occupations']['width'], 'eV'))
            p.addRealValue('total_charge', parms['charge'])
            with o(p, 'section_XC_functionals'):
                p.addValue('XC_functional_name',
                           get_libxc_name(parms['xc']))
        with o(p, 'section_single_configuration_calculation'):
            p.addValue('single_configuration_calculation_to_system_ref',
                       system_gid)
            p.addValue('single_configuration_to_calculation_method_ref',
                       method_gid)
            p.addValue('single_configuration_calculation_converged',
                      r.scf.converged)
            p.addRealValue('energy_total',
                           c(r.hamiltonian.e_total_extrapolated, 'eV'))
            p.addRealValue('energy_free',
                           c(r.hamiltonian.e_total_free, 'eV'))
            p.addRealValue('energy_XC', c(r.hamiltonian.e_xc, 'eV'))
            p.addRealValue('electronic_kinetic_energy',
                           c(r.hamiltonian.e_kinetic, 'eV'))
            p.addRealValue('energy_correction_entropy',
                           c(r.hamiltonian.e_entropy, 'eV'))
            p.addRealValue('energy_reference_fermi',
                          c(r.occupations.fermilevel, 'eV'))
            p.addRealValue('energy_reference_fermi',
                          c(r.occupations.fermilevel, 'eV'))
            if 'forces' in r.results:
                p.addArrayValues('atom_forces_free_raw',
                                 c(r.results.forces, 'eV/angstrom'))
            if 'magmons' in r.results:
                p.addArrayValues('x_gpaw_magnetic_moments',
                                 r.results.magmoms)
                p.addRealValue('x_gpaw_spin_Sz', r.results.magmoms.sum() / 2.0)
            #p.addArrayValues('x_gpaw_atomic_density_matrices',
            #                 r.AtomicDensityMatrices)
            #p.addArrayValues('x_gpaw_projections_real', r.Projections.real)
            #p.addArrayValues('x_gpaw_projections_imag', r.Projections.imag)
            with o(p, 'section_eigenvalues'):
                p.addValue('eigenvalues_kind', 'normal')
                p.addArrayValues('eigenvalues_values',
                                 c(r.wave_functions.eigenvalues, 'eV'))
                p.addArrayValues('eigenvalues_occupation',
                                 r.wave_functions.occupations)
                #p.addArrayValues('eigenvalues_kpoints', r.IBZKPoints)
            if 'band_paths' in r.wave_functions: # could change
                with o(p, 'section_k_band'):
                    for band_path in r.wave_functions.band_paths:
                        with o(p, 'section_k_band_segment'):
                            p.addArrayValues('band_energies',
                                            c(band_path.eigenvalues, 'eV'))
                            p.addArrayValues('band_k_points', 'eV',
                                             band_path.kpoints)
                            p.addArrayValues('band_segm_labels',
                                            band_path.labels)
                            p.addArrayValues('band_segm_start_end',
                                             np.asarray(
                                                 [band_path.kpoints[0],
                                                  band_path.kpoints[-1]]))


    p.finishedParsingSession("ParseSuccess", None)

if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    parse(filename)
