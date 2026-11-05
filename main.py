import tkinter as tk
import csv
from tkinter import ttk, messagebox
from pathlib import Path

from analysis import (
    calculate_revenue,
    calculate_manufacturing_cost,
    calculate_gross_profit,
    calculate_profit_margin,
)
from storage import load_sales, save_sales
from reporting import (
    format_summary,
    gross_profit_by_medicine,
    format_medicine_table,
)


DATA_FILE = Path(__file__).with_name("practice_sales.csv")

sales_records = [
    {
        "country": "Switzerland",
        "medicine": "Med-A",
        "selling_price": 100,
        "unit_cost": 40,
        "units_sold": 2000,
        "month": "2026-01",
    },
    {
        "country": "Switzerland",
        "medicine": "Med-B",
        "selling_price": 50,
        "unit_cost": 30,
        "units_sold": 100,
        "month": "2026-01",
    },
]

if DATA_FILE.exists():
    try:
        sales_records = load_sales(DATA_FILE)
    except (OSError, ValueError, csv.Error) as error:
        print(f"Could not load sales data: {error}")
        raise SystemExit(1)


def get_units_sold(medicine):
    """Ask for a whole-number quantity of zero or more."""
    while True:
        try:
            units = int(input(f"Enter units sold for {medicine}: "))

            if units < 0:
                print("Enter zero or more.")
            else:
                return units

        except ValueError:
            print("Enter a whole number, such as 100.")


def display_summary(record):
    """Calculate and display the financial summary for one sale."""
    units_sold = record["units_sold"]

    total_revenue = calculate_revenue(
        record["selling_price"], units_sold
    )
    total_manufacturing_cost = calculate_manufacturing_cost(
        record["unit_cost"], units_sold
    )
    gross_profit = calculate_gross_profit(
        total_revenue, total_manufacturing_cost
    )
    gross_profit_margin = calculate_profit_margin(
        gross_profit, total_revenue
    )

    print(
        format_summary(
            record,
            total_revenue,
            total_manufacturing_cost,
            gross_profit,
            gross_profit_margin,
        )
    )
    print()


def run_terminal_version():
    """Run the terminal workflow."""
    for record in sales_records:
        record["units_sold"] = get_units_sold(record["medicine"])
        display_summary(record)

    save_sales(sales_records, DATA_FILE)
    print(f"Sales records saved to {DATA_FILE.name}.")


def run_gui():
    """Display controls for selecting and analysing sales records."""
    window = tk.Tk()
    window.title("PharmaMarket Sales Analyser")
    window.geometry("650x650")

    ttk.Label(
        window,
        text="PharmaMarket Sales Analyser",
        font=("Arial", 18, "bold"),
    ).pack(pady=20)

    ttk.Label(window, text="Select a sales record:").pack()

    record_choices = [
        f"{index + 1}: {record['month']} - "
        f"{record['medicine']} - {record['country']}"
        for index, record in enumerate(sales_records)
    ]

    medicine_box = ttk.Combobox(
        window,
        values=record_choices,
        state="readonly",
        width=45,
    )
    medicine_box.pack(pady=5)

    if sales_records:
        medicine_box.current(0)

    ttk.Label(
        window,
        text="Units sold (whole number, zero or more):",
    ).pack(pady=(15, 0))

    units_entry = ttk.Entry(window)
    units_entry.pack(pady=5)

    result_text = tk.StringVar(
        value="Your results will appear here."
    )

    def calculate_selected():
        """Validate the quantity and display the selected sale."""
        selected_index = medicine_box.current()

        if selected_index == -1:
            messagebox.showerror(
                "No selection", "Select a sales record."
            )
            return

        try:
            units = int(units_entry.get())
        except ValueError:
            messagebox.showerror(
                "Invalid quantity", "Enter a whole number."
            )
            return

        if units < 0:
            messagebox.showerror(
                "Invalid quantity", "Enter zero or more."
            )
            return

        record = sales_records[selected_index].copy()
        record["units_sold"] = units

        revenue = calculate_revenue(
            record["selling_price"], units
        )
        cost = calculate_manufacturing_cost(
            record["unit_cost"], units
        )
        profit = calculate_gross_profit(revenue, cost)
        margin = calculate_profit_margin(profit, revenue)

        result_text.set(
            format_summary(record, revenue, cost, profit, margin)
        )

    def save_quantity():
        """Validate and save the selected record's quantity."""
        selected_index = medicine_box.current()

        if selected_index == -1:
            messagebox.showerror(
                "No selection", "Select a sales record."
            )
            return

        try:
            units = int(units_entry.get())
        except ValueError:
            messagebox.showerror(
                "Invalid quantity", "Enter a whole number."
            )
            return

        if units < 0:
            messagebox.showerror(
                "Invalid quantity", "Enter zero or more."
            )
            return

        updated_records = [
            record.copy() for record in sales_records
        ]
        updated_records[selected_index]["units_sold"] = units

        try:
            save_sales(updated_records, DATA_FILE)
        except (OSError, ValueError) as error:
            messagebox.showerror("Save failed", str(error))
            return

        sales_records[selected_index]["units_sold"] = units
        calculate_selected()
        messagebox.showinfo(
            "Saved", "Quantity saved successfully."
        )

    def show_profit_chart():
        """Display total gross profit by medicine."""
        profit_totals = gross_profit_by_medicine(sales_records)

        if not profit_totals:
            messagebox.showerror(
                "No data",
                "There are no sales records to chart.",
            )
            return

        chart_window = tk.Toplevel(window)
        chart_window.title("Gross Profit by Medicine")
        chart_window.geometry("700x450")

        canvas = tk.Canvas(
            chart_window,
            width=660,
            height=360,
            background="white",
        )
        canvas.pack(padx=20, pady=20)

        maximum_profit = max(profit_totals.values()) or 1
        baseline = 280
        chart_height = 220
        bar_width = 90
        gap = 45

        canvas.create_line(
            50,
            baseline,
            620,
            baseline,
            fill="#333333",
            width=2,
        )

        for index, (medicine, profit) in enumerate(
            sorted(profit_totals.items())
        ):
            x1 = 75 + index * (bar_width + gap)
            x2 = x1 + bar_width
            bar_height = (
                float(profit / maximum_profit) * chart_height
            )
            y1 = baseline - bar_height

            canvas.create_rectangle(
                x1,
                y1,
                x2,
                baseline,
                fill="#4F81BD",
                outline="#17365D",
            )

            canvas.create_text(
                (x1 + x2) / 2,
                baseline + 20,
                text=medicine,
                font=("Arial", 11, "bold"),
            )

            canvas.create_text(
                (x1 + x2) / 2,
                y1 - 15,
                text=f"£{profit:,.0f}",
                font=("Arial", 10),
            )

        canvas.create_text(
            330,
            20,
            text="Gross Profit by Medicine - All Loaded Records",
            font=("Arial", 15, "bold"),
        )

    def show_summary_table():
        """Display totals by medicine using all loaded records."""
        if not sales_records:
            messagebox.showerror(
                "No data", "There are no sales records."
            )
            return

        table_window = tk.Toplevel(window)
        table_window.title("Summary Table by Medicine")

        table_text = tk.Text(
            table_window,
            width=65,
            height=12,
            font=("Courier", 12),
            wrap="none",
        )
        table_text.pack(padx=20, pady=20)
        table_text.insert(
            "1.0", format_medicine_table(sales_records)
        )
        table_text.configure(state="disabled")

    ttk.Button(
        window,
        text="Calculate",
        command=calculate_selected,
    ).pack(pady=15)

    ttk.Button(
        window,
        text="Save quantity",
        command=save_quantity,
    ).pack(pady=5)

    ttk.Button(
        window,
        text="Show gross profit chart",
        command=show_profit_chart,
    ).pack(pady=5)

    ttk.Button(
        window,
        text="Show summary table",
        command=show_summary_table,
    ).pack(pady=5)

    ttk.Label(
        window,
        textvariable=result_text,
        justify="left",
    ).pack(padx=20, pady=10)

    window.mainloop()


if __name__ == "__main__":
    run_gui()