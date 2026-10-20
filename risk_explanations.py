"""Plain-language signal descriptions; they are not clinical explanations."""


def observed_signals(readings: list[dict]) -> list[str]:
    if not readings:
        return ["No glucose readings are available."]
    ordered = sorted(readings, key=lambda item: item["timestamp"])
    latest = ordered[-1]
    signals = [f"Most recent measured glucose: {latest['glucose_mg_dl']:.0f} mg/dL."]
    if len(ordered) > 1:
        delta = latest["glucose_mg_dl"] - ordered[-2]["glucose_mg_dl"]
        direction = "increased" if delta > 0 else "decreased" if delta < 0 else "was unchanged"
        signals.append(f"Compared with the previous reading, glucose {direction} by {abs(delta):.0f} mg/dL.")
    if latest.get("heart_rate_bpm") is None:
        signals.append("Heart-rate context is missing for the latest reading.")
    if latest.get("sleep_hours") is None:
        signals.append("Sleep context is missing for the latest reading.")
    if latest.get("steps") is None:
        signals.append("Step-count context is missing for the latest reading.")
    return signals
