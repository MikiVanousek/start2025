from belimo.cloudsimulation.devices.device import Device
from belimo.cloudsimulation.control.pi import PIController


class EnergyValve(Device):
    """Basic simulation of an EnergyValve"""

    data_profile: dict = Device.data_profile | {
        'DifferentialWaterTemperatureSetpoint': 'float',
        'DifferentialWaterTemperatureControlStatus': 'int',
        'DifferentialTemperatureManagerActiveHours': 'int',
        'DifferentialTemperatureManagerDisabledHours': 'int',
        'DifferentialTemperatureManagerStandbyHours': 'int',
        'DifferentialWaterTemperature': 'float',
        'EnableDifferentialTemperatureManagerMinimumWaterFlow': 'bool',
        'GlycolConcentration': 'float',
        'AbsoluteActuatorPosition': 'float',
        'AbsoluteCoolingPower': 'float',
        'AbsoluteHeatingPower': 'float',
        'AbsolutePower': 'float',
        'AbsoluteWaterFlow': 'float',
        'AccumulatedVolumeSensorReading': 'float',
        'AppliedSetpoint': 'float',
        'CoolingEnergy': 'float',
        'CoolingEnergyLifetime': 'float',
        'CoolingEnergyMeterReading': 'float',
        'HeatingEnergy': 'float',
        'HeatingEnergyLifetime': 'float',
        'HeatingEnergyMeterReading': 'float',
        'NominalPower': 'float',
        'RelativeActuatorPosition': 'float',
        'RelativeActuatorPositionSetpoint': 'float',
        'RelativePower': 'float',
        'RelativeWaterFlow': 'float',
        'RelativePowerSetpoint': 'float',
        'RelativeWaterFlowSetpoint': 'float',
        'FlowBodyWaterTemperature': 'float',
        'RemoteWaterTemperature': 'float',
        'SelectSetpointSource': 'int',
        'SelectWaterMediumType': 'int',
        'SelectWaterControlMode': 'int',
        'SelectWaterFlowControlCharacteristic': 'int',
        "SetDifferentialTemperatureManagerMinimumWaterFlow": 'float',
        "SetDifferentialTemperatureManagerRelativeMinimumWaterFlow": 'float',
        "SetDifferentialTemperatureManagerScaledSaturationRelativeWaterFlow": 'float',  # noqa 501
        "SetDifferentialTemperatureManagerScaledSaturationWaterFlow": 'float',
        "SetDifferentialWaterTemperature": 'float',
        'SetMaximumPower': 'float',
        'SetMaximumWaterFlow': 'float',
        'SetRelativeSetpoint': 'float',
        'SetWaterDeviceInstallationPosition': 'int',
        'WaterDeviceDnSize': 'int',
        'MasterDeviceErrorStatus': 'int',
        "WaterFlowVolume": 'float',
        "WaterFlowVolumeLifetime": 'float'}

    def __init__(self,
                 settings: dict = {
                    "DifferentialWaterTemperatureSetpoint": 0.0,
                    'DifferentialWaterTemperatureControlStatus': 0,
                    'EnableDifferentialTemperatureManagerMinimumWaterFlow': False,  # noqa 501
                    'NominalPower': 880000.0,
                    'NominalWaterFlow': 0.00416666,
                    'SelectSetpointSource': 1,
                    'SelectWaterMediumType': 0,
                    'SelectWaterControlMode': 1,
                    'SelectWaterFlowControlCharacteristic': 0,
                    "SetDifferentialTemperatureManagerMinimumWaterFlow": 0.0030555556,  # noqa 501
                    "SetDifferentialTemperatureManagerRelativeMinimumWaterFlow": 73.33345173,  # noqa 501
                    "SetDifferentialTemperatureManagerScaledSaturationRelativeWaterFlow": 100.0,  # noqa 501
                    "SetDifferentialTemperatureManagerScaledSaturationWaterFlow": 0.00416666,  # noqa 501
                    "SetDifferentialWaterTemperature": 20.0,
                    'SetMaximumPower': 256000.0,
                    'SetMaximumWaterFlow': 0.0030555556,
                    'SetWaterDeviceInstallationPosition': '1',
                    'WaterDeviceDnSize': '5'},
                 sensor_values: dict = {
                    'AppliedSetpoint': 'setpoint_percent',
                    'DifferentialWaterTemperature': 'dt',
                    'GlycolConcentration': 'glycol_conc',
                    'AbsoluteActuatorPosition': 'absolute_valve_position',
                    'AbsoluteWaterFlow': 'flow',
                    'AbsoluteCoolingPower': 'cooling_power',
                    'AbsoluteHeatingPower': 'heating_power',
                    'AbsolutePower': 'absolute_power',
                    'FlowBodyWaterTemperature': 'return_water_temperature',
                    'RelativeActuatorPosition': 'valve_position_percent',
                    'RelativeActuatorPositionSetpoint': 'valve_setpoint_percent',  # noqa 501
                    'RelativePower': 'relative_power_percent',
                    'RelativeWaterFlow': 'relative_flow_percent',
                    'RelativePowerSetpoint': 'setpoint_percent',
                    'RelativeWaterFlowSetpoint': 'setpoint_percent',
                    'RemoteWaterTemperature': 'supply_water_temperature',
                    'SetRelativeSetpoint': 'setpoint_percent',
                    'MasterDeviceErrorStatus': 'status'},
                 accumulator_values: dict = {
                    'DifferentialTemperatureManagerActiveHours': 'dtactive_hour_counter',  # noqa 501
                    'DifferentialTemperatureManagerDisabledHours': 'dtdisabled_hour_counter',  # noqa 501
                    'DifferentialTemperatureManagerStandbyHours': 'dtstandby_hour_counter',  # noqa 501
                    'CoolingEnergy': 'cooling_power_integral',
                    'CoolingEnergyLifetime': 'cooling_power_integral',
                    'CoolingEnergyMeterReading': 'cooling_power_integral',
                    'AccumulatedVolumeSensorReading': 'flow_integral',
                    'HeatingEnergy': 'heating_power_integral',
                    'HeatingEnergyLifetime': 'heating_power_integral',
                    'HeatingEnergyMeterReading': 'heating_power_integral',
                    "WaterFlowVolume": 'flow_integral',
                    "WaterFlowVolumeLifetime": 'flow_integral'},
                 accumulators: dict = {
                    'dtactive': 'hour_counter',
                    'dtdisables': 'hour_counter',
                    'dtstandby': 'hour_counter',
                    'cooling_power': 'integral',
                    'heating_power': 'integral',
                    'flow': 'integral'},
                 **kwargs):
        super(EnergyValve, self).__init__(
                settings=settings,
                sensor_values=sensor_values,
                accumulator_values=accumulator_values,
                accumulators=accumulators,
                **kwargs)
        self.vnom = self.settings['NominalWaterFlow']
        self.vmax = self.settings['SetMaximumWaterFlow'] / self.vnom
        self.pnom = self.settings['NominalPower']
        self.pmax = self.settings['SetMaximumPower'] / self.pnom
        self.base_dt = ((self.pmax * self.pnom) /
                        (self.vmax * self.vnom * 4184.0 * 1000.0))
        self.flow_controller = \
            PIController(
                tn=25.0,
                kp=0.0,
                lower_saturation=0.0,
                upper_saturation=1.0,
                control_signal_name='valve_setpoint')

    def measure(self,
                supply_water_temperature: float = 273.15,
                return_water_temperature: float = 273.15,
                flow: float = 0.0,
                valve_position: float = 0.0,
                setpoint: float = 0.0,
                valve_setpoint: float = 0.0,
                **kwargs) -> dict[str, float]:
        dt = supply_water_temperature - return_water_temperature
        # flow relative to vnom
        flow_rel_vnom = flow / self.vnom
        relative_flow = flow_rel_vnom / self.vmax
        relative_power = relative_flow * dt / self.base_dt
        error = setpoint * self.vmax - flow_rel_vnom
        return dict(
            dtactive=False,
            dtdisabled=True,
            dtstandby=False,
            dt=abs(dt),
            relative_flow=relative_flow,
            relative_flow_percent=relative_flow * 100,
            valve_position_percent=valve_position * 100,
            valve_setpoint_percent=valve_setpoint * 100,
            setpoint_percent=setpoint * 100,
            glycol_conc=10.0,
            absolute_valve_position=valve_position * 90.0,
            cooling_power=abs(
                min(relative_power, 0.0) * self.pmax * self.pnom),
            heating_power=abs(
                max(relative_power, 0.0) * self.pmax * self.pnom),
            absolute_power=abs(relative_power) * self.pmax * self.pnom,
            relative_power=abs(relative_power),
            relative_power_percent=abs(relative_power) * 100,
            control_deviation=error,
            status=0)

    def control(self, **kwargs) -> dict[str, float]:
        # apply flow control only for the moment
        return self.flow_controller(**kwargs)
