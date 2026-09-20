import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from decimal import Decimal, getcontext
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

getcontext().prec = 50  # arbitrary-precision fallback for overflowed projections

# Tax data for various countries
TAX_DATA = {
    "United States": {"domestic_rate": 15.0, "withholding_us": 0.0, "withholding_nonUS": 15.0},
    "Canada": {"domestic_rate": 26.0, "withholding_us": 15.0, "withholding_nonUS": 25.0},
    "United Kingdom": {"domestic_rate": 8.75, "withholding_us": 15.0, "withholding_nonUS": 0.0},
    "Germany": {"domestic_rate": 26.375, "withholding_us": 15.0, "withholding_nonUS": 26.375},
    "France": {"domestic_rate": 30.0, "withholding_us": 15.0, "withholding_nonUS": 30.0},
    "Australia": {"domestic_rate": 30.0, "withholding_us": 15.0, "withholding_nonUS": 30.0},
    "Japan": {"domestic_rate": 20.315, "withholding_us": 10.0, "withholding_nonUS": 20.315},
    "Singapore": {"domestic_rate": 0.0, "withholding_us": 30.0, "withholding_nonUS": 0.0},
    "Trinidad and Tobago": {"domestic_rate": 10.0, "withholding_us": 30.0, "withholding_nonUS": 15.0},
    "India": {"domestic_rate": 10.0, "withholding_us": 25.0, "withholding_nonUS": 20.0},
    "China": {"domestic_rate": 20.0, "withholding_us": 10.0, "withholding_nonUS": 10.0},
    "Brazil": {"domestic_rate": 15.0, "withholding_us": 15.0, "withholding_nonUS": 15.0},
    "South Africa": {"domestic_rate": 20.0, "withholding_us": 15.0, "withholding_nonUS": 20.0},
    "Mexico": {"domestic_rate": 10.0, "withholding_us": 10.0, "withholding_nonUS": 10.0},
    "Netherlands": {"domestic_rate": 26.9, "withholding_us": 15.0, "withholding_nonUS": 15.0},
    "Switzerland": {"domestic_rate": 35.0, "withholding_us": 15.0, "withholding_nonUS": 35.0},
    "Sweden": {"domestic_rate": 30.0, "withholding_us": 15.0, "withholding_nonUS": 30.0},
    "Spain": {"domestic_rate": 19.0, "withholding_us": 15.0, "withholding_nonUS": 19.0},
    "Italy": {"domestic_rate": 26.0, "withholding_us": 15.0, "withholding_nonUS": 26.0},
    "South Korea": {"domestic_rate": 14.0, "withholding_us": 15.0, "withholding_nonUS": 22.0},
    "Hong Kong": {"domestic_rate": 0.0, "withholding_us": 30.0, "withholding_nonUS": 0.0},
    "New Zealand": {"domestic_rate": 33.0, "withholding_us": 15.0, "withholding_nonUS": 30.0},
    "Ireland": {"domestic_rate": 25.0, "withholding_us": 15.0, "withholding_nonUS": 25.0},
    "Belgium": {"domestic_rate": 30.0, "withholding_us": 15.0, "withholding_nonUS": 30.0},
    "Austria": {"domestic_rate": 27.5, "withholding_us": 15.0, "withholding_nonUS": 27.5},
    "Denmark": {"domestic_rate": 27.0, "withholding_us": 15.0, "withholding_nonUS": 27.0},
    "Norway": {"domestic_rate": 35.2, "withholding_us": 15.0, "withholding_nonUS": 25.0},
    "Finland": {"domestic_rate": 30.0, "withholding_us": 15.0, "withholding_nonUS": 30.0},
    "Poland": {"domestic_rate": 19.0, "withholding_us": 15.0, "withholding_nonUS": 19.0},
    "Portugal": {"domestic_rate": 28.0, "withholding_us": 15.0, "withholding_nonUS": 28.0},
    "Greece": {"domestic_rate": 5.0, "withholding_us": 30.0, "withholding_nonUS": 15.0},
    "Turkey": {"domestic_rate": 10.0, "withholding_us": 15.0, "withholding_nonUS": 10.0},
    "Thailand": {"domestic_rate": 10.0, "withholding_us": 15.0, "withholding_nonUS": 10.0},
    "Malaysia": {"domestic_rate": 0.0, "withholding_us": 30.0, "withholding_nonUS": 0.0},
    "Philippines": {"domestic_rate": 10.0, "withholding_us": 25.0, "withholding_nonUS": 30.0},
    "Indonesia": {"domestic_rate": 10.0, "withholding_us": 15.0, "withholding_nonUS": 20.0},
    "Vietnam": {"domestic_rate": 5.0, "withholding_us": 30.0, "withholding_nonUS": 5.0},
    "Chile": {"domestic_rate": 10.0, "withholding_us": 15.0, "withholding_nonUS": 35.0},
    "Argentina": {"domestic_rate": 7.0, "withholding_us": 15.0, "withholding_nonUS": 7.0},
    "Colombia": {"domestic_rate": 10.0, "withholding_us": 15.0, "withholding_nonUS": 20.0},
    "Peru": {"domestic_rate": 5.0, "withholding_us": 15.0, "withholding_nonUS": 5.0},
    "Israel": {"domestic_rate": 25.0, "withholding_us": 25.0, "withholding_nonUS": 25.0},
    "Saudi Arabia": {"domestic_rate": 0.0, "withholding_us": 30.0, "withholding_nonUS": 5.0},
    "UAE": {"domestic_rate": 0.0, "withholding_us": 30.0, "withholding_nonUS": 0.0},
    "Egypt": {"domestic_rate": 10.0, "withholding_us": 15.0, "withholding_nonUS": 10.0},
    "Nigeria": {"domestic_rate": 10.0, "withholding_us": 15.0, "withholding_nonUS": 10.0},
    "Kenya": {"domestic_rate": 5.0, "withholding_us": 30.0, "withholding_nonUS": 10.0},
    "Pakistan": {"domestic_rate": 15.0, "withholding_us": 30.0, "withholding_nonUS": 15.0},
    "Bangladesh": {"domestic_rate": 10.0, "withholding_us": 30.0, "withholding_nonUS": 20.0},
}

EXCHANGE_MAP = {
    'NYSE': 'United States', 'NASDAQ': 'United States', 'NYQ': 'United States',
    'NMS': 'United States', 'TSX': 'Canada', 'TSE': 'Canada',
    'LSE': 'United Kingdom', 'LON': 'United Kingdom',
    'FRA': 'Germany', 'XETRA': 'Germany',
    'PAR': 'France', 'EPA': 'France',
    'ASX': 'Australia', 'AUS': 'Australia',
    'JPX': 'Japan', 'TYO': 'Japan',
    'SGX': 'Singapore', 'SES': 'Singapore',
    'HKG': 'Hong Kong', 'HKEX': 'Hong Kong',
}


def determine_stock_country(info):
    try:
        country = info.get('country', 'United States')
        exchange = (info.get('exchange') or '').upper()
        for key, val in EXCHANGE_MAP.items():
            if key in exchange:
                return val
        return country if country else 'United States'
    except Exception:
        return 'United States'


def calculate_growth_rate(series, periods=5):
    """CAGR from a price series (daily closes)."""
    if series is None or len(series) < 2:
        return 0.0
    try:
        clean = series.dropna()
        if len(clean) < 2:
            return 0.0
        if len(clean) > periods * 252:
            clean = clean[-periods * 252:]
        start_val, end_val = clean.iloc[0], clean.iloc[-1]
        years = len(clean) / 252
        if start_val <= 0 or years <= 0:
            return 0.0
        return round((pow(end_val / start_val, 1 / years) - 1) * 100, 2)
    except Exception:
        return 0.0


def calculate_dividend_growth(dividends, periods=5):
    """CAGR of yearly dividend totals."""
    if dividends is None or len(dividends) < 2:
        return 0.0
    try:
        df = pd.DataFrame({'dividend': dividends})
        df['year'] = df.index.year
        yearly = df.groupby('year')['dividend'].sum()
        if len(yearly) < 2:
            return 0.0
        if len(yearly) > periods:
            yearly = yearly[-periods:]
        start_val, end_val = yearly.iloc[0], yearly.iloc[-1]
        years = len(yearly) - 1
        if start_val <= 0 or years <= 0:
            return 0.0
        return round((pow(end_val / start_val, 1 / years) - 1) * 100, 2)
    except Exception:
        return 0.0


def detect_frequency(dividends):
    """Classify payout cadence from real dividend history.

    Uses the median gap between consecutive payments, not the average
    total span divided by count. A single old/irregular distribution
    sitting in the history (common for newly-launched funds -- e.g. one
    inception-era payment from years ago, followed by a consistent weekly
    schedule since) can drag a span-based average up into the wrong
    bucket entirely (seen in practice: true weekly payer misclassified as
    "Annually" because of exactly one leftover far-past data point). The
    median is unaffected by a single such outlier.
    """
    if dividends is None or len(dividends) < 2:
        return "Quarterly"
    recent = dividends[-12:] if len(dividends) >= 12 else dividends
    gaps = sorted((recent.index[i] - recent.index[i - 1]).days for i in range(1, len(recent)))
    if not gaps:
        return "Quarterly"
    median_gap = gaps[len(gaps) // 2]
    if median_gap < 10:
        return "Weekly"
    elif median_gap < 40:
        return "Monthly"
    elif median_gap < 120:
        return "Quarterly"
    return "Annually"


def trailing_12mo_dividends(dividends):
    """Sum of dividend payments in the last ~365 days, tz-safe."""
    if dividends is None or len(dividends) == 0:
        return 0.0
    try:
        now = pd.Timestamp.now(tz=dividends.index.tz) if dividends.index.tz else pd.Timestamp.now()
        cutoff = now - pd.Timedelta(days=365)
        recent = dividends[dividends.index >= cutoff]
        return float(recent.sum())
    except Exception:
        return 0.0


def safe_float(value):
    """Convert to a finite float, or None if invalid. Plain `x or default`
    doesn't catch NaN -- NaN is truthy in Python, so `nan or 0` returns nan,
    not 0. That gap let a NaN price from Yahoo (common for thin/newly
    listed tickers) silently flow into the simulation and poison every
    downstream number into inf/nan."""
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    if v != v or v in (float('inf'), float('-inf')):  # v != v is the NaN check
        return None
    return v


@st.cache_data(ttl=3600)
def fetch_stock_data(ticker):
    """Fetch live from yfinance, cached for an hour per ticker so repeated
    clicks/reruns for the same ticker in a session don't re-hit the API.

    Dividend yield is always derived as dividend_rate / price -- never
    taken directly from yfinance's raw 'dividendYield' field, whose scale
    has changed between yfinance versions and was the source of badly
    wrong yields (e.g. showing 0.045% instead of 4.5%)."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info or {}
        hist = stock.history(period="5y")
        if hist is None:
            hist = pd.DataFrame()
        dividends = stock.dividends
        if dividends is None:
            dividends = pd.Series(dtype=float)

        current_price = safe_float(info.get('currentPrice', info.get('regularMarketPrice')))
        if not current_price and len(hist) > 0:
            current_price = safe_float(hist['Close'].iloc[-1])
        if not current_price:
            return {"success": False, "error": (
                f"'{ticker}': no valid price data returned by Yahoo Finance "
                f"(got missing/NaN price -- this happens for very new or thinly-traded tickers)."
            )}

        # Prefer yfinance's own dividendRate ($/share/year); fall back to
        # trailing-12mo actual payments if that field is missing/zero/NaN.
        dividend_rate = safe_float(info.get('dividendRate'))
        if not dividend_rate:
            dividend_rate = safe_float(trailing_12mo_dividends(dividends))
        dividend_rate = dividend_rate or 0.0

        dividend_yield = (dividend_rate / current_price * 100) if current_price > 0 else 0.0

        return {
            "success": True,
            "current_price": current_price,
            "dividend_rate": round(dividend_rate, 4),
            "dividend_yield": round(dividend_yield, 4),
            "stock_country": determine_stock_country(info),
            "price_growth_5y": calculate_growth_rate(hist['Close']) if len(hist) > 0 else 0.0,
            "div_growth_5y": calculate_dividend_growth(dividends) if len(dividends) > 0 else 0.0,
            "div_freq_detected": detect_frequency(dividends),
            "last_updated": datetime.now().isoformat(timespec="seconds"),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def calculate_tax(gross_dividend, investor_country, stock_country, override_withholding=None, override_domestic=None):
    """Calculate tax on dividends with withholding and domestic tax"""
    
    # Get tax rates
    investor_tax = TAX_DATA.get(investor_country, TAX_DATA["United States"])
    
    # Determine withholding rate
    if override_withholding is not None:
        withholding_rate = override_withholding
    else:
        if stock_country == "United States":
            if investor_country == "United States":
                withholding_rate = investor_tax["withholding_us"]
            else:
                withholding_rate = investor_tax["withholding_us"]
        else:
            if investor_country == stock_country:
                withholding_rate = 0.0  # No withholding for domestic stocks
            else:
                withholding_rate = investor_tax["withholding_nonUS"]
    
    # Determine domestic rate
    if override_domestic is not None:
        domestic_rate = override_domestic
    else:
        domestic_rate = investor_tax["domestic_rate"]
    
    # Calculate taxes. Works with either plain floats (the normal fast path)
    # or Decimal (the arbitrary-precision fallback for overflowed results) --
    # rates get cast to match gross_dividend's type so the two never mix.
    is_decimal = isinstance(gross_dividend, Decimal)
    hundred = Decimal(100) if is_decimal else 100
    zero = Decimal(0) if is_decimal else 0
    rate_of = (lambda r: Decimal(str(r)) / hundred) if is_decimal else (lambda r: r / hundred)

    withholding_tax = gross_dividend * rate_of(withholding_rate)
    after_withholding = gross_dividend - withholding_tax
    
    domestic_tax = after_withholding * rate_of(domestic_rate)
    net_dividend = after_withholding - domestic_tax
    
    total_tax = withholding_tax + domestic_tax
    effective_rate = (total_tax / gross_dividend * hundred) if gross_dividend > zero else zero
    
    return {
        "gross": gross_dividend,
        "withholding_tax": withholding_tax,
        "withholding_rate": withholding_rate,
        "after_withholding": after_withholding,
        "domestic_tax": domestic_tax,
        "domestic_rate": domestic_rate,
        "net": net_dividend,
        "total_tax": total_tax,
        "effective_rate": effective_rate
    }

def tapered_growth_rate(year_num, initial_rate, terminal_rate, taper_years):
    """Linear decay from initial_rate (year 1) down to terminal_rate (by
    year `taper_years`), then holds flat at terminal_rate afterward.
    taper_years <= 0 disables tapering entirely (always initial_rate) --
    this keeps the function a no-op / backward compatible when tapering
    isn't requested."""
    if taper_years <= 0:
        return initial_rate
    if year_num >= taper_years or taper_years == 1:
        return terminal_rate
    frac = (year_num - 1) / (taper_years - 1)
    return initial_rate + (terminal_rate - initial_rate) * frac


def simulate_investment(initial_investment, current_price, annual_dividend_per_share, 
                       additional_investment, additional_freq, investment_years,
                       dividend_growth, price_growth, dividend_freq, drip_enabled,
                       investor_country, stock_country, override_withholding, override_domestic,
                       dividend_growth_taper_years=0, dividend_growth_terminal=None):
    """Simulate dividend investment over time.

    Runs at weekly resolution (52 steps/year) so Weekly-paying dividends
    (common on high-yield income ETFs) compound on their actual real-world
    cadence rather than being approximated as monthly. Monthly/Quarterly/
    Annually schedules are derived from the same weekly loop by tracking
    when each period's index increases, rather than a modulo check --
    52 isn't evenly divisible by 12, so modulo would misfire for monthly
    events. This keeps every frequency, and every combination of dividend
    vs. additional-investment frequency, exact.

    dividend_growth_taper_years > 0 linearly decays dividend_growth down to
    dividend_growth_terminal over that many years, then holds flat -- for
    when the input dividend_growth reflects a young fund's early growth
    rather than a rate that repeats every year for decades. Price growth
    is never tapered; it's left as a flat rate throughout.
    """
    periods_per_year = {"Weekly": 52, "Monthly": 12, "Quarterly": 4, "Annually": 1}
    dividend_periods = periods_per_year[dividend_freq]
    additional_periods = periods_per_year[additional_freq]
    if dividend_growth_terminal is None:
        dividend_growth_terminal = dividend_growth

    # Defensive guard: refuse to simulate on invalid price data rather than
    # silently producing NaN/Infinity throughout the results (division by
    # a zero/NaN price is exactly what corrupted every downstream number
    # for tickers with bad Yahoo data).
    if current_price is None or current_price != current_price or current_price <= 0:
        return None

    weeks_per_year = 52
    total_weeks = investment_years * weeks_per_year

    # Initialize tracking
    shares = initial_investment / current_price
    cash = 0
    price = current_price
    dividend_per_share = annual_dividend_per_share / dividend_periods

    # Geometric weekly growth rate equivalent to the stated annual rate,
    # so price compounds to exactly the target CAGR after 52 weeks.
    weekly_price_growth = (1 + price_growth / 100) ** (1 / weeks_per_year) - 1

    results = []
    last_div_period = 0
    last_add_period = 0
    last_year_applied = 0

    for week in range(1, total_weeks + 1):
        year = week / weeks_per_year

        # Price growth (weekly)
        price = price * (1 + weekly_price_growth)

        # Dividend growth applied once per completed year -- tapered from
        # dividend_growth toward dividend_growth_terminal if requested
        year_index = week // weeks_per_year
        if year_index > last_year_applied:
            year_growth = tapered_growth_rate(
                year_index, dividend_growth, dividend_growth_terminal, dividend_growth_taper_years)
            dividend_per_share = dividend_per_share * (1 + year_growth / 100)
            last_year_applied = year_index

        # Dividend payment -- fires when this week crosses into a new
        # dividend period (period boundaries spaced evenly across the year)
        div_period = int(week / (weeks_per_year / dividend_periods))
        gross_dividend_paid = 0
        if div_period > last_div_period:
            last_div_period = div_period
            gross_dividend_paid = shares * dividend_per_share
            
            # Calculate tax
            tax_info = calculate_tax(gross_dividend_paid, investor_country, stock_country, 
                                    override_withholding, override_domestic)
            net_dividend_paid = tax_info["net"]
            
            if drip_enabled:
                # Reinvest net dividends
                new_shares = net_dividend_paid / price
                shares += new_shares
            else:
                cash += net_dividend_paid
        else:
            tax_info = calculate_tax(0, investor_country, stock_country, 
                                    override_withholding, override_domestic)
        
        # Additional investment -- same period-crossing approach
        add_period = int(week / (weeks_per_year / additional_periods))
        if add_period > last_add_period:
            last_add_period = add_period
            new_shares = additional_investment / price
            shares += new_shares
        
        # Record results
        portfolio_value = shares * price + cash
        total_invested = initial_investment + (additional_investment * additional_periods * year)
        
        results.append({
            "week": week,
            "year": round(year, 3),
            "shares": shares,
            "price": price,
            "cash": cash,
            "portfolio_value": portfolio_value,
            "total_invested": total_invested,
            "gross_dividend": gross_dividend_paid,
            "net_dividend": tax_info["net"] if gross_dividend_paid > 0 else 0,
            "withholding_tax": tax_info["withholding_tax"],
            "domestic_tax": tax_info["domestic_tax"],
            "total_tax": tax_info["total_tax"]
        })
    
    return pd.DataFrame(results)


def simulate_investment_decimal_summary(initial_investment, current_price, annual_dividend_per_share,
                       additional_investment, additional_freq, investment_years,
                       dividend_growth, price_growth, dividend_freq, drip_enabled,
                       investor_country, stock_country, override_withholding, override_domestic,
                       dividend_growth_taper_years=0, dividend_growth_terminal=None):
    """Same math as simulate_investment, but using arbitrary-precision
    Decimal arithmetic and returning only final totals (no per-week rows,
    no chart data). Used as a fallback when the fast float64 simulation
    overflows to inf/nan -- Decimal has no practical upper bound (unlike
    float64's ~1.8e308 ceiling), so a genuinely enormous but mathematically
    real result can still be computed and shown instead of blocked."""
    periods_per_year = {"Weekly": 52, "Monthly": 12, "Quarterly": 4, "Annually": 1}
    dividend_periods = periods_per_year[dividend_freq]
    additional_periods = periods_per_year[additional_freq]
    if dividend_growth_terminal is None:
        dividend_growth_terminal = dividend_growth

    def D(x):
        return Decimal(str(x))

    weeks_per_year = 52
    total_weeks = investment_years * weeks_per_year

    shares = D(initial_investment) / D(current_price)
    cash = Decimal(0)
    price = D(current_price)
    dividend_per_share = D(annual_dividend_per_share) / D(dividend_periods)
    weekly_price_growth = (Decimal(1) + D(price_growth) / Decimal(100)) ** (Decimal(1) / Decimal(weeks_per_year)) - Decimal(1)

    total_gross_div = Decimal(0)
    total_net_div = Decimal(0)
    total_tax_paid = Decimal(0)
    total_withholding = Decimal(0)
    total_domestic = Decimal(0)

    last_div_period = 0
    last_add_period = 0
    last_year_applied = 0

    for week in range(1, total_weeks + 1):
        price = price * (Decimal(1) + weekly_price_growth)

        year_index = week // weeks_per_year
        if year_index > last_year_applied:
            year_growth = tapered_growth_rate(
                year_index, dividend_growth, dividend_growth_terminal, dividend_growth_taper_years)
            dividend_per_share = dividend_per_share * (Decimal(1) + D(year_growth) / Decimal(100))
            last_year_applied = year_index

        div_period = int(week / (weeks_per_year / dividend_periods))
        if div_period > last_div_period:
            last_div_period = div_period
            gross_dividend_paid = shares * dividend_per_share
            tax_info = calculate_tax(gross_dividend_paid, investor_country, stock_country,
                                    override_withholding, override_domestic)
            net_dividend_paid = tax_info["net"]

            total_gross_div += gross_dividend_paid
            total_net_div += net_dividend_paid
            total_tax_paid += tax_info["total_tax"]
            total_withholding += tax_info["withholding_tax"]
            total_domestic += tax_info["domestic_tax"]

            if drip_enabled:
                shares += net_dividend_paid / price
            else:
                cash += net_dividend_paid

        add_period = int(week / (weeks_per_year / additional_periods))
        if add_period > last_add_period:
            last_add_period = add_period
            shares += D(additional_investment) / price

    portfolio_value = shares * price + cash
    total_invested = D(initial_investment) + D(additional_investment) * Decimal(additional_periods) * Decimal(investment_years)

    return {
        "final_shares": shares,
        "final_price": price,
        "portfolio_value": portfolio_value,
        "total_invested": total_invested,
        "total_gross_dividend": total_gross_div,
        "total_net_dividend": total_net_div,
        "total_tax_paid": total_tax_paid,
        "total_withholding": total_withholding,
        "total_domestic_tax": total_domestic,
    }


def format_large(value, prefix="$"):
    """Format a Decimal that might be astronomically large. Normal
    comma-formatting below 1e15; scientific notation above that, since
    a 200-digit number isn't more meaningful to read than its magnitude."""
    try:
        if abs(value) < Decimal("1e15"):
            return f"{prefix}{float(value):,.2f}"
        exponent = value.adjusted()
        mantissa = value / (Decimal(10) ** exponent)
        return f"{prefix}{float(mantissa):.3f} \u00d7 10^{exponent}"
    except Exception:
        return f"{prefix}{value}"


_ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
         "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
         "eighteen", "nineteen"]
_TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

# Reevah's own names for 10^18 .. 10^33 (real names: quintillion .. decillion).
# Million-Quadrillion keep their normal names; above Xenon the real names resume.
CUSTOM_ILLIONS = {5: "Omnion", 6: "Sixtiton", 7: "Setiton", 8: "Octoiton", 9: "Nieniton", 10: "Xenon"}


def _words_under_1000(n):
    """1-999 in English words (0 returns an empty string)."""
    parts = []
    if n >= 100:
        parts.append(f"{_ONES[n // 100]} hundred")
        n %= 100
    if n >= 20:
        parts.append(_TENS[n // 10] + (f"-{_ONES[n % 10]}" if n % 10 else ""))
    elif n > 0:
        parts.append(_ONES[n])
    return " ".join(parts)


def illion_name(n, custom=False):
    """Name for 10^(3n+3): million, billion ... centillion, and beyond that
    the Conway-Wechsler system (the standard way to name very large numbers).
    Valid for 1 <= n <= 999. With custom=True, 10^18..10^33 use CUSTOM_ILLIONS."""
    if custom and n in CUSTOM_ILLIONS:
        return CUSTOM_ILLIONS[n]
    small = ["", "m", "b", "tr", "quadr", "quint", "sext", "sept", "oct", "non"]
    teens = ["dec", "undec", "duodec", "tredec", "quattuordec", "quindec",
             "sexdec", "septendec", "octodec", "novemdec"]
    if n < 10:
        return small[n] + "illion"
    if n < 20:
        return teens[n - 10] + "illion"
    units = ["", "un", "duo", "tre", "quattuor", "quinqua", "se", "septe", "octo", "nove"]
    tens = ["", "deci", "viginti", "triginta", "quadraginta", "quinquaginta",
            "sexaginta", "septuaginta", "octoginta", "nonaginta"]
    hundreds = ["", "centi", "ducenti", "trecenti", "quadringenti", "quingenti",
                "sescenti", "septingenti", "octingenti", "nongenti"]
    tens_marks = ["", "N", "MS", "NS", "NS", "NS", "N", "N", "MX", ""]
    hundreds_marks = ["", "NX", "N", "NS", "NS", "NS", "N", "N", "MX", ""]
    u, t, h = n % 10, (n // 10) % 10, n // 100
    marks = tens_marks[t] if t else hundreds_marks[h]
    unit = units[u]
    if u == 3 and ("S" in marks or "X" in marks):
        unit += "s"
    elif u == 6:
        unit += "s" if "S" in marks else ("x" if "X" in marks else "")
    elif u in (7, 9):
        unit += "m" if "M" in marks else ("n" if "N" in marks else "")
    name = unit + tens[t] + hundreds[h]
    return name[:-1] + "illion"  # every component ends in a vowel; drop it


def number_in_words(value, custom=False):
    """Spell a Decimal out in words. Anything large is rounded to 3
    significant figures, e.g. 6.778e1283 -> 'about six hundred seventy-eight
    sesvigintiquadringentillion'."""
    try:
        if value == 0:
            return "zero"
        sign = "negative " if value < 0 else ""
        v = abs(value)
        if v < Decimal("999999.5"):
            r = int(v.to_integral_value())
            if r == 0:
                return f"{sign}less than one"
            words = _words_under_1000(r) if r < 1000 else (
                _words_under_1000(r // 1000) + " thousand" +
                (" " + _words_under_1000(r % 1000) if r % 1000 else ""))
            about = "about " if abs(v - r) >= Decimal("0.005") else ""
            return f"{about}{sign}{words}"
        exponent = v.adjusted()
        n = (exponent - 3) // 3
        m = v / (Decimal(10) ** (3 * n + 3))          # 1 <= m < 1000
        m = round(m, 0 if m >= 100 else (1 if m >= 10 else 2))
        if m >= 1000:
            m, n = Decimal(1), n + 1
        if n > 999:                                    # beyond nameable range
            mant = float(v / (Decimal(10) ** exponent))
            return f"about {sign}{mant:.2f} times ten to the power of {exponent:,}"
        text = format(m, "f")
        if "." in text:
            text = text.rstrip("0").rstrip(".")
        int_part, _, frac = text.partition(".")
        words = _words_under_1000(int(int_part))
        if frac:
            words += " point " + " ".join(_ONES[int(d)] for d in frac)
        about = "" if m * Decimal(10) ** (3 * n + 3) == v else "about "
        return f"{about}{sign}{words} {illion_name(n, custom)}"
    except Exception:
        return str(value)

# Streamlit UI
st.set_page_config(page_title="Dividend Calculator", layout="wide")

st.title("💰 Comprehensive Dividend Investment Calculator")
st.markdown("### Global Market Support with Tax Estimation")

# Sidebar for inputs
with st.sidebar:
    st.header("📊 Stock Information")
    ticker = st.text_input("Ticker Symbol", value="AAPL", help="Enter stock ticker (e.g., AAPL, MSFT, VOO)")
    
    if st.button("Fetch Stock Data", type="primary"):
        st.session_state.fetch_data = True

    if st.button("🔄 Clear Cache & Re-fetch", help="Forces a fresh pull from Yahoo Finance, "
                 "bypassing the 1hr cache. Use this if numbers look stale or wrong."):
        st.cache_data.clear()
        st.session_state.fetch_data = True
        st.rerun()
    
    st.divider()

# Initialize session state
if 'fetch_data' not in st.session_state:
    st.session_state.fetch_data = False
if 'stock_data' not in st.session_state:
    st.session_state.stock_data = None

# Fetch data
if st.session_state.fetch_data and ticker:
    with st.spinner("Fetching stock data..."):
        st.session_state.stock_data = fetch_stock_data(ticker)
        st.session_state.fetch_data = False

# Display stock info and calculator
if st.session_state.stock_data and st.session_state.stock_data["success"]:
    data = st.session_state.stock_data

    current_price = data["current_price"] or 0
    dividend_yield = data["dividend_yield"] or 0
    dividend_rate = data["dividend_rate"] or 0
    stock_country = data["stock_country"] or "United States"
    price_growth = data["price_growth_5y"] or 0
    div_growth = data["div_growth_5y"] or 0
    div_freq_detected = data["div_freq_detected"] or "Quarterly"

    st.caption(f"📅 Data fetched: {data['last_updated']} (live from Yahoo Finance, cached 1hr)")

    # Display stock info
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Current Price", f"${current_price:.2f}")
    with col2:
        st.metric("Dividend Yield", f"{dividend_yield:.2f}%")
    with col3:
        st.metric("Annual Dividend", f"${dividend_rate:.2f}")
    with col4:
        st.metric("Stock Country", stock_country)
    
    col5, col6, col7 = st.columns(3)
    with col5:
        st.metric("Div. Growth (5yr)", f"{div_growth:.2f}%")
    with col6:
        st.metric("Price Growth (5yr)", f"{price_growth:.2f}%")
    with col7:
        st.metric("Detected Frequency", div_freq_detected)
    
    st.divider()
    
    # Investment parameters
    st.header("💼 Investment Parameters")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Investment Details")
        initial_investment = st.number_input("Initial Investment ($)", min_value=0.0, value=10000.0, step=100.0)
        additional_investment = st.number_input("Additional Investment ($)", min_value=0.0, value=500.0, step=50.0)
        additional_freq = st.selectbox("Additional Investment Frequency", ["Monthly", "Quarterly", "Annually"])
        investment_years = st.slider("Investment Period (Years)", min_value=1, max_value=50, value=20)
        drip_enabled = st.checkbox("Enable DRIP (Dividend Reinvestment)", value=True)
    
    with col2:
        st.subheader("Growth Assumptions")
        growth_bound = 1000.0  # some high-yield weekly/leveraged funds show extreme early CAGR
        dividend_growth_rate = st.number_input("Dividend Growth Rate (% annually)",
                                              min_value=-50.0, max_value=growth_bound,
                                              value=float(min(max(div_growth, -50.0), growth_bound)), step=0.1,
                                              help="Historical or expected annual dividend growth rate. "
                                                   "Clamped to a sane input range; the raw computed 5yr figure "
                                                   "is shown in the metric above.")

        taper_enabled = st.checkbox(
            "Taper dividend growth to a long-term rate over time", value=False,
            help="Applies the rate above for the first N years, then linearly decays it down to "
                 "a more sustainable rate. Useful when the rate above reflects a young fund's "
                 "early growth (common for newly-launched high-yield funds) rather than something "
                 "that repeats every year for decades. Doesn't change the historical figure itself "
                 "-- only how far into the future it's assumed to keep applying.")
        if taper_enabled:
            taper_col1, taper_col2 = st.columns(2)
            with taper_col1:
                taper_years = st.number_input(
                    "Years to taper over", min_value=1, max_value=max(investment_years, 1),
                    value=min(5, max(investment_years, 1)), step=1)
            with taper_col2:
                terminal_growth_rate = st.number_input(
                    "Long-term rate after taper (%)", min_value=-20.0, max_value=growth_bound,
                    value=5.0, step=0.5,
                    help="A typical sustainable long-term dividend growth rate for a mature payer "
                         "is roughly 3-7%/year. This is what the rate decays toward, then holds at.")
        else:
            taper_years = 0
            terminal_growth_rate = dividend_growth_rate

        price_growth_rate = st.number_input("Share Price Growth Rate (% annually)",
                                           min_value=-50.0, max_value=growth_bound,
                                           value=float(min(max(price_growth, -50.0), growth_bound)), step=0.1,
                                           help="Historical or expected annual price appreciation")
        freq_options = ["Weekly", "Monthly", "Quarterly", "Annually"]
        dividend_frequency = st.selectbox("Dividend Frequency", freq_options,
                                         index=freq_options.index(div_freq_detected)
                                         if div_freq_detected in freq_options else 1)

    # A high growth rate auto-filled from a short/volatile dividend history
    # (common for newly-launched high-yield weekly funds) compounded over
    # a long horizon produces enormous but not-technically-wrong numbers --
    # flag this clearly so it doesn't read as a trustworthy projection.
    # Not shown when tapering is on and actually brings the long-run rate
    # down to something sane -- that's exactly what tapering is for.
    EXTREME_GROWTH_THRESHOLD = 50.0
    LONG_HORIZON_YEARS = 10
    dividend_rate_is_extreme = abs(dividend_growth_rate) > EXTREME_GROWTH_THRESHOLD and not (
        taper_enabled and abs(terminal_growth_rate) <= EXTREME_GROWTH_THRESHOLD)
    price_rate_is_extreme = abs(price_growth_rate) > EXTREME_GROWTH_THRESHOLD
    if (dividend_rate_is_extreme or price_rate_is_extreme) and investment_years > LONG_HORIZON_YEARS:
        st.warning(
            f"⚠️ A growth rate above {EXTREME_GROWTH_THRESHOLD:.0f}%/year, compounded over "
            f"{investment_years} years, will produce very large numbers that aren't a realistic "
            f"forecast -- rates this high are usually an artifact of a short or volatile dividend "
            f"history (common for newly-launched funds) and can't be sustained for decades. "
            f"Consider lowering the growth rate(s) above, enabling the dividend growth taper, "
            f"or shortening the investment period."
        )
    
    st.divider()
    
    # Tax settings
    st.header("🌍 Tax Configuration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        investor_country = st.selectbox("Your Country (Investor)", sorted(TAX_DATA.keys()), 
                                       index=sorted(TAX_DATA.keys()).index("Trinidad and Tobago"))
    
    with col2:
        st.info(f"**Stock Listed In:** {stock_country}")
        
        # Show default rates
        investor_tax = TAX_DATA[investor_country]
        if stock_country == "United States":
            default_withholding = investor_tax["withholding_us"]
        else:
            if investor_country == stock_country:
                default_withholding = 0.0
            else:
                default_withholding = investor_tax["withholding_nonUS"]
        
        st.write(f"Default Withholding: {default_withholding}%")
        st.write(f"Default Domestic Tax: {investor_tax['domestic_rate']}%")
    
    with col3:
        st.subheader("Override Tax Rates")
        override_withholding = st.number_input("Withholding Tax (%)", min_value=0.0, max_value=100.0, 
                                              value=float(default_withholding), step=0.1,
                                              help="Tax withheld at source by stock's country")
        override_domestic = st.number_input("Domestic Tax (%)", min_value=0.0, max_value=100.0, 
                                           value=float(investor_tax['domestic_rate']), step=0.1,
                                           help="Tax paid in your country on net dividends")
    
    st.info("💡 **Tax Disclaimer:** These are estimates. Actual tax depends on your personal situation, tax treaties, account type (retirement/taxable), and current tax laws. Consult a tax professional.")
    
    st.divider()
    
    # Calculate button
    if st.button("📈 Calculate Investment Projection", type="primary", use_container_width=True):
        
        # Run simulation
        results_df = simulate_investment(
            initial_investment, current_price, dividend_rate,
            additional_investment, additional_freq, investment_years,
            dividend_growth_rate, price_growth_rate, dividend_frequency,
            drip_enabled, investor_country, stock_country,
            override_withholding, override_domestic,
            dividend_growth_taper_years=taper_years,
            dividend_growth_terminal=terminal_growth_rate
        )

        if results_df is None:
            st.error(f"Can't run a projection: '{ticker}' has no valid price data to simulate from.")
            st.stop()

        # Guard against extreme growth-rate compounding overflowing float64
        # (e.g. a very high growth rate compounded for 20-30 years can
        # exceed ~1.8e308). Rather than blocking, fall back to computing the
        # true totals with arbitrary-precision Decimal math -- charts and
        # the week-by-week table aren't meaningful at that scale, but the
        # actual final numbers are real and are shown below.
        numeric_cols = ["portfolio_value", "shares", "gross_dividend", "net_dividend", "total_tax"]
        if not np.isfinite(results_df[numeric_cols].to_numpy()).all():
            st.warning(
                "This projection overflows standard floating-point range (beyond ~10\u00b3\u2070\u2078) "
                "before the investment period ends -- a result of the growth rate(s) compounding "
                "this far. Showing the true totals below using arbitrary-precision math instead; "
                "charts and the week-by-week breakdown aren't shown since they're not meaningful "
                "at this scale."
            )
            summary = simulate_investment_decimal_summary(
                initial_investment, current_price, dividend_rate,
                additional_investment, additional_freq, investment_years,
                dividend_growth_rate, price_growth_rate, dividend_frequency,
                drip_enabled, investor_country, stock_country,
                override_withholding, override_domestic,
                dividend_growth_taper_years=taper_years,
                dividend_growth_terminal=terminal_growth_rate
            )
            st.header("📊 Investment Summary (arbitrary-precision)")
            if taper_years > 0:
                div_text = (f"dividends growing {dividend_growth_rate:,.1f}% a year at first, "
                            f"tapering to {terminal_growth_rate:,.1f}% over {taper_years} years")
            else:
                div_text = f"dividends growing {dividend_growth_rate:,.1f}% every year"
            drip_text = ", with every payout reinvested" if drip_enabled else ""
            st.info(
                "These numbers are far too big to be a real forecast. They come from assuming "
                f"{div_text} and the share price growing {price_growth_rate:,.1f}% every year, "
                f"for {investment_years} years{drip_text}. Growth rates that high usually come "
                "from a young fund's short history and can't last for decades. "
                "The plain-English version of each figure is at the bottom."
            )
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Total Invested", format_large(summary["total_invested"]))
                st.metric("Final Shares", format_large(summary["final_shares"], prefix=""))
            with m2:
                st.metric("Final Portfolio Value", format_large(summary["portfolio_value"]))
                st.metric("Final Share Price", format_large(summary["final_price"]))
            with m3:
                st.metric("Total Return", format_large(summary["portfolio_value"] - summary["total_invested"]))
                st.metric("Gross Dividends (total)", format_large(summary["total_gross_dividend"]))
            m4, m5 = st.columns(2)
            with m4:
                st.metric("Net Dividends (After Tax)", format_large(summary["total_net_dividend"]))
            with m5:
                st.metric("Total Tax Paid", format_large(summary["total_tax_paid"]))
            st.subheader("🗣️ In words")
            words_rows = [
                ("Total Invested", summary["total_invested"], " dollars"),
                ("Final Shares", summary["final_shares"], " shares"),
                ("Final Portfolio Value", summary["portfolio_value"], " dollars"),
                ("Final Share Price", summary["final_price"], " dollars"),
                ("Total Return", summary["portfolio_value"] - summary["total_invested"], " dollars"),
                ("Gross Dividends (total)", summary["total_gross_dividend"], " dollars"),
                ("Net Dividends (After Tax)", summary["total_net_dividend"], " dollars"),
                ("Total Tax Paid", summary["total_tax_paid"], " dollars"),
            ]
            st.markdown("\n".join(
                f"- **{label}:** {number_in_words(val)}{unit}" for label, val, unit in words_rows))
            st.caption("Names above a centillion (10^303) follow the Conway-Wechsler system; "
                       "they aren't everyday words because nothing in real life is this large.")
            st.stop()
        
        # Summary metrics
        st.header("📊 Investment Summary")
        
        final_row = results_df.iloc[-1]
        total_invested = final_row['total_invested']
        final_value = final_row['portfolio_value']
        total_return = final_value - total_invested
        total_return_pct = (total_return / total_invested * 100) if total_invested > 0 else 0
        
        # Calculate CAGR
        years = investment_years
        cagr = (pow(final_value / total_invested, 1 / years) - 1) * 100 if total_invested > 0 and years > 0 else 0
        
        # Dividend totals
        total_gross_div = results_df['gross_dividend'].sum()
        total_net_div = results_df['net_dividend'].sum()
        total_tax_paid = results_df['total_tax'].sum()
        
        # First row - Investment metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Invested", f"${total_invested:,.0f}")
        with col2:
            st.metric("Final Portfolio Value", f"${final_value:,.0f}", 
                     delta=f"{total_return_pct:.1f}%")
        with col3:
            st.metric("Total Return", f"${total_return:,.0f}")
        
        # Second row - Performance metrics
        col4, col5, col6 = st.columns(3)
        with col4:
            st.metric("CAGR", f"{cagr:.2f}%")
        with col5:
            st.metric("Final Shares", f"{final_row['shares']:.2f}")
        with col6:
            st.metric("Gross Dividends", f"${total_gross_div:,.0f}")
        
        # Third row - Tax metrics
        col7, col8 = st.columns(2)
        with col7:
            st.metric("Net Dividends (After Tax)", f"${total_net_div:,.0f}")
        with col8:
            st.metric("Total Tax Paid", f"${total_tax_paid:,.0f}", 
                     delta=f"-{(total_tax_paid/total_gross_div*100):.1f}%")
        
        # In words (uses the custom Omnion...Xenon ladder)
        st.subheader("🗣️ In words")
        words_rows = [
            ("Total Invested", total_invested, " dollars"),
            ("Final Portfolio Value", final_value, " dollars"),
            ("Total Return", total_return, " dollars"),
            ("Final Shares", final_row['shares'], " shares"),
            ("Gross Dividends", total_gross_div, " dollars"),
            ("Net Dividends (After Tax)", total_net_div, " dollars"),
            ("Total Tax Paid", total_tax_paid, " dollars"),
        ]
        words_lines = [
            f"- **{label}:** {number_in_words(Decimal(str(float(val))), custom=True)}{unit}"
            for label, val, unit in words_rows
        ]
        st.markdown("\n".join(words_lines))
        if any(name in line for line in words_lines for name in CUSTOM_ILLIONS.values()):
            st.caption("Omnion = 10^18, Sixtiton = 10^21, Setiton = 10^24, "
                       "Octoiton = 10^27, Nieniton = 10^30, Xenon = 10^33.")

        # Charts
        st.header("📈 Projection Charts")
        
        # Create subplot
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=("Portfolio Value vs Investment", "Share Accumulation", 
                          "Dividend Income (Net)", "Tax Breakdown"),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"type": "pie"}]]
        )
        
        # Portfolio value
        fig.add_trace(
            go.Scatter(x=results_df['year'], y=results_df['portfolio_value'], 
                      name="Portfolio Value", line=dict(color='green', width=3)),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=results_df['year'], y=results_df['total_invested'], 
                      name="Total Invested", line=dict(color='blue', width=2, dash='dash')),
            row=1, col=1
        )
        
        # Shares
        fig.add_trace(
            go.Scatter(x=results_df['year'], y=results_df['shares'], 
                      name="Shares Owned", line=dict(color='purple', width=2)),
            row=1, col=2
        )
        
        # Dividends (aggregate by year for clarity)
        yearly_data = results_df.groupby(results_df['year'].astype(int)).agg({
            'gross_dividend': 'sum',
            'net_dividend': 'sum'
        }).reset_index()
        
        fig.add_trace(
            go.Bar(x=yearly_data['year'], y=yearly_data['net_dividend'], 
                  name="Net Dividends", marker_color='lightgreen'),
            row=2, col=1
        )
        
        # Tax pie chart
        fig.add_trace(
            go.Pie(labels=['Withholding Tax', 'Domestic Tax', 'Net Dividends'],
                  values=[results_df['withholding_tax'].sum(), 
                         results_df['domestic_tax'].sum(),
                         total_net_div],
                  marker=dict(colors=['#ff6b6b', '#feca57', '#48dbfb'])),
            row=2, col=2
        )
        
        fig.update_xaxes(title_text="Years", row=1, col=1)
        fig.update_xaxes(title_text="Years", row=1, col=2)
        fig.update_xaxes(title_text="Year", row=2, col=1)
        
        fig.update_yaxes(title_text="Value ($)", row=1, col=1)
        fig.update_yaxes(title_text="Shares", row=1, col=2)
        fig.update_yaxes(title_text="Amount ($)", row=2, col=1)
        
        fig.update_layout(height=800, showlegend=True)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed table
        st.header("📋 Year-by-Year Breakdown")
        
        # Aggregate by year
        yearly_summary = results_df.groupby(results_df['year'].astype(int)).agg({
            'shares': 'last',
            'price': 'last',
            'portfolio_value': 'last',
            'total_invested': 'last',
            'gross_dividend': 'sum',
            'net_dividend': 'sum',
            'total_tax': 'sum'
        }).reset_index()
        
        yearly_summary['return'] = yearly_summary['portfolio_value'] - yearly_summary['total_invested']
        yearly_summary['return_pct'] = (yearly_summary['return'] / yearly_summary['total_invested'] * 100).round(2)
        
        # Format for display
        display_df = yearly_summary.copy()
        display_df.columns = ['Year', 'Shares', 'Price', 'Portfolio Value', 'Total Invested', 
                             'Gross Dividends', 'Net Dividends', 'Tax Paid', 'Return ($)', 'Return (%)']
        
        display_df['Shares'] = display_df['Shares'].round(2)
        display_df['Price'] = display_df['Price'].apply(lambda x: f"${x:.2f}")
        display_df['Portfolio Value'] = display_df['Portfolio Value'].apply(lambda x: f"${x:,.2f}")
        display_df['Total Invested'] = display_df['Total Invested'].apply(lambda x: f"${x:,.2f}")
        display_df['Gross Dividends'] = display_df['Gross Dividends'].apply(lambda x: f"${x:,.2f}")
        display_df['Net Dividends'] = display_df['Net Dividends'].apply(lambda x: f"${x:,.2f}")
        display_df['Tax Paid'] = display_df['Tax Paid'].apply(lambda x: f"${x:,.2f}")
        display_df['Return ($)'] = display_df['Return ($)'].apply(lambda x: f"${x:,.2f}")
        display_df['Return (%)'] = display_df['Return (%)'].apply(lambda x: f"{x:.2f}%")
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Download button
        csv = results_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Full Results (CSV)",
            data=csv,
            file_name=f"{ticker}_dividend_projection.csv",
            mime="text/csv"
        )

elif st.session_state.stock_data and not st.session_state.stock_data["success"]:
    st.error(f"❌ Error fetching data: {st.session_state.stock_data['error']}")
    st.info("Please check the ticker symbol and try again. Make sure to use the correct format (e.g., AAPL for Apple, MSFT for Microsoft)")

else:
    st.info("👆 Enter a ticker symbol in the sidebar and click 'Fetch Stock Data' to begin")
    
    # Show example usage
    with st.expander("ℹ️ How to Use This Calculator"):
        st.markdown("""
        ### Quick Start Guide
        
        1. **Enter Ticker Symbol**: Input any stock ticker (e.g., AAPL, MSFT, JNJ, VOO)
        2. **Fetch Data**: Click the button to retrieve current stock information
        3. **Review Auto-Fetched Data**: 
           - Current price, dividend yield, and dividend rate
           - Historical dividend growth rate (5-year CAGR)
           - Historical price growth rate (5-year CAGR)
           - Detected dividend frequency
        
        4. **Set Investment Parameters**:
           - Initial investment amount
           - Additional monthly/quarterly/annual investments
           - Investment time horizon
           - Enable/disable DRIP (Dividend Reinvestment Plan)
        
        5. **Configure Tax Settings**:
           - Select your country (investor location)
           - View automatic stock country detection
           - See default tax rates (withholding + domestic)
           - Override rates if needed for your situation
        
        6. **Calculate**: View comprehensive projections with charts and tables
        
        ### Global Market Support
        - **US Stocks**: NYSE, NASDAQ (e.g., AAPL, MSFT, JNJ)
        - **Canadian**: TSX (add .TO, e.g., RY.TO)
        - **UK**: LSE (add .L, e.g., BP.L)
        - **European**: Various exchanges (e.g., SAP.DE for Germany)
        - **Asian**: (e.g., 9988.HK for Hong Kong)
        - **Australian**: ASX (add .AX, e.g., BHP.AX)
        
        ### Tax Calculation
        The calculator applies a two-layer tax system:
        1. **Withholding Tax**: Applied at source by the country where stock is listed
        2. **Domestic Tax**: Applied by your country on received dividends
        
        For example, a Trinidad & Tobago investor in US stocks typically pays:
        - 30% US withholding tax (or 15% with treaty)
        - 10% Trinidad domestic tax on remaining amount
        
        ### Features
        - ✅ Automatic data fetching (current price, yield, dividends)
        - ✅ Historical growth rate calculation from 5yr price/dividend history
        - ✅ DRIP on/off toggle
        - ✅ Comprehensive tax estimation for 45+ countries
        - ✅ CAGR calculation
        - ✅ Visual charts and year-by-year breakdown
        - ✅ CSV export for further analysis
        - ✅ Efficient API usage with caching (1-hour cache per ticker)
        
        ### Notes
        - All calculations are estimates for planning purposes
        - Tax laws vary by individual circumstances
        - Consult with a financial advisor for personalized advice
        - Historical performance doesn't guarantee future results
        """)
    
    with st.expander("🌍 Supported Countries"):
        st.markdown("### Tax Database Includes:")
        
        col1, col2, col3 = st.columns(3)
        countries_list = sorted(TAX_DATA.keys())
        third = len(countries_list) // 3
        
        with col1:
            for country in countries_list[:third]:
                st.write(f"🌍 {country}")
        
        with col2:
            for country in countries_list[third:third*2]:
                st.write(f"🌍 {country}")
        
        with col3:
            for country in countries_list[third*2:]:
                st.write(f"🌍 {country}")
        
        st.info("Don't see your country? Use the tax override feature to manually input your rates!")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #888;'>
    <p>💡 <b>Disclaimer:</b> This calculator provides estimates for educational purposes only. 
    Tax laws are complex and vary by jurisdiction. Always consult with qualified tax and financial professionals.</p>
    <p>Data provided by Yahoo Finance via yfinance.</p>
</div>
""", unsafe_allow_html=True)