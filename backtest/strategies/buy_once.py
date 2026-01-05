"""Buy all at once strategy."""

from typing import Dict

import pandas as pd

from strategies.base import BaseStrategy


class BuyOnceStrategy(BaseStrategy):
    """Buy all shares on the first day."""

    def __init__(self):
        super().__init__(
            name="Buy All At Once",
            description="Lump sum investment on first day"
        )

    def execute(self, data: pd.DataFrame, amount: float) -> Dict:
        """Execute buy-once strategy."""
        data = data.copy()
        data['Date'] = pd.to_datetime(data['Date'])

        if len(data) == 0:
            return {
                'shares': 0,
                'total_cost': 0,
                'final_value': 0,
                'transactions': [],
                'gain_pct': 0,
                'gain_amount': 0
            }

        # Buy on first day
        first_row = data.iloc[0]
        buy_price = first_row['Close']
        shares = amount / buy_price

        transactions = [{
            'date': first_row['Date'],
            'type': 'BUY',
            'price': buy_price,
            'shares': shares,
            'cost': amount
        }]

        # Calculate final value
        final_price = data.iloc[-1]['Close']
        final_value = shares * final_price

        # Calculate metrics
        metrics = self.calculate_metrics(amount, final_value)

        return {
            'shares': shares,
            'total_cost': amount,
            'final_value': final_value,
            'transactions': transactions,
            **metrics
        }
