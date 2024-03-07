from dataclasses import dataclass
from typing import Literal


@dataclass
class Order:
    """ Order class to represent an order to be traded """
    type: Literal["bid", "order"]
    quantity: int
    price: float

    def __post_init__(self):
        if self.type not in ["bid", "order"]:
            raise ValueError("Type must be either 'bid' or 'order'")
        if self.quantity < 1:
            raise ValueError("Quantity must be greater than 0")
        if self.price < 0:
            raise ValueError("Price must be greater than or equal to 0")

    def json(self) -> dict:
        return {
            'type': self.type,
            'quantity': self.quantity,
            'price': self.price,
        }
