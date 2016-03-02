import os
from contextlib import contextmanager
import numpy as np
from ase.data import chemical_symbols
import setup_paths
from nomadcore.unit_conversion.unit_conversion import convert_unit as cu
from nomadcore.local_meta_info import loadJsonFile, InfoKindEl
from nomadcore.parser_backend import JsonParseEventsWriterBackend
from tar import Reader


@contextmanager
def open_section(p, name):
    gid = p.openSection(name)
    yield
    p.closeSection(name, gid)


def c(value, unit=None):
    """ Dummy function for unit conversion"""
    return cu(value, unit)


parser_info = {"name": "parser_gpaw", "version": "1.0"}
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
    r = Reader(filename)
    p.startedParsingSession(filename, parser_info)

    with o(p, 'section_run'):
        p.addValue('program_name', 'GPAW')
        if r.Mode == 'pw':
            with o(p, 'section_basis_set_cell_associated'):
                p.addValue('basis_set_cell_associated_name',
                           'PW_%.1f_Ry' % (r.PlaneWaveCutoff * 2.0))  # in Ry
                p.addRealValue('basis_set_plane_wave_cutoff',
                               c(r.PlaneWaveCutoff, 'hartree'))
        elif r.Mode == 'fd':
            with o(p, 'section_basis_set_cell_associated'):
                h1 = np.linalg.norm(r.UnitCell[0]) / r.dims['ngptsx']
                h2 = np.linalg.norm(r.UnitCell[1]) / r.dims['ngptsy']
                h3 = np.linalg.norm(r.UnitCell[2]) / r.dims['ngptsz']
                h = (h1 + h2 + h3) / 3.0
                p.addValue('basis_set_cell_associated_name',
                           'GR_%.1f' % (c(h, 'bohr') * 1.0E15))  # in fm
        elif r.Mode == 'lcao':
            pass
        with o(p, 'section_system_description'):
            p.addArrayValues('simulation_cell', c(r.UnitCell, 'bohr'))
            symbols = np.array([chemical_symbols[z] for z in r.AtomicNumbers])
            p.addArrayValues('atom_label', symbols)
            p.addArrayValues('atom_position', c(r.CartesianPositions, 'bohr'))
            p.addArrayValues('configuration_periodic_dimensions',
                             np.array(r.BoundaryConditions, bool))
        with o(p, 'section_single_configuration_calculation'):
            p.addRealValue('energy_total', c(r.Epot, 'hartree'))
            p.addRealValue('energy_XC', c(r.Exc, 'hartree'))
            p.addRealValue('electronic_kinetic_energy', c(r.Ekin, 'hartree'))
            if 'CartesianForces' in r:
                p.addArrayValues('atom_forces_free',
                                 c(r.CartesianForces, 'bohr/hartree'))
            with o(p, 'section_method'):
                p.addValue('XC_functional', r.XCFunctional)
                if 'FermiWidth' in r:
                    p.addValue('smearing_kind', 'fermi')
                    p.addRealVaule('smearing_width',
                                   cu(r.FermiWidth, 'hartree'))
            with o(p, 'section_eigenvalues_group'):
                for eps_kn, occ_kn in zip(r.Eigenvalues, r.OccupationNumbers):
                    with o(p, 'section_eigenvalues'):
                        p.addArrayValues('eigenvalues_eigenvalues',
                                         c(eps_kn, 'hartree'))
                        p.addArrayValues('eigenvalues_occupation', occ_kn)
                        p.addArrayValues('eigenvalues_kpoints', r.IBZKPoints)
    p.finishedParsingSession("ParseSuccess", None)

if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    parse(filename)
