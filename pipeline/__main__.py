import sys

from pipeline.run_market_snapshot import run_snapshot_pipeline
from pipeline.run_market_timeseries import run_timeseries_pipeline

def main() :
    if len(sys.argv) < 2 :
        print(
            "Usage:\n"
            " python -m pipeline snapshot\n"
            " python -m pipeline timeseries"
        )
        sys.exit(1)

    mode = sys.argv[1].lower()

    if mode == "snapshot" :
        run_snapshot_pipeline()

    elif mode == "timeseries" :
        run_timeseries_pipeline()
    else :
        print(f"Unknown pipeline mode: {mode}")
        sys.exit(1)

if __name__ == "__main__" :
    main()