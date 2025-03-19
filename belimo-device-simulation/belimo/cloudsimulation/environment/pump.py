import numpy as np

from belimo.cloudsimulation.environment.element import Element


class Pump(Element):
    """
    Basic simulation of a pump
    """

    def __init__(self,
                 pressure_level: float = 100000.0,
                 pressure_amplitude: float = 0.0,
                 pressure_frequency: float = 0.0,
                 **kwargs):
        super(Pump, self).__init__(**kwargs)
        self.pressure_level = pressure_level
        self.pressure_amplitude = pressure_amplitude
        self.pressure_frequency = pressure_frequency
        self.pressure = self.pressure_level

    def update_states(self, **kwargs):
        self.pressure = self.pressure_level \
            + self.pressure_amplitude * np.sin(
                2 * np.pi
                * self.pressure_frequency * self.time)

    def step(self, **kwargs) -> dict[str, float]:
        return dict(pressure=self.pressure)
