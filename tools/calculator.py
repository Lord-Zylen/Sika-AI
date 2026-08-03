import json


def calculate_compound_interest(
    principal: float,
    rate: float,
    years: float,
    compounds_per_year: int = 12,
) -> str:
    """Calculate compound interest."""
    amount = principal * (1 + rate / compounds_per_year) ** (compounds_per_year * years)
    interest_earned = amount - principal
    return json.dumps({
        "principal": round(principal, 2),
        "annual_rate_pct": round(rate * 100, 2),
        "years": years,
        "compounds_per_year": compounds_per_year,
        "final_amount": round(amount, 2),
        "interest_earned": round(interest_earned, 2),
    })


def calculate_loan_payment(principal: float, annual_rate: float, years: float) -> str:
    """Calculate monthly payment and total cost for a fixed-rate loan."""
    monthly_rate = annual_rate / 12
    n_payments = int(years * 12)

    if monthly_rate == 0:
        monthly_payment = principal / n_payments
    else:
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** n_payments) / (
            (1 + monthly_rate) ** n_payments - 1
        )

    total_paid = monthly_payment * n_payments
    total_interest = total_paid - principal

    return json.dumps({
        "principal": round(principal, 2),
        "annual_rate_pct": round(annual_rate * 100, 2),
        "term_years": years,
        "monthly_payment": round(monthly_payment, 2),
        "total_paid": round(total_paid, 2),
        "total_interest": round(total_interest, 2),
    })


def project_savings(monthly_deposit: float, annual_rate: float, years: float) -> str:
    """Project future value of regular monthly savings with compound interest."""
    monthly_rate = annual_rate / 12
    n_months = int(years * 12)

    if monthly_rate == 0:
        total_contributions = monthly_deposit * n_months
        future_value = total_contributions
    else:
        future_value = monthly_deposit * (((1 + monthly_rate) ** n_months - 1) / monthly_rate)
        total_contributions = monthly_deposit * n_months

    interest_earned = future_value - total_contributions

    return json.dumps({
        "monthly_deposit": round(monthly_deposit, 2),
        "annual_rate_pct": round(annual_rate * 100, 2),
        "years": years,
        "total_contributions": round(total_contributions, 2),
        "future_value": round(future_value, 2),
        "interest_earned": round(interest_earned, 2),
    })


def convert_currency(amount: float, from_currency: str) -> str:
    """Convert an amount from a foreign currency to GHS using live rates."""
    from .live_data import get_forex_rates

    rates_resp = json.loads(get_forex_rates())
    rates = rates_resp.get("rates", {})

    key = f"{from_currency.upper()}_GHS"
    rate = rates.get(key)

    if rate is None:
        return json.dumps({
            "error": f"Rate not available for {from_currency.upper()} to GHS",
            "available": list(rates.keys()),
        })

    converted = amount * rate
    return json.dumps({
        "from_currency": from_currency.upper(),
        "amount": amount,
        "rate": rate,
        "to_currency": "GHS",
        "converted_amount": round(converted, 2),
    })
