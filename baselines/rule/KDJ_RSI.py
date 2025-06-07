import yfinance_test as yf
import pandas as pd
import numpy as np


# ========== 指标计算 ==========
# 计算KDJ指标
def calculate_kdj(df, n=9, m=3):
    low_min = df['low'].rolling(n).min()
    high_max = df['high'].rolling(n).max()
    rsv = (df['close'] - low_min) / (high_max - low_min) * 100
    df['K'] = rsv.ewm(alpha=1/m).mean()  # K值 = RSV的EMA
    df['D'] = df['K'].ewm(alpha=1/m).mean()  # D值 = K的EMA
    df['J'] = 3 * df['K'] - 2 * df['D']  # J值
    return df.dropna()

# 计算RSI指标
def calculate_rsi(df, window=14):
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df.dropna()


# ========== 计算评估指标 ==========
def evaluate_strategy(data):
    # 年化交易日数
    trading_days = 252

    # 年化收益率
    total_return = data['Strategy_Cumulative'].iloc[-1] - 1
    years = len(data) / trading_days
    annual_return = (1 + total_return) ** (1/years) - 1

    # 年化波动率
    annual_volatility = data['Strategy_Return'].std() * np.sqrt(trading_days)

    # 夏普比率 (无风险利率=0)
    sharpe_ratio = annual_return / annual_volatility

    # 最大回撤
    cumulative_returns = data['Strategy_Cumulative']
    peak = cumulative_returns.cummax()
    drawdown = (cumulative_returns - peak) / peak
    max_drawdown = drawdown.min()

    return {
        'Annual_Return': annual_return,
        'Annual_Volatility': annual_volatility,
        'Sharpe_Ratio': sharpe_ratio,
        'Max_Drawdown': max_drawdown
    }



if __name__ == '__main__':
    df = pd.read_csv('/nasdaq_stocks_data_top20/AAPL.csv')
    start_date = '2023-06-01'
    end_date = '2024-01-01'
    data = df[(df['dt'] >= start_date) & (df['dt'] <= end_date)]
    data['dt'] = pd.to_datetime(data['dt'])
    data = data.sort_values(by='dt')

    # 执行计算
    data = calculate_kdj(data)
    data = calculate_rsi(data)

    # ========== 交易信号生成 ==========
    data['Signal'] = 0
    # 买入条件：J<20且RSI<30
    data.loc[(data['J'] < 20) & (data['RSI'] < 30), 'Signal'] = 1
    # 卖出条件：J>80且RSI>70
    data.loc[(data['J'] > 80) & (data['RSI'] > 70), 'Signal'] = -1

    # ========== 回测策略 ==========
    data['Position'] = data['Signal']
    data['Strategy_Return'] = data['Position'].shift(1) * data['close'].pct_change()  # 策略收益率
    data['Strategy_Cumulative'] = (1 + data['Strategy_Return']).cumprod()  # 累计收益

    # 主流程
    metrics = evaluate_strategy(data)

    # 打印结果
    print("策略评估指标:")
    for key, value in metrics.items():
        print(f"{key}: {value:.4f}")