import unittest
import pandas as pd

from belimo.cloudsimulation.simulations.simulation import Simulation


class TestSimulation(unittest.TestCase):

    def setUp(self):
        env = 'belimo.cloudsimulation.environment.{Module}.{Class}'

        elements = {
            env.format(Module='heat_source', Class='HeatSource'): dict(),
            env.format(Module='setpoint_source', Class='SetpointSource'): dict(
                setpoint_level=0.5,
                setpoint_amplitude=0.5,
                setpoint_frequency=1/1800),
            env.format(Module='pump', Class='Pump'): dict(),
            env.format(Module='pipe_delay', Class='PipeDelay'): dict(
                pipe_delay=20),
            env.format(Module='heat_exchanger', Class='HeatExchanger'): dict(
                dt_max=12.0,
                dt_min=2.0,
                noise_level=0.1),
            env.format(Module='pipe_delay', Class='PipeDelay'): dict(
                pipe_delay=10),
            'belimo.cloudsimulation.devices.energyvalve.EnergyValve': dict(
                cloud_connected=False),
            env.format(Module='valve_actuator', Class='ValveActuator'): dict(),
        }

        self.simulation = Simulation(
            timestep=1.0,
            elements=elements,
            ic=dict(
                relative_flow=0.0,
                flow=0.0,
                valve_position=0.0,
                valve_setpoint=0.0))

    def test_simulation(self):

        steps = 5 * 60 * 60
        states = []

        for _ in range(0, steps):
            self.simulation.run_simulation()
            states.append(self.simulation.state)

        df = pd.DataFrame(states)

        self.assertTrue(df.shape[0] > 0)
