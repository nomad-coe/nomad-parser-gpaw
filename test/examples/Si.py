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
