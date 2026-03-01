"""
Fetch BSE, NSE, and NIFTY indices.
Uses yfinance when available (BSE SENSEX, NIFTY 50, NIFTY BANK); else NSE API.
"""
import json
import urllib.error
import urllib.request
from http.cookiejar import CookieJar
from typing import Any, Dict, List, Optional

BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/",
}


TIMEOUT = 6


def fetch_nse_indices() -> Optional[Dict[str, Any]]:
    """Fetch indices from NSE India API (NIFTY 50, NIFTY BANK)."""
    cookie_jar = CookieJar()
    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cookie_jar),
        urllib.request.HTTPRedirectHandler(),
    )

    # Try API directly first (faster; often works with Referer)
    req = urllib.request.Request(
        "https://www.nseindia.com/api/allIndices",
        headers=BROWSER_HEADERS,
    )
    try:
        with opener.open(req, timeout=TIMEOUT) as response:
            return json.load(response)
    except (urllib.error.URLError, urllib.error.HTTPError, OSError):
        pass

    # Fallback: establish session via homepage, then retry API
    req = urllib.request.Request(
        "https://www.nseindia.com/",
        headers=BROWSER_HEADERS,
    )
    try:
        opener.open(req, timeout=TIMEOUT)
    except (urllib.error.URLError, urllib.error.HTTPError, OSError):
        return None

    req = urllib.request.Request(
        "https://www.nseindia.com/api/allIndices",
        headers=BROWSER_HEADERS,
    )
    try:
        with opener.open(req, timeout=TIMEOUT) as response:
            return json.load(response)
    except (urllib.error.URLError, urllib.error.HTTPError, OSError):
        return None


def fetch_yahoo_indices() -> Optional[Dict[str, Any]]:
    """Fetch indices via yfinance if available."""
    try:
        import yfinance as yf
    except ImportError:
        return None

    symbols = {"^BSESN": "S&P BSE SENSEX", "^NSEI": "NIFTY 50", "^NSEBANK": "NIFTY BANK"}
    try:
        tickers = yf.Tickers(" ".join(symbols.keys()))
        result = {}
        for sym, name in symbols.items():
            t = tickers.tickers.get(sym)
            if t is not None:
                info = t.info
                price = info.get("regularMarketPrice") or info.get("previousClose")
                change = info.get("regularMarketChange")
                pct = info.get("regularMarketChangePercent")
                if price is not None:
                    result[sym] = {
                        "name": name,
                        "price": price,
                        "change": change,
                        "pct": pct,
                    }
        return result if result else None
    except Exception:
        return None


def get_indices() -> List[Dict[str, Any]]:
    """Return unified list of indices: [{name, price, change, pct}, ...]."""
    yf_data = fetch_yahoo_indices()
    if yf_data:
        return [
            {"name": info["name"], "price": info["price"], "change": info.get("change"), "pct": info.get("pct")}
            for info in yf_data.values()
        ]
    nse_data = fetch_nse_indices()
    if nse_data:
        return parse_nse_data(nse_data)
    return []


def get_stocks() -> List[Dict[str, Any]]:
    """Return stocks: Infosys, TCS, Accenture. Uses yfinance."""
    try:
        import yfinance as yf
    except ImportError:
        return []

    # INFY.NS, TCS.NS = NSE; ACN = NYSE (Accenture)
    symbols = {"INFY.NS": "Infosys", "TCS.NS": "TCS", "ACN": "Accenture"}
    try:
        tickers = yf.Tickers(" ".join(symbols.keys()))
        result = []
        for sym, name in symbols.items():
            t = tickers.tickers.get(sym)
            if t is None:
                continue
            info = t.info
            price = info.get("regularMarketPrice") or info.get("previousClose")
            if price is None:
                continue
            result.append({
                "name": name,
                "price": price,
                "change": info.get("regularMarketChange"),
                "pct": info.get("regularMarketChangePercent"),
            })
        return result
    except Exception:
        return []


def parse_nse_data(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract NIFTY 50, NIFTY BANK from NSE response."""
    indices = []
    want = {"NIFTY 50", "NIFTY BANK"}
    for item in data.get("data", []):
        if item.get("index") in want:
            indices.append(
                {
                    "name": item["index"],
                    "price": item.get("last"),
                    "change": item.get("variation"),
                    "pct": item.get("percentChange"),
                }
            )
    return indices


def main() -> None:
    indices = get_indices()
    if indices:
        print("Current Indian market indices:")
        for i in indices:
            ch = i.get("change")
            pct = i.get("pct")
            extra = ""
            if ch is not None and pct is not None:
                extra = f"  ({ch:+.2f}, {pct:+.2f}%)"
            print(f" - {i['name']}: {i['price']}{extra}")
    else:
        print("Could not fetch index data.")


if __name__ == "__main__":
    main()
