import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import adv, ts_product, ts_delta, ts_std_dev

def factor_5570(data, **kwargs):
    """
    因子名称: factor_volume_momentum_deviation_40165
    数学表达式: ts_delta(ts_product(adv(vol, 10), 5), 5) - ts_std_dev(ts_delta(ts_product(adv(vol, 10), 5), 5), 20)
    中文描述: 该因子旨在捕捉交易量动量的变化及其偏离程度。首先，计算过去10天平均交易量在过去5天内的乘积，以衡量短期交易量动量。然后，计算这个动量指标的5日差分，以捕捉动量变化的速度。最后，从动量变化的速度中减去过去20天动量变化速度的标准差，以衡量当前动量变化相对于历史波动率的偏离程度。该因子可用于识别交易量异常变化，可能预示着价格趋势的反转或加速。
    因子应用场景：
    1. 交易量异常检测：识别交易量突然放大或缩小的股票，可能预示着市场关注度的变化。
    2. 趋势反转预测：当因子值显著偏离历史水平时，可能预示着当前趋势即将发生反转。
    3. 交易策略优化：结合其他技术指标，优化交易策略，提高盈利能力。
    """
    # 1. 计算 adv(vol, 10)
    data_adv_vol = adv(data['vol'], d = 10)
    # 2. 计算 ts_product(adv(vol, 10), 5)
    data_ts_product = ts_product(data_adv_vol, d = 5)
    # 3. 计算 ts_delta(ts_product(adv(vol, 10), 5), 5)
    data_ts_delta = ts_delta(data_ts_product, d = 5)
    # 4. 计算 ts_std_dev(ts_delta(ts_product(adv(vol, 10), 5), 5), 20)
    data_ts_std_dev = ts_std_dev(data_ts_delta, d = 20)
    # 5. 计算 ts_delta(ts_product(adv(vol, 10), 5), 5) - ts_std_dev(ts_delta(ts_product(adv(vol, 10), 5), 5), 20)
    factor = subtract(data_ts_delta, data_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()