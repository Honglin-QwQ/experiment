import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_delta, inverse, ts_std_dev, log, adv, multiply

def factor_5609(data, **kwargs):
    """
    因子名称: factor_0002_96097
    数学表达式: ts_rank(ts_delta(close, 3), 10) * inverse(ts_std_dev(vol, 5)) * log(adv(20))
    中文描述: 该因子在历史因子factor_0001的基础上，引入了log(adv(20))。ts_rank(ts_delta(close, 3), 10) * inverse(ts_std_dev(vol, 5))反映了价格动量和成交量波动率的结合，而log(adv(20))则表示过去20天平均成交量的对数，可以理解为市场活跃度的度量。该因子旨在识别价格快速上涨、成交量相对稳定且市场活跃度高的股票，可能代表市场关注度提升和价格趋势的持续性，同时考虑了成交量的规模效应。
    因子应用场景：
    1. 识别价格快速上涨、成交量相对稳定且市场活跃度高的股票。
    2. 辅助判断市场关注度提升和价格趋势的持续性。
    3. 结合成交量规模效应进行选股。
    """
    # 1. 计算 ts_delta(close, 3)
    data_ts_delta = ts_delta(data['close'], d=3)
    # 2. 计算 ts_rank(ts_delta(close, 3), 10)
    data_ts_rank = ts_rank(data_ts_delta, d=10)
    # 3. 计算 ts_std_dev(vol, 5)
    data_ts_std_dev = ts_std_dev(data['vol'], d=5)
    # 4. 计算 inverse(ts_std_dev(vol, 5))
    data_inverse = inverse(data_ts_std_dev)
    # 5. 计算 adv(20)
    data_adv = adv(data['vol'], d=20)
    # 6. 计算 log(adv(20))
    data_log = log(data_adv)
    # 7. 计算 ts_rank(ts_delta(close, 3), 10) * inverse(ts_std_dev(vol, 5)) * log(adv(20))
    factor = multiply(data_ts_rank, data_inverse, data_log)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()