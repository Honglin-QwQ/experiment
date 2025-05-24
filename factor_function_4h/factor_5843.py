import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_std_dev, ts_decay_linear, abs, ts_delta

def factor_5843(data, **kwargs):
    """
    因子名称: VWAP_Volatility_Decay_Ratio_19794
    数学表达式: divide(ts_std_dev(vwap, 10), ts_decay_linear(abs(ts_delta(vwap, 1)), 10, dense=True))
    中文描述: 该因子衡量VWAP的短期波动率与近期VWAP绝对变化的线性衰减平均值之比。分子使用ts_std_dev(vwap, 10)计算过去10天VWAP的标准差，代表VWAP的短期波动性。分母使用ts_decay_linear(abs(ts_delta(vwap, 1)), 10, dense=True)计算过去10天VWAP日间绝对变化的线性衰减加权平均值，其中abs(ts_delta(vwap, 1))计算每日VWAP的绝对变化。通过divide操作将两者相除，得到一个反映波动率相对于近期平均价格变动幅度的指标。当比值较高时，可能表明VWAP波动较大但近期价格变动幅度相对较小，反之亦然。这可以用于识别价格趋势的稳定性和潜在的市场情绪变化。
    因子应用场景：
    1. 波动率分析：用于衡量VWAP的波动率相对于近期价格变动幅度的大小。
    2. 趋势稳定性判断：比值较高可能表明VWAP波动较大但近期价格变动幅度相对较小，可能预示着趋势的不稳定性。
    3. 市场情绪变化：可用于识别潜在的市场情绪变化。
    """
    # 1. 计算 ts_std_dev(vwap, 10)
    data_ts_std_dev = ts_std_dev(data['vwap'], 10)
    # 2. 计算 ts_delta(vwap, 1)
    data_ts_delta = ts_delta(data['vwap'], 1)
    # 3. 计算 abs(ts_delta(vwap, 1))
    data_abs_ts_delta = abs(data_ts_delta)
    # 4. 计算 ts_decay_linear(abs(ts_delta(vwap, 1)), 10, dense=True)
    data_ts_decay_linear = ts_decay_linear(data_abs_ts_delta, 10, dense=True)
    # 5. 计算 divide(ts_std_dev(vwap, 10), ts_decay_linear(abs(ts_delta(vwap, 1)), 10, dense=True))
    factor = divide(data_ts_std_dev, data_ts_decay_linear)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()