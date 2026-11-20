"""Rebuild every strategy, the blend, the website data (docs/data/*.json) and README.md."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from daalab.pipeline import run_all  # noqa: E402

if __name__ == "__main__":
    run_all(sensitivity="--fast" not in sys.argv)
    import replication_check  # noqa: E402  (same folder)
    replication_check.main()
    import build_readme  # noqa: E402  (same folder)
    build_readme.main()
