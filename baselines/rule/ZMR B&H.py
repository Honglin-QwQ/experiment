import numpy as np
import pandas as pd

# 策略表现评估函数
def evaluate_performance(returns):
    n_years = len(returns) / 252  # 交易日数转年数

    # 年化收益率
    total_return = returns.iloc[-1] / returns.iloc[0] - 1
    annual_return = (1 + total_return) ** (1/n_years) - 1

    # 年化波动率
    annual_volatility = returns.pct_change().std() * np.sqrt(252)

    # 夏普比率 (无风险利率=0)
    sharpe_ratio = annual_return / annual_volatility

    # 最大回撤
    cumulative = (1 + returns.pct_change()).cumprod()
    peak = cumulative.expanding().max()
    drawdown = (cumulative - peak) / peak
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
    prices = data['close'].to_frame(name='Price')

    # 参数设置
    window = 20      # 滚动窗口
    z_entry = 1.5    # 触发交易的Z-score阈值
    z_exit = 0.5     # 平仓的Z-score阈值

    # 计算滚动均值与标准差
    prices['Mean'] = prices['Price'].rolling(window).mean()
    prices['Std'] = prices['Price'].rolling(window).std()

    # 计算Z-score
    prices['Z'] = (prices['Price'] - prices['Mean']) / prices['Std']

    # 生成交易信号 (1:做多, -1:做空, 0:空仓)
    prices['Signal'] = 0
    prices.loc[prices['Z'] < -z_entry, 'Signal'] = 1    # Z过低 → 买入
    prices.loc[prices['Z'] > z_entry, 'Signal'] = -1     # Z过高 → 卖出
    prices.loc[prices['Z'].abs() < z_exit, 'Signal'] = 0 # 回归均值 → 平仓

    # 持仓计算 (次日执行信号)
    prices['Position'] = prices['Signal'].shift(1)

    # 计算策略收益率
    prices['Return'] = prices['Price'].pct_change()
    prices['Strategy_Return'] = prices['Position'] * prices['Return']

    # 删除初始空值
    prices = prices.dropna()

    # 计算累计净值
    prices['Cumulative_Strategy'] = (1 + prices['Strategy_Return']).cumprod()
    prices['Cumulative_BuyHold'] = (1 + prices['Return']).cumprod()
    # 评估策略表现
    strategy_perf = evaluate_performance(prices['Cumulative_Strategy'])
    buyhold_perf = evaluate_performance(prices['Cumulative_BuyHold'])

    # 打印结果
    print("策略表现:")
    for k, v in strategy_perf.items():
        print(f"{k}: {v:.4f}")

    print("\n买入持有表现:")
    for k, v in buyhold_perf.items():
        print(f"{k}: {v:.4f}")