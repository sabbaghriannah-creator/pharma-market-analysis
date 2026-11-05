from analysis import (
    calculate_revenue,
    calculate_manufacturing_cost,
    calculate_gross_profit,
    calculate_profit_margin,
)


def format_summary(record, revenue, manufacturing_cost, gross_profit, margin):
    """Create a readable financial summary for one sales record."""
    lines = [
        f"Month: {record['month']}",
        f"Medicine: {record['medicine']}",
        f"Country: {record['country']}",
        f"Units sold: {record['units_sold']}",
        f"Total revenue: £{revenue:,.2f}",
        f"Manufacturing costs: £{manufacturing_cost:,.2f}",
        f"Gross profit: £{gross_profit:,.2f}",
    ]

    if margin is None:
        lines.append("Gross profit margin: N/A")
    else:
        lines.append(f"Gross profit margin: {margin:.2f}%")

    return "\n".join(lines)


def gross_profit_by_medicine(records):
    """Return total gross profit grouped by medicine."""
    totals = {}

    for record in records:
        revenue = calculate_revenue(
            record["selling_price"],
            record["units_sold"],
        )
        cost = calculate_manufacturing_cost(
            record["unit_cost"],
            record["units_sold"],
        )
        profit = calculate_gross_profit(revenue, cost)

        medicine = record["medicine"]
        totals[medicine] = totals.get(medicine, 0) + profit

    return totals


def format_medicine_table(records):
    """Return an aligned table of totals per medicine, with a total row."""
    totals = {}

    for record in records:
        revenue = calculate_revenue(
            record["selling_price"], record["units_sold"]
        )
        cost = calculate_manufacturing_cost(
            record["unit_cost"], record["units_sold"]
        )
        old_revenue, old_cost = totals.get(record["medicine"], (0, 0))
        totals[record["medicine"]] = (
            old_revenue + revenue,
            old_cost + cost,
        )

    def make_line(name, revenue, cost):
        profit = revenue - cost
        margin = calculate_profit_margin(profit, revenue)
        margin_text = "N/A" if margin is None else f"{margin:.2f}%"

        return (
            f"{name:<10}"
            f"{'£' + format(revenue, ',.2f'):>14}"
            f"{'£' + format(profit, ',.2f'):>14}"
            f"{margin_text:>9}"
        )

    lines = [
        f"{'Medicine':<10}{'Revenue':>14}{'Profit':>14}{'Margin':>9}"
    ]
    total_revenue = total_cost = 0

    for medicine, (revenue, cost) in sorted(totals.items()):
        lines.append(make_line(medicine, revenue, cost))
        total_revenue += revenue
        total_cost += cost

    lines.append("-" * 47)
    lines.append(make_line("TOTAL", total_revenue, total_cost))
    return "\n".join(lines)