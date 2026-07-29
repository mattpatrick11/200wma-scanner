#!/usr/bin/env python3
"""
200-Week Moving Average Stock Scanner — v3
Large/Mid/Small Cap · Embedded Charts · GitHub Dark Theme
175 stocks · Years-Public column · Dividend / Aristocrat badges
"""

import subprocess, sys
for pkg in ['yfinance', 'pandas']:
    try: __import__(pkg)
    except ImportError: subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg, '-q'])

import yfinance as yf
import pandas as pd
from datetime import datetime, timezone
import time, json, math

# ── Stock Universe ─────────────────────────────────────────────────────────────

LARGE_CAP = [
    # Technology (16)
    ("AAPL","Apple Inc.","Technology"),("MSFT","Microsoft Corp.","Technology"),
    ("GOOGL","Alphabet Inc.","Technology"),("META","Meta Platforms","Technology"),
    ("NVDA","NVIDIA Corp.","Technology"),("AVGO","Broadcom Inc.","Technology"),
    ("ADBE","Adobe Inc.","Technology"),("CRM","Salesforce Inc.","Technology"),
    ("TXN","Texas Instruments","Technology"),("AMD","Adv. Micro Devices","Technology"),
    ("ASML","ASML Holding","Technology"),("TSM","Taiwan Semiconductor","Technology"),
    ("INTC","Intel Corp.","Technology"),("QCOM","Qualcomm Inc.","Technology"),
    ("IBM","IBM Corp.","Technology"),("ADP","Auto. Data Processing","Technology"),
    # Consumer Discretionary (8)
    ("AMZN","Amazon.com Inc.","Cons. Discretionary"),("TSLA","Tesla Inc.","Cons. Discretionary"),
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
    # Healthcare (13)
    ("JNJ","Johnson & Johnson","Healthcare"),("UNH","UnitedHealth Group","Healthcare"),
    ("LLY","Eli Lilly & Co.","Healthcare"),("ABBV","AbbVie Inc.","Healthcare"),
    ("TMO","Thermo Fisher","Healthcare"),("MRK","Merck & Co.","Healthcare"),
    ("PFE","Pfizer Inc.","Healthcare"),("ABT","Abbott Laboratories","Healthcare"),
    ("MDT","Medtronic plc","Healthcare"),("GILD","Gilead Sciences","Healthcare"),
    ("ISRG","Intuitive Surgical","Healthcare"),("SYK","Stryker Corp.","Healthcare"),
    ("BDX","Becton Dickinson","Healthcare"),
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
    # Materials (6)
    ("SHW","Sherwin-Williams","Materials"),("APD","Air Products","Materials"),
    ("LIN","Linde plc","Materials"),("ECL","Ecolab Inc.","Materials"),
    ("NUE","Nucor Corp.","Materials"),("DOW","Dow Inc.","Materials"),
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
]

ALL_TIERS = [
    ("Large Cap", LARGE_CAP),
    ("Mid Cap",   MID_CAP),
    ("Small Cap", SMALL_CAP),
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

            if len(hist) < 30:
                print(f"  [{idx:03d}/{total_stocks}] {ticker:6s}: insufficient data, skipping")
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
            w52h = w52l = None
            years_public = None
            pays_div = False
            try:
                fi   = stock.fast_info
                mc   = getattr(fi, 'market_cap', None)
                if mc:
                    mc_str = f"${mc/1e12:.2f}T" if mc >= 1e12 else f"${mc/1e9:.0f}B"
                w52h = round(float(fi.fifty_two_week_high), 2) if hasattr(fi, 'fifty_two_week_high') else None
                w52l = round(float(fi.fifty_two_week_low),  2) if hasattr(fi, 'fifty_two_week_low')  else None

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

            # ── Chart data: last 200 weeks ──────────────────────────────────
            chart_hist = hist.tail(200).copy()
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
                "week52_high": w52h,
                "week52_low":  w52l,
                "market_cap":  mc_str,
                "weeks_data":  len(hist),
                "full_200wma": len(hist) >= 200,
                "years_public": years_public,
                "pays_div":    pays_div,
            })

            time.sleep(0.25)

        except Exception as e:
            print(f"  [{idx:03d}/{total_stocks}] {ticker:6s}: ERROR — {e}")

    results.sort(key=lambda x: (CAT_ORDER.index(x['category']), x['pct_diff']))
    tier_results[tier_name] = results
    print()

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

def div_badge_html(ticker, pays_div):
    if ticker in DIVIDEND_ARISTOCRATS:
        return '<span class="div-badge aristocrat" title="Dividend Aristocrat — 25+ consecutive years of dividend increases">👑</span>'
    elif pays_div:
        return '<span class="div-badge payer" title="Pays dividend">💰</span>'
    else:
        return '<span class="div-badge none">—</span>'

# ── Build Sections HTML ────────────────────────────────────────────────────────

def build_tier_html(tier_name, results):
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
        w52   = ""
        if r['week52_high'] and r['week52_low']:
            w52 = f"${r['week52_low']:,.2f} – ${r['week52_high']:,.2f}"

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
      <td class="muted w52">{w52}</td>
    </tr>
    <tr class="chart-row" id="chart-{ticker_safe}" style="display:none">
      <td colspan="12">
        <div class="chart-container">
          <div class="chart-header">
            <span class="chart-title">{r['ticker']} — {r['name']}</span>
            <span class="chart-sub">Weekly Close vs 200-Week Moving Average · Last 200 Weeks</span>
            <span class="chart-stat" style="color:{cat_c}">{'+' if r['pct_diff']>=0 else ''}{r['pct_diff']:.1f}% vs 200WMA</span>
          </div>
          <canvas id="canvas-{ticker_safe}" height="260"></canvas>
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
            <th class="num">Yrs Public</th><th>Div</th>
            <th class="num">Price</th><th class="num">200-WMA</th>
            <th class="num">vs 200-WMA</th><th>Position</th>
            <th>Status</th><th class="num">Mkt Cap</th><th>52-Wk Range</th>
          </tr>
        </thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>
  </div>"""

all_sections = ""
for tier_name, results in tier_results.items():
    all_sections += build_tier_html(tier_name, results)

# ── Global Summary Stats ───────────────────────────────────────────────────────

all_results = [r for results in tier_results.values() for r in results]
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
.div-badge {{ font-size:15px; display:inline-block }}
.div-badge.aristocrat {{ filter: drop-shadow(0 0 3px #fed33060) }}
.div-badge.none {{ color:var(--muted); font-size:13px }}

/* Years public */
.yrs-pub {{ text-align:center; color:var(--muted) }}

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

/* Notes box */
.notes-box {{
  margin-top:20px; padding:12px 16px; background:var(--bg2);
  border:1px solid var(--border); border-radius:6px;
  font-size:12px; color:var(--muted); line-height:1.8;
}}

@media (max-width:768px) {{
  header, .stats, main, .strategy, .tier-nav {{ padding-left:14px; padding-right:14px }}
  .mc, .w52, .yrs-pub {{ display:none }}
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
</div>

<main>
{all_sections}
  <div class="notes-box">
    <strong style="color:var(--text)">How to read this:</strong>
    <span style="color:#ff6b6b;font-weight:600">Deep Value</span> (&lt;−10%) ·
    <span style="color:#ff9f43;font-weight:600">Undervalued</span> (−3% to −10%) ·
    <span style="color:#26de81;font-weight:600">Buy Zone</span> (±3%) ·
    <span style="color:#fed330;font-weight:600">Watchlist</span> (+3% to +15%) ·
    <span style="color:#a4b0be;font-weight:600">Extended</span> (&gt;+15%) ·
    Click any row to expand the price chart.
    <span class="warn">†</span> = fewer than 200 weeks of price history available.
    👑 = Dividend Aristocrat (25+ consecutive years of dividend increases) · 💰 = Pays dividend
    Data from Yahoo Finance via yfinance. <em>Not financial advice.</em>
  </div>
</main>

<footer>
  <strong>200-Week MA Stock Scanner v3</strong> · Built by Tuchus 🐶 ·
  175 stocks · Data: Yahoo Finance · Not financial advice · {now_str}
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
