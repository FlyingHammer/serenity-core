from app.models.schemas import MRSignal


def test_signal_serialization_contains_confidence_and_rule_values():
    sig = MRSignal(
        pair="EURUSD",
        timeframe="1H",
        state="WATCH",
        direction=None,
        entry_type=None,
        checklist={"x": True},
        rule_values={"cci": 120.0},
        confidence_score=50,
        confirmation_mode="close_confirm",
    )
    payload = sig.model_dump()
    assert "confidence_score" in payload
    assert "rule_values" in payload
