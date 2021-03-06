"""
Created at 25.11.2019
"""

from PySDM.core import Core
from PySDM.physics import formulae as phys
from ..physics import constants as const
from ._moist import _Moist
from ._moist_lagrangian_parcel import _MoistLagrangianParcel
from PySDM.mesh import Mesh


class MoistLagrangianParcelAdiabatic(_MoistLagrangianParcel):

    def __init__(
            self, dt,
            mass_of_dry_air: float,
            p0: float, q0: float, T0: float,
            w: callable, z0: float = 0):

        super().__init__(dt, Mesh.mesh_0d(), ['rhod', 'z', 't'], mass_of_dry_air)

        # TODO: move w-related logic to _MoistLagrangianParcel
        self.w = w

        pd0 = p0 * (1 - (1 + const.eps / q0)**-1)

        self.params = (q0, phys.th_std(pd0, T0), pd0 / const.Rd / T0, z0, 0)

    def register(self, builder):
        _MoistLagrangianParcel.register(self, builder)
        self['qv'][:] = self.params[0]
        self['thd'][:] = self.params[1]
        self['rhod'][:] = self.params[2]
        self['z'][:] = self.params[3]
        self['t'][:] = self.params[4]
        delattr(self, 'params')

        self.sync_parcel_vars()
        _Moist.sync(self)
        self.notify()

    def advance_parcel_vars(self):
        dt = self.core.dt
        qv = self['qv'][0]
        T = self['T'][0]
        p = self['p'][0]
        t = self['t'][0]

        rho = p / phys.R(qv) / T
        pd = p * (1 - 1 / (1 + const.eps / qv))

        # mid-point value for w
        dz_dt = self.w(t + dt/2)

        # Explicit Euler for p,T (predictor step assuming dq=0)
        dp_dt = - rho * const.g * dz_dt
        dpd_dt = dp_dt  # dq=0
        dT_dt = dp_dt / rho / phys.c_p(qv)

        self._tmp['t'][:] += dt
        self._tmp['z'][:] += dt * dz_dt
        self._tmp['rhod'][:] += dt * (
                dpd_dt / const.Rd / T +
                -dT_dt * pd / const.Rd / T**2
        )
