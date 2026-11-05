# PharmaMarket Sales Analyser

A Python desktop application designed to analyse pharmaceutical sales data, calculate financial performance and visualise sales profitability.

## Project Overview

I developed PharmaMarket as part of my practical learning in Python programming and data analysis.

The application processes a sample dataset containing 108 pharmaceutical sales records across three countries (France, Germany and Switzerland), three medicines and 12 months in 2026.

The aim of the project is to demonstrate how programming can be used to transform sales data into useful financial information.

## Key Features

- **Sales Analysis:** Calculate total revenue, manufacturing costs, gross profit and profit margins.
- **Graphical User Interface:** Interactive desktop application built using Tkinter.
- **Data Visualisation:** Display gross profit by medicine using bar charts.
- **Financial Reporting:** Generate summary tables comparing revenue and profitability.
- **CSV Data Management:** Load, update and save sales information.
- **Input Validation:** Check quantities and prevent invalid entries.
- **Financial Accuracy:** Use Python's Decimal module for financial calculations.

## Technologies Used

- Python 3
- Tkinter
- CSV
- Decimal
- pathlib

## Project Structure

| File | Description |
|---|---|
| `main.py` | Main application and graphical interface |
| `analysis.py` | Financial calculations |
| `reporting.py` | Reporting, summaries and profit aggregation |
| `storage.py` | CSV data storage |
| `teststorage.py` | Basic data validation tests |
| `practice_sales.csv` | Sample pharmaceutical sales dataset |

## How to Run

1. Download the repository.
2. Ensure all project files are in the same folder.
3. Open the folder in Visual Studio Code.
4. Run the following command:

```bash
python3 main.py
```

The application will open in a desktop window where users can select sales records, enter quantities and explore financial results.

Python must have Tkinter available. No additional third-party Python libraries are required.

## Financial Calculations

The application calculates:

**Revenue = Selling Price × Units Sold**

**Manufacturing Cost = Unit Cost × Units Sold**

**Gross Profit = Revenue − Manufacturing Cost**

**Gross Profit Margin (%) = (Gross Profit ÷ Revenue) × 100**

When revenue is zero, the profit margin is displayed as N/A.

## Testing

The project includes basic tests checking that CSV files with missing required columns or negative sales quantities are rejected.

Run these checks using:

```bash
python3 teststorage.py
```

## Skills Demonstrated

Through this project, I developed practical experience in:

- Python programming and modular software development
- Financial and business data analysis
- Data validation and processing
- Creating graphical user interfaces
- Designing visual reports
- Problem-solving and debugging

## Future Development

Future improvements could include interactive data filtering, additional visualisations, automated testing and exporting financial reports.

---

*This project uses sample data and was developed for educational and portfolio purposes.*
