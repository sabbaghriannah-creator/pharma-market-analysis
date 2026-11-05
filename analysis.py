from decimal import Decimal


def to_decimal(value):
    """Convert a numeric value to Decimal through its text form."""
    return Decimal(str(value))


def calculate_revenue(price, units_sold):
    """Calculate total revenue using decimal currency arithmetic."""
    return to_decimal(price) * Decimal(units_sold)


def calculate_manufacturing_cost(unit_cost, units_sold):
    """Calculate manufacturing cost using decimal currency arithmetic."""
    return to_decimal(unit_cost) * Decimal(units_sold)


def calculate_gross_profit(revenue, manufacturing_cost):
    """Calculate gross profit using decimal currency arithmetic."""
    return revenue - manufacturing_cost


def calculate_profit_margin(gross_profit, revenue):
    """Return profit margin, or None when revenue is zero."""
    if revenue == 0:
        return None

    return (gross_profit / revenue) * Decimal("100")