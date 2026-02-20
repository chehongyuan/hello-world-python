"""纳斯达克指数双均线（金叉/死叉）量化策略示例。

策略规则：
1. 20日均线上穿100日均线（金叉）时买入。
2. 20日均线下穿100日均线（死叉）时卖出。

默认使用纳斯达克综合指数（^IXIC）历史数据进行回测。
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import pandas as pd
import yfinance as yf


@dataclass
class BacktestResult:
    """保存回测结果。"""

    symbol: str
    start: str
    end: str
    trades: pd.DataFrame
    total_return: float
    buy_hold_return: float


def load_price_data(symbol: str, start: str, end: str) -> pd.DataFrame:
    """下载并清洗价格数据。"""
    data = yf.download(symbol, start=start, end=end, auto_adjust=True, progress=False)
    if data.empty:
        raise ValueError(f"未下载到 {symbol} 的价格数据，请检查代码或日期区间。")

    price_col = "Close"
    if price_col not in data.columns:
        raise ValueError("价格数据缺少 Close 列，无法计算均线。")

    df = data[[price_col]].copy()
    df.columns = ["close"]
    return df


def generate_signals(df: pd.DataFrame) -> pd.DataFrame:
    """计算均线并生成交易信号。"""
    result = df.copy()
    result["ma20"] = result["close"].rolling(window=20).mean()
    result["ma100"] = result["close"].rolling(window=100).mean()

    result["signal"] = 0
    result.loc[result["ma20"] > result["ma100"], "signal"] = 1

    # 1: 买入信号（金叉），-1: 卖出信号（死叉）
    result["trade_signal"] = result["signal"].diff().fillna(0)
    return result


def run_backtest(signals: pd.DataFrame, symbol: str, start: str, end: str) -> BacktestResult:
    """执行简化回测：有仓位时按指数涨跌计收益，无仓位时收益为0。"""
    bt = signals.copy()

    bt["daily_return"] = bt["close"].pct_change().fillna(0)
    bt["position"] = bt["signal"].shift(1).fillna(0)
    bt["strategy_return"] = bt["daily_return"] * bt["position"]

    bt["strategy_curve"] = (1 + bt["strategy_return"]).cumprod()
    bt["buy_hold_curve"] = (1 + bt["daily_return"]).cumprod()

    trades = bt.loc[bt["trade_signal"] != 0, ["close", "ma20", "ma100", "trade_signal"]].copy()
    trades["action"] = trades["trade_signal"].map({1.0: "买入(金叉)", -1.0: "卖出(死叉)"})

    return BacktestResult(
        symbol=symbol,
        start=start,
        end=end,
        trades=trades,
        total_return=bt["strategy_curve"].iloc[-1] - 1,
        buy_hold_return=bt["buy_hold_curve"].iloc[-1] - 1,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="纳斯达克双均线量化策略（20/100）")
    parser.add_argument("--symbol", default="^IXIC", help="标的代码，默认 ^IXIC（纳斯达克综合指数）")
    parser.add_argument("--start", default="2015-01-01", help="开始日期，如 2015-01-01")
    parser.add_argument("--end", default="2026-01-01", help="结束日期，如 2026-01-01")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    df = load_price_data(args.symbol, args.start, args.end)
    signals = generate_signals(df)
    result = run_backtest(signals, args.symbol, args.start, args.end)

    print(f"标的: {result.symbol}")
    print(f"区间: {result.start} ~ {result.end}")
    print(f"策略累计收益: {result.total_return:.2%}")
    print(f"买入并持有收益: {result.buy_hold_return:.2%}")

    if result.trades.empty:
        print("\n该区间没有出现有效金叉/死叉信号。")
    else:
        print("\n交易信号如下（仅显示前10条）：")
        print(result.trades.head(10).to_string())

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
