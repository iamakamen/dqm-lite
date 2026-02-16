import os
import numpy as np

DATA_DIR = "data"
NUM_RUNS = 20
EVENTS_PER_RUN = 1000
ANOMALY_RUNS = {5, 12, 17}  # runs with injected anomalies


def generate_run(run_id: int):
    """Generate a single run of synthetic data."""
    # Normal distribution for good runs
    mean = 0
    std = 1

    # Inject anomalies
    if run_id in ANOMALY_RUNS:
        mean = 4       # shifted mean
        std = 2        # higher variance

    values = np.random.normal(mean, std, EVENTS_PER_RUN)

    # Save to CSV
    filename = os.path.join(DATA_DIR, f"run_{run_id:03d}.csv")
    np.savetxt(filename, values, delimiter=",")

    print(f"Generated {filename}")


def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    for run_id in range(1, NUM_RUNS + 1):
        generate_run(run_id)

    print("Data generation complete.")


if __name__ == "__main__":
    main()
