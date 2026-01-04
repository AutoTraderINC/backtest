def flatten_option_data(option_chain_data):
    """
    Flattens Alpaca option chain data (dictionary of OptionsSnapshot objects)
    into a list of flat dictionaries for Polars.
    """
    flat_records = []

    for symbol, snapshot in option_chain_data.items():
        # Initialize record with basic fields from the snapshot object attributes
        record = {
            "symbol": symbol,
            "implied_volatility": snapshot.implied_volatility,
        }

        # Flatten Greeks (delta, gamma, rho, theta, vega)
        if snapshot.greeks:
            # vars() extracts the attributes into a dictionary
            greeks_data = vars(snapshot.greeks)
            for k, v in greeks_data.items():
                record[f"greek_{k}"] = v

        # Flatten Latest Quote
        if snapshot.latest_quote:
            quote_data = vars(snapshot.latest_quote)
            for k, v in quote_data.items():
                if k != "symbol":  # Avoid redundant symbol column
                    record[f"quote_{k}"] = v

        # Flatten Latest Trade
        if snapshot.latest_trade:
            trade_data = vars(snapshot.latest_trade)
            for k, v in trade_data.items():
                if k != "symbol":  # Avoid redundant symbol column
                    record[f"trade_{k}"] = v

        flat_records.append(record)

    return flat_records
