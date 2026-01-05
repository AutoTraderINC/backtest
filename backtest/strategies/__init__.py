"""Trading strategy implementations."""

from strategies.base import BaseStrategy
from strategies.buy_once import BuyOnceStrategy
from strategies.dca_friday import DCAFridayStrategy
from strategies.earnings_play import EarningsPlayStrategy
from strategies.intraday import IntradayStrategy

# Available strategies
STRATEGIES = {
    "DCA Every Friday": DCAFridayStrategy(),
    "Buy All At Once": BuyOnceStrategy(),
    "Intraday (4PM-9AM)": IntradayStrategy(),
    "Earnings Play": EarningsPlayStrategy(),
}

__all__ = ["BaseStrategy", "STRATEGIES"]
