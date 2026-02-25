from __future__ import annotations

import pandas as pd


def build_quality_report(raw_df: pd.DataFrame, clean_df: pd.DataFrame) -> str:
    def missing_pct(df: pd.DataFrame) -> pd.Series:
        return (df.isna().mean() * 100).round(2).sort_values(ascending=False)

    lines: list[str] = []
    lines.append("# Data Quality Report\n")
    lines.append("## Row counts\n")
    lines.append(f"- Raw rows: **{len(raw_df):,}**\n")
    lines.append(f"- Clean rows: **{len(clean_df):,}**\n")
    lines.append(f"- Dropped rows: **{len(raw_df) - len(clean_df):,}**\n")

    lines.append("\n## Missing values (raw)\n")
    lines.append(missing_pct(raw_df).to_string())
    lines.append("\n\n## Missing values (clean)\n")
    lines.append(missing_pct(clean_df).to_string())

    lines.append("\n\n## Duplicates\n")
    lines.append(f"- Raw duplicate rows: **{raw_df.duplicated().sum():,}**\n")
    lines.append(f"- Clean duplicate rows: **{clean_df.duplicated().sum():,}**\n")

    # integrity checks
    lines.append("\n## Integrity checks (clean)\n")
    lines.append(f"- precincts_reporting > precincts_total: **{(clean_df['precincts_reporting'] > clean_df['precincts_total']).sum():,}**\n")
    lines.append(f"- negative votes: **{(clean_df['votes'] < 0).sum():,}**\n")
    lines.append(f"- vote_share_recalc outside [0,1]: **{((clean_df['vote_share_recalc'] < 0) | (clean_df['vote_share_recalc'] > 1)).sum():,}**\n")

    return "\n".join(lines)