"""
Created at 05.02.2020
"""

from PySDM.product import Product
from PySDM.dynamics.condensation.condensation import Condensation


class RipeningRate(Product):

    def __init__(self):
        super().__init__(
            name='ripening_rate',
            description='ripening rate'
        )
        self.condensation = None

    def register(self, builder):
        super().register(builder)
        self.condensation = self.core.dynamics[str(Condensation)]

    def get(self):  # TODO: take into account NUMBER of substeps (?)
        self.download_to_buffer(self.condensation.ripening_flags)
        self.condensation.ripening_flags[:] = 0
        return self.buffer
