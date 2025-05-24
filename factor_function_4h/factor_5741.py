import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_linear, ts_std_dev, log_diff, divide

def factor_5741(data, **kwargs):
    """
    因子名称: Volatility_Adjusted_Price_Momentum_Ratio_67059
    数学表达式: divide(ts_decay_linear(close, 10), ts_std_dev(log_diff(close), 20))
    中文描述: 该因子旨在捕捉经过波动率调整后的价格动量。首先，它计算过去10天收盘价的线性衰减值，给予近期价格更高的权重，以衡量短期价格趋势。
            然后，计算过去20天收盘价对数差（即对数收益率）的标准差，作为短期价格波动率的度量。最后，将线性衰减的收盘价除以对数收益率的波动率。
            这个因子试图识别那些在相对较低波动率环境下表现出较强短期价格趋势的股票。相较于参考因子，创新点在于使用了对数收益率的波动率作为调整项，
            并且结合了线性衰减来捕捉动量，而不是简单的价格倒数或最小值。改进建议中提到的波动率标准化收益率和动量与波动率结合的策略在此因子中得到了体现，
            通过将衰减后的价格（代表动量）除以波动率进行调整。同时，参数的时间窗口也进行了调整，以探索不同的时间尺度效应。
    因子应用场景：
    1. 动量交易：识别在低波动率环境下具有较强价格动量的股票，可能预示着趋势的开始。
    2. 风险调整：通过波动率调整，筛选出性价比更高的动量机会。
    """
    # 1. 计算 ts_decay_linear(close, 10)
    data_ts_decay_linear = ts_decay_linear(data['close'], 10)
    # 2. 计算 log_diff(close)
    data_log_diff = log_diff(data['close'])
    # 3. 计算 ts_std_dev(log_diff(close), 20)
    data_ts_std_dev = ts_std_dev(data_log_diff, 20)
    # 4. 计算 divide(ts_decay_linear(close, 10), ts_std_dev(log_diff(close), 20))
    factor = divide(data_ts_decay_linear, data_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()