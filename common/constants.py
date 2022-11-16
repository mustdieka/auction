from enum import Enum


class Status(Enum):
    SOLD = 1
    UNSOLD = 2


SELL_ACTION = "SELL"
BID_ACTION = "BID"
SOLD_LITERAL = "SOLD"
UNSOLD_LITERAL = "UNSOLD"

DEFAULT_PRICE_PAID = 0.00
