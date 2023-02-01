from PriceIndices import MarketHistory


def test_history_market_data():
    history = MarketHistory()
    df_history = history.get_history("bitcoin", "2020-03-16", "2021-03-15")
    assert df_history.shape == (364, 7)

    price_data = history.get_price("bitcoin", "2020-03-16", "2021-03-15")

    assert price_data.shape == (364, 2)
