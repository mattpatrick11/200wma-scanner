#!/usr/bin/env python3
"""
200-Week Moving Average Stock Scanner — v4
Large/Mid/Small Cap · Embedded Charts · GitHub Dark Theme
190 stocks · Years-Public column · Dividend / Aristocrat badges
"""

import subprocess, sys
for pkg in ['yfinance', 'pandas']:
    try: __import__(pkg)
    except ImportError: subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg, '-q'])

import yfinance as yf
import pandas as pd
from datetime import datetime, timezone, timedelta
import time, json, math

# ── Stock Universe ─────────────────────────────────────────────────────────────

LARGE_CAP = [
    # Technology (16)
    ("AAPL","Apple Inc.","Technology"),("MSFT","Microsoft Corp.","Technology"),("SPCX","SpaceX","Industrials"),
    ("GOOGL","Alphabet Inc.","Technology"),("META","Meta Platforms","Technology"),
    ("NVDA","NVIDIA Corp.","Technology"),("AVGO","Broadcom Inc.","Technology"),
    ("ADBE","Adobe Inc.","Technology"),("CRM","Salesforce Inc.","Technology"),
    ("TXN","Texas Instruments","Technology"),("AMD","Adv. Micro Devices","Technology"),
    ("ASML","ASML Holding","Technology"),("TSM","Taiwan Semiconductor","Technology"),
    ("INTC","Intel Corp.","Technology"),("QCOM","Qualcomm Inc.","Technology"),
    ("IBM","IBM Corp.","Technology"),("ADP","Auto. Data Processing","Technology"),("PANW","Palo Alto Networks","Technology"),
    # Consumer Discretionary (9)
    ("AMZN","Amazon.com Inc.","Cons. Discretionary"),("TSLA","Tesla Inc.","Cons. Discretionary"),
    ("BABA","Alibaba Group","Cons. Discretionary"),
    ("MCD","McDonald's Corp.","Cons. Discretionary"),("NKE","Nike Inc.","Cons. Discretionary"),
    ("HD","Home Depot Inc.","Cons. Discretionary"),("SBUX","Starbucks Corp.","Cons. Discretionary"),
    ("LOW","Lowe's Companies","Cons. Discretionary"),("TGT","Target Corp.","Cons. Discretionary"),
    # Consumer Staples (11)
    ("PG","Procter & Gamble","Consumer Staples"),("KO","Coca-Cola Co.","Consumer Staples"),
    ("PEP","PepsiCo Inc.","Consumer Staples"),("COST","Costco Wholesale","Consumer Staples"),
    ("WMT","Walmart Inc.","Consumer Staples"),("CL","Colgate-Palmolive","Consumer Staples"),
    ("MO","Altria Group","Consumer Staples"),("PM","Philip Morris Intl.","Consumer Staples"),
    ("GIS","General Mills","Consumer Staples"),("HRL","Hormel Foods","Consumer Staples"),
    ("CLX","Clorox Co.","Consumer Staples"),
    # Financials (13)
    ("BRK-B","Berkshire Hathaway B","Financials"),("JPM","JPMorgan Chase","Financials"),
    ("V","Visa Inc.","Financials"),("MA","Mastercard Inc.","Financials"),
    ("GS","Goldman Sachs","Financials"),("BAC","Bank of America","Financials"),
    ("SPGI","S&P Global Inc.","Financials"),("CB","Chubb Ltd.","Financials"),
    ("MMC","Marsh & McLennan","Financials"),("AFL","Aflac Inc.","Financials"),
    ("USB","U.S. Bancorp","Financials"),("COF","Capital One Financial","Financials"),
    ("BEN","Franklin Resources","Financials"),
    # Healthcare (16)
    ("JNJ","Johnson & Johnson","Healthcare"),("UNH","UnitedHealth Group","Healthcare"),
    ("LLY","Eli Lilly & Co.","Healthcare"),("ABBV","AbbVie Inc.","Healthcare"),
    ("TMO","Thermo Fisher","Healthcare"),("MRK","Merck & Co.","Healthcare"),
    ("PFE","Pfizer Inc.","Healthcare"),("ABT","Abbott Laboratories","Healthcare"),
    ("MDT","Medtronic plc","Healthcare"),("GILD","Gilead Sciences","Healthcare"),
    ("ISRG","Intuitive Surgical","Healthcare"),("SYK","Stryker Corp.","Healthcare"),
    ("BDX","Becton Dickinson","Healthcare"),("NVO","Novo Nordisk A/S","Healthcare"),
    ("BMY","Bristol-Myers Squibb","Healthcare"),("BSX","Boston Scientific Corp.","Healthcare"),("OSCR","Oscar Health Inc.","Healthcare"),
    # Communication (5)
    ("NFLX","Netflix Inc.","Communication"),("DIS","Walt Disney Co.","Communication"),
    ("T","AT&T Inc.","Communication"),("VZ","Verizon Comm.","Communication"),
    ("CMCSA","Comcast Corp.","Communication"),
    # Energy (4)
    ("XOM","Exxon Mobil","Energy"),("CVX","Chevron Corp.","Energy"),
    ("COP","ConocoPhillips","Energy"),("EOG","EOG Resources","Energy"),
    # Utilities (6)
    ("NEE","NextEra Energy","Utilities"),("SO","Southern Company","Utilities"),
    ("DUK","Duke Energy","Utilities"),("D","Dominion Energy","Utilities"),
    ("AEP","American Elec. Power","Utilities"),("WEC","WEC Energy Group","Utilities"),
    # Industrials (12)
    ("CAT","Caterpillar Inc.","Industrials"),("RTX","RTX Corp.","Industrials"),
    ("HON","Honeywell Intl.","Industrials"),("EMR","Emerson Electric","Industrials"),
    ("ITW","Illinois Tool Works","Industrials"),("DE","Deere & Company","Industrials"),
    ("LMT","Lockheed Martin","Industrials"),("NOC","Northrop Grumman","Industrials"),
    ("GD","General Dynamics","Industrials"),("UPS","United Parcel Service","Industrials"),
    ("FDX","FedEx Corp.","Industrials"),("MMM","3M Company","Industrials"),
    # Materials (7)
    ("SHW","Sherwin-Williams","Materials"),("APD","Air Products","Materials"),
    ("LIN","Linde plc","Materials"),("ECL","Ecolab Inc.","Materials"),
    ("NUE","Nucor Corp.","Materials"),("DOW","Dow Inc.","Materials"),
    ("NEM","Newmont Corp.","Materials"),
    # Real Estate (6)
    ("AMT","American Tower","Real Estate"),("PLD","Prologis Inc.","Real Estate"),
    ("O","Realty Income","Real Estate"),("SPG","Simon Property Group","Real Estate"),
    ("CCI","Crown Castle Intl.","Real Estate"),("FRT","Federal Realty Trust","Real Estate"),
]

MID_CAP = [
    ("CRWD","CrowdStrike Holdings","Technology"),("NET","Cloudflare Inc.","Technology"),
    ("DDOG","Datadog Inc.","Technology"),("ZS","Zscaler Inc.","Technology"),
    ("TTD","The Trade Desk","Technology"),("PLTR","Palantir Technologies","Technology"),
    ("SNOW","Snowflake Inc.","Technology"),("APP","AppLovin Corp.","Technology"),
    ("NOW","ServiceNow Inc.","Technology"),("SHOP","Shopify Inc.","Technology"),
    ("VEEV","Veeva Systems","Technology"),("HUBS","HubSpot Inc.","Technology"),
    ("MDB","MongoDB Inc.","Technology"),("NTNX","Nutanix Inc.","Technology"),
    ("TWLO","Twilio Inc.","Technology"),("ROKU","Roku Inc.","Technology"),
    ("OKTA","Okta Inc.","Technology"),("DOCU","DocuSign Inc.","Technology"),
    ("PAYC","Paycom Software","Technology"),("PCTY","Paylocity Holding","Technology"),
    ("ZI","ZoomInfo Technologies","Technology"),("MNDY","Monday.com Ltd.","Technology"),
    ("CFLT","Confluent Inc.","Technology"),("DOCN","DigitalOcean Holdings","Technology"),
    ("S","SentinelOne Inc.","Technology"),("GTLB","GitLab Inc.","Technology"),
    ("BSY","Bentley Systems","Technology"),("FROG","JFrog Ltd.","Technology"),
    ("BRZE","Braze Inc.","Technology"),("ABNB","Airbnb Inc.","Cons. Discretionary"),
    ("DASH","DoorDash Inc.","Cons. Discretionary"),("UBER","Uber Technologies","Cons. Discretionary"),
    ("LYFT","Lyft Inc.","Cons. Discretionary"),("DKNG","DraftKings Inc.","Cons. Discretionary"),
    ("ETSY","Etsy Inc.","Cons. Discretionary"),("CHWY","Chewy Inc.","Cons. Discretionary"),
    ("W","Wayfair Inc.","Cons. Discretionary"),
    ("COIN","Coinbase Global","Financials"),("PYPL","PayPal Holdings","Financials"),
    ("HOOD","Robinhood Markets","Financials"),("AFRM","Affirm Holdings","Financials"),
    ("NU","Nu Holdings","Financials"),("RKT","Rocket Companies","Financials"),
    ("FOUR","Shift4 Payments","Financials"),("Z","Zillow Group","Real Estate"),
    ("CELH","Celsius Holdings","Consumer Staples"),("HIMS","Hims & Hers Health","Healthcare"),
    ("RBLX","Roblox Corp.","Communication"),("PINS","Pinterest Inc.","Communication"),
    ("SNAP","Snap Inc.","Communication"),
    # International / Emerging
    ("SE","Sea Limited","Technology"),("GRAB","Grab Holdings","Technology"),
    ("NBIS","Nebius Group","Technology"),("ZETA","Zeta Global Holdings","Technology"),
    ("ASTS","AST SpaceMobile","Communication"),
    ("GNRC","Generac Holdings","Industrials"),
]

SMALL_CAP = [
    ("IONQ","IonQ Inc.","Technology"),("AI","C3.ai Inc.","Technology"),
    ("ESTC","Elastic N.V.","Technology"),("BILL","Bill.com Holdings","Technology"),
    ("PATH","UiPath Inc.","Technology"),("DBX","Dropbox Inc.","Technology"),
    ("ZM","Zoom Video Comm.","Technology"),("DUOL","Duolingo Inc.","Technology"),
    ("AMBA","Ambarella Inc.","Technology"),("FORM","FormFactor Inc.","Technology"),
    ("RXRX","Recursion Pharma","Healthcare"),("COUR","Coursera Inc.","Technology"),
    ("FSLY","Fastly Inc.","Technology"),("MGNI","Magnite Inc.","Technology"),
    ("PUBM","PubMatic Inc.","Technology"),("PAYO","Payoneer Global","Financials"),
    ("LMND","Lemonade Inc.","Financials"),("SOFI","SoFi Technologies","Financials"),
    ("UPST","Upstart Holdings","Financials"),("OPEN","Opendoor Technologies","Financials"),
    ("TMDX","TransMedics Group","Healthcare"),("PRCT","Procept BioRobotics","Healthcare"),
    ("ACHR","Archer Aviation","Industrials"),("SOUN","SoundHound AI","Technology"),
    ("KVYO","Klaviyo Inc.","Technology"),
    ("JOBY","Joby Aviation","Industrials"),("AUR","Aurora Innovation","Technology"),
    ("ADUR","Aduro Clean Technologies","Energy"),("WYFI","Wyfi Inc.","Technology"),
    ("GRRR","Gorilla Technology Group","Technology"),
    ("ONDS","Ondas Holdings","Technology"),
    ("PCT","PureCycle Technologies","Materials"),
    ("NUAI","NuScale Power Corp.","Energy"),
    ("IREN","Iris Energy Ltd.","Technology"),
]

ETF = [
    # U.S. Broad Market
    ("SPY",  "SPDR S&P 500 ETF",                "U.S. Broad Market"),
    ("VOO",  "Vanguard S&P 500 ETF",             "U.S. Broad Market"),
    ("VTI",  "Vanguard Total Stock Market ETF",   "U.S. Broad Market"),
    ("QQQ",  "Invesco QQQ (Nasdaq-100)",          "U.S. Broad Market"),
    ("DIA",  "SPDR Dow Jones Industrial Avg ETF", "U.S. Broad Market"),
    ("IWM",  "iShares Russell 2000 ETF",          "U.S. Broad Market"),
    ("MDY",  "SPDR S&P MidCap 400 ETF",           "U.S. Broad Market"),
    # Sectors
    ("XLK",  "Technology Select Sector SPDR",     "Sector"),
    ("XLF",  "Financial Select Sector SPDR",      "Sector"),
    ("XLV",  "Health Care Select Sector SPDR",    "Sector"),
    ("XLE",  "Energy Select Sector SPDR",         "Sector"),
    ("XLI",  "Industrial Select Sector SPDR",     "Sector"),
    ("XLY",  "Consumer Discret. Select Sector",   "Sector"),
    ("XLP",  "Consumer Staples Select Sector",    "Sector"),
    ("XLU",  "Utilities Select Sector SPDR",      "Sector"),
    ("SOXX", "iShares Semiconductor ETF",         "Sector"),
    # International
    ("VXUS", "Vanguard Total Intl. Stock ETF",    "International"),
    ("VEA",  "Vanguard Developed Markets ETF",    "International"),
    ("VWO",  "Vanguard Emerging Markets ETF",     "International"),
    ("EEM",  "iShares MSCI Emerging Markets ETF", "International"),
    ("IEMG", "iShares Core MSCI Emerging Mkts",  "International"),
    # Fixed Income
    ("TLT",  "iShares 20+ Year Treasury Bond",    "Fixed Income"),
    ("IEF",  "iShares 7-10 Year Treasury Bond",   "Fixed Income"),
    ("HYG",  "iShares High Yield Corporate Bond", "Fixed Income"),
    ("LQD",  "iShares IG Corporate Bond ETF",     "Fixed Income"),
    # Commodities
    ("GLD",  "SPDR Gold Shares",                  "Commodities"),
    ("IAU",  "iShares Gold Trust",                "Commodities"),
    ("SLV",  "iShares Silver Trust",              "Commodities"),
    # Dividend / Income
    ("SCHD", "Schwab US Dividend Equity ETF",     "Dividend"),
    ("VYM",  "Vanguard High Dividend Yield ETF",  "Dividend"),
    ("NOBL", "ProShares S&P 500 Div. Aristocrats","Dividend"),
    ("CGDV", "Capital Group Dividend Value ETF",  "Dividend"),
    # Thematic
    ("ARKK", "ARK Innovation ETF",               "Thematic"),
    ("BOTZ", "Global X Robotics & AI ETF",        "Thematic"),
    ("CIBR", "First Trust Nasdaq Cybersecurity",  "Thematic"),
    ("VNQ",  "Vanguard Real Estate ETF",          "Thematic"),
]

ALL_TIERS = [
    ("Large Cap", LARGE_CAP),
    ("Mid Cap",   MID_CAP),
    ("Small Cap", SMALL_CAP),
    ("ETFs",      ETF),
]

# ── Dividend Aristocrats ───────────────────────────────────────────────────────

DIVIDEND_ARISTOCRATS = {
    "ABT","ABBV","ADP","AFL","APD","AOS","BDX","CAT","CB","CINF","CL","CVX",
    "DOV","ECL","EMR","ESS","EXPD","FDS","FRT","GD","GIS","GPC","HRL","HSY",
    "ITW","JNJ","KO","LIN","LOW","MCD","MDT","MMC","NUE","O","PEP","PG","PPG",
    "ROP","ROST","RTX","SHW","SPGI","SYY","TGT","WMT","XOM","BEN","AFL",
    "CHRW","TROW","CTAS",
}

# ── Category Config ────────────────────────────────────────────────────────────

CAT_ORDER  = ["deep_value", "undervalued", "buy_zone", "watchlist", "extended"]
CAT_LABELS = {
    "deep_value":  "🔴 Deep Value",
    "undervalued": "🟠 Undervalued",
    "buy_zone":    "🟢 Buy Zone",
    "watchlist":   "🟡 Watchlist",
    "extended":    "⬜ Extended",
}
CAT_COLORS = {
    "deep_value":  ("#ff6b6b", "#3a1414"),
    "undervalued": ("#ff9f43", "#2d1f0f"),
    "buy_zone":    ("#26de81", "#0d2b1a"),
    "watchlist":   ("#fed330", "#2a250a"),
    "extended":    ("#a4b0be", "#1c2029"),
}
CAT_DESC = {
    "deep_value":  "More than 10% <em>below</em> the 200-Week MA — historically rare entry points.",
    "undervalued": "3–10% <em>below</em> the 200-Week MA — prime buy territory per the strategy.",
    "buy_zone":    "Within ±3% of the 200-Week MA — at or very near the ideal entry.",
    "watchlist":   "3–15% <em>above</em> the 200-Week MA — quality names to watch for a pullback.",
    "extended":    "More than 15% above the 200-Week MA — wait for a better entry.",
}

# ── Fibonacci Helper (defined here so it's available in the data fetch loop) ──

def calc_fib(hist_close, current_price):
    """
    52-week Fibonacci retracement analysis.
    Measures how far price has pulled back from the 52-week swing high.
    Key buy-zone levels: 38.2%, 50.0%, 61.8% (golden ratio).
    """
    recent      = hist_close.tail(52)
    swing_high  = float(recent.max())
    swing_low   = float(recent.min())
    rng         = swing_high - swing_low
    if rng < 0.01:
        return {"fib_zone": "\u2014", "fib_color": "#8b949e", "fib_is_buy": False,
                "fib_retracement": None, "fib_nearest": "\u2014",
                "fib_swing_high": swing_high, "fib_swing_low": swing_low}

    pct_from_high = max(0.0, min(100.0, (swing_high - current_price) / rng * 100))

    FIB_LEVELS = [
        (0.0,   "0%",    False),
        (23.6,  "23.6%", False),
        (38.2,  "38.2%", True),
        (50.0,  "50.0%", True),
        (61.8,  "61.8%", True),
        (78.6,  "78.6%", False),
        (100.0, "100%",  False),
    ]

    nearest                       = min(FIB_LEVELS, key=lambda x: abs(x[0] - pct_from_high))
    fib_pct, fib_name, is_buy_level = nearest
    dist      = abs(pct_from_high - fib_pct)
    TOLERANCE = 4.0
    in_golden = 38.2 <= pct_from_high <= 61.8

    if dist <= TOLERANCE and is_buy_level:
        fib_zone   = f"\U0001f3af {fib_name}"
        fib_color  = "#26de81"
        fib_is_buy = True
    elif in_golden:
        fib_zone   = "\U0001f4d0 Golden Zone"
        fib_color  = "#4ecdc4"
        fib_is_buy = True
    elif dist <= TOLERANCE:
        fib_zone   = f"\u2014 {fib_name}"
        fib_color  = "#fed330"
        fib_is_buy = False
    else:
        fib_zone   = f"~{fib_name}"
        fib_color  = "#8b949e"
        fib_is_buy = False

    return {
        "fib_zone":        fib_zone,
        "fib_color":       fib_color,
        "fib_is_buy":      fib_is_buy,
        "fib_retracement": round(pct_from_high, 1),
        "fib_nearest":     fib_name,
        "fib_swing_high":  round(swing_high, 2),
        "fib_swing_low":   round(swing_low, 2),
    }

# ── Data Fetch ─────────────────────────────────────────────────────────────────

total_stocks = sum(len(s) for _, s in ALL_TIERS)
print(f"Fetching 5-year weekly history for {total_stocks} stocks...\n")

tier_results = {}   # tier_name -> list of result dicts
chart_data   = {}   # ticker -> {labels, prices, wma, wma_p5, wma_m5, wma_p10, wma_m10}

idx = 0
for tier_name, stocks in ALL_TIERS:
    results = []
    print(f"── {tier_name} ({len(stocks)} stocks) ──")
    for ticker, name, sector in stocks:
        idx += 1
        try:
            stock = yf.Ticker(ticker)
            hist  = stock.history(period="5y", interval="1wk")

            if len(hist) < 4:
                print(f"  [{idx:03d}/{total_stocks}] {ticker:6s}: insufficient data, skipping")
                continue

            # Drop incomplete current-week bar (close is NaN before market opens)
            hist = hist.dropna(subset=['Close'])

            if len(hist) < 4:
                print(f"  [{idx:03d}/{total_stocks}] {ticker:6s}: insufficient data after dropna, skipping")
                continue

            window = min(200, len(hist))
            hist['WMA'] = hist['Close'].rolling(window=window).mean()

            current_price = float(hist['Close'].iloc[-1])
            wma_val       = float(hist['WMA'].iloc[-1])

            if pd.isna(wma_val):
                print(f"  [{idx:03d}/{total_stocks}] {ticker:6s}: WMA is NaN, skipping")
                continue

            pct_diff = ((current_price - wma_val) / wma_val) * 100

            if   pct_diff <= -10: category = "deep_value"
            elif pct_diff <=  -3: category = "undervalued"
            elif pct_diff <=   3: category = "buy_zone"
            elif pct_diff <=  15: category = "watchlist"
            else:                  category = "extended"

            mc_str = "N/A"
            years_public = None
            pays_div = False
            pe_ratio = None
            try:
                fi   = stock.fast_info
                mc   = getattr(fi, 'market_cap', None)
                if mc:
                    mc_str = f"${mc/1e12:.2f}T" if mc >= 1e12 else f"${mc/1e9:.0f}B"

                # Years public
                try:
                    fte = getattr(fi, 'first_trade_date_epoch_utc', None)
                    if fte:
                        first_dt = datetime.fromtimestamp(float(fte), tz=timezone.utc)
                        years_public = int((datetime.now(tz=timezone.utc) - first_dt).days / 365.25)
                except:
                    pass

                # Dividend
                try:
                    ldv = getattr(fi, 'last_dividend_value', None)
                    if ldv and float(ldv) > 0:
                        pays_div = True
                except:
                    pass

            except:
                pass

            # PE ratio (trailing; fallback to forward)
            try:
                info_data = stock.info
                pe = info_data.get('trailingPE')
                if pe is None or float(pe) <= 0:
                    pe = info_data.get('forwardPE')
                if pe is not None and float(pe) > 0:
                    pe_ratio = round(float(pe), 1)
            except:
                pass

            # ── Fibonacci retracement (52-week swing) ──
            fib_data = calc_fib(hist['Close'], current_price)

            # ── Chart data: valid-WMA rows only, last 156 weeks (~3 yr) ──
            chart_hist = hist.dropna(subset=['WMA']).tail(156).copy()
            ch_labels  = [d.strftime("%Y-%m-%d") for d in chart_hist.index]
            ch_prices  = [round(float(v), 2) if not pd.isna(v) else None for v in chart_hist['Close']]
            ch_wma     = [round(float(v), 2) if not pd.isna(v) else None for v in chart_hist['WMA']]
            ch_wmap5   = [round(v * 1.05, 2) if v is not None else None for v in ch_wma]
            ch_wmam5   = [round(v * 0.95, 2) if v is not None else None for v in ch_wma]
            ch_wmap10  = [round(v * 1.10, 2) if v is not None else None for v in ch_wma]
            ch_wmam10  = [round(v * 0.90, 2) if v is not None else None for v in ch_wma]

            chart_data[ticker] = {
                "labels":   ch_labels,
                "prices":   ch_prices,
                "wma":      ch_wma,
                "wma_p5":   ch_wmap5,
                "wma_m5":   ch_wmam5,
                "wma_p10":  ch_wmap10,
                "wma_m10":  ch_wmam10,
            }

            arrow = "▲" if pct_diff >= 0 else "▼"
            yrs_str = f"{years_public}y" if years_public is not None else " N/A"
            div_str = "👑" if ticker in DIVIDEND_ARISTOCRATS else ("💰" if pays_div else " —")
            print(f"  [{idx:03d}/{total_stocks}] {ticker:6s}: ${current_price:>9.2f} | 200WMA ${wma_val:>9.2f} | {arrow}{abs(pct_diff):5.1f}% → {CAT_LABELS[category].split(' ',1)[1]}  {yrs_str}  {div_str}")

            results.append({
                "ticker":      ticker,
                "name":        name,
                "sector":      sector,
                "price":       round(current_price, 2),
                "wma200":      round(wma_val, 2),
                "pct_diff":    round(pct_diff, 2),
                "category":    category,
                "pe_ratio":    pe_ratio,
                "market_cap":  mc_str,
                "weeks_data":  len(hist),
                "full_200wma": len(hist) >= 200,
                "years_public":     years_public,
                "pays_div":         pays_div,
                "fib_zone":         fib_data["fib_zone"],
                "fib_color":        fib_data["fib_color"],
                "fib_is_buy":       fib_data["fib_is_buy"],
                "fib_retracement":  fib_data["fib_retracement"],
                "fib_nearest":      fib_data["fib_nearest"],
                "fib_swing_high":   fib_data["fib_swing_high"],
                "fib_swing_low":    fib_data["fib_swing_low"],
            })

            time.sleep(0.25)

        except Exception as e:
            print(f"  [{idx:03d}/{total_stocks}] {ticker:6s}: ERROR — {e}")

    results.sort(key=lambda x: (CAT_ORDER.index(x['category']), x['pct_diff']))
    tier_results[tier_name] = results
    print()

# ── Conviction Signals ────────────────────────────────────────────────────────
import os as _os
_CURATED_PATH = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'conviction_signals.json')
_curated_signals = []
if _os.path.exists(_CURATED_PATH):
    try:
        with open(_CURATED_PATH) as _f:
            _curated_signals = json.load(_f).get('signals', [])
        print(f"Loaded {len(_curated_signals)} curated conviction signal(s)")
    except Exception as _ce:
        print(f"Warning: could not load conviction_signals.json — {_ce}")

conviction_map = {}  # ticker -> list of signal dicts
for _sig in _curated_signals:
    conviction_map.setdefault(_sig['ticker'], []).append(_sig)

_CUTOFF   = datetime.now() - timedelta(days=90)
_etf_set  = {t for t, _, _ in ETF}
_all_tkrs = [r['ticker'] for _rv in tier_results.values() for r in _rv]

print(f"Fetching insider transactions ({len(_all_tkrs)} tickers, skipping ETFs)...")
_insider_rows = 0
for _ticker in _all_tkrs:
    if _ticker in _etf_set:
        continue
    try:
        _stk = yf.Ticker(_ticker)
        _df  = _stk.insider_transactions
        if _df is None or (hasattr(_df, 'empty') and _df.empty):
            time.sleep(0.04)
            continue
        for _, _row in _df.iterrows():
            _txn = str(_row.get('Transaction', '')).lower()
            if 'purchase' not in _txn and 'buy' not in _txn:
                continue
            _dv = _row.get('Date') or _row.get('Start Date')
            if _dv is None:
                continue
            try:
                _dts = pd.Timestamp(_dv)
                if _dts < pd.Timestamp(_CUTOFF):
                    continue
            except Exception:
                continue
            _ins = str(_row.get('Insider', 'Unknown'))
            _rel = str(_row.get('Relation', ''))
            _shr = _row.get('#Shares', 0)
            _val = _row.get('Value', None)
            try:    _si = int(float(str(_shr).replace(',', '')))
            except: _si = 0
            try:    _vf = float(str(_val).replace(',','').replace('$','')) if _val else None
            except: _vf = None
            if _si <= 0:
                continue
            conviction_map.setdefault(_ticker, []).append({
                'type':         'insider_purchase',
                'actor':        _ins,
                'role':         _rel,
                'shares':       _si,
                'value_usd':    round(_vf) if _vf else None,
                'date':         _dts.strftime('%Y-%m-%d'),
                'date_display': _dts.strftime('%B %Y'),
                'note':         'Open-market purchase — always verify 10b5-1 plan status on SEC EDGAR before acting.',
                'scheduled':    False,
            })
            _insider_rows += 1
        time.sleep(0.06)
    except Exception:
        time.sleep(0.04)

print(f"  ✓ {len(conviction_map)} tickers with conviction signals ({_insider_rows} automated insider rows)\n")

# ── HTML Helpers ───────────────────────────────────────────────────────────────

def pct_cell(pct):
    if   pct <= -10: c = "#ff6b6b"
    elif pct <=  -3: c = "#ff9f43"
    elif pct <=   3: c = "#26de81"
    elif pct <=  15: c = "#fed330"
    else:            c = "#a4b0be"
    arrow = "▲" if pct >= 0 else "▼"
    sign  = "+" if pct >= 0 else ""
    return f'<td class="num pct" style="color:{c};font-weight:600">{arrow}&nbsp;{sign}{pct:.1f}%</td>'

def bar_html(pct):
    MIN, MAX = -40, 60
    clamped   = max(MIN, min(MAX, pct))
    zero_pct  = (0 - MIN) / (MAX - MIN) * 100
    val_pct   = (clamped - MIN) / (MAX - MIN) * 100
    width     = abs(val_pct - zero_pct)
    left      = min(val_pct, zero_pct)
    fill      = "#26de81" if pct >= 0 else "#ff6b6b"
    return (
        f'<div class="bar-wrap">'
        f'<div class="bar-track">'
        f'<div class="bar-center" style="left:{zero_pct:.1f}%"></div>'
        f'<div class="bar-fill" style="left:{left:.1f}%;width:{width:.1f}%;background:{fill}"></div>'
        f'</div></div>'
    )

def pe_cell(pe):
    if pe is None or pe <= 0:
        return '<td class="num pe-col muted">—</td>'
    if   pe < 15: c = "#26de81"   # green  — value
    elif pe < 25: c = "#e6edf3"   # white  — fair
    elif pe < 40: c = "#fed330"   # yellow — growth premium
    else:         c = "#ff9f43"   # orange — expensive
    return f'<td class="num pe-col" style="color:{c}" title="P/E Ratio">{pe:.1f}x</td>'

def fib_cell(r):
    fib_ret  = r.get("fib_retracement")
    fib_zone = r.get("fib_zone", "—")
    fib_c    = r.get("fib_color", "#8b949e")
    fib_high = r.get("fib_swing_high", 0)
    fib_low  = r.get("fib_swing_low", 0)
    if fib_ret is None:
        return '<td class="fib-td muted">—</td>'
    tip = f"52wk High: ${fib_high:,.2f} | Low: ${fib_low:,.2f} | Retrace: {fib_ret:.1f}% from high"
    return f'<td class="fib-td" title="{tip}"><span class="fib-badge" style="color:{fib_c}">{fib_zone}</span></td>'

def div_badge_html(ticker, pays_div):
    if ticker in DIVIDEND_ARISTOCRATS:
        return '<span class="div-yes aristocrat" title="Dividend Aristocrat or King — 25+ consecutive years of consecutive dividend increases">👑 Yes</span>'
    elif pays_div:
        return '<span class="div-yes payer">Yes</span>'
    else:
        return '<span class="div-no">No</span>'

def conv_cell(ticker, conv_map):
    sigs = (conv_map or {}).get(ticker, [])
    if not sigs:
        return '<td class="conv-td muted">—</td>'
    types  = {s.get('type', '') for s in sigs}
    badges = ''
    if 'insider_purchase' in types: badges += '👤'
    if 'company_buyback'  in types: badges += '🏦'
    tip = f"{len(sigs)} conviction signal(s) — see Leadership Conviction section below"
    return f'<td class="conv-td"><a href="#tier-conviction" title="{tip}" style="text-decoration:none;font-size:14px">{badges}</a></td>'

# ── Build Sections HTML ────────────────────────────────────────────────────────

def build_conviction_html(conv_map, all_res):
    """Build the Leadership Conviction section."""
    lookup = {r['ticker']: r for r in all_res}
    flat   = []
    for ticker, sigs in conv_map.items():
        company = lookup.get(ticker, {}).get('name', ticker)
        for s in sigs:
            flat.append((ticker, company, s))
    if not flat:
        return ''
    flat.sort(key=lambda x: x[2].get('date', '1900-01-01'), reverse=True)

    cards = ''
    for ticker, company, sig in flat:
        stype     = sig.get('type', 'insider_purchase')
        actor     = sig.get('actor', 'Unknown')
        role      = sig.get('role', '')
        shares    = sig.get('shares', 0)
        value_usd = sig.get('value_usd')
        date_disp = sig.get('date_display', sig.get('date', ''))
        note      = sig.get('note', '')
        scheduled = sig.get('scheduled', False)

        emoji    = '🏦' if stype == 'company_buyback' else '👤'
        type_lbl = 'Company Buyback' if stype == 'company_buyback' else 'Insider Purchase'
        type_col = '#58a6ff' if stype == 'company_buyback' else '#26de81'
        left_col = '#58a6ff' if stype == 'company_buyback' else '#26de81'

        sched_badge = '' if scheduled else '<span class="conv-nsched">🔴 Non-Scheduled</span>'
        shares_str  = f"{shares:,}" if shares else '—'
        val_str = ''
        if value_usd:
            val_str = f'~${value_usd/1e6:.1f}M' if value_usd >= 1_000_000 else f'~${value_usd/1e3:.0f}K'
        role_str = f' · {role}' if role and role not in ('Unknown', 'nan', '') else ''

        cards += f"""
    <div class="conv-card" style="border-left-color:{left_col}">
      <div class="conv-top">
        <div class="conv-left">
          <span class="conv-ticker">{ticker}</span>
          <span class="conv-company">{company}</span>
        </div>
        <div class="conv-right">
          {sched_badge}
          <span class="conv-type" style="color:{type_col};border-color:{type_col}40">{emoji} {type_lbl}</span>
        </div>
      </div>
      <div class="conv-details">
        <span class="conv-actor">{actor}{role_str}</span>
        <span class="conv-sep">·</span>
        <span class="conv-shares">{shares_str} shares{(' · ' + val_str) if val_str else ''}</span>
        <span class="conv-sep">·</span>
        <span class="conv-date">{date_disp}</span>
      </div>
      <div class="conv-note">{note}</div>
    </div>"""

    n = len(flat)
    plural = 's' if n != 1 else ''
    return f"""
  <div class="conv-section" id="tier-conviction">
    <div class="tier-header">
      <div class="tier-left">
        <h2 class="tier-title">💡 Leadership Conviction</h2>
        <span class="tier-count">{n} signal{plural}</span>
      </div>
    </div>
    <p class="conv-subtitle">Non-routine insider open-market purchases &amp; discretionary company buybacks — decision-makers putting real capital behind their conviction. Excludes pre-scheduled 10b5-1 plan transactions where identifiable. 👤 = insider purchase &nbsp;·&nbsp; 🏦 = company buyback</p>
    <div class="conv-grid">{cards}
    </div>
    <p class="conv-footnote">⚠️ Automated insider data sourced via SEC Form 4 / Yahoo Finance. Always verify 10b5-1 plan status directly on SEC EDGAR before acting on any insider signal. Curated buyback entries (🏦) added manually — see <code>conviction_signals.json</code> to add new ones. <em>Not financial advice.</em></p>
  </div>"""

def build_tier_html(tier_name, results, conv_map=None):
    if not results:
        return ""

    # Summary pills for this tier
    counts = {c: len([r for r in results if r['category'] == c]) for c in CAT_ORDER}
    pills = ""
    for cat in CAT_ORDER:
        if counts[cat]:
            c, _ = CAT_COLORS[cat]
            lbl = CAT_LABELS[cat].split(" ",1)[1]
            pills += f'<span class="tier-pill" style="color:{c};border-color:{c}40;background:{c}12">{lbl} <b>{counts[cat]}</b></span>'

    rows_html = ""
    for r in results:
        note  = "" if r['full_200wma'] else '<sup class="warn" title="&lt;200 weeks of data">†</sup>'

        cat_c, cat_bg = CAT_COLORS[r['category']]
        cat_lbl = CAT_LABELS[r['category']].split(" ",1)[1]

        ticker_safe = r['ticker'].replace('-', '_')

        yrs_display = f"{r['years_public']} yrs" if r['years_public'] is not None else "N/A"
        div_html = div_badge_html(r['ticker'], r['pays_div'])

        rows_html += f"""
    <tr class="stock-row" onclick="toggleChart('{ticker_safe}')" id="row-{ticker_safe}" data-cat="{r['category']}">
      <td class="ticker-cell">
        <span class="ticker">{r['ticker']}{note}</span>
        <span class="expand-icon" id="icon-{ticker_safe}">▶</span>
      </td>
      <td class="company">{r['name']}</td>
      <td><span class="sector-pill">{r['sector']}</span></td>
      <td class="num muted yrs-pub">{yrs_display}</td>
      <td class="div-td">{div_html}</td>
      <td class="num">${r['price']:,.2f}</td>
      <td class="num muted">${r['wma200']:,.2f}</td>
      {pct_cell(r['pct_diff'])}
      <td class="bar-td">{bar_html(r['pct_diff'])}</td>
      <td><span class="cat-badge" style="color:{cat_c};background:{cat_bg};border:1px solid {cat_c}40">{cat_lbl}</span></td>
      <td class="num muted mc">{r['market_cap']}</td>
      {pe_cell(r['pe_ratio'])}
      {fib_cell(r)}
      {conv_cell(r['ticker'], conv_map)}
    </tr>
    <tr class="chart-row" id="chart-{ticker_safe}" style="display:none">
      <td colspan="14">
        <div class="chart-container">
          <div class="chart-header">
            <span class="chart-title">{r['ticker']} — {r['name']}</span>
            <span class="chart-sub">Weekly Close vs 200-Week Moving Average · Last 200 Weeks</span>
            <span class="chart-stat" style="color:{cat_c}">{'+' if r['pct_diff']>=0 else ''}{r['pct_diff']:.1f}% vs 200WMA</span>
          </div>
          <canvas id="canvas-{ticker_safe}" height="180"></canvas>
        </div>
      </td>
    </tr>"""

    return f"""
  <div class="tier-section" id="tier-{tier_name.replace(' ','-').lower()}">
    <div class="tier-header">
      <div class="tier-left">
        <h2 class="tier-title">{tier_name}</h2>
        <span class="tier-count">{len(results)} stocks</span>
      </div>
      <div class="tier-pills">{pills}</div>
    </div>
    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Ticker</th><th>Company</th><th>Sector</th>
            <th class="num">Yrs Public</th><th title="👑 = Dividend Aristocrat or King (25+ yrs of consecutive increases) | Yes = pays div | No = none">Div ℹ️</th>
            <th class="num">Price</th><th class="num">200-WMA</th>
            <th class="num">vs 200-WMA</th><th>Position</th>
            <th>Status</th><th class="num">Mkt Cap</th><th class="num">P/E Ratio</th>
            <th class="fib-td" title="Fibonacci retracement from 52-week swing high/low. 🎯 = at key Fib level (38.2 / 50 / 61.8%). 📐 = inside golden zone (38.2–61.8% retracement). These levels act as support in an uptrend.">Fib Zone ℹ️</th>
            <th class="conv-th" title="💡 Leadership Conviction — 👤 insider open-market purchase or 🏦 non-scheduled company buyback in the last 90 days. Click to jump to detail section.">💡</th>
          </tr>
        </thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>
  </div>"""

all_sections = ""
for tier_name, results in tier_results.items():
    all_sections += build_tier_html(tier_name, results, conv_map=conviction_map)

# ── Global Summary Stats ───────────────────────────────────────────────────────

all_results = [r for results in tier_results.values() for r in results]
conviction_section = build_conviction_html(conviction_map, all_results)
global_counts = {c: len([r for r in all_results if r['category'] == c]) for c in CAT_ORDER}

summary_cards = ""
for cat in CAT_ORDER:
    c, bg = CAT_COLORS[cat]
    lbl   = CAT_LABELS[cat].split(" ",1)[1]
    emoji = CAT_LABELS[cat].split(" ")[0]
    summary_cards += f"""
    <div class="stat-card" style="border-top:3px solid {c}">
      <div class="stat-num" style="color:{c}">{global_counts[cat]}</div>
      <div class="stat-lbl">{emoji} {lbl}</div>
    </div>"""

now_str = datetime.now().strftime("%B %d, %Y at %I:%M %p EDT")

# ── Chart JSON ─────────────────────────────────────────────────────────────────
# Convert tickers with - to _ for JS variable names
chart_data_js = {}
for ticker, data in chart_data.items():
    chart_data_js[ticker.replace('-', '_')] = data

chart_json = json.dumps(chart_data_js, separators=(',', ':'))

# ── Full HTML ──────────────────────────────────────────────────────────────────

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>200-Week MA Stock Scanner</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0 }}
:root {{
  --bg:     #0d1117;
  --bg2:    #161b22;
  --bg3:    #21262d;
  --border: #30363d;
  --text:   #e6edf3;
  --muted:  #8b949e;
  --font:   -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  --mono:   "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
}}
html {{ scroll-behavior: smooth }}
body {{ background:var(--bg); color:var(--text); font-family:var(--font); font-size:14px; line-height:1.5 }}

/* Header */
header {{
  background:var(--bg2); border-bottom:1px solid var(--border);
  padding:18px 32px; display:flex; align-items:center; gap:16px;
  position:sticky; top:0; z-index:100;
}}
.logo {{ font-size:26px }}
.htext h1 {{ font-size:18px; font-weight:700 }}
.htext p  {{ font-size:12px; color:var(--muted); margin-top:1px }}
.updated  {{ margin-left:auto; font-size:11px; color:var(--muted); text-align:right; line-height:1.6 }}

/* Strategy banner */
.strategy {{
  margin:20px 32px 0; padding:13px 18px;
  background:var(--bg2); border:1px solid var(--border);
  border-left:4px solid #58a6ff; border-radius:6px;
  font-size:13px; color:var(--muted); font-style:italic;
}}
.strategy strong {{ color:#58a6ff; font-style:normal }}

/* Summary stats */
.stats {{ display:flex; gap:14px; padding:20px 32px 0; flex-wrap:wrap }}
.stat-card {{
  background:var(--bg2); border:1px solid var(--border);
  border-radius:8px; padding:12px 18px; flex:1; min-width:110px; text-align:center;
}}
.stat-num {{ font-size:26px; font-weight:700; line-height:1 }}
.stat-lbl {{ font-size:11px; color:var(--muted); margin-top:3px }}

/* Nav tabs */
.tier-nav {{
  display:flex; gap:8px; padding:20px 32px 0; flex-wrap:wrap;
}}
.tier-nav a {{
  padding:6px 16px; border-radius:20px; font-size:13px; font-weight:500;
  text-decoration:none; color:var(--muted); border:1px solid var(--border);
  transition:all .15s;
}}
.tier-nav a:hover {{ color:var(--text); border-color:#58a6ff; background:#58a6ff15 }}

/* Main */
main {{ padding:24px 32px 60px }}

/* Tier section */
.tier-section {{ margin-bottom:36px }}
.tier-header {{
  display:flex; align-items:center; justify-content:space-between;
  flex-wrap:wrap; gap:10px; margin-bottom:10px;
}}
.tier-left {{ display:flex; align-items:center; gap:10px }}
.tier-title {{ font-size:18px; font-weight:700 }}
.tier-count {{
  display:inline-block; padding:2px 10px; border-radius:12px;
  font-size:12px; font-weight:600; background:var(--bg3); color:var(--muted);
  border:1px solid var(--border);
}}
.tier-pills {{ display:flex; gap:6px; flex-wrap:wrap }}
.tier-pill {{
  padding:2px 10px; border-radius:12px; font-size:11px; font-weight:500;
  border:1px solid; white-space:nowrap;
}}

/* Table */
.table-wrap {{
  overflow-x:auto; border:1px solid var(--border); border-radius:8px;
}}
table {{ width:100%; border-collapse:collapse }}
thead th {{
  background:var(--bg3); padding:8px 12px; text-align:left;
  font-size:11px; font-weight:600; color:var(--muted);
  text-transform:uppercase; letter-spacing:.04em;
  border-bottom:1px solid var(--border); white-space:nowrap;
}}
th.num {{ text-align:right }}
.stock-row {{
  border-bottom:1px solid var(--border); cursor:pointer; transition:background .1s;
}}
.stock-row:hover {{ background:var(--bg3) }}
.stock-row td {{ padding:9px 12px; vertical-align:middle; white-space:nowrap }}
.chart-row td {{ padding:0; background:var(--bg2) }}
.chart-row:last-child td {{ border-radius:0 0 8px 8px }}

/* Ticker cell */
.ticker-cell {{ display:flex; align-items:center; gap:6px }}
.ticker {{
  font-family:var(--mono); font-weight:700; font-size:14px;
  color:#58a6ff; letter-spacing:.02em;
}}
.expand-icon {{
  font-size:10px; color:var(--muted); transition:transform .2s;
  display:inline-block;
}}
.expand-icon.open {{ transform:rotate(90deg) }}
.company {{ color:var(--text); max-width:180px; overflow:hidden; text-overflow:ellipsis }}
.num {{ text-align:right; font-variant-numeric:tabular-nums }}
.muted {{ color:var(--muted) }}
.warn {{ color:#fed330; font-size:10px }}

/* Sector pill */
.sector-pill {{
  display:inline-block; padding:2px 8px; border-radius:10px;
  font-size:11px; background:var(--bg3); border:1px solid var(--border);
  color:var(--muted); white-space:nowrap;
}}

/* Category badge */
.cat-badge {{
  display:inline-block; padding:2px 9px; border-radius:4px;
  font-size:11px; font-weight:600; white-space:nowrap;
}}

/* Dividend badge */
.div-td {{ text-align:center }}
.div-yes {{ font-size:12px; font-weight:600; color:#26de81 }}
.div-yes.aristocrat {{ color:#fed330 }}
.div-no {{ font-size:12px; color:var(--muted) }}

/* Years public */
.yrs-pub {{ text-align:center; color:var(--muted) }}

/* Fibonacci badge */
.fib-td {{ text-align:center; min-width:110px }}
.fib-badge {{ font-size:12px; font-weight:600; white-space:nowrap; cursor:default }}

/* Position bar */
.bar-td {{ min-width:130px }}
.bar-wrap {{ width:120px }}
.bar-track {{
  position:relative; height:6px; background:var(--bg3);
  border-radius:3px; overflow:hidden;
}}
.bar-center {{
  position:absolute; top:0; bottom:0; width:1px;
  background:var(--border); z-index:1;
}}
.bar-fill {{
  position:absolute; top:0; bottom:0; border-radius:3px; z-index:2;
}}

/* Chart container */
.chart-container {{
  padding:16px 20px 20px; border-top:1px solid var(--border);
}}
.chart-header {{
  display:flex; align-items:baseline; gap:14px; margin-bottom:12px; flex-wrap:wrap;
}}
.chart-title {{ font-weight:700; font-size:15px }}
.chart-sub   {{ font-size:12px; color:var(--muted) }}
.chart-stat  {{ font-size:13px; font-weight:700; margin-left:auto }}

/* Footer */
footer {{
  border-top:1px solid var(--border); padding:18px 32px;
  font-size:12px; color:var(--muted); background:var(--bg2);
}}

/* Notes box (legacy) */
.notes-box {{
  margin-top:20px; padding:12px 16px; background:var(--bg2);
  border:1px solid var(--border); border-radius:6px;
  font-size:12px; color:var(--muted); line-height:1.8;
}}

/* ── Legend / Key section ── */
.legend-section {{ margin-top:0; margin-bottom:36px }}
.legend-heading {{
  font-size:16px; font-weight:700; color:var(--text);
  margin-bottom:14px; padding-bottom:10px;
  border-bottom:1px solid var(--border);
}}
.legend-grid {{
  display:grid; grid-template-columns:repeat(3,1fr); gap:14px;
}}
.legend-card {{
  background:var(--bg2); border:1px solid var(--border);
  border-radius:8px; padding:18px;
}}
.legend-card-title {{
  font-size:13px; font-weight:700; color:var(--text);
  margin-bottom:10px; padding-bottom:9px;
  border-bottom:1px solid var(--border);
}}
.legend-card-desc {{
  font-size:12px; color:var(--muted); line-height:1.65;
  margin-bottom:14px;
}}
.legend-rows {{ display:flex; flex-direction:column; gap:10px }}
.legend-row {{ display:flex; align-items:flex-start; gap:10px }}
.legend-lbadge {{
  display:inline-block; padding:2px 9px; border-radius:4px;
  font-size:11px; font-weight:600; white-space:nowrap;
  flex-shrink:0; min-width:86px; text-align:center;
}}
.legend-lbadge.w126 {{ min-width:126px }}
.legend-pe-val {{
  font-size:12px; font-weight:700; white-space:nowrap;
  flex-shrink:0; min-width:44px; font-family:var(--mono);
  padding-top:1px;
}}
.legend-text {{ font-size:12px; color:var(--muted); line-height:1.55 }}
.legend-text strong {{ color:var(--text) }}
.legend-footnote {{
  margin-top:14px; padding:11px 15px; background:var(--bg2);
  border:1px solid var(--border); border-radius:6px;
  font-size:12px; color:var(--muted); line-height:2.0;
}}
@media (max-width:960px) {{
  .legend-grid {{ grid-template-columns:1fr }}
}}

/* Conviction column */
.conv-th {{ text-align:center; min-width:44px; font-size:14px }}
.conv-td {{ text-align:center }}
/* Conviction section */
.conv-section {{ margin-bottom:36px }}
.conv-subtitle {{ font-size:13px; color:var(--muted); margin-bottom:16px; font-style:italic; line-height:1.6; max-width:860px }}
.conv-grid {{ display:flex; flex-direction:column; gap:12px }}
.conv-card {{
  background:var(--bg2); border:1px solid var(--border);
  border-radius:8px; padding:16px 18px; border-left:3px solid #58a6ff;
}}
.conv-top {{ display:flex; align-items:flex-start; justify-content:space-between; flex-wrap:wrap; gap:8px; margin-bottom:8px }}
.conv-left {{ display:flex; align-items:center; gap:10px }}
.conv-ticker {{ font-family:var(--mono); font-weight:700; font-size:15px; color:#58a6ff }}
.conv-company {{ font-size:13px; color:var(--muted) }}
.conv-right {{ display:flex; align-items:center; gap:8px; flex-wrap:wrap }}
.conv-nsched {{ font-size:11px; font-weight:600; padding:2px 8px; border-radius:4px; background:#3a141499; color:#ff6b6b; border:1px solid #ff6b6b40 }}
.conv-type {{ font-size:11px; font-weight:600; padding:2px 8px; border-radius:4px; border:1px solid }}
.conv-details {{ font-size:13px; color:var(--muted); margin-bottom:6px; display:flex; flex-wrap:wrap; gap:6px; align-items:center }}
.conv-actor {{ color:var(--text); font-weight:500 }}
.conv-shares {{ color:var(--text) }}
.conv-date {{ color:var(--muted) }}
.conv-sep {{ color:var(--border) }}
.conv-note {{ font-size:12px; color:var(--muted); font-style:italic; line-height:1.5 }}
.conv-footnote {{ margin-top:14px; font-size:12px; color:var(--muted); line-height:1.7; padding:10px 14px; background:var(--bg2); border:1px solid var(--border); border-radius:6px }}
.conv-footnote code {{ font-family:var(--mono); color:#58a6ff; font-size:11px }}
@media (max-width:768px) {{
  header, .stats, main, .strategy, .tier-nav {{ padding-left:14px; padding-right:14px }}
  .mc, .pe-col, .yrs-pub, .fib-td, .conv-td, .conv-th {{ display:none }}
  .bar-td {{ display:none }}
}}
</style>
</head>
<body>

<header>
  <div class="logo">📈</div>
  <div class="htext">
    <h1>200-Week Moving Average Scanner</h1>
    <p>Large · Mid · Small Cap stocks ranked by proximity to their 200-week moving average</p>
  </div>
  <div class="updated">Last updated<br><strong>{now_str}</strong></div>
</header>

<div class="strategy">
  <strong>"Strategy:"</strong> "If all you ever did was buy high-quality stocks on the 200-week moving average,
  you would beat the S&amp;P 500 by a large margin over time. The problem is,
  few human beings have that kind of discipline."
</div>

<div class="stats">
  {summary_cards}
</div>

<div class="tier-nav">
  <a href="#tier-large-cap">📊 Large Cap ({len(tier_results.get("Large Cap",[]))})</a>
  <a href="#tier-mid-cap">🚀 Mid Cap ({len(tier_results.get("Mid Cap",[]))})</a>
  <a href="#tier-small-cap">🌱 Small Cap ({len(tier_results.get("Small Cap",[]))})</a>
  <a href="#tier-etfs">🌎 ETFs ({len(tier_results.get("ETFs",[]))})</a>
  <a href="#tier-conviction">💡 Conviction ({len(conviction_map)})</a>
</div>

<main>
  <div class="legend-section">
    <h2 class="legend-heading">📖 Column Reference Guide</h2>
    <div class="legend-grid">

      <!-- ── STATUS CARD ── -->
      <div class="legend-card">
        <div class="legend-card-title">📊 Status — 200-Week Moving Average</div>
        <p class="legend-card-desc">Ranks each stock by how far its current price sits above or below its <strong style="color:var(--text)">200-Week Moving Average (200-WMA)</strong> — the average closing price over the last ~4 years. Stocks near or below their 200-WMA have historically offered the strongest long-term entry points.</p>
        <div class="legend-rows">
          <div class="legend-row">
            <span class="legend-lbadge" style="color:#ff6b6b;background:#3a1414;border:1px solid #ff6b6b40">🔴 Deep Value</span>
            <span class="legend-text"><strong>&gt;10% below</strong> the 200-WMA. Historically rare. The stock has dropped well below its long-term average — highest potential upside, but worth understanding <em>why</em> it fell.</span>
          </div>
          <div class="legend-row">
            <span class="legend-lbadge" style="color:#ff9f43;background:#2d1f0f;border:1px solid #ff9f4340">🟠 Undervalued</span>
            <span class="legend-text"><strong>3–10% below</strong> the 200-WMA. Prime buy territory per the strategy — price is approaching its long-term average from below.</span>
          </div>
          <div class="legend-row">
            <span class="legend-lbadge" style="color:#26de81;background:#0d2b1a;border:1px solid #26de8140">🟢 Buy Zone</span>
            <span class="legend-text"><strong>Within ±3%</strong> of the 200-WMA. The ideal entry point — price is right at its long-term average, the sweet spot of the strategy.</span>
          </div>
          <div class="legend-row">
            <span class="legend-lbadge" style="color:#fed330;background:#2a250a;border:1px solid #fed33040">🟡 Watchlist</span>
            <span class="legend-text"><strong>3–15% above</strong> the 200-WMA. Quality stock trading above its average — add to your watchlist and wait for a pullback to Buy Zone or below.</span>
          </div>
          <div class="legend-row">
            <span class="legend-lbadge" style="color:#a4b0be;background:#1c2029;border:1px solid #a4b0be40">⬜ Extended</span>
            <span class="legend-text"><strong>&gt;15% above</strong> the 200-WMA. Overextended — the stock has run far above its average. Patience required; a better entry will likely come.</span>
          </div>
        </div>
      </div>

      <!-- ── P/E RATIO CARD ── -->
      <div class="legend-card">
        <div class="legend-card-title">📉 P/E Ratio (Price-to-Earnings)</div>
        <p class="legend-card-desc">How much investors pay for each <strong style="color:var(--text)">$1 of annual profit</strong>. A stock at $50 earning $5/share has a P/E of 10x. Lower generally = cheaper relative to earnings. Uses trailing 12-month P/E; falls back to forward P/E when unavailable.</p>
        <div class="legend-rows">
          <div class="legend-row">
            <span class="legend-pe-val" style="color:#26de81">&lt;15x</span>
            <span class="legend-text"><strong>Value territory.</strong> Cheap relative to earnings. Common in mature, slow-growth industries. May signal an undervalued opportunity — or a declining business.</span>
          </div>
          <div class="legend-row">
            <span class="legend-pe-val" style="color:#e6edf3">15–25x</span>
            <span class="legend-text"><strong>Fair value.</strong> The historical average for the S&amp;P 500. Reasonable pricing for a stable, profitable company with moderate growth.</span>
          </div>
          <div class="legend-row">
            <span class="legend-pe-val" style="color:#fed330">25–40x</span>
            <span class="legend-text"><strong>Growth premium.</strong> Investors are paying up for expected future earnings growth. Justified if the company is expanding fast; risky if growth disappoints.</span>
          </div>
          <div class="legend-row">
            <span class="legend-pe-val" style="color:#ff9f43">&gt;40x</span>
            <span class="legend-text"><strong>Expensive.</strong> Very high expectations baked in. Earnings must grow substantially to justify the price — elevated risk if the growth story falters.</span>
          </div>
          <div class="legend-row">
            <span class="legend-pe-val" style="color:#8b949e">—</span>
            <span class="legend-text"><strong>Not available.</strong> Company is unprofitable (negative earnings make P/E meaningless), or data is unavailable from the data source.</span>
          </div>
        </div>
      </div>

      <!-- ── FIB ZONE CARD ── -->
      <div class="legend-card">
        <div class="legend-card-title">📐 Fib Zone (Fibonacci Retracement)</div>
        <p class="legend-card-desc">Measures how far a stock has <strong style="color:var(--text)">pulled back from its 52-week high</strong>. The key Fibonacci levels — 38.2%, 50%, and 61.8% — tend to act as natural support zones during an uptrend. Hover any badge for the exact 52-week high, low, and retracement %.</p>
        <div class="legend-rows">
          <div class="legend-row">
            <span class="legend-lbadge w126" style="color:#26de81">🎯 61.8% — Golden Ratio</span>
            <span class="legend-text"><strong>Strongest level.</strong> Derived from the golden ratio (1.618) — the most-watched Fibonacci support. Major reversals most often occur here during an uptrend. Highest-conviction entry of the three.</span>
          </div>
          <div class="legend-row">
            <span class="legend-lbadge w126" style="color:#26de81">🎯 50.0% — Midpoint</span>
            <span class="legend-text"><strong>Psychological level.</strong> Not a true Fibonacci number, but traders widely treat the halfway point of a move as key support/resistance. Broadly followed and self-reinforcing.</span>
          </div>
          <div class="legend-row">
            <span class="legend-lbadge w126" style="color:#26de81">🎯 38.2% — Shallow</span>
            <span class="legend-text"><strong>Strong trend signal.</strong> A modest pullback — bulls stepped in early. Indicates a robust uptrend. Least downside risk of the three key levels, but also least upside if the trend stalls.</span>
          </div>
          <div class="legend-row">
            <span class="legend-lbadge w126" style="color:#4ecdc4">📐 Golden Zone</span>
            <span class="legend-text"><strong>38.2–61.8% range.</strong> Price is inside the golden zone but not pinned to a specific level. Still a favorable area — most traders consider the full 38.2–61.8% band the primary buy zone in an uptrend.</span>
          </div>
          <div class="legend-row">
            <span class="legend-lbadge w126" style="color:#fed330;background:transparent">— 23.6% / 78.6%</span>
            <span class="legend-text"><strong>Minor Fib levels.</strong> 23.6% = very shallow pullback (powerful, fast-moving trend). 78.6% = deep retracement (trend under pressure — watch for a breakdown below the swing low).</span>
          </div>
          <div class="legend-row">
            <span class="legend-lbadge w126" style="color:#8b949e">~xx%</span>
            <span class="legend-text"><strong>Between levels.</strong> Price is not near any key Fibonacci level. No actionable Fib signal at this time — consider other indicators or wait for price to reach a level.</span>
          </div>
        </div>
      </div>

    </div><!-- /legend-grid -->

    <div class="legend-footnote">
      <strong style="color:var(--text)">Other notes:</strong>
      Click any stock row to expand its price chart ·
      <span class="warn">†</span> = fewer than 200 weeks of price data (200-WMA is an approximation) ·
      <strong style="color:#fed330">👑 Crown</strong> = Dividend Aristocrat or King — 25+ consecutive years of dividend increases (e.g. KO, JNJ, PG) ·
      <strong style="color:#26de81">Yes</strong> = pays a dividend ·
      <span style="color:var(--muted)">No</span> = no dividend ·
      Data via Yahoo Finance (yfinance) · <em>Not financial advice.</em>
    </div>
  </div>

{all_sections}
{conviction_section}
</main>

<footer>
  <strong>200-Week MA Stock Scanner v4</strong> · Built by Tuchus 🐶 ·
  230 stocks · Leadership Conviction signals · Data: Yahoo Finance · Not financial advice · {now_str}
</footer>

<script>
// ── Embedded chart data ──────────────────────────────────────────────────────
const CHART_DATA = {chart_json};

const activeCharts = {{}};

function toggleChart(ticker) {{
  const row  = document.getElementById('chart-' + ticker);
  const icon = document.getElementById('icon-' + ticker);
  if (!row) return;

  if (row.style.display === 'none') {{
    row.style.display = '';
    icon.classList.add('open');
    if (!activeCharts[ticker]) {{
      setTimeout(() => renderChart(ticker), 30);
    }}
  }} else {{
    row.style.display = 'none';
    icon.classList.remove('open');
  }}
}}

function renderChart(ticker) {{
  const data = CHART_DATA[ticker];
  if (!data) return;

  const canvas = document.getElementById('canvas-' + ticker);
  if (!canvas) return;

  const ctx = canvas.getContext('2d');

  activeCharts[ticker] = new Chart(ctx, {{
    type: 'line',
    data: {{
      labels: data.labels,
      datasets: [
        // +10% band (top edge, invisible line)
        {{
          label: '+10% zone',
          data: data.wma_p10,
          borderColor: 'transparent',
          backgroundColor: 'rgba(255,107,107,0.08)',
          fill: '+1',
          pointRadius: 0,
          tension: 0.3,
        }},
        // -10% band (bottom edge)
        {{
          label: '−10% zone',
          data: data.wma_m10,
          borderColor: 'transparent',
          backgroundColor: 'transparent',
          fill: false,
          pointRadius: 0,
          tension: 0.3,
        }},
        // +5% band (top edge)
        {{
          label: '+5% zone',
          data: data.wma_p5,
          borderColor: 'transparent',
          backgroundColor: 'rgba(38,222,129,0.12)',
          fill: '+1',
          pointRadius: 0,
          tension: 0.3,
        }},
        // -5% band (bottom edge)
        {{
          label: '−5% zone',
          data: data.wma_m5,
          borderColor: 'transparent',
          backgroundColor: 'transparent',
          fill: false,
          pointRadius: 0,
          tension: 0.3,
        }},
        // 200-Week MA line
        {{
          label: '200-Week MA',
          data: data.wma,
          borderColor: '#ff9f43',
          borderWidth: 2,
          borderDash: [6, 3],
          backgroundColor: 'transparent',
          fill: false,
          pointRadius: 0,
          tension: 0.3,
          order: 1,
        }},
        // Weekly close price
        {{
          label: 'Weekly Close',
          data: data.prices,
          borderColor: '#58a6ff',
          borderWidth: 2,
          backgroundColor: 'rgba(88,166,255,0.08)',
          fill: 'origin',
          pointRadius: 0,
          tension: 0.3,
          order: 0,
        }},
      ]
    }},
    options: {{
      responsive: true,
      maintainAspectRatio: true,
      interaction: {{ mode: 'index', intersect: false }},
      plugins: {{
        legend: {{
          display: true,
          labels: {{
            color: '#8b949e',
            font: {{ size: 11 }},
            filter: (item) => !['−5% zone','+5% zone','−10% zone','+10% zone'].includes(item.text),
            boxWidth: 20,
            boxHeight: 2,
          }}
        }},
        tooltip: {{
          backgroundColor: '#161b22',
          borderColor: '#30363d',
          borderWidth: 1,
          titleColor: '#e6edf3',
          bodyColor: '#8b949e',
          padding: 10,
          filter: (item) => !['−5% zone','+5% zone','−10% zone','+10% zone'].includes(item.dataset.label),
          callbacks: {{
            label: (ctx) => ` ${{ctx.dataset.label}}: $${{ctx.parsed.y?.toFixed(2) ?? 'N/A'}}`,
          }}
        }}
      }},
      scales: {{
        x: {{
          grid:   {{ color: '#21262d' }},
          ticks:  {{
            color: '#8b949e', font: {{ size: 10 }},
            maxTicksLimit: 10,
            maxRotation: 0,
          }}
        }},
        y: {{
          grid:   {{ color: '#21262d' }},
          ticks:  {{
            color: '#8b949e', font: {{ size: 10 }},
            callback: (v) => '$' + v.toLocaleString()
          }}
        }}
      }}
    }}
  }});
}}
</script>
</body>
</html>"""

OUT = "/Users/patmaverick/.openclaw/workspace/stock_scanner/index.html"
with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

CANVAS = "/Users/patmaverick/.openclaw/canvas/stock_scanner.html"
import shutil, os
os.makedirs(os.path.dirname(CANVAS), exist_ok=True)
shutil.copy(OUT, CANVAS)

total = len(all_results)
print(f"\n✅ Done! {total} stocks successfully processed across {len(tier_results)} tiers")
for cat in CAT_ORDER:
    n = global_counts[cat]
    if n: print(f"   {CAT_LABELS[cat]}: {n}")
print(f"\n→ HTML: {OUT}")
print(f"→ Canvas: {CANVAS}")

# Notable picks
notable = [r for r in all_results if r['category'] in ('deep_value', 'buy_zone')]
if notable:
    print(f"\n⭐ Notable (Deep Value + Buy Zone):")
    for r in notable[:15]:
        sign = "+" if r['pct_diff'] >= 0 else ""
        print(f"   {r['ticker']:6s} {r['name']:30s} {sign}{r['pct_diff']:.1f}%  [{CAT_LABELS[r['category']].split(' ',1)[1]}]")
