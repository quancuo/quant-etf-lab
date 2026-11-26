import json
from pathlib import Path

import pandas as pd


SYMBOL = "510300"
SNAPSHOT_PATH = Path(__file__).resolve().parents[1] / "day-02" / "data" / "510300_20250616_20250620.json"
KEY = ["symbol", "date"]
PRICE_FIELDS = ["open", "high", "low", "close"]
OHLCV = [*PRICE_FIELDS, "volume"]
LISTED_ON = pd.Timestamp("2012-05-28")

# 本课只覆盖指定示例日期。预期交易日独立于实际收到的行情。
SESSIONS = pd.date_range("2025-06-16", "2025-06-20", freq="D")
AUDIT_DATES = pd.DatetimeIndex(["2012-05-25", "2025-06-02"]).append(
    pd.date_range("2025-06-16", "2025-06-22", freq="D")
).rename("date")


def load_prices():
    snapshot = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    raw = snapshot["series"]["unadjusted"]
    data = raw["response"]["data"]
    if data["code"] != SYMBOL or raw["fqt"] != 0:
        raise ValueError("应读入 510300 的不复权行情")

    rows = [line.split(",") for line in data["klines"]]
    prices = pd.DataFrame(rows, columns=snapshot["kline_columns_in_order"])
    prices["symbol"] = SYMBOL
    return prices[["date", "symbol", *OHLCV]]


def make_dirty_example(prices):
    # 在副本中制造缺行、坏价格、重复行和日期乱序。
    demo = prices.loc[prices["date"] != "2025-06-18"].copy()
    demo.loc[demo["date"] == "2025-06-19", "close"] = "0"
    repeated_row = demo.loc[demo["date"] == "2025-06-17"]
    return pd.concat([demo, repeated_row], ignore_index=True).iloc[::-1]


def clean_prices(rows):
    prices = rows.copy()
    prices["date"] = pd.to_datetime(prices["date"], format="%Y-%m-%d")
    if prices[KEY].isna().any().any():
        raise ValueError("symbol 和 date 都必须有值")
    if not prices["symbol"].eq(SYMBOL).all():
        raise ValueError("此示例按日期索引，只接收 510300 的行情")
    prices[OHLCV] = prices[OHLCV].apply(pd.to_numeric, errors="coerce")

    # 先找出同一标的同一天的所有记录。字段完全相同才删除额外副本。
    duplicates = prices.loc[prices.duplicated(subset=KEY, keep=False), KEY]
    prices = prices.drop_duplicates()
    conflicts = prices.loc[prices.duplicated(subset=KEY, keep=False)]
    if not conflicts.empty:
        raise ValueError(f"同一标的同一天的 OHLCV 冲突，需回查来源\n{conflicts}")

    ohlc = prices[PRICE_FIELDS]
    missing_or_infinite = (prices[OHLCV].isna() | prices[OHLCV].abs().eq(float("inf"))).any(axis=1)
    nonpositive = ohlc.le(0).any(axis=1)
    out_of_range = ohlc["high"].lt(ohlc.max(axis=1)) | ohlc["low"].gt(ohlc.min(axis=1))
    invalid = missing_or_infinite | nonpositive | out_of_range | prices["volume"].lt(0)
    rejected = prices.loc[invalid, ["date", "symbol", *OHLCV]].sort_values("date")
    clean = prices.loc[~invalid].set_index("date").sort_index()
    return clean, duplicates.drop_duplicates().sort_values(KEY), rejected


def audit_dates(clean, rejected):
    rejected_dates = pd.DatetimeIndex(rejected["date"])
    received_dates = clean.index.union(rejected_dates)
    unexpected_dates = received_dates.difference(SESSIONS)
    if not unexpected_dates.empty:
        raise ValueError(f"存在超出本课交易日范围的行情 {unexpected_dates.date}")

    # 交易日完全没收到行与收到了坏行是两种情况。
    missing_dates = SESSIONS.difference(received_dates)
    report = clean.reindex(AUDIT_DATES)
    report["symbol"] = SYMBOL
    report["status"] = "休市"
    report.loc[report.index < LISTED_ON, "status"] = "上市前"
    report.loc[missing_dates, "status"] = "交易日缺行"
    report.loc[rejected_dates, "status"] = "异常行已剔除"
    report.loc[clean.index, "status"] = "有有效行情"
    return report, missing_dates


def main():
    raw = load_prices()
    clean, duplicates, rejected = clean_prices(raw)
    _, missing = audit_dates(clean, rejected)
    print(f"D2 真实快照  有效 {len(clean)} 行 | 重复组 {len(duplicates)} | 异常 {len(rejected)} | 缺行 {len(missing)}")
    print(clean.to_string())

    demo = make_dirty_example(raw)
    clean, duplicates, rejected = clean_prices(demo)
    report, missing = audit_dates(clean, rejected)
    print("\nD3 练习副本  这里的坏数据为教学演示人工加入")
    print(f"重复组 {len(duplicates)}  {duplicates['date'].dt.strftime('%Y-%m-%d').tolist()}")
    print(f"异常行 {len(rejected)}  {rejected['date'].dt.strftime('%Y-%m-%d').tolist()}")
    print(f"缺行 {len(missing)}  {missing.strftime('%Y-%m-%d').tolist()}")
    print(report.to_string(na_rep="—", formatters={"volume": "{:.0f}".format}))


if __name__ == "__main__":
    main()
