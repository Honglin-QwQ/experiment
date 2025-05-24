import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_delay, sigmoid, ts_delta, multiply

def factor_5960(data, **kwargs):
    """
    因子名称: SigmoidWeightedVolumeTrend_20592
    数学表达式: multiply(ts_delay(vol, 1), sigmoid(ts_delta(vol, 1)))
    中文描述: 该因子通过将前一日的成交量与当日成交量变化（相对于前一日）的Sigmoid函数值相乘来捕捉成交量的动量和情绪。Sigmoid函数将成交量变化压缩到0到1之间，平滑了极端变化的影响，并赋予不同程度的成交量变化不同的权重。当成交量显著增加时，Sigmoid值接近1，因子值主要取决于前一日的成交量；当成交量显著减少时，Sigmoid值接近0，因子值趋近于零。这可以用于识别成交量持续增长或萎缩的趋势，并结合前一日的成交量水平来判断趋势的强度。创新点在于结合了时间延迟、差分和Sigmoid函数来刻画成交量的非线性变化和趋势。
    因子应用场景：
    1. 成交量趋势识别：用于识别成交量持续增长或萎缩的趋势。
    2. 动量和情绪分析：捕捉成交量的动量和市场情绪。
    3. 趋势强度判断：结合前一日的成交量水平来判断趋势的强度。
    """
    # 1. 计算 ts_delay(vol, 1)
    data_ts_delay_vol = ts_delay(data['vol'], 1)
    # 2. 计算 ts_delta(vol, 1)
    data_ts_delta_vol = ts_delta(data['vol'], 1)
    # 3. 计算 sigmoid(ts_delta(vol, 1))
    data_sigmoid_ts_delta_vol = sigmoid(data_ts_delta_vol)
    # 4. 计算 multiply(ts_delay(vol, 1), sigmoid(ts_delta(vol, 1)))
    factor = multiply(data_ts_delay_vol, data_sigmoid_ts_delta_vol)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()