import pandas as pd
import requests


NYC_9_URL = "https://data.cityofnewyork.us/resource/frre-6z6q.json?$limit=50000"
NYC_4_URL = "https://data.cityofnewyork.us/resource/p8i7-ix2s.json?$limit=50000"

APP_TOKEN = None


def fetch_socrata_json(url: str, credit_type: str) -> pd.DataFrame:
    headers = {
        "User-Agent": "SUPtown-Housing-Dashboard/1.0",
        "Accept": "application/json",
    }

    if APP_TOKEN:
        headers["X-App-Token"] = APP_TOKEN

    response = requests.get(url, headers=headers, timeout=60)
    response.raise_for_status()

    data = response.json()
    df = pd.DataFrame(data)
    df["credit_type"] = credit_type
    return df


def load_data():
    df9 = fetch_socrata_json(NYC_9_URL, "9%")
    df4 = fetch_socrata_json(NYC_4_URL, "4%")

    df = pd.concat([df9, df4], ignore_index=True)

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("/", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )

    # Year
    if "credit_year" in df.columns:
        df["year"] = pd.to_numeric(df["credit_year"], errors="coerce")
    else:
        df["year"] = pd.NA

    # 9% amount
    if "cra_amount" in df.columns:
        df["cra_amount"] = (
            df["cra_amount"]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        df["cra_amount"] = pd.to_numeric(df["cra_amount"], errors="coerce")
    else:
        df["cra_amount"] = pd.NA

    # 4% amount
    if "doce_amount" in df.columns:
        df["doce_amount"] = (
            df["doce_amount"]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        df["doce_amount"] = pd.to_numeric(df["doce_amount"], errors="coerce")
    else:
        df["doce_amount"] = pd.NA

    # Unified amount
    df["amount"] = None
    df.loc[df["credit_type"] == "9%", "amount"] = df.loc[df["credit_type"] == "9%", "cra_amount"]
    df.loc[df["credit_type"] == "4%", "amount"] = df.loc[df["credit_type"] == "4%", "doce_amount"]
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # Total units
    if "total_units" in df.columns:
        df["total_units"] = (
            df["total_units"]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        df["total_units"] = pd.to_numeric(df["total_units"], errors="coerce")
    else:
        df["total_units"] = pd.NA

    # Borough
    if "project_borough" in df.columns:
        df["borough"] = df["project_borough"].astype(str).str.strip().str.title()
    else:
        df["borough"] = pd.NA

    borough_map = {
        "Bronx": "Bronx",
        "Brooklyn": "Brooklyn",
        "Manhattan": "Manhattan",
        "Queens": "Queens",
        "Staten Island": "Staten Island",
    }

    df["borough"] = df["borough"].map(borough_map)
    df = df[df["borough"].notna()].copy()

    # Developer
    if "applicant_name" in df.columns:
        df["developer"] = df["applicant_name"].astype(str).str.strip()
    else:
        df["developer"] = pd.NA

    # Project name
    if "project_name" not in df.columns:
        df["project_name"] = pd.NA

    # Coordinates
    if "latitude" not in df.columns:
        df["latitude"] = pd.NA

    if "longitude" not in df.columns:
        df["longitude"] = pd.NA

    for alt_lat in ["latitude_1", "latitude_internal", "lat", "y_coord"]:
        if alt_lat in df.columns:
            df["latitude"] = df["latitude"].combine_first(df[alt_lat])

    for alt_lon in ["longitude_1", "longitude_internal", "lon", "lng", "x_coord"]:
        if alt_lon in df.columns:
            df["longitude"] = df["longitude"].combine_first(df[alt_lon])

    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

    # Construction type
    if "new_construction" in df.columns:
        raw_col = df["new_construction"]
    elif "new_construction_rehabilitation" in df.columns:
        raw_col = df["new_construction_rehabilitation"]
    else:
        raw_col = pd.Series([None] * len(df), index=df.index)

    df["construction_type"] = raw_col.astype(str).str.strip()

    def clean_construction(x, credit_type):
        if pd.isna(x) or x == "nan":
            return None

        x_clean = x.strip()
        x_lower = x_clean.lower()

        # 4% dataset
        if credit_type == "4%":
            if "new" in x_lower:
                return "New Construction"
            if "rehab" in x_lower:
                return "Rehabilitation"
            return "Rehabilitation"

        # 9% dataset
        if x_clean in ["Acquisition & Rehabilitation", "Acquistion & Rehabilitation"]:
            return "Acquisition & Rehabilitation"

        if x_clean == "New Construction":
            return "New Construction"

        if x_clean == "New Construction / Rehabilitation":
            return "New Construction / Rehabilitation"

        if x_clean in [
            "Rehab Only",
            "Rehabilitation",
            "Rehabilitation Only",
            "Rehabilitationilitation",
        ]:
            return "Rehabilitation"

        if "acq" in x_lower:
            return "Acquisition & Rehabilitation"
        if "new construction / rehab" in x_lower:
            return "New Construction / Rehabilitation"
        if "new" in x_lower:
            return "New Construction"
        if "rehab" in x_lower:
            return "Rehabilitation"

        return x_clean

    df["construction_type"] = df.apply(
        lambda row: clean_construction(row["construction_type"], row["credit_type"]),
        axis=1
    )

    return df


def inspect_data(df):
    print("\nCLEANED COLUMNS:")
    print(list(df.columns))

    print("\nYEAR RANGE:")
    print(df["year"].min(), "to", df["year"].max())

    print("\nBOROUGHS:")
    print(sorted(df["borough"].dropna().unique()))

    print("\nCREDIT TYPES:")
    print(sorted(df["credit_type"].dropna().unique()))

    print("\nCONSTRUCTION TYPES:")
    print(df["construction_type"].value_counts(dropna=False))

    print("\nCOORDINATE COVERAGE BY CREDIT TYPE:")
    print(
        df.assign(has_coords=df["latitude"].notna() & df["longitude"].notna())
        .groupby("credit_type")["has_coords"]
        .value_counts()
    )

    print("\nSAMPLE DATA:")
    print(
        df[
            [
                "project_name",
                "developer",
                "borough",
                "credit_type",
                "year",
                "amount",
                "total_units",
                "latitude",
                "longitude",
                "construction_type",
            ]
        ].head()
    )