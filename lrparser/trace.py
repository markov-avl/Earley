from dataclasses import dataclass

from .configuration import Configuration


@dataclass
class Trace:
    step: int | float
    configuration: Configuration

    def __str__(self) -> str:
        if self.step > 0:
            return f'⊢ {self.step:<4}{self.configuration}'
        return f'{"":<6}{self.configuration}'
