"""Print the held-out metrics produced by the reproducible training command."""

import json

from app.config import evaluation_path


def main() -> None:
    path = evaluation_path()
    if not path.exists():
        raise SystemExit(f"Evaluation report not found at {path}. Run: python -m app.ml.train")
    report = json.loads(path.read_text(encoding="utf-8"))
    print(json.dumps({"selected_model": report["selected_model"],
                      "test_metrics_at_threshold_0_5": report["test_metrics_at_threshold_0_5"]}, indent=2))


if __name__ == "__main__":
    main()
