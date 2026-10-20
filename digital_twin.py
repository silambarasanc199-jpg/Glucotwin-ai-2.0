"""A transparent in-memory view of the patient's stored static and dynamic data."""


def build_digital_twin(patient: dict, readings: list[dict]) -> dict:
    ordered = sorted(readings, key=lambda item: item["timestamp"])
    return {
        "patient": patient,
        "reading_count": len(ordered),
        "first_reading_at": ordered[0]["timestamp"] if ordered else None,
        "latest_reading_at": ordered[-1]["timestamp"] if ordered else None,
        "latest_reading": ordered[-1] if ordered else None,
        "data_sources": sorted({item["source"] for item in ordered}),
        "contains_synthetic_data": bool(patient.get("is_synthetic")) or any(
            bool(item.get("is_synthetic")) for item in ordered
        ),
    }
