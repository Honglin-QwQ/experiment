import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_delta, sigmoid, ts_arg_min, multiply

def factor_5578(data, **kwargs):
    """
    因子名称: factor_0001_55459
    数学表达式: ts_rank(ts_delta(close,3), 240)*sigmoid(open)*ts_arg_min(returns,6)
    中文描述: 本因子融合了动量、情绪和短期反转的元素。首先，`ts_rank(ts_delta(close,3), 240)`衡量了过去3天收盘价变化在过去240天内的排名，反映了价格的动量效应。其次，`sigmoid(open)`捕捉了开盘价的市场情绪，将开盘价映射到0到1之间。最后，`ts_arg_min(returns,6)`寻找过去6天内收益率最低的时间点，暗示潜在的短期反转机会。三者相乘，旨在捕捉在特定动量状态下，市场情绪与短期反转信号共振时的交易机会。创新点在于将三种不同类型的因子结合，期望能提高信号的稳定性和预测能力。
    因子应用场景：
    1. 动量捕捉：用于识别具有持续上涨动力的股票。
    2. 情绪分析：结合开盘价情绪，筛选市场情绪高涨的股票。
    3. 短期反转：寻找短期内可能出现反转的股票。
    """
    # 1. 计算 ts_delta(close, 3)
    data_ts_delta_close = ts_delta(data['close'], 3)
    # 2. 计算 ts_rank(ts_delta(close,3), 240)
    data_ts_rank = ts_rank(data_ts_delta_close, 240)
    # 3. 计算 sigmoid(open)
    data_sigmoid_open = sigmoid(data['open'])
    # 4. 计算 ts_arg_min(returns, 6)
    data_ts_arg_min_returns = ts_arg_min(data['returns'], 6)
    # 5. 计算 ts_rank(ts_delta(close,3), 240)*sigmoid(open)*ts_arg_min(returns,6)
    factor = multiply(data_ts_rank, data_sigmoid_open, data_ts_arg_min_returns)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()