"""
Created at 22.11.2019
"""

from PySDM_examples.ICMW_2012_case_1.simulation import Simulation
from PySDM_examples.ICMW_2012_case_1.setup import Setup
import numpy as np
from matplotlib import pyplot


class DummyStorage:
    def __init__(self):
        self.profiles = {}

    def init(*_): pass

    def save(self, data: np.ndarray, step: int, name: str):
        if name == "qv":
            self.profiles[step] = {"qv": np.mean(data, axis=0)}


def test_spin_up(plot=False):
    # Arrange
    Setup.n_steps = 20
    Setup.outfreq = 1
    setup = Setup()

    for key in setup.processes.keys():
        setup.processes[key] = False
    setup.processes["condensation"] = True
    setup.processes["fluid advection"] = True

    storage = DummyStorage()
    simulation = Simulation(setup, storage)
    simulation.reinit()

    # Act
    simulation.run()

    # Plot
    if plot:
        levels = np.arange(setup.grid[1])
        for step, datum in storage.profiles.items():
            pyplot.plot(datum["qv"], levels, label=str(step))
        pyplot.legend()
        pyplot.show()

    # Assert
    step_num = len(storage.profiles) - 1
    for step in range(step_num):
        next = storage.profiles[step+Setup.outfreq]["qv"]
        prev = storage.profiles[step]["qv"]
        eps = 1e-5
        assert ((prev + eps) >= next).all()
    assert storage.profiles[step_num]["qv"][-1] < 7.
