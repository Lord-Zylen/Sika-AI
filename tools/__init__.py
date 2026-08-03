from .calculator import calculate_compound_interest, calculate_loan_payment, project_savings, convert_currency
from .live_data import get_forex_rates, get_bog_policy_rate, get_inflation_rate, web_search
from skills.loader import load_skill_content

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_forex_rates",
            "description": "Get current USD/GHS, GBP/GHS, EUR/GHS exchange rates from the Bank of Ghana or fallback source.",
            "parameters": {
                "type": "object",
                "properties": {
                    "base_currency": {
                        "type": "string",
                        "description": "Currency to convert from, e.g. 'USD'",
                        "default": "USD",
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_bog_policy_rate",
            "description": "Get the Bank of Ghana monetary policy rate (MPR).",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_inflation_rate",
            "description": "Get Ghana's latest inflation rate (year-on-year).",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_compound_interest",
            "description": "Calculate compound interest. Returns total amount and interest earned.",
            "parameters": {
                "type": "object",
                "properties": {
                    "principal": {"type": "number", "description": "Initial amount in GHS"},
                    "rate": {"type": "number", "description": "Annual interest rate as decimal, e.g. 0.12 for 12%"},
                    "years": {"type": "number", "description": "Number of years"},
                    "compounds_per_year": {
                        "type": "number",
                        "description": "Compounding frequency per year (default 12 for monthly)",
                        "default": 12,
                    },
                },
                "required": ["principal", "rate", "years"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_loan_payment",
            "description": "Calculate monthly payment and total cost for a fixed-rate loan (amortization).",
            "parameters": {
                "type": "object",
                "properties": {
                    "principal": {"type": "number", "description": "Loan amount in GHS"},
                    "annual_rate": {"type": "number", "description": "Annual interest rate as decimal"},
                    "years": {"type": "number", "description": "Loan term in years"},
                },
                "required": ["principal", "annual_rate", "years"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "project_savings",
            "description": "Project future value of regular monthly savings with interest.",
            "parameters": {
                "type": "object",
                "properties": {
                    "monthly_deposit": {"type": "number", "description": "Amount saved each month in GHS"},
                    "annual_rate": {"type": "number", "description": "Expected annual return as decimal"},
                    "years": {"type": "number", "description": "Number of years"},
                },
                "required": ["monthly_deposit", "annual_rate", "years"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "convert_currency",
            "description": "Convert an amount from one currency to GHS using current rates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {"type": "number", "description": "Amount to convert"},
                    "from_currency": {"type": "string", "description": "Source currency code, e.g. 'USD'"},
                },
                "required": ["amount", "from_currency"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for current information. Returns titles, URLs, and snippets. Use when RAG documents don't cover the topic or you need up-to-date information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query",
                    },
                    "max_results": {
                        "type": "number",
                        "description": "Maximum number of results to return (default 5)",
                        "default": 5,
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "load_skill",
            "description": "Load the full instructions for a specific skill. Call this when you identify which skill matches the user's request, to get the detailed steps and decision logic.",
            "parameters": {
                "type": "object",
                "properties": {
                    "skill_name": {
                        "type": "string",
                        "description": "Name of the skill to load, e.g. 'calculate-loan-repayment'",
                    }
                },
                "required": ["skill_name"],
            },
        },
    },
]

TOOL_MAP = {
    "get_forex_rates": get_forex_rates,
    "get_bog_policy_rate": get_bog_policy_rate,
    "get_inflation_rate": get_inflation_rate,
    "calculate_compound_interest": calculate_compound_interest,
    "calculate_loan_payment": calculate_loan_payment,
    "project_savings": project_savings,
    "convert_currency": convert_currency,
    "web_search": web_search,
    "load_skill": load_skill_content,
}
