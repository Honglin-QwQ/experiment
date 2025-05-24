import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_exp_window, multiply, ts_std_dev, ts_delta

def factor_6111(data, **kwargs):
    """
    因子名称: Volatility_Decay_Momentum_Trade_Count_88285
    数学表达式: ts_decay_exp_window(multiply(ts_std_dev(close, 10), ts_delta(trades, 5)), d=20, factor=0.7)
    中文描述: 该因子结合了短期收盘价波动率的指数衰减加权平均和近期的交易笔数变化。首先计算过去10天收盘价的标准差，反映短期价格波动；然后计算当前交易笔数与5天前交易笔数的差值，衡量交易活跃度的变化。将这两个值相乘，得到一个综合波动率和交易活跃度变化的指标。最后，对这个指标应用一个20天窗口、衰减因子为0.7的指数衰减加权平均。创新点在于结合了价格波动率和交易笔数变化，并使用指数衰减加权平均赋予近期数据更高的权重，旨在捕捉市场在波动和交易活跃度变化驱动下的短期动量或反转机会。
    """
    # 1. 计算 ts_std_dev(close, 10)
    data_ts_std_dev_close = ts_std_dev(data['close'], d=10)
    # 2. 计算 ts_delta(trades, 5)
    data_ts_delta_trades = ts_delta(data['trades'], d=5)
    # 3. 计算 multiply(ts_std_dev(close, 10), ts_delta(trades, 5))
    data_multiply = multiply(data_ts_std_dev_close, data_ts_delta_trades)
    # 4. 计算 ts_decay_exp_window(multiply(ts_std_dev(close, 10), ts_delta(trades, 5)), d=20, factor=0.7)
    factor = ts_decay_exp_window(data_multiply, d=20, factor=0.7)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()