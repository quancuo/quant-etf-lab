import numpy as np
import pandas as pd


def main() -> None:
    # 用固定模拟价格对照手算，不下载行情。
    closing_prices = pd.Series([2.00, 2.20, 1.98], dtype=float)
    period_returns = closing_prices.pct_change().dropna()
    cumulative_return = (1 + period_returns).prod() - 1
    endpoint_return = closing_prices.iloc[-1] / closing_prices.iloc[0] - 1
    if not np.isclose(cumulative_return, endpoint_return):
        raise ValueError("收益连乘与首尾价格比不一致")

    entry_price = 2.06
    following_open = 2.08
    holding_return = following_open / entry_price - 1

    print(f"NumPy {np.__version__} | pandas {pd.__version__}")
    print("各段收益", ", ".join(f"{value:+.2%}" for value in period_returns))
    print(f"累计收益 {cumulative_return:+.2%}")
    print(f"下一开盘买入后的持仓毛收益 {holding_return:+.2%}")


if __name__ == "__main__":
    main()
