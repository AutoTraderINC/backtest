# Stock EDA - Exploratory Data Analysis Tool

A modular Python tool for stock market analysis with customizable trading strategies.

## Features

- **Interactive UI**: Simple Jupyter notebook interface with widgets
- **Multiple Strategies**: DCA, lump sum, intraday trading
- **Modular Design**: Easy to add custom strategies
- **Visual Analytics**: Stock price charts and performance metrics
- **Real Data**: Uses yfinance for historical stock data

## Quick Start

```bash
# Run setup (installs uv, creates venv, installs dependencies)
python setup.py

# Activate environment
source .venv/bin/activate

# Start Jupyter
jupyter notebook

# Open nbs/stock_analysis.ipynb and select 'stock-eda' kernel

# Optional: Lint and format code
uv run ruff check . --fix  # Fix linting issues
uv run ruff format .       # Format all files
```

## Project Structure
```
backtest/
├── backtest/
│   ├── strategies/      # Trading strategy modules
│   │   ├── __init__.py
│   │   ├── base.py     # Base strategy class
│   │   └── ...
│   └── data/           # Data storage
├── nbs/
│   └── stock_analysis.ipynb # Main notebook with UI
├── utils/              # Utility functions
├── setup.py            # Environment setup script
├── pyproject.toml      # Dependencies
└── README.md
```

## Usage

1. Open `nbs/stock_analysis.ipynb` in Jupyter
2. Run all cells to display the UI
3. Enter:
   - **Ticker**: Stock symbol (e.g., AAPL, MSFT)
   - **Start/End Date**: Date range for analysis
   - **Amount**: Investment amount in USD
   - **Strategy**: Select from dropdown
4. Click "Analyze" to see results

## Adding Custom Strategies

Create a new file in `backtest/strategies/` inheriting from `BaseStrategy`:

```python
from backtest.strategies.base import BaseStrategy
import pandas as pd

class MyStrategy(BaseStrategy):
    """Your custom strategy."""
    
    def execute(self, data: pd.DataFrame, amount: float) -> dict:
        # Implement your logic
        return {
            'shares': shares_bought,
            'total_cost': total_spent,
            'final_value': current_value,
            'transactions': transaction_list
        }
```

Register in `backtest/strategies/__init__.py` and the notebook will automatically detect it.

## Requirements

- Python 3.10+
- uv (installed automatically by setup.py)

## Dependencies

- yfinance: Stock data
- pandas/numpy: Data processing
- matplotlib: Visualization
- ipywidgets: Interactive UI
- jupyter: Notebook environment
