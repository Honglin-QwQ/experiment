import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_delta, ts_median, abs, ts_returns, divide

def factor_6044(data, **kwargs):
    """
    因子名称: VolatilityAdjustedPriceDeviation_Robust_70451
    数学表达式: divide(ts_delta(close, 2), ts_median(abs(ts_returns(close, 1, mode=1)), 30))
    中文描述: 该因子是原因子的改进版本，旨在提高预测能力和稳定性。它计算的是过去两天收盘价变化与过去30天日收益率绝对值中位数的比值。相较于原因子使用标准差作为波动率衡量，这里采用中位数绝对偏差（通过计算收益率绝对值的历史中位数来近似），使其对极端值更加鲁棒。同时，将价格变化的时间窗口从1天增加到2天，旨在捕捉更长期一些的价格动量。因子值越大，表示过去两天的价格变动相对于近期波动性越显著且方向性更强。这可能有助于识别更持续的价格趋势或反转信号。
    因子应用场景：
    1. 趋势识别：因子值较高可能表示价格趋势较强。
    2. 反转信号：极高的因子值可能预示价格反转。
    3. 波动率调整：用于调整价格变动，使其与近期波动率水平相对应。
    """
    # 1. 计算 ts_delta(close, 2)
    data_ts_delta_close = ts_delta(data['close'], d = 2)
    # 2. 计算 ts_returns(close, 1, mode=1)
    data_ts_returns_close = ts_returns(data['close'], d = 1, mode = 1)
    # 3. 计算 abs(ts_returns(close, 1, mode=1))
    data_abs_ts_returns_close = abs(data_ts_returns_close)
    # 4. 计算 ts_median(abs(ts_returns(close, 1, mode=1)), 30)
    data_ts_median_abs_ts_returns_close = ts_median(data_abs_ts_returns_close, d = 30)
    # 5. 计算 divide(ts_delta(close, 2), ts_median(abs(ts_returns(close, 1, mode=1)), 30))
    factor = divide(data_ts_delta_close, data_ts_median_abs_ts_returns_close)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()