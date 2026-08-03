import json
import requests
from ddgs import DDGS

_FOREX_CACHE: dict = {}

# Free fallback API (no key required, rate-limited)
_FALLBACK_URL = "https://open.er-api.com/v6/latest/USD"


def get_forex_rates(base_currency: str = "USD") -> str:
    """Return major forex rates against GHS.

    Tries the open exchange-rate API as a fallback. Returns a JSON string
    with rates for USD, GBP, EUR against GHS.
    """
    cache_key = f"forex_{base_currency}"
    if cache_key in _FOREX_CACHE:
        return json.dumps(_FOREX_CACHE[cache_key])

    # Hardcoded reference rates (Bank of Ghana indicative rates, update periodically)
    reference_rates = {
        "USD_GHS": 15.80,
        "GBP_GHS": 20.10,
        "EUR_GHS": 17.20,
        "NGN_GHS": 0.0105,
        "ZAR_GHS": 0.87,
        "CNY_GHS": 2.18,
    }

    try:
        resp = requests.get(_FALLBACK_URL, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        rates_to_usd = data.get("rates", {})

        ghs_per_usd = rates_to_usd.get("GHS")
        if ghs_per_usd and ghs_per_usd > 0:
            computed = {}
            for cur in ["USD", "GBP", "EUR", "NGN", "ZAR", "CNY"]:
                rate = rates_to_usd.get(cur)
                if rate and rate > 0:
                    computed[f"{cur}_GHS"] = round(ghs_per_usd / rate, 4)
            if computed:
                result = {
                    "source": "open.er-api.com",
                    "base": "GHS",
                    "rates": computed,
                }
                _FOREX_CACHE[cache_key] = result
                return json.dumps(result)
    except Exception:
        pass

    # Fallback to reference rates
    result = {"source": "reference_rates (indicative)", "base": "GHS", "rates": reference_rates}
    _FOREX_CACHE[cache_key] = result
    return json.dumps(result)


def get_bog_policy_rate() -> str:
    """Return Ghana's Bank of Ghana Monetary Policy Rate.

    This is a static reference — update the value when BOG announces changes.
    """
    return json.dumps({
        "source": "Bank of Ghana (reference)",
        "policy_rate_pct": 29.5,
        "last_announced": "2025-01-27",
        "note": "Verify at bog.gov.gh for the latest",
    })


def get_inflation_rate() -> str:
    """Return Ghana's latest year-on-year inflation rate.

    Static reference — update when GSS publishes new figures.
    """
    return json.dumps({
        "source": "Ghana Statistical Service (reference)",
        "inflation_yoy_pct": 23.2,
        "period": "2025-01",
        "note": "Verify at statsghana.gov.gh for the latest",
    })


def web_search(query: str, max_results: int = 5) -> str:
    """Search the web using DuckDuckGo and return results with titles, URLs, and snippets.

    Use this when the user asks about something not covered by RAG documents
    or when you need current information from the web.
    """
    try:
        results = DDGS().text(query, max_results=max_results)
        if not results:
            return json.dumps({"query": query, "results": [], "note": "No results found"})
        formatted = []
        for r in results:
            formatted.append({
                "title": r.get("title", ""),
                "url": r.get("href", r.get("link", "")),
                "snippet": r.get("body", ""),
            })
        return json.dumps({"query": query, "results": formatted})
    except Exception as e:
        return json.dumps({"query": query, "error": f"Web search failed: {str(e)}"})
