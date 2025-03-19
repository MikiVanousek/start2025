import time
import sys


class Simulation:
    """Docstring for Simulation. """

    importer = staticmethod(__import__)

    def __init__(self,
                 run_in_real_time: bool = False,
                 timestep: float = 1.0,
                 elements: dict[str, dict] = dict(),
                 ic: dict[str, float] = dict(),
                 **kwargs):
        """
        Args:
        timestep: basic timestep in seconds
        elements: ordered list of elements to run.
        """
        self.run_in_real_time = run_in_real_time
        self.timestep = timestep
        self.elements = [
                self._resolve(cls)(timestep=timestep, **cfg)
                for cls, cfg in elements.items()]
        self.state = ic

    def run_simulation(self) -> None:
        state = self.state
        for e in self.elements:
            state = e(**state)
        self.state = state

    def run(self) -> None:
        while True:
            if self.run_in_real_time:
                start = time.time()
                self.run_simulation()
                stop = time.time()
                time.sleep(max(self.timestep - (stop - start), 0.0))
            else:
                self.run_simulation()

    def _resolve(self, s: str):
        """
        Resolve strings to objects using standard import and attribute
        syntax.
        -- copied from lib/logging/config
        """
        name = s.split('.')
        used = name.pop(0)
        try:
            found = self.importer(used)
            for frag in name:
                used += '.' + frag
                try:
                    found = getattr(found, frag)
                except AttributeError:
                    self.importer(used)
                    found = getattr(found, frag)
            return found
        except ImportError:
            e, tb = sys.exc_info()[1:]
            v = ValueError('Cannot resolve %r: %s' % (s, e))
            v.__cause__, v.__traceback__ = e, tb
            raise v
