import abc
import requests as req
from requests.exceptions import HTTPError
import datetime

from belimo.cloudsimulation.environment.element import Element


class Device(Element):

    family_settings: dict = {
        'f4tkRaHd.7': 1,
        'SetSiteName': "",
        'SetProjecName': "TestDevice",
        'SetPlantIdentificationCode': 0,
        'SetCloudDatalogSampleInterval': 30,
        'SetCloudDatalogSendInterval': 300,
        "SetBuildingArea": "",
        "SetBuildingFloor": "",
        "SetBuildingName": "",
        "SetBuildingPart": "",
        "SetAddressCity": "Hinwil",
        "SetAddressCountry": "CH",
        "SetAddressNameLine1": "Brunnenbachstrasse 1",
        "SetAddressState": "ZH",
        "SetAddressZipCode": "8340",
        "OcWebUnitSettings": "default/Power:kilowatt, \
                default/WaterFlow:cubicMetrePerHour, \
                default/Temperature:celsius, \
                default/Energy:kilowattHour",
        "OemString": "My OEM name",
        "CloudConnected": True,
        "CloudPatchAvailable": False,
        "ApplyCloudPatches": True,
        "DeviceBelimoString": "EV050R2+MID",
        "DeviceMpAddress": 0,
        "DeviceMpSerialNumber": "22126-10004-022-182"}

    data_profile = {
        'f4tkRaHd.7': 'int',
        'SetSiteName': "str",
        'SetProjecName': "str",
        'SetPlantIdentificationCode': 'int',
        'SetCloudDatalogSampleInterval': 'int',
        'SetCloudDatalogSendInterval': 'int',
        "SetBuildingArea": "str",
        "SetBuildingFloor": "str",
        "SetBuildingName": "str",
        "SetBuildingPart": "str",
        "SetAddressCity": "str",
        "SetAddressCountry": "str",
        "SetAddressNameLine1": "str",
        "SetAddressState": "str",
        "SetAddressZipCode": "str",
        "OcWebUnitSettings": "str",
        "OemString": "str",
        "CloudConnected": 'bool',
        "CloudPatchAvailable": 'bool',
        "ApplyCloudPatches": 'bool',
        "DeviceBelimoString": "str",
        "DeviceMpAddress": 'int',
        "DeviceMpSerialNumber": 'str'}

    def __init__(self,
                 device_id: str = "",
                 certificate_file: str = "",
                 cloud_endpoint: str = "https://connect.g2bcc.com",
                 cloud_connected: bool = True,
                 owner: str = "",
                 reporting_interval: int = 30,
                 reporting_interval_full_sample: int = 24 * 60 * 2 * 30,
                 send_interval: int = 3 * 60,
                 settings: dict = dict(),
                 sensor_values: dict[str, str] = dict(),
                 accumulator_values: dict[str, str] = dict(),
                 accumulators: dict[str, str] = dict(),
                 debug: bool = False,
                 **kwargs):
        """
        Args:
        timestep: basis timestep in seconds
        """
        super(Device, self).__init__(**kwargs)
        self.device_id = device_id
        self.certificate_file = certificate_file
        self.cloud_connected = cloud_connected
        self.cloud_endpoint = cloud_endpoint
        self.reporting_interval = reporting_interval
        self.reporting_interval_full_sample = reporting_interval_full_sample
        self.send_interval = send_interval
        self.settings = settings
        self.sensor_values = sensor_values
        self.sample_buffer = []
        self.accumulator_values = accumulator_values
        self.accumulators = accumulators
        self.accumulator_states = dict()
        self.debug = debug
        self.full_state = dict()

    def take_sample(self, data: dict) -> None:
        # import pdb; pdb.set_trace()
        datapoint_values = dict()
        for key, dp_type in self.data_profile.items():
            value = data.get(key)
            if value is not None:
                if dp_type == 'bool':
                    value = bool(value)
                elif dp_type == 'int':
                    value = int(value)
                elif dp_type == 'float':
                    value = float(value)
                else:
                    value = str(value)
                datapoint_values.update({key: value})
        if not self.should_take_full_sample():
            # determine change
            change = dict()
            for key, val in datapoint_values.items():
                if self._has_value_changed(key, val):
                    change.update({key: val})
            datapoint_values = change
        # make sample
        sample = {
            'timestamp': self._current_time(),
            'data': datapoint_values}
        self.sample_buffer.append(sample)
        self.full_state.update(datapoint_values)

    def _has_value_changed(self, key, val):
        return ((len(self.sample_buffer) > 0)
                and key in self.full_state.keys()
                and self.full_state[key] != val) or (
                        key not in self.full_state.keys())

    def _current_time(self) -> int:
        return round(datetime.datetime.utcnow().timestamp() * 1000)

    def send_samples(self) -> None:
        data = dict(
            sendtime=self._current_time(),
            samples=self.sample_buffer)
        # send
        url = '{cloud}/device-api/v2/devices/{device}/data'.format(
                cloud=self.cloud_endpoint,
                device=self.device_id)
        # import pdb; pdb.set_trace()
        if self.debug:
            print('About to send {data} to {url}'.format(
                data=str(data), url=url))
        # headers = {'Content-Type': 'application/json'}
        r = req.post(url=url, json=data, cert=self.certificate_file)
        try:
            r.raise_for_status()
            self.sample_buffer = []
        except HTTPError as e:
            print('Status code: {}, error {}'.format(
                r.status_code,
                r.text))
            raise e

    def collect_sensor_values(self, **kwargs) -> dict[str, float]:
        return {
            key: kwargs[name]
            for key, name in self.sensor_values.items()
            if name in kwargs.keys()} | {
            key: self.accumulator_states[name]
            for key, name in self.accumulator_values.items()
            if name in self.accumulator_states.keys()}

    def collect_settings(self) -> dict:
        return self.family_settings | self.settings

    def is_integer_multiple(self, t):
        return self.time / t == self.time // t

    def should_take_full_sample(self) -> bool:
        return self.is_integer_multiple(self.reporting_interval_full_sample)

    def should_take_sample(self) -> bool:
        if self.debug:
            print('Current time: {}'.format(self.time))
            print('Reporting interval: {}'.format(self.reporting_interval))
        return self.is_integer_multiple(self.reporting_interval)

    def should_send_samples(self) -> bool:
        return self.cloud_connected & self.is_integer_multiple(
                self.send_interval)

    def update_states(self, **kwargs) -> None:
        for key, method in self.accumulators.items():
            state_key = '{}_{}'.format(key, method)
            if state_key not in self.accumulator_states.keys():
                if key in kwargs.keys():
                    self.accumulator_states.update(dict(state_key=kwargs[key]))
            else:
                last_value = self.accumulator_states[state_key]
                current_value = kwargs.get(key, 0.0)
                if method == 'max':
                    new_value = max(last_value, current_value)
                elif method == 'min':
                    new_value = min(last_value, current_value)
                elif method == 'sum':
                    new_value = last_value + current_value
                elif method == 'counter':
                    new_value = last_value + 1
                elif method == 'integral':
                    new_value = last_value + current_value * self.timestep
                elif method == 'hour_counter':
                    if current_value:
                        new_value = current_value + self.timesstep / (60 * 60)
                else:
                    raise Exception(
                        "accumulation method {} not supported".format(method))
                self.accumulator_states.update(dict(state_key=new_value))

    def step(self, **kwargs) -> dict[str, float]:
        kwargs = kwargs | self.measure(**kwargs)
        kwargs = kwargs | self.control(**kwargs)
        if self.should_take_sample():
            self.take_sample(
                self.collect_sensor_values(**kwargs)
                | self.collect_settings())
        if self.should_send_samples():
            self.send_samples()
        return kwargs

    @abc.abstractmethod
    def measure(self, **kwargs) -> dict[str, float]:
        return kwargs

    @abc.abstractmethod
    def control(self, **kwargs) -> dict[str, float]:
        return kwargs
