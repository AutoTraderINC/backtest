"""Intraday trading strategy: Buy at 4PM, sell at 9AM next day."""

import pandas as pd
from typing import Dict
from strategies.base import BaseStrategy

class IntradayStrategy(BaseStrategy):
    """Buy at market close (4PM), sell at market open (9:30AM) next day."""
    
    def __init__(self):
        super().__init__(
            name="Intraday (4PM-9AM)",
            description="Buy at close, sell at next open"
        )
    
    def execute(self, data: pd.DataFrame, amount: float) -> Dict:
        """
        Execute intraday strategy.
        
        Note: Uses Close price as buy (4PM) and next day's Open as sell (9:30AM).
        Amount is reinvested each day.
        """
        data = data.copy()
        data['Date'] = pd.to_datetime(data['Date'])
        
        if len(data) < 2:
            return {
                'shares': 0,
                'total_cost': 0,
                'final_value': 0,
                'transactions': [],
                'gain_pct': 0,
                'gain_amount': 0
            }
        
        transactions = []
        current_amount = amount
        
        # Trade each day except the last
        for i in range(len(data) - 1):
            buy_row = data.iloc[i]
            sell_row = data.iloc[i + 1]
            
            buy_price = buy_row['Close']  # 4PM
            sell_price = sell_row['Open']  # 9:30AM next day
            
            shares = current_amount / buy_price
            proceeds = shares * sell_price
            
            transactions.append({
                'date': buy_row['Date'],
                'type': 'BUY',
                'price': buy_price,
                'shares': shares,
                'cost': current_amount
            })
            
            transactions.append({
                'date': sell_row['Date'],
                'type': 'SELL',
                'price': sell_price,
                'shares': shares,
                'cost': proceeds
            })
            
            current_amount = proceeds
        
        # Calculate metrics
        final_value = current_amount
        metrics = self.calculate_metrics(amount, final_value)
        
        return {
            'shares': 0,  # All sold
            'total_cost': amount,
            'final_value': final_value,
            'transactions': transactions,
            **metrics
        }
