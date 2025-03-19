import numpy as np
from belimo.cloudsimulation.environment.element import Element


class PIController(Element):

    """PIController with clamping."""

    def __init__(self,
                 tn: float = 0.0,
                 kp: float = 0.0,
                 initial_condition: float = 0.0,
                 lower_saturation: float = 0.0,
                 upper_saturation: float = 0.0,
                 control_signal_name: str = 'control',
                 **kwargs):
        super(PIController, self).__init__(**kwargs)
        self.integrator = initial_condition
        self.kp = kp
        self.tn = tn
        self.lower = lower_saturation
        self.upper = upper_saturation
        self.control_signal_name = control_signal_name

    def update_states(self, control_deviation: float = 0.0, **kwargs) -> None:
        p = self.kp * control_deviation
        i = 1 / self.tn * control_deviation * self.timestep
        if ((p + self.integrator) > self.upper) | ((p + self.integrator) < self.lower):
            # output would violate saturation, apply clamping
            if np.sign(i) != np.sign(control_deviation):
                # integration resumes
                self.integrator += i
        else:
            self.integrator += i

    def step(self, control_deviation: float = 0.0, **kwargs) -> dict[str, float]:
        return {self.control_signal_name: self.saturation(
            self.kp * control_deviation + self.integrator)}

    def saturation(self, signal) -> float:
        return max(min(signal, self.upper), self.lower)
