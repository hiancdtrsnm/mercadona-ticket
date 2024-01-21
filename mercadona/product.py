from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    name: str
    quantity: int
    price: float
