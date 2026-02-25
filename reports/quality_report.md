# Data Quality Report

## Row counts

- Raw rows: **37**

- Clean rows: **28**

- Dropped rows: **9**


## Missing values (raw)

election_id            0.0
region_id              0.0
region_name            0.0
report_ts              0.0
precincts_total        0.0
precincts_reporting    0.0
candidate              0.0
party                  0.0
votes                  0.0
vote_share             0.0


## Missing values (clean)

vote_share_recalc      7.14
region_id              0.00
election_id            0.00
region_name            0.00
report_ts              0.00
precincts_reporting    0.00
precincts_total        0.00
candidate              0.00
party                  0.00
votes                  0.00
vote_share             0.00


## Duplicates

- Raw duplicate rows: **1**

- Clean duplicate rows: **0**


## Integrity checks (clean)

- precincts_reporting > precincts_total: **0**

- negative votes: **0**

- vote_share_recalc outside [0,1]: **0**
