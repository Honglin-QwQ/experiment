import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_delta, ts_scale, ts_arg_min, add, divide

def factor_5841(data, **kwargs):
    """
    因子名称: ts_scaled_delta_vwap_arg_min_close_ratio_47909
    数学表达式: divide(ts_scale(ts_delta(vwap, 5), 30), add(ts_arg_min(close, 20), 1))
    中文描述: 该因子结合了VWAP的短期变化、其长期波动性的缩放以及收盘价最低点的位置信息。首先计算VWAP与5天前VWAP的差值，衡量短期价格动量。然后对这些短期变化在过去30天内进行时间序列缩放，使其值在一定范围内。最后，将缩放后的VWAP变化除以过去20天收盘价最低点出现的相对天数加1。分母加1是为了避免除以零。这个因子旨在捕捉短期价格动量在考虑长期价格底部支撑下的相对强度。当短期价格上涨动量较强且近期出现价格底部时，因子值可能较高，反之较低。这可能用于识别具有短期上涨潜力且近期有触底迹象的股票。
    因子应用场景：
    1. 动量分析：捕捉短期价格动量在考虑长期价格底部支撑下的相对强度。
    2. 底部识别：识别具有短期上涨潜力且近期有触底迹象的股票。
    """
    # 1. 计算 ts_delta(vwap, 5)
    data_ts_delta_vwap = ts_delta(data['vwap'], d = 5)
    # 2. 计算 ts_scale(ts_delta(vwap, 5), 30)
    data_ts_scale = ts_scale(data_ts_delta_vwap, d = 30)
    # 3. 计算 ts_arg_min(close, 20)
    data_ts_arg_min_close = ts_arg_min(data['close'], d = 20)
    # 4. 计算 add(ts_arg_min(close, 20), 1)
    data_add = add(data_ts_arg_min_close, 1)
    # 5. 计算 divide(ts_scale(ts_delta(vwap, 5), 30), add(ts_arg_min(close, 20), 1))
    factor = divide(data_ts_scale, data_add)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()