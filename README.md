# Data Cleaning Pipeline - Sample Election Results

This repository demostrates a data cleaning pipeline that can be reproduced and used for real-world election results data. The goal is to take messy, partially corrupted CSV input and create a clean dataset for future analysis. 

All data in this repo is fake and created for demo purposes. 

--------------------------------------------------------------------
Project structure:

data-cleaning-elections/ \
  data/ \
    raw/                      # original messy input CSV \
    clean/                    # cleaned outputs (CSV + Parquet) \
  reports/                    # data quality reports + quarantined CSV issues \
  src/ \
    cleaning/ \
      clean_results.py        # core cleaning logic \
      quality_report.py      # data quality & integrity checks \
      run.py                  # pipeline entrypoint \
  analysis/ \
    top_regions.py            # example consumer of cleaned data \
  tests/ \
    test_clean_results.py    # minimal data quality test \
  requirements.txt \
  README.md

--------------------------------------------------------------------
Raw data issues:

- multiple timestamp formats and invalid dates
- duplicate rows
- inconsistent casinf in categorical fields (party names)
- numeric fields stored as strings with commas/spaces
- percent values mixed with raw decimals
- rows where precincts_reporting > precincts_total
- regions with zero total votes 
- corrupted CSV rows

---------------------------------------------------------------------
Cleaning and integrity rules:

The pipeline enforces the following restrictions on the cleaned dataset:

- report_ts parsed to datetime; invalid dates dropped
- party normalized to uppercase
- votes, precincts_total, precincts_reporting parsed as integers
- duplicate rows removed
- precincts_reporting <= precincts_total
- votes >= 0
- vote_share_recalc recomputed from votes per region
- NaN when total votes in a region are zero
- consistent column names and ordering
- sorted output for readability

---------------------------------------------------------------------
Running the pipeline:

-- set up the environment:
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows PowerShell
or
source .venv/bin/activate   # macOS/Linux

pip install -r requirements.txt

-- run cleaning pipeline:
python -m src.cleaning.run

---------------------------------------------------------------------
Output files:

data/clean/election_results_clean.csv
data/clean/election_results_clean.parquet
reports/quality_report.md


Example of cleaning:

-- raw data: \
ELX-2026-01,R06,Lakeview,2026-01-12 18:05,60,61,A. Rivera,IND,4020,51.5%

--clean: \
election_id           = ELX-2026-01  
region_id             = R06  
region_name           = Lakeview  
report_ts             = 2026-01-12 18:05:00  
precincts_total       = 60  
precincts_reporting   = 60  
candidate             = A. Rivera  
party                 = IND  
votes                 = 4020  
vote_share_recalc     = 0.515  

--raw data: \
ELX-2026-01,R09,Pinecrest,2026-01-12 20:33,55,55,A. Rivera,IND,0,0%

--clean: \
election_id         = ELX-2026-01  
region_id           = R09  
region_name         = Pinecrest  
votes               = 0  
vote_share_recalc   = NaN  

---------------------------------------------------------------------
Integrity checks:

The pipeline enfonces the following integrity checks:
- no duplicate rows
- no negative vote coutns
- precincts_reporting <= precincts total 
- vote shares recomputed 
- handling zero vote regions 

A summary of these checks is written to reports/quality_report.md

---------------------------------------------------------------------
Analysis example:

The cleaned output can be used directly for analysis.

-- run: \
python analysis/top_regions.py

-- example output: \
region_name  candidate  votes \ 
6   Central City    B. Chen  30500 \
13     Northvale  A. Rivera  24900 \
11    Meadowgate  A. Rivera  15980 \
12    Meadowgate    B. Chen  14860 \
19      Riverton  A. Rivera  14010 \
20      Riverton    B. Chen  12940 \
14     Northvale    B. Chen  11460 \
7   Harbor Point  A. Rivera  11200 \
8   Harbor Point    B. Chen  11050 \
2    Bridgewater  A. Rivera  10100 

---------------------------------------------------------------------
Testing:

--run from root: \
pytest

