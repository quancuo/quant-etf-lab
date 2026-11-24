import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd


SYMBOL = "510300"
TRADING_DATES = [f"2025-06-{day}" for day in range(16, 21)]
SNAPSHOT_PATH = Path(__file__).parent / "data" / "510300_20250616_20250620.json"
ENDPOINT = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
AKSHARE_DOC = "https://akshare.akfamily.xyz/data/fund/fund_public.html"
AKSHARE_SOURCE = "https://github.com/akfamily/akshare/blob/main/akshare/fund/fund_etf_em.py"
DIVIDEND_NOTICE = "https://static.cninfo.com.cn/finalpage/2025-06-11/1223837903.PDF"
COLUMNS = [
    "date", "open", "close", "high", "low", "volume", "amount", "amplitude_pct",
    "provider_change_pct", "provider_change_amount", "turnover_pct",
]
MODES = {"unadjusted": ("", 0), "hfq": ("hfq", 2)}


def download_series(adjust, fqt):
    # 参数对应 AKShare 的东方财富 ETF 日线接口。
    query = urlencode({
        "secid": f"1.{SYMBOL}",
        "klt": 101,
        "beg": TRADING_DATES[0].replace("-", ""),
        "end": TRADING_DATES[-1].replace("-", ""),
        "fqt": fqt,
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f116",
        "ut": "7eea3edcaed734bea9cbfc24409ed989",
    })
    url = f"{ENDPOINT}?{query}"
    request = Request(url, headers={
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://quote.eastmoney.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/133.0.0.0 Safari/537.36",
    })
    with urlopen(request, timeout=15) as response:
        payload = json.load(response)
    return {"akshare_adjust": adjust, "fqt": fqt, "request_url": url, "response": payload}


def download_snapshot():
    series = {name: download_series(*mode) for name, mode in MODES.items()}
    return {
        "provider": "东方财富 ETF 日 K",
        "symbol": SYMBOL,
        "period": "daily",
        "start_date": TRADING_DATES[0],
        "end_date": TRADING_DATES[-1],
        "retrieved_at": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"),
        "retrieved_timezone": "Asia/Shanghai",
        "akshare_docs": AKSHARE_DOC,
        "akshare_upstream_reference": AKSHARE_SOURCE,
        "kline_columns_in_order": COLUMNS,
        "cash_distribution": {
            "ex_date": "2025-06-18",
            "record_date": "2025-06-17",
            "payment_date": "2025-06-27",
            "yuan_per_unit": 0.088,
            "notice_url": DIVIDEND_NOTICE,
        },
        "series": series,
    }


def read_prices(series, mode):
    if (series["akshare_adjust"], series["fqt"]) != MODES[mode]:
        raise ValueError(f"{mode} 的复权参数不匹配")
    payload = series["response"]
    data = payload.get("data") or {}
    if payload.get("rc") != 0 or data.get("code") != SYMBOL or not data.get("klines"):
        raise ValueError(f"{mode} 响应缺少 {SYMBOL} 的日线")

    # 接口用逗号分隔每条 K 线，按已知顺序拆成列。
    rows = [line.split(",") for line in data["klines"]]
    prices = pd.DataFrame(rows, columns=COLUMNS)
    if prices["date"].tolist() != TRADING_DATES:
        raise ValueError(f"{mode} 日期应为连续五个指定交易日且没有重复")

    prices[COLUMNS[1:]] = prices[COLUMNS[1:]].apply(pd.to_numeric, errors="raise")
    ohlc = prices[["open", "high", "low", "close"]]
    if ohlc.isna().any().any() or (ohlc <= 0).any().any():
        raise ValueError(f"{mode} 有缺失或非正价格")
    if (ohlc["high"] < ohlc.max(axis=1)).any() or (ohlc["low"] > ohlc.min(axis=1)).any():
        raise ValueError(f"{mode} 的最高价或最低价与开收盘价不一致")
    activity = prices[["volume", "amount"]]
    if activity.isna().any().any() or (activity < 0).any().any():
        raise ValueError(f"{mode} 的成交量或成交额缺失或为负")
    return prices


def compare_prices(snapshot):
    raw = read_prices(snapshot["series"]["unadjusted"], "unadjusted")
    adjusted = read_prices(snapshot["series"]["hfq"], "hfq")
    for column in ["volume", "amount"]:
        if not raw[column].equals(adjusted[column]):
            raise ValueError(f"两种复权口径的 {column} 字段不一致")

    # 对照时按交易日期一对一合并，日收益用相邻两天的收盘价自行计算。
    comparison = raw[["date", "open", "close", "volume"]].merge(
        adjusted[["date", "open", "close"]],
        on="date", suffixes=("_raw", "_hfq"), validate="one_to_one",
    )
    comparison["return_raw"] = comparison["close_raw"].pct_change()
    comparison["return_hfq"] = comparison["close_hfq"].pct_change()
    return comparison


def main():
    parser = argparse.ArgumentParser(description="对照 510300 的五条不复权与后复权日线")
    parser.add_argument("--download", action="store_true", help="首次取数并保存新快照")
    args = parser.parse_args()

    if args.download:
        if SNAPSHOT_PATH.exists():
            parser.error("快照已存在。直接运行可从快照复算。")
        snapshot = download_snapshot()
    else:
        snapshot = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))

    comparison = compare_prices(snapshot)
    if args.download:
        # 两组数据都通过校验后才落盘，并保留两份原始响应。
        content = json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n"
        SNAPSHOT_PATH.parent.mkdir(exist_ok=True)
        with SNAPSHOT_PATH.open("x", encoding="utf-8") as file:
            file.write(content)

    print(f"快照获取时间 {snapshot['retrieved_at']}  |  {snapshot['provider']}")
    print(comparison.to_string(
        index=False, na_rep="—",
        formatters={
            "open_raw": "{:.3f}".format, "close_raw": "{:.3f}".format,
            "open_hfq": "{:.3f}".format, "close_hfq": "{:.3f}".format,
            "return_raw": "{:+.4%}".format, "return_hfq": "{:+.4%}".format,
        },
    ))
    dividend = snapshot["cash_distribution"]
    closing_prices = comparison.set_index("date")["close_raw"]
    prior_close = closing_prices.loc[dividend["record_date"]]
    ex_close = closing_prices.loc[dividend["ex_date"]]
    cash_return = (ex_close + dividend["yuan_per_unit"]) / prior_close - 1
    print(f"除息日按不复权收盘价计入每份现金分红后的收益 {cash_return:+.4%}")


if __name__ == "__main__":
    main()
