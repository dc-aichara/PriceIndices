from importlib.metadata import version

__version__ = version("PriceIndices")

from .crypto_history import MarketHistory
from .price_indicators import Indices
