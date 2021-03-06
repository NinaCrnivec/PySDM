"""
Created at 20.03.2020
"""

from PySDM.backends.thrustRTC.nice_thrust import nice_thrust
from PySDM.backends.thrustRTC.conf import NICE_THRUST_FLAGS


class Methods:

    @staticmethod
    @nice_thrust(**NICE_THRUST_FLAGS)
    def apply(function, args, output):
        raise NotImplementedError()

    @staticmethod
    @nice_thrust(**NICE_THRUST_FLAGS)
    def first_element_is_zero(arr):
        return arr.to_host()[0] == 0

    @staticmethod
    @nice_thrust(**NICE_THRUST_FLAGS)
    def _apply_f_3_3(function, arg0, arg1, arg2, output0, output1, output2):
        raise NotImplementedError()
