import numpy as np

from belimo.cloudsimulation.environment.element import Element


class ValveActuator(Element):
    """
    Basic simulation of a Valve actuator
    KVs in m3/h for DN15 valve
    """

    def __init__(self,
                 closing_point: float = 0.05,
                 middle_point: float = 0.1,
                 valve_kvs: float = 2.5,
                 zone_kvs: float = 0.8,
                 valve_factor: float = 11.0,
                 valve_shift: float = 0.97,
                 factor: float = 40,
                 **kwargs):
        super(ValveActuator, self).__init__(**kwargs)
        self.closing_point = closing_point
        self.middle_point = middle_point
        self.valve_kvs = valve_kvs
        self.zone_kvs = zone_kvs
        self.valve_factor = valve_factor
        self.valve_shift = valve_shift
        self.factor = factor
        self.position = 0.0

    def _curve(self, position: float) -> float:
        return self.zone_kvs / (1 + self.zone_kvs**2 * np.sqrt(
            self.valve_kvs + np.exp(- self.valve_factor * (
                position - self.valve_shift))))

    def _compute_kvs(self) -> float:
        if self.position < self.closing_point:
            return 0.0
        elif self.position < self.middle_point:
            return self.position * (
                    self._curve(self.middle_point) / self.middle_point)
        else:
            return self._curve(self.position)

    def _compute_flow(self, pressure) -> float:
        return self.factor * self._compute_kvs() * np.sqrt(pressure / 100000.0) / 3600

    def update_states(self, valve_setpoint: float = 0.0, **kwargs):
        self.position = valve_setpoint

    def step(self,
             pressure: float = 0.0,
             valve_setpoint: float = 0.0,
             **kwargs) -> dict[str, float]:
        return dict(
            valve_position=self.position,
            flow=self._compute_flow(pressure))
