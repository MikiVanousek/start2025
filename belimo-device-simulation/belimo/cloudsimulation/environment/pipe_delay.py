from collections import deque

from belimo.cloudsimulation.environment.element import Element


class PipeDelay(Element):
    """
    Basic simulation of a pipe
    """

    def __init__(self,
                 pipe_delay: int = 0,
                 **kwargs):
        super(PipeDelay, self).__init__(**kwargs)
        self.queue = deque(maxlen=pipe_delay)

    def update_states(self, **kwargs) -> None:
        self.queue.append(kwargs)

    def step(self, **kwargs) -> dict[str, float]:
        # startup behaviour: if the queue is not yet full, just pass
        if len(self.queue) < self.queue.maxlen:
            return kwargs
        else:
            return self.queue.pop()
