import pandas as pd

from app.ml.generate_synthetic_data import generate


def test_synthetic_generator_is_reproducible_and_explicit(tmp_path):
    first = generate(tmp_path / "first.csv", patients=2, days=1)
    second = generate(tmp_path / "second.csv", patients=2, days=1)
    pd.testing.assert_frame_equal(first, second)
    assert len(first) == 2 * 96
    assert first["is_synthetic"].all()
    assert first.groupby("patient_id").size().eq(96).all()
