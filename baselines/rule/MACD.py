import yfinance_test as yf
import numpy as np
import pandas as pd

# # 下载历史数据 (示例：苹果股票 2010-2020)
# data = yf.download('AAPL', start='2010-01-01', end='2020-12-31')
# data = data[['close']].copy()

# 计算MACD指标
def calculate_macd(data, short=12, long=26, signal=9):
    data['EMA_short'] = data['close'].ewm(span=short, adjust=False).mean()
    data['EMA_long'] = data['close'].ewm(span=long, adjust=False).mean()
    data['MACD'] = data['EMA_short'] - data['EMA_long']
    data['Signal'] = data['MACD'].ewm(span=signal, adjust=False).mean()
    return data

# 生成交易信号 (1: 持有, 0: 空仓)
def generate_signals(data):
    data['Position'] = 0  # 初始化仓位
    # MACD上穿信号线 → 买入信号
    data.loc[data['MACD'] > data['Signal'], 'Position'] = 1
    # 避免未来数据：信号延迟一天执行
    data['Position'] = data['Position'].shift(1)
    return data

# 计算策略收益
def calculate_returns(data):
    # 标的资产每日收益率
    data['Asset_Return'] = data['close'].pct_change()
    # 策略每日收益率 = 资产收益率 * 前一日仓位
    data['Strategy_Return'] = data['Asset_Return'] * data['Position'].shift(1)
    # 计算累计净值
    data['Asset_Cumulative'] = (1 + data['Asset_Return']).cumprod()
    data['Strategy_Cumulative'] = (1 + data['Strategy_Return']).cumprod()
    return data

# 评估策略表现
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

def optimize_macd_params(data, timeframe='daily'):
    """
    自动优化MACD参数适应不同时间尺度
    """
    params_dict = {
        'daily': (12, 26, 9),
        'weekly': (24, 52, 9),
        'monthly': (6, 13, 3)
    }

    if timeframe.lower() in params_dict:
        return params_dict[timeframe.lower()]

    # 自动计算参数（按时间尺度比例）
    if len(data) > 2000:  # 10年以上的日线数据
        return (24, 52, 9)  # 长期参数
    elif len(data) > 1000:
        return (18, 39, 6)  # 中期参数
    else:
        return (12, 26, 9)  # 标准参数

if __name__ == '__main__':
    df = pd.read_csv('/nasdaq_stocks_data_top20/AAPL.csv')
    start_date = '2024-06-01'
    end_date = '2025-06-01'

    filtered_df = df[(df['dt'] >= start_date) & (df['dt'] <= end_date)]
    data = filtered_df[['dt', 'close']].copy()
    data['dt'] = pd.to_datetime(data['dt'])
    data = data.sort_values(by='dt')
    # # 检测数据频率
    # freq = 'daily' if len(data) > 1000 else 'weekly'
    # # 获取优化参数
    # short, long, signal = optimize_macd_params(data, freq)
    # print(f"Optimized MACD params: ({short}, {long}, {signal})")

    # 主流程
    data = calculate_macd(data)
    data = generate_signals(data)
    data = calculate_returns(data)
    results = evaluate_strategy(data)

    # 打印结果
    print("策略表现评估:")
    for key, value in results.items():
        print(f"{key}: {value:.4f}")