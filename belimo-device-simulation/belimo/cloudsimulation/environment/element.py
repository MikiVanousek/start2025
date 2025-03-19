import abc


class Element(abc.ABC):

    def __init__(self, timestep: float = 1.0, **kwargs):
        """
        Args:
        timestep: basis timestep in seconds
        """
        self.timestep = timestep
        self.time = 0.0

    def update_states(self, **kwargs) -> None:
        return None

    @abc.abstractmethod
    def step(self, **kwargs) -> dict[str, float]:
        return kwargs

    def forward(self, **kwargs) -> dict[str, float]:
        out = self.step(**kwargs)
        self.update_states(**kwargs)
        self.time = self.time + self.timestep
        return kwargs | out

    def __call__(self, **kwargs) -> dict[str, float]:
        return self.forward(**kwargs)
