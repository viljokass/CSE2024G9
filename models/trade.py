from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Trade:
    """ Trade class to represent a made trade """
    quantity: int
    price: float
    time: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if self.quantity < 1:
            raise ValueError("Quantity must be greater than 0")
        if self.price < 0:
            raise ValueError("Price must be greater than or equal to 0")

    def json(self) -> dict:
        return {
            'quantity': self.quantity,
            'price': self.price,
            'time': self.time
        }

