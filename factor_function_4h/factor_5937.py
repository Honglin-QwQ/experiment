import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_delta, ts_min_diff

def factor_5937(data, **kwargs):
    """
    因子名称: PriceMomentum_MinDiff_Ratio_26394
    数学表达式: divide(ts_delta(close, 1), ts_min_diff(close, 77))
    中文描述: 该因子结合了短期价格变化和长期价格底部差异的信息。它计算了当前收盘价与前一日收盘价的差值（短期动量），然后将其除以当前收盘价与过去77天最低收盘价的差值（长期底部差异）。这个因子的创新之处在于，它不是简单地将两个指标相乘，而是通过除法来衡量短期动量相对于长期底部差异的强度。当短期价格上涨（ts_delta(close, 1) > 0）并且价格已经远离长期底部（ts_min_diff(close, 77) 较大）时，因子值会相对较小，可能表明上涨动量正在减弱。反之，如果短期价格上涨但仍然接近长期底部，因子值会较大，可能预示着强劲的反弹潜力。该因子可用于识别那些在经历长期低迷后开始出现强劲反弹的股票，或者那些短期上涨但可能面临回调的股票。它结合了参考因子中使用的close和ts_min_diff，并引入了ts_delta和divide运算符，通过比率的方式捕捉价格行为的相对强度。
    """
    # 1. 计算 ts_delta(close, 1)
    data_ts_delta = ts_delta(data['close'], 1)
    # 2. 计算 ts_min_diff(close, 77)
    data_ts_min_diff = ts_min_diff(data['close'], 77)
    # 3. 计算 divide(ts_delta(close, 1), ts_min_diff(close, 77))
    factor = divide(data_ts_delta, data_ts_min_diff)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()