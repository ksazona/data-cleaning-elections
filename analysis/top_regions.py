import pandas as pd

df = pd.read_csv("data/clean/election_results_clean.csv")
summary = (
    df.groupby(["region_name", "candidate"])["votes"]
      .sum()
      .reset_index()
      .sort_values("votes", ascending=False)
)
print(summary.head(10))