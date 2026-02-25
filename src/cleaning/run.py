from __future__ import annotations

from pathlib import Path
import pandas as pd

from .clean_results import clean_election_results
from .quality_report import build_quality_report


ROOT = Path(__file__).resolve().parents[2]
RAW_PATH = ROOT / "data" / "raw" / "election_results.csv"
CLEAN_DIR = ROOT / "data" / "clean"
REPORTS_DIR = ROOT / "reports"


def main() -> None:
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    raw_df = pd.read_csv(
    RAW_PATH,
    engine="python",
    quotechar='"',
    escapechar="\\",
)
    clean_df = clean_election_results(raw_df)

    clean_csv = CLEAN_DIR / "election_results_clean.csv"
    clean_parquet = CLEAN_DIR / "election_results_clean.parquet"
    report_path = REPORTS_DIR / "quality_report.md"

    clean_df.to_csv(clean_csv, index=False)
    clean_df.to_parquet(clean_parquet, index=False)

    report_md = build_quality_report(raw_df, clean_df)
    report_path.write_text(report_md, encoding="utf-8")

    print(f"Wrote: {clean_csv}")
    print(f"Wrote: {clean_parquet}")
    print(f"Wrote: {report_path}")


if __name__ == "__main__":
    main()