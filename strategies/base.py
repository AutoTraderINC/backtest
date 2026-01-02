"""Base strategy class for stock trading strategies."""

from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, List

class BaseStrategy(ABC):
    """Abstract base class for all trading strategies."""
    
    def __init__(self, name: str, description: str):
        """
        Initialize strategy.
        
        Args:
            name: Strategy name
            description: Brief description
        """
        self.name = name
        self.description = description
    
    @abstractmethod
    def execute(self, data: pd.DataFrame, amount: float) -> Dict:
        """
        Execute the trading strategy.
        
        Args:
            data: DataFrame with columns ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
            amount: Total investment amount in USD
            
        Returns:
            dict with keys:
                - shares: Total shares owned
                - total_cost: Total amount invested
                - final_value: Current portfolio value
                - transactions: List of transaction dicts
                - gain_pct: Percentage gain
                - gain_amount: Dollar gain
        """
        pass
    
    def calculate_metrics(self, total_cost: float, final_value: float) -> Dict:
        """Calculate performance metrics."""
        gain_amount = final_value - total_cost
        gain_pct = (gain_amount / total_cost * 100) if total_cost > 0 else 0
        
        return {
            'gain_amount': gain_amount,
            'gain_pct': gain_pct
        }
