from util import load_data, inspect_data

df = load_data()
inspect_data(df)

print("\nYEAR RANGE BY CREDIT TYPE:")
print(df.groupby("credit_type")["year"].agg(["min", "max"]))

print("\nBOROUGH TOTALS BY YEAR:")
summary = (
    df.groupby(["year", "borough", "credit_type"], as_index=False)["amount"]
    .sum()
    .sort_values(["year", "borough", "credit_type"])
)

print(summary.head(20))