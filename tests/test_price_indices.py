from PriceIndices import Indices, MarketHistory

history = MarketHistory()

price_data = history.get_price("bitcoin", "2020-03-16", "2021-03-15")
indices = Indices(df=price_data, plot_dir="tests/plots")


def test_vola():
    df_bvol = indices.get_vola_index(
        plot=True, plot_name="vola_index.png", show_plot=False
    )

    assert df_bvol.shape == (334, 3)


def test_rsi():
    df_rsi = indices.get_rsi(
        plot=True,
        plot_name="rsi.png",
        show_plot=False,
    )
    assert df_rsi.shape == (363, 5)


def test_bollinger_bands():
    df_bb = indices.get_bollinger_bands(
        days=20,
        plot=True,
        plot_name="bollinger_bands.png",
        show_plot=False,
    )

    assert df_bb.shape == (364, 4)


def test_moving_average_convergence_divergence():
    df_macd = indices.get_moving_average_convergence_divergence(
        plot=True,
        plot_name="macd.png",
        show_plot=False,
    )
    assert df_macd.shape == (364, 3)


def test_simple_moving_average():
    df_sma = indices.get_simple_moving_average(
        days=20,
        plot=True,
        plot_name="sma.png",
        show_plot=False,
    )

    assert df_sma.shape == (345, 3)


def test_exponential_moving_average():
    df_ema = indices.get_exponential_moving_average(
        periods=(20, 70),
        plot=True,
        plot_name="ema.png",
        show_plot=False,
    )

    assert df_ema.shape == (364, 4)


def test_if_plots_saved():
    for plot_name in [
        "bollinger_bands",
        "sma",
        "vola_index",
        "ema",
        "macd",
        "rsi",
    ]:
        full_plot_path = indices.plot_dir.joinpath(f"{plot_name}.png")
        assert full_plot_path.exists() == 1
        # Clean plots folder: Remove all saved plot
        full_plot_path.unlink()
