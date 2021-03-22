#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD. See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import pytest
import numpy as np

from nomad.datamodel import EntryArchive
from gpawparser import GPAWParser


@pytest.fixture(scope='module')
def parser():
    return GPAWParser()


def test_gpw(parser):
    archive = EntryArchive()
    parser.parse('tests/data/H2.gpw', archive, None)

    assert archive.section_run[0].program_version == '1.1.0'
    assert archive.section_run[0].program_basis_set_type == 'real space grid'
    assert archive.section_run[0].section_basis_set_cell_dependent[0].basis_set_cell_dependent_name == 'GR_20900.5'

    sec_method = archive.section_run[0].section_method[0]
    assert pytest.approx(sec_method.scf_threshold_energy_change.magnitude, 1.42196374e-24)
    assert sec_method.smearing_width == 0.0
    assert sec_method.total_charge == 0.0
    assert sec_method.section_XC_functionals[1].XC_functional_name == 'LDA_C_PW'
    assert sec_method.x_gpaw_symmetry_time_reversal_switch

    sec_system = archive.section_run[0].section_system[0]
    assert sec_system.atom_labels == ['H', 'H']
    assert pytest.approx(sec_system.lattice_vectors[2][2].magnitude, 4.73716558e-10)
    assert True not in sec_system.configuration_periodic_dimensions
    assert pytest.approx(sec_system.atom_positions[0][2].magnitude, 2.73716576e-10)

    sec_scc = archive.section_run[0].section_single_configuration_calculation[0]
    assert pytest.approx(sec_scc.energy_total.magnitude, -1.51414975e-18)
    assert sec_scc.x_gpaw_fixed_spin_Sz == 0.0
    assert pytest.approx(sec_scc.energy_reference_fermi[1].magnitude, -4.99922789e-19)
    # there is supposed to be magnetic but read eigenvalues are not spinpol
    assert np.shape(sec_scc.section_eigenvalues[0].eigenvalues_values) == (1, 1, 2)
    assert np.shape(sec_scc.section_eigenvalues[0].eigenvalues_kpoints) == (1, 3)
    assert pytest.approx(sec_scc.section_eigenvalues[0].eigenvalues_values[0][0][1].magnitude, 5.54481608e-19)
    assert pytest.approx(sec_scc.section_eigenvalues[0].eigenvalues_occupation[0][0][0], 2.0)
    assert sec_scc.single_configuration_calculation_converged


def test_gpw2(parser):
    archive = EntryArchive()
    parser.parse('tests/data/Si_pw.gpw2', archive, None)

    assert archive.section_run[0].program_version == '1.1.1b1'
    assert archive.section_run[0].program_basis_set_type == 'plane waves'
    assert pytest.approx(archive.section_run[0].section_basis_set_cell_dependent[0].basis_set_planewave_cutoff.magnitude, 4.8065299e-17)

    sec_method = archive.section_run[0].section_method[0]
    assert pytest.approx(sec_method.scf_threshold_energy_change.magnitude, 8.01088317e-23)
    assert pytest.approx(sec_method.smearing_width, 1.60217663e-20)
    assert not sec_method.x_gpaw_fix_density
    assert sec_method.section_XC_functionals[0].XC_functional_name == 'LDA_X'

    sec_system = archive.section_run[0].section_system[0]
    assert sec_system.atom_labels == ['Si', 'Si']
    assert pytest.approx(sec_system.lattice_vectors[0][1].magnitude, 2.715e-10)
    assert False not in sec_system.configuration_periodic_dimensions
    assert pytest.approx(sec_system.atom_positions[1][0].magnitude, 1.3575e-10)

    sec_scc = archive.section_run[0].section_single_configuration_calculation[0]
    assert pytest.approx(sec_scc.energy_XC.magnitude, -2.19623851e-18)
    assert pytest.approx(sec_scc.energy_reference_fermi[0].magnitude, 8.60653138e-19)
    assert np.shape(sec_scc.section_eigenvalues[0].eigenvalues_values) == (1, 10, 8)
    assert pytest.approx(sec_scc.section_eigenvalues[0].eigenvalues_values[0][7][4].magnitude, 9.50790908e-19)
    assert pytest.approx(sec_scc.section_eigenvalues[0].eigenvalues_occupation[0][0][0], 7.22642797590849e-09)
    assert sec_scc.single_configuration_calculation_converged


def test_spinpol(parser):
    archive = EntryArchive()
    parser.parse('tests/data/Hspinpol.gpw', archive, None)

    sec_eig = archive.section_run[0].section_single_configuration_calculation[0].section_eigenvalues[0]
    assert np.shape(sec_eig.eigenvalues_kpoints) == (1, 3)
    assert np.shape(sec_eig.eigenvalues_occupation) == (2, 1, 1)
    assert np.shape(sec_eig.eigenvalues_values) == (2, 1, 1)
    assert pytest.approx(sec_eig.eigenvalues_values[0][0][0].magnitude, -1.20983278e-18)
    assert archive.section_run[0].section_single_configuration_calculation[0].x_gpaw_magnetic_moments[0] == 1.


def test_lcao(parser):
    archive = EntryArchive()
    parser.parse('tests/data/Si_lcao.gpw2', archive, None)

    assert archive.section_run[0].program_version == '1.1.1b1'
    assert archive.section_run[0].program_basis_set_type == 'numeric AOs'
    assert archive.section_run[0].section_basis_set_atom_centered[0].basis_set_atom_centered_short_name == 'dzp'

    sec_vols = archive.section_run[0].section_single_configuration_calculation[0].section_volumetric_data
    assert len(sec_vols) == 2
    assert sec_vols[1].volumetric_data_kind == 'potential_effective'
    assert pytest.approx(sec_vols[0].volumetric_data_values[0][13][2][8], 8.70353098415676e+28)
    assert pytest.approx(sec_vols[1].volumetric_data_values[0][5][14][1], -1235219198924.2632)
