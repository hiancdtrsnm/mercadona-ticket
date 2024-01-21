from dataclasses import dataclass
from datetime import datetime

from mercadona.product import Product


@dataclass(frozen=True)
class Ticket:
    bought_at: datetime
    products: list[Product]
