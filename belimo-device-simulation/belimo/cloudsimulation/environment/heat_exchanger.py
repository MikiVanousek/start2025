import numpy as np

from belimo.cloudsimulation.environment.element import Element


class HeatExchanger(Element):
    """
    Basic simulation of an heat exchanger based on the NTU model
    """

    def __init__(self,
                 dt_max: float = 10.0,
                 dt_min: float = 3.0,
                 noise_level: float = 0.0,
                 **kwargs):
        super(HeatExchanger, self).__init__(**kwargs)
        self.a = dt_max
        self.b = dt_max / dt_min - 1
        self.noise_level = noise_level

    def dt(self, relative_flow: float) -> float:
        return self.a / (1 + self.b * relative_flow)

    def return_water_temperature(self,
                                 relative_flow: float,
                                 supply_water_temperature: float) -> float:
        return supply_water_temperature + self.dt(relative_flow) + \
            np.random.normal(scale=self.noise_level)

    def step(self,
             relative_flow: float = 0.0,
             supply_water_temperature: float = 273.15,
             **kwargs) -> dict[str, float]:
        return dict(
            return_water_temperature=self.return_water_temperature(
                relative_flow, supply_water_temperature))
