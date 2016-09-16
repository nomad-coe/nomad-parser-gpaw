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
