import pandas as pd
from src.cleaning.clean_results import clean_election_results

def test_precincts_never_exceed_total():
    raw = pd.read_csv("data/raw/election_results.csv")
    clean = clean_election_results(raw)
    assert (clean["precincts_reporting"] <= clean["precincts_total"]).all()