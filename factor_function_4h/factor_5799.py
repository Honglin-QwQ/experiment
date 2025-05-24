import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_delta, ts_sum, divide

def factor_5799(data, **kwargs):
    """
    因子名称: VolumeWeightedPrice_Volatility_Momentum_Ratio_44042
    数学表达式: divide(ts_std_dev(vwap, 14), ts_delta(ts_sum(returns, 60), 10))
    中文描述: 该因子旨在捕捉成交量加权平均价格(vwap)的短期波动性与长期累计收益动量之间的关系。它计算过去14天vwap的标准差，作为短期波动性的衡量。同时，计算过去60天收益率之和，并取其10天前的差值，作为长期收益动量的衡量。最后，用vwap的短期波动性除以长期收益动量。这个因子的创新点在于结合了价格的波动性特征和收益的动量特征，并使用了除法来衡量两者的相对强度。高波动性但长期动量较弱的股票可能因子值较高，反之亦然。这可以用于识别潜在的价格反转机会或动量衰竭的信号。
    因子应用场景：
    1. 识别潜在的价格反转机会
    2. 识别动量衰竭的信号
    """
    # 1. 计算 ts_std_dev(vwap, 14)
    data_ts_std_dev_vwap = ts_std_dev(data['vwap'], 14)
    # 2. 计算 ts_sum(returns, 60)
    data_ts_sum_returns = ts_sum(data['returns'], 60)
    # 3. 计算 ts_delta(ts_sum(returns, 60), 10)
    data_ts_delta_ts_sum_returns = ts_delta(data_ts_sum_returns, 10)
    # 4. 计算 divide(ts_std_dev(vwap, 14), ts_delta(ts_sum(returns, 60), 10))
    factor = divide(data_ts_std_dev_vwap, data_ts_delta_ts_sum_returns)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()