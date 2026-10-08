"""Clean the raw sales files into one Pink Morsel dataset.

Reads data/daily_sales_data_*.csv, keeps Pink Morsel rows, computes
sales = quantity x price, and writes processed_data/combined_pink_morsels_sales.csv
with the columns sales, date, region. app.py reads that file.

    python data_processor.py
"""
import glob
import os

import pandas as pd

RAW_GLOB = os.path.join("data", "daily_sales_data_*.csv")
OUT_DIR = "processed_data"
OUT_FILE = os.path.join(OUT_DIR, "combined_pink_morsels_sales.csv")


def process(files):
    frames = []
    for path in files:
        print(f"Processing {path}")
        df = pd.read_csv(path)
        # The raw data spells it "pink morsel"; match case-insensitively so no rows are lost.
        df = df[df["product"].str.strip().str.lower() == "pink morsel"].copy()
        df["price"] = pd.to_numeric(df["price"].astype(str).str.replace("$", "", regex=False))
        df["quantity"] = pd.to_numeric(df["quantity"])
        df["sales"] = df["quantity"] * df["price"]
        frames.append(df[["sales", "date", "region"]])
    return pd.concat(frames, ignore_index=True)


def main():
    files = sorted(glob.glob(RAW_GLOB))
    if not files:
        raise SystemExit(f"No files match {RAW_GLOB}")
    combined = process(files)
    os.makedirs(OUT_DIR, exist_ok=True)
    combined.to_csv(OUT_FILE, index=False)
    print(f"Wrote {len(combined):,} rows to {OUT_FILE}")


if __name__ == "__main__":
    main()
