"""Small inference helper for application or notebook reuse."""

from app.services.prediction_service import load_bundle, make_prediction

__all__ = ["load_bundle", "make_prediction"]
