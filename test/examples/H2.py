#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD.
# See https://nomad-lab.eu for further info.
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

from ase.build import molecule
from gpaw import GPAW, PW, FermiDirac
from ase.constraints import FixAtoms
atoms = molecule('H2')
atoms.center(vacuum=2.0)

modes = [{'name': 'pw', 'ecut': 300}, 'fd', 'lcao']
for mode in modes:
    calc = GPAW(mode=mode, txt='H2.txt', basis='dzp',spinpol=True,
                occupations=FermiDirac(0.05))
    atoms.calc = calc
    atoms.set_constraint(FixAtoms(indices=[0]))
    atoms.set_velocities([[1.0,0.0,0.0],[2.0,3.0,4.0]])
    atoms.get_potential_energy()
    atoms.get_forces()
    if isinstance(mode, basestring):
        mode = {'name': mode}
    print(mode)
    calc.write('H2_' + mode['name'] + '.gpw2')
