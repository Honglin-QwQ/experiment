import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, ts_std_dev, divide, adv

def factor_6098(data, **kwargs):
    """
    因子名称: PriceVolumeVolatilitySkew_90697
    数学表达式: ts_skewness(divide(close, adv(vol, 5)), 10) * ts_std_dev(divide(close, adv(vol, 5)), 10)
    中文描述: 该因子计算收盘价与短期平均成交量比值的时序偏度和标准差的乘积。首先，通过计算收盘价除以5日平均成交量（adv(vol, 5)），得到一个衡量价格相对于近期成交活跃度的指标。然后，计算这个指标在过去10天内的偏度（ts_skewness）和标准差（ts_std_dev）。偏度衡量了该指标分布的对称性，标准差衡量了其波动性。将偏度和标准差相乘，旨在捕捉价格-成交量相对强度的波动特征和不对称性。正值可能表示在近期高成交量时价格倾向于出现正向的极端波动，负值则表示负向极端波动。这可以用于识别由成交量驱动的异常价格行为，可能预示着潜在的反转或趋势延续。
    因子应用场景：
    1. 识别成交量驱动的异常价格行为。
    2. 辅助判断潜在的反转或趋势延续。
    """
    # 1. 计算 adv(vol, 5)
    data_adv_vol = adv(data['vol'], d = 5)
    # 2. 计算 divide(close, adv(vol, 5))
    data_divide_close_adv_vol = divide(data['close'], data_adv_vol)
    # 3. 计算 ts_skewness(divide(close, adv(vol, 5)), 10)
    data_ts_skewness = ts_skewness(data_divide_close_adv_vol, d = 10)
    # 4. 计算 ts_std_dev(divide(close, adv(vol, 5)), 10)
    data_ts_std_dev = ts_std_dev(data_divide_close_adv_vol, d = 10)
    # 5. 计算 ts_skewness(divide(close, adv(vol, 5)), 10) * ts_std_dev(divide(close, adv(vol, 5)), 10)
    factor = data_ts_skewness * data_ts_std_dev

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()