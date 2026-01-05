"""Earnings play strategy: Buy 2 weeks before earnings, sell day before."""

from datetime import timedelta
from typing import Dict

import pandas as pd

from strategies.base import BaseStrategy


class EarningsPlayStrategy(BaseStrategy):
    """Buy 2 weeks before earnings, sell day before earnings."""

    def __init__(self):
        super().__init__(
            name="Earnings Play",
            description="Buy 14 days before earnings, sell 1 day before"
        )

    def execute(self, data: pd.DataFrame, amount: float) -> Dict:
        """
        Execute earnings play strategy.
        
        Note: Divides investment equally across all earnings cycles.
        """

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

        # Get ticker symbol from data (need to fetch earnings)
        # Try to infer ticker or use a passed parameter
        # For now, we'll work with the data we have

        # Get earnings dates from the data range
        # yfinance provides earnings dates via the calendar property
        ticker_symbol = None

        # Since we don't have direct access to ticker symbol from data,
        # we need to get it another way. Let's add it as a note that
        # this requires the ticker to be passed or stored.

        # For this implementation, we'll simulate earnings quarters
        # Typically earnings are ~quarterly (every ~90 days)
        # This is a simplified approach

        start_date = data['Date'].min()
        end_date = data['Date'].max()

        # Simulate quarterly earnings (every 90 days)
        # In practice, you'd use: ticker.calendar or ticker.earnings_dates
        earnings_dates = []
        current = start_date
        while current <= end_date:
            current += timedelta(days=90)
            if current <= end_date:
                earnings_dates.append(current)

        if len(earnings_dates) == 0:
            # If no earnings in range, return no trades
            return {
                'shares': 0,
                'total_cost': 0,
                'final_value': 0,
                'transactions': [],
                'gain_pct': 0,
                'gain_amount': 0
            }

        # Divide amount across all earnings cycles
        amount_per_cycle = amount / len(earnings_dates)

        transactions = []
        total_profit = 0
        total_cost = 0

        for earnings_date in earnings_dates:
            # Buy date: 14 days before earnings
            buy_target = earnings_date - timedelta(days=14)
            # Sell date: 1 day before earnings
            sell_target = earnings_date - timedelta(days=1)

            # Find closest trading day for buy
            buy_candidates = data[data['Date'] <= buy_target].copy()
            if len(buy_candidates) == 0:
                continue
            buy_row = buy_candidates.iloc[-1]

            # Find closest trading day for sell
            sell_candidates = data[
                (data['Date'] >= buy_row['Date']) &
                (data['Date'] <= sell_target)
            ].copy()
            if len(sell_candidates) == 0:
                continue
            sell_row = sell_candidates.iloc[-1]

            # Execute trade
            buy_price = buy_row['Close']
            sell_price = sell_row['Close']
            shares = amount_per_cycle / buy_price
            proceeds = shares * sell_price

            transactions.append({
                'date': buy_row['Date'],
                'type': 'BUY',
                'price': buy_price,
                'shares': shares,
                'cost': amount_per_cycle
            })

            transactions.append({
                'date': sell_row['Date'],
                'type': 'SELL',
                'price': sell_price,
                'shares': shares,
                'cost': proceeds
            })

            total_cost += amount_per_cycle
            total_profit += (proceeds - amount_per_cycle)

        # All positions are closed
        final_value = total_cost + total_profit

        # Calculate metrics
        metrics = self.calculate_metrics(total_cost, final_value)

        return {
            'shares': 0,  # All sold
            'total_cost': total_cost,
            'final_value': final_value,
            'transactions': transactions,
            **metrics
        }
