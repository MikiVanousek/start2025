import numpy as np

from belimo.cloudsimulation.environment.element import Element


class SetpointSource(Element):
    """
    Basic simulation of a Setpoint
    """

    def __init__(self,
                 setpoint_level: float = 0.5,
                 setpoint_amplitude: float = 0.0,
                 setpoint_frequency: float = 0.0,
                 **kwargs):
        super(SetpointSource, self).__init__(**kwargs)
        self.setpoint_level = setpoint_level
        self.setpoint_amplitude = setpoint_amplitude
        self.setpoint_frequency = setpoint_frequency
        self.setpoint = self.setpoint_level

    def update_states(self, **kwargs):
        self.setpoint = self.setpoint_level \
            + self.setpoint_amplitude * np.sin(
                2 * np.pi
                * self.setpoint_frequency * self.time)

    def step(self, **kwargs) -> dict[str, float]:
        return dict(setpoint=self.setpoint)
