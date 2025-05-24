import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_delta, abs, divide

def factor_5798(data, **kwargs):
    """
    因子名称: VWAP_Volatility_Momentum_Ratio_61528
    数学表达式: divide(ts_std_dev(vwap, 10), abs(ts_delta(vwap, 5)))
    中文描述: 该因子计算过去10天VWAP的标准差与过去5天VWAP绝对差值的比值。它衡量了VWAP的波动性相对于其短期动量的强度。高值可能表示VWAP波动较大但短期动量较弱，低值可能表示VWAP波动较小但短期动量较强。这可以用于识别价格趋势的稳定性和强度。
    因子应用场景：
    1. 波动性分析：用于衡量VWAP价格的波动程度。
    2. 动量分析：评估VWAP价格的短期动量。
    3. 趋势识别：结合波动性和动量信息，辅助识别价格趋势的稳定性和强度。
    """
    # 1. 计算 ts_std_dev(vwap, 10)
    data_ts_std_dev = ts_std_dev(data['vwap'], 10)
    # 2. 计算 ts_delta(vwap, 5)
    data_ts_delta = ts_delta(data['vwap'], 5)
    # 3. 计算 abs(ts_delta(vwap, 5))
    data_abs_ts_delta = abs(data_ts_delta)
    # 4. 计算 divide(ts_std_dev(vwap, 10), abs(ts_delta(vwap, 5)))
    factor = divide(data_ts_std_dev, data_abs_ts_delta)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()