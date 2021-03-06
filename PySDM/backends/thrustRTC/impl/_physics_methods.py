"""
Created at 20.03.2020
"""

import ThrustRTC as trtc
from PySDM.backends.thrustRTC.nice_thrust import nice_thrust
from PySDM.backends.thrustRTC.conf import NICE_THRUST_FLAGS


class PhysicsMethods:
    @staticmethod
    @nice_thrust(**NICE_THRUST_FLAGS)
    def explicit_in_space(omega, c_l, c_r):
        return "c_l * (1 - omega) + c_r * omega;"

    @staticmethod
    @nice_thrust(**NICE_THRUST_FLAGS)
    def implicit_in_space(omega, c_l, c_r):
        """
        see eqs 14-16 in Arabas et al. 2015 (libcloudph++)
        """
        result = "(omega * (c_r - c_l) + c_l) / (1 - (c_r - c_l));"
        return result

    @staticmethod
    @nice_thrust(**NICE_THRUST_FLAGS)
    def temperature_pressure_RH(rhod, thd, qv):
        return "temperature_pressure_RH;"

    __terminal_velocity_body = trtc.For(["values", "radius", "k1", "k2", "k3", "r1", "r2"], "i", '''
            if (radius[i] < r1) {
                values[i] = k1 * radius[i] * radius[i];
            }
            else {
                if (radius[i] < r2) {
                    values[i] = k2 * radius[i];
                }
                else {
                    values[i] = k3 * pow(radius[i], .5);
                }
            }
        ''')

    @staticmethod
    @nice_thrust(**NICE_THRUST_FLAGS)
    def terminal_velocity(values, radius, k1, k2, k3, r1, r2):
        k1 = trtc.DVDouble(k1)
        k2 = trtc.DVDouble(k2)
        k3 = trtc.DVDouble(k3)
        r1 = trtc.DVDouble(r1)
        r2 = trtc.DVDouble(r2)
        PhysicsMethods.__terminal_velocity_body.launch_n(values.size(), [values, radius, k1, k2, k3, r1, r2])

    @staticmethod
    @nice_thrust(**NICE_THRUST_FLAGS)
    def radius(volume):
        return ""

    @staticmethod
    @nice_thrust(**NICE_THRUST_FLAGS)
    def dr_dt_MM(r, T, p, RH, kp, rd):
        return ""

    @staticmethod
    @nice_thrust(**NICE_THRUST_FLAGS)
    def dr_dt_FF(r, T, p, qv, kp, rd, T_i):
        return ""

    @staticmethod
    @nice_thrust(**NICE_THRUST_FLAGS)
    def dthd_dt(rhod, thd, T, dqv_dt):
        return ""
