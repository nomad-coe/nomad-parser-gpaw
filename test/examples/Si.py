# Copyright 2015-2018 Mikkel Strange, Fawzi Mohamed, Ankit Kariryaa, Ask Hjorth Larsen, Jens Jørgen Mortensen
# 
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from ase.build import bulk
from gpaw import GPAW, PW, FermiDirac

a = 5.43
si = bulk('Si', 'diamond', a)

modes = [{'name': 'pw', 'ecut': 300}, 'fd', 'lcao']
for mode in modes:
    calc = GPAW(mode=mode, kpts=(4, 4,4), txt='Si.txt', basis='dzp')
    si.calc = calc
    si.get_potential_energy()
    if isinstance(mode, basestring):
        mode = {'name': mode}
    print(mode)
    calc.write('Si_' + mode['name'] + '.gpw2')
