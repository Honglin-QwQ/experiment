import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_arg_max, subtract, ts_min, divide

def factor_5740(data, **kwargs):
    """
    因子名称: VWAP_ArgMax_MinDiff_Ratio_72646
    数学表达式: divide(ts_arg_max(vwap, 22), subtract(vwap, ts_min(vwap, 5), filter=True))
    中文描述: 该因子结合了VWAP的最大值位置和短期最小值差异。首先计算过去22天VWAP最大值出现的相对索引（ts_arg_max(vwap, 22)），该值越大表示近期高点出现的时间越靠前。然后计算当前VWAP与过去5天VWAP最小值的差值（subtract(vwap, ts_min(vwap, 5), filter=True)），该值越大表示当前价格相对于近期低点有较大的上涨。最后计算这两个指标的比率。较高的比率可能意味着近期高点出现较早，但当前价格相对于近期低点有显著上涨，这可能预示着价格的潜在回调或趋势的转变。该因子创新性地结合了时间序列的最大值位置信息和短期价格差异，提供了对VWAP动态的独特视角。
    因子应用场景：
    1. 潜在回调识别：较高的因子值可能预示着价格的潜在回调。
    2. 趋势转变信号：因子值变化可能提示趋势的转变。
    """
    # 1. 计算 ts_arg_max(vwap, 22)
    data_ts_arg_max_vwap = ts_arg_max(data['vwap'], d=22)
    # 2. 计算 ts_min(vwap, 5)
    data_ts_min_vwap = ts_min(data['vwap'], d=5)
    # 3. 计算 subtract(vwap, ts_min(vwap, 5), filter=True)
    data_subtract_vwap_ts_min_vwap = subtract(data['vwap'], data_ts_min_vwap, filter=True)
    # 4. 计算 divide(ts_arg_max(vwap, 22), subtract(vwap, ts_min(vwap, 5), filter=True))
    factor = divide(data_ts_arg_max_vwap, data_subtract_vwap_ts_min_vwap)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()