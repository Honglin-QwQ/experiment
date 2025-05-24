import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_linear, ts_std_dev, divide, abs, ts_delta

def factor_5803(data, **kwargs):
    """
    因子名称: VWAP_Volatility_Momentum_Decay_Ratio_97449
    数学表达式: divide(ts_decay_linear(ts_std_dev(vwap, 15), 10), abs(ts_delta(vwap, 7)))
    中文描述: 该因子计算过去15天VWAP标准差的10天线性衰减加权平均值与过去7天VWAP绝对差值的比值。相较于参考因子，该因子在波动率计算中引入了更长的时间窗口（15天）和线性衰减（10天），更强调近期波动率的变化趋势，同时调整了动量计算的时间窗口（7天）。这可能更有效地捕捉VWAP波动性和短期动量之间的动态关系，并对近期数据赋予更高的权重，从而提高因子的预测能力和稳定性。
    因子应用场景：
    1. 波动率分析：用于衡量VWAP波动率的近期变化趋势与短期动量之间的关系。
    2. 趋势跟踪：可用于识别价格趋势的强度和稳定性。
    3. 风险管理：通过捕捉VWAP波动率和动量的动态关系，辅助风险管理。
    """
    # 1. 计算 ts_std_dev(vwap, 15)
    data_ts_std_dev_vwap = ts_std_dev(data['vwap'], 15)
    # 2. 计算 ts_decay_linear(ts_std_dev(vwap, 15), 10)
    data_ts_decay_linear = ts_decay_linear(data_ts_std_dev_vwap, 10)
    # 3. 计算 ts_delta(vwap, 7)
    data_ts_delta_vwap = ts_delta(data['vwap'], 7)
    # 4. 计算 abs(ts_delta(vwap, 7))
    data_abs_ts_delta_vwap = abs(data_ts_delta_vwap)
    # 5. 计算 divide(ts_decay_linear(ts_std_dev(vwap, 15), 10), abs(ts_delta(vwap, 7)))
    factor = divide(data_ts_decay_linear, data_abs_ts_delta_vwap)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()