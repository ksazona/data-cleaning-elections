from __future__ import annotations

import re
import pandas as pd
import numpy as np


def _parse_int_loose(x) -> int | None:
    if x is None:
        return None
    s = str(x).strip()
    if s == "" or s.lower() == "nan":
        return None
    # remove commas and spaces inside numbers
    s = s.replace(",", "").replace(" ", "")
    # keep digits and minus only
    s = re.sub(r"[^0-9\-]", "", s)
    try:
        return int(s)
    except ValueError:
        return None


def _parse_share(x) -> float | None:
    """
    Accept "52.1%", " 50.2 %", "47.9" -> float in [0, 1]
    """
    if x is None:
        return None
    s = str(x).strip().lower().replace(" ", "")
    if s == "" or s == "-" or s == "nan":
        return None
    s = s.replace("%", "")
    try:
        v = float(s)
    except ValueError:
        return None
    # if it looks like 52.1 treat as percent
    if v > 1.0:
        v = v / 100.0
    return v


def clean_election_results(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    # strip object columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    # parse timestamps
    df["report_ts"] = pd.to_datetime(df["report_ts"], errors="coerce")

    # normalize party
    df["party"] = df["party"].str.upper()

    # numeric fields
    for c in ["precincts_total", "precincts_reporting", "votes"]:
        df[c] = df[c].apply(_parse_int_loose)

    df["vote_share"] = df["vote_share"].apply(_parse_share)

    # drop exact duplicate rows
    df = df.drop_duplicates()

    # drop rows missing key fields
    df = df.dropna(subset=["election_id", "region_id", "candidate", "report_ts", "votes"])

    # reporting cannot exceed total
    df = df.dropna(subset=["precincts_total", "precincts_reporting"])
    df = df[df["precincts_total"] >= 0]
    df = df[(df["precincts_reporting"] >= 0) & (df["precincts_reporting"] <= df["precincts_total"])]

    # remove negative votes
    df = df[df["votes"] >= 0]

    # normalize region_name
    df["region_name"] = df["region_name"].str.replace(r"\s+", " ", regex=True)

    # If vote_share missing, compute within region based on votes
    df["vote_share"] = df["vote_share"].astype("float64")
    missing_share = df["vote_share"].isna()
    if missing_share.any():
        totals = df.groupby(["election_id", "region_id"])["votes"].transform("sum")
        df.loc[missing_share, "vote_share"] = df.loc[missing_share, "votes"] / totals[missing_share].replace(0, pd.NA)

    # recompute vote_share for ALL rows 
    totals = df.groupby(["election_id", "region_id"])["votes"].transform("sum")

    denom = totals.where(totals != 0, np.nan)  # avoid divide-by-zero
    df["vote_share_recalc"] = (df["votes"] / denom).astype("float64")

    # types
    df["precincts_total"] = df["precincts_total"].astype("int64")
    df["precincts_reporting"] = df["precincts_reporting"].astype("int64")
    df["votes"] = df["votes"].astype("int64")

    # sort (readability)
    df = df.sort_values(["region_id", "candidate"]).reset_index(drop=True)

    return df