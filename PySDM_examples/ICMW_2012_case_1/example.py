"""
Created at 25.09.2019

@author: Piotr Bartman
@author: Michael Olesik
@author: Sylwester Arabas
"""

from PySDM_examples.ICMW_2012_case_1.setup import Setup
from PySDM_examples.ICMW_2012_case_1.simulation import Simulation
from PySDM_examples.ICMW_2012_case_1.storage import Storage


def main():
    # with np.errstate(all='raise'):
    setup = Setup()
    storage = Storage()
    simulation = Simulation(setup, storage)
    simulation.run()


if __name__ == '__main__':
    main()
