from enum import Enum

class CostFunction(Enum):
    SEG = 'seg'
    SSE = 'sse'
    MASKED = 'masked'
    SMOOTH = 'smooth'
    L1 = "L1"
    WGAN = 'wgan'

    def __str__(self) -> str:
        return self.value
    
    def json(self) -> str:
        return str(self)