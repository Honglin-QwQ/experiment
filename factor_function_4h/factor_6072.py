import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_exp_window, divide, add

def factor_6072(data, **kwargs):
    """
    因子名称: ts_decay_exp_window_volume_returns_ratio_53155
    数学表达式: ts_decay_exp_window(divide(returns, add(vol, 1e-9)), d=7, factor=0.7)
    中文描述: 该因子计算过去7天内，每日收益率与成交量的比值的指数衰减加权平均值。收益率除以成交量可以视为单位成交量带来的收益，反映了交易效率。通过指数衰减加权平均，该因子更侧重于最近的交易效率表现。这可能有助于识别短期内交易效率较高或较低的股票，从而捕捉潜在的动量或反转机会。相较于参考因子仅关注收益率的最小值，该因子引入了成交量信息，并使用指数衰减加权平均，结构上更复杂，逻辑上更侧重交易效率。
    因子应用场景：
    1. 交易效率分析：用于识别交易效率较高或较低的股票。
    2. 动量或反转机会：捕捉潜在的动量或反转机会。
    """
    # 1. 计算 add(vol, 1e-9)
    data_add = add(data['vol'], 1e-9)
    # 2. 计算 divide(returns, add(vol, 1e-9))
    data_divide = divide(data['returns'], data_add)
    # 3. 计算 ts_decay_exp_window(divide(returns, add(vol, 1e-9)), d=7, factor=0.7)
    factor = ts_decay_exp_window(data_divide, d=7, factor=0.7)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()