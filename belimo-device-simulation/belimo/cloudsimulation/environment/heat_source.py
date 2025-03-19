import numpy as np

from belimo.cloudsimulation.environment.element import Element


class HeatSource(Element):
    """
    Basic simulation of a heat source
    """

    def __init__(self,
                 supply_water_temperature_level: float = 288.0,
                 supply_water_temperature_amplitude: float = 0.0,
                 supply_water_temperature_frequency: float = 0.0,
                 **kwargs):
        super(HeatSource, self).__init__(**kwargs)
        self.supply_water_temperature_level = supply_water_temperature_level
        self.supply_water_temperature_amplitude = \
            supply_water_temperature_amplitude
        self.supply_water_temperature_frequency = \
            supply_water_temperature_frequency
        self.temperature = self.supply_water_temperature_level

    def update_states(self, **kwargs):
        self.temperature = self.supply_water_temperature_level \
            + self.supply_water_temperature_amplitude * np.sin(
                2 * np.pi
                * self.supply_water_temperature_frequency * self.time)

    def step(self, **kwargs) -> dict[str, float]:
        return dict(supply_water_temperature=self.temperature)
