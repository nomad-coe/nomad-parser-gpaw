import os
from contextlib import contextmanager
import numpy as np
#from nomadcore.unit_conversion.unit_conversion import convert_unit as cu
from nomadcore.local_meta_info import loadJsonFile, InfoKindEl
from nomadcore.parser_backend import JsonParseEventsWriterBackend
from tar import Reader


@contextmanager
def open_section(p, name):
    gid = p.openSection(name)
    yield
    p.closeSection(name, gid)


def cu(value, unit=None):
    """ Dummy function for unit conversion"""
    return value


parser_info = {"name": "parser_gpaw", "version": "1.0"}
metaInfoPath = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../nomad-meta-info/meta_info/nomad_meta_info/gpaw.nomadmetainfo.json"))

metaInfoEnv, warns = loadJsonFile(filePath=metaInfoPath,
                                  dependencyLoader=None,
                                  extraArgsHandling=InfoKindEl.ADD_EXTRA_ARGS,
                                  uri=None)


# TODO: convert to SI units
def parse(filename):
    p = JsonParseEventsWriterBackend(metaInfoEnv)
    o = open_section
    r = Reader(filename)
    p.startedParsingSession(filename, parser_info)
    with o(p, 'section_run'):
        p.addValue('program_name', 'GPAW')
        with o(p, 'section_system_describtion'):
            p.addArrayValues('simulation_cell', r.UnitCell)
            p.addArrayValues('atom_label', r.CartesianPositions)
            p.addArrayValues('configuration_periodic_dimensions',
                             np.array(r.BoundaryConditions, bool))
        with o(p, 'section_single_configuration_calculation'):
            p.addRealValue('energy_total', r.Epot)
            p.addRealValue('energy_XC', r.Exc)
            p.addRealValue('electronic_kinetic_energy', r.Ekin)
            if 'CartesianForces' in r:
                p.addArrayValues('atom_forces_free', r.CartesianForces)
            with o(p, 'section_method'):
                p.addValue('XC_functional', r.XCFunctional)
            with o(p, 'section_eigenvalues_group'):
                for eps_kn, occ_kn in zip(r.Eigenvalues, r.OccupationNumbers):
                    with o(p, 'section_eigenvalues'):
                        p.addArrayValues('eigenvalues_eigenvalues', eps_kn)
                        p.addArrayValues('eigenvalues_occupation', occ_kn)

    p.finishedParsingSession("ParseSuccess", None)

if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    parse(filename)
