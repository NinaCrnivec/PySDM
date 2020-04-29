"""
Created at 23.10.2019

@author: Piotr Bartman
@author: Michael Olesik
@author: Sylwester Arabas
"""

import numpy as np
from PySDM.simulation.particles_builder import ParticlesBuilder


class Displacement:
    def __init__(self, particles_builder: ParticlesBuilder, scheme='FTBS', sedimentation=False):
        self.particles = particles_builder.particles
        courant_field = self.particles.environment.get_courant_field_data()

        # CFL # TODO: this should be done by MPyDATA
        for d in range(len(courant_field)):
            assert np.amax(abs(courant_field[d])) <= 1

        if scheme == 'FTFS':
            method = self.particles.backend.explicit_in_space
        elif scheme == 'FTBS':
            method = self.particles.backend.implicit_in_space
        else:
            raise NotImplementedError()

        self.scheme = method
        self.sedimentation = sedimentation

        self.dimension = len(courant_field)
        self.grid = np.array([courant_field[1].shape[0], courant_field[0].shape[1]], dtype=np.int64)

        self.courant = [self.particles.backend.from_ndarray(courant_field[i]) for i in range(self.dimension)]

        self.displacement = self.particles.backend.from_ndarray(np.zeros((self.particles.n_sd, self.dimension)))
        self.temp = self.particles.backend.from_ndarray(np.zeros((self.particles.n_sd, self.dimension), dtype=np.int64))

    def __call__(self):
        # TIP: not need all array only [idx[:sd_num]]
        displacement = self.displacement
        cell_origin = self.particles.state.cell_origin
        position_in_cell = self.particles.state.position_in_cell

        self.calculate_displacement(displacement, self.courant, cell_origin, position_in_cell)
        self.update_position(position_in_cell, displacement)
        if self.sedimentation:
            self.particles.remove_precipitated()
        self.update_cell_origin(cell_origin, position_in_cell)
        self.boundary_condition(cell_origin)
        self.particles.state.recalculate_cell_id()

    def calculate_displacement(self, displacement, courant, cell_origin, position_in_cell):
        for dim in range(self.dimension):
            self.particles.backend.calculate_displacement(dim, self.scheme, displacement, courant[dim], cell_origin, position_in_cell)
        if self.sedimentation:
            displacement_z = displacement[:, -1]
            dt_over_dz = self.particles.dt / self.particles.mesh.dz
            self.particles.backend.multiply(displacement_z, 1 / dt_over_dz)
            self.particles.backend.subtract(displacement_z, self.particles.terminal_velocity.values)
            self.particles.backend.multiply(displacement_z, dt_over_dz)

    def update_position(self, position_in_cell, displacement):
        self.particles.backend.add(position_in_cell, displacement)

    def update_cell_origin(self, cell_origin, position_in_cell):
        floor_of_position = self.temp[:position_in_cell.shape[0]]
        self.particles.backend.floor_out_of_place(floor_of_position, position_in_cell)
        self.particles.backend.add(cell_origin, floor_of_position)
        self.particles.backend.subtract(position_in_cell, floor_of_position)

    def boundary_condition(self, cell_origin):
        # TODO: hardcoded periodic
        # TODO: particles above the mesh
        self.particles.backend.column_modulo(cell_origin, self.grid)
