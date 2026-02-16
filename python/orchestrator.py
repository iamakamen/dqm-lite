import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from db import init_db, insert_run

DATA_DIR = Path("data")
METRICS_ENGINE = Path("cpp/build/metrics_engine")


def get_run_id_from_filename(path: Path) -> int:
    # run_001.csv -> 1
    stem = path.stem  # run_001
    _, num = stem.split("_")
    return int(num)


def process_run_file(path: Path):
    run_id = get_run_id_from_filename(path)

    result = subprocess.run(
        [str(METRICS_ENGINE), str(path)],
        capture_output=True,
        text=True,
        check=True,
    )

    metrics = json.loads(result.stdout)
    processed_at = datetime.now(timezone.utc).isoformat()

    insert_run(
        run_id=run_id,
        mean=metrics["mean"],
        stddev=metrics["stddev"],
        outlier_count=metrics["outlier_count"],
        status=metrics["status"],
        processed_at=processed_at,
    )

    print(f"Processed run {run_id}: {metrics['status']}")


def main():
    if not METRICS_ENGINE.exists():
        raise RuntimeError(f"Metrics engine not found at {METRICS_ENGINE}")

    init_db()

    csv_files = sorted(DATA_DIR.glob("run_*.csv"))
    if not csv_files:
        print("No run files found in data/.")
        return

    for path in csv_files:
        process_run_file(path)

    print("Orchestration complete.")


if __name__ == "__main__":
    main()
