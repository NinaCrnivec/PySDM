from PySDM.mesh import Mesh
from PySDM.particles_builder import ParticlesBuilder


class Box:
    def __init__(self, _: ParticlesBuilder, dt, dv=None):
        self.dt = dt
        self.mesh = Mesh.mesh_0d(dv)

    def ante_step(self): pass
    def post_step(self): pass