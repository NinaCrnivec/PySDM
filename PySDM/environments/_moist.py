"""
Created at 28.11.2019
"""

import numpy as np
from PySDM.builder import Builder


class _Moist:

    def __init__(self, dt, mesh, variables):
        variables += ['qv', 'thd', 'T', 'p', 'RH']
        self.core = None
        self.dt = dt
        self.mesh = mesh
        self.variables = variables
        self._values = None
        self._tmp = None

    def register(self, builder):
        self.core = builder.core
        self.core.observers.append(self)
        self._values = {
            "predicted": None,
            "current": self._allocate(self.variables)
        }
        self._tmp = self._allocate(self.variables)

    def _allocate(self, variables):
        result = {}
        for var in variables:
            result[var] = self.core.Storage.empty((self.mesh.n_cell,), float)
        return result

    def __getitem__(self, index):
        return self._values['current'][index]

    def get_predicted(self, index):
        if self._values['predicted'] is None:
            raise AssertionError("Condensation not called.")
        return self._values['predicted'][index]

    def sync(self):
        target = self._tmp
        target['qv'].ravel(self._get_qv())
        target['thd'].ravel(self._get_thd())

        self.core.backend.apply(
            function=self.core.backend.temperature_pressure_RH,
            args=(target['rhod'], target['thd'], target['qv']),
            output=(target['T'], target['p'], target['RH'])
        )
        self._values["predicted"] = target

    def _get_qv(self) -> np.ndarray: raise NotImplemented()
    def _get_thd(self) -> np.ndarray: raise NotImplemented()

    def notify(self):
        if self._values["predicted"] is None:
            return

        self._tmp = self._values["current"]
        self._values["current"] = self._values["predicted"]
        self._values["predicted"] = None
