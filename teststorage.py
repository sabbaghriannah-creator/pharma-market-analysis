from pathlib import Path
from tempfile import TemporaryDirectory

from storage import load_sales


with TemporaryDirectory() as folder:
    test_file = Path(folder) / "missing_month.csv"

    test_file.write_text(
        "medicine,country,units_sold,selling_price,unit_cost\n"
        "Med-A,Switzerland,2000,100,40\n",
        encoding="utf-8",
    )

    try:
        load_sales(test_file)
    except ValueError as error:
        print("Actual result:", error)
    else:
        print("FAIL: The file was accepted despite its missing month column.")
with TemporaryDirectory() as folder:
    test_file = Path(folder) / "negative_units.csv"

    test_file.write_text(
        "month,medicine,country,units_sold,selling_price,unit_cost\n"
        "2026-01,Med-A,Switzerland,-1,100,40\n",
        encoding="utf-8",
    )

    try:
        load_sales(test_file)
    except ValueError as error:
        expected = (
            "Selling price, unit cost and units sold "
            "must be zero or more."
        )
        if str(error) == expected:
            print("PASS: Negative units rejected.")
        else:
            print("FAIL: Unexpected error:", error)
    else:
        print("FAIL: Negative units were accepted.")