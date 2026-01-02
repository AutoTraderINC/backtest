"""DCA (Dollar Cost Averaging) every Friday strategy."""

import pandas as pd
from typing import Dict
from strategies.base import BaseStrategy

class DCAFridayStrategy(BaseStrategy):
    """Buy fixed amount every Friday."""
    
    def __init__(self):
        super().__init__(
            name="DCA Every Friday",
            description="Invest equal amounts every Friday"
        )
    
    def execute(self, data: pd.DataFrame, amount: float) -> Dict:
        """Execute DCA Friday strategy."""
        # Filter for Fridays (weekday 4)
        data = data.copy()
        data['Date'] = pd.to_datetime(data['Date'])
        data['Weekday'] = data['Date'].dt.weekday
        fridays = data[data['Weekday'] == 4].copy()
        
        if len(fridays) == 0:
            return {
                'shares': 0,
                'total_cost': 0,
                'final_value': 0,
                'transactions': [],
                'gain_pct': 0,
                'gain_amount': 0
            }
        
        # Calculate amount per Friday
        num_fridays = len(fridays)
        amount_per_buy = amount / num_fridays
        
        # Execute purchases
        transactions = []
        total_shares = 0
        total_cost = 0
        
        for _, row in fridays.iterrows():
            price = row['Close']
            shares = amount_per_buy / price
            total_shares += shares
            total_cost += amount_per_buy
            
            transactions.append({
                'date': row['Date'],
                'type': 'BUY',
                'price': price,
                'shares': shares,
                'cost': amount_per_buy
            })
        
        # Calculate final value
        final_price = data.iloc[-1]['Close']
        final_value = total_shares * final_price
        
        # Calculate metrics
        metrics = self.calculate_metrics(total_cost, final_value)
        
        return {
            'shares': total_shares,
            'total_cost': total_cost,
            'final_value': final_value,
            'transactions': transactions,
            **metrics
        }
