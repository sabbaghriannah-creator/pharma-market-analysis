import csv


CSV_COLUMNS = [
    "month",
    "medicine",
    "country",
    "units_sold",
    "selling_price",
    "unit_cost",
]


def save_sales(records, filename):
    """Save sales records to a CSV file with column headings."""
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(records)

def load_sales(filename):
    """Load sales records and convert numeric fields to numbers."""
    records = []

    with open(filename, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames is None:
            raise ValueError("The CSV file is empty.")

        missing_columns = [
            column for column in CSV_COLUMNS
            if column not in reader.fieldnames
        ]

        if missing_columns:
            raise ValueError(
                "Missing CSV columns: " + ", ".join(missing_columns)
            )

        for row in reader:
            row["selling_price"] = float(row["selling_price"])
            row["unit_cost"] = float(row["unit_cost"])
            row["units_sold"] = int(row["units_sold"])
            if (
                row["selling_price"] < 0
                or row["unit_cost"] < 0
                or row["units_sold"] < 0
            ):
                raise ValueError(
                    "Selling price, unit cost and units sold "
                    "must be zero or more."
                )

            records.append(row)

    return records