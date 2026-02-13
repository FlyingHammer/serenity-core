from app.risk.calculations import lot_size_for_risk, pip_size, pips_between


def test_pip_size_jpy_vs_non_jpy():
    assert pip_size("USDJPY") == 0.01
    assert pip_size("EURUSD") == 0.0001


def test_pips_between():
    assert pips_between("USDJPY", 150.0, 149.5) == 50
    assert pips_between("EURUSD", 1.1000, 1.0950) == 50


def test_lot_size_calc():
    lot = lot_size_for_risk(100000, 0.5, 50, 10)
    assert lot == 1.0
