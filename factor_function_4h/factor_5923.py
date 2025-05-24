import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_entropy, abs, ts_delta, divide

def factor_5923(data, **kwargs):
    """
    因子名称: VWAP_Entropy_Delta_Ratio_94405
    数学表达式: divide(ts_entropy(vwap, 106), abs(ts_delta(vwap, 113)))
    中文描述: 该因子计算了过去106天成交量加权平均价格（VWAP）的时间序列熵与过去113天VWAP变化的绝对值之比。时间序列熵衡量了VWAP的波动性和不确定性，而VWAP变化绝对值衡量了VWAP在一段时间内的趋势强度。该因子旨在捕捉市场的不确定性与趋势强度之间的关系。较高的因子值可能表明在VWAP变化相对较小的情况下存在较高的不确定性，这可能预示着趋势的潜在反转或市场进入震荡阶段。相较于单独使用熵或变化量，该因子通过结合两者，提供了一个更全面的视角来评估市场状态。
    因子应用场景：
    1. 趋势反转预测：当因子值较高时，可能预示着趋势的潜在反转。
    2. 市场震荡判断：因子有助于识别市场是否进入震荡阶段。
    3. 风险评估：结合熵和变化量，更全面地评估市场状态。
    """
    # 1. 计算 ts_entropy(vwap, 106)
    data_ts_entropy_vwap = ts_entropy(data['vwap'], 106)
    # 2. 计算 ts_delta(vwap, 113)
    data_ts_delta_vwap = ts_delta(data['vwap'], 113)
    # 3. 计算 abs(ts_delta(vwap, 113))
    data_abs_ts_delta_vwap = abs(data_ts_delta_vwap)
    # 4. 计算 divide(ts_entropy(vwap, 106), abs(ts_delta(vwap, 113)))
    factor = divide(data_ts_entropy_vwap, data_abs_ts_delta_vwap)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()