import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_delta, inverse, ts_std_dev, log, divide, adv

def factor_5614(data, **kwargs):
    """
    数学表达式: ts_rank(ts_delta(close, 3), 10) * inverse(ts_std_dev(close, 20)) * log(divide(vol, adv(20)))
    中文描述: 该因子基于历史因子factor_0002进行改进，旨在结合价格动量、价格波动率和相对成交量来识别潜在的交易机会。ts_rank(ts_delta(close, 3), 10)反映了短期价格变化的动量，inverse(ts_std_dev(close, 20))衡量了价格的长期波动率，而log(divide(vol, adv(20)))则表示当前成交量与过去20天平均成交量的比率的对数，可以理解为成交量相对活跃度的度量。相较于历史因子，该因子使用close计算波动率，减少了异常成交量数据的影响，并使用相对成交量而非平均成交量的对数，更能捕捉成交量突然放大的情况。该因子旨在识别价格快速上涨、价格波动相对稳定且成交量显著高于平均水平的股票，可能代表市场关注度提升和价格趋势的持续性，同时考虑了成交量的相对变化。
    因子应用场景：
    1. 动量捕捉：捕捉短期价格快速上涨的股票。
    2. 波动率分析：筛选价格波动相对稳定的股票。
    3. 成交量活跃度：识别成交量显著高于平均水平的股票，可能代表市场关注度提升。
    """
    # 1. 计算 ts_delta(close, 3)
    data_ts_delta = ts_delta(data['close'], d=3)
    # 2. 计算 ts_rank(ts_delta(close, 3), 10)
    data_ts_rank = ts_rank(data_ts_delta, d=10)
    # 3. 计算 ts_std_dev(close, 20)
    data_ts_std_dev = ts_std_dev(data['close'], d=20)
    # 4. 计算 inverse(ts_std_dev(close, 20))
    data_inverse = inverse(data_ts_std_dev)
    # 5. 计算 adv(20)
    data_adv = adv(data['vol'], d=20)
    # 6. 计算 divide(vol, adv(20))
    data_divide = divide(data['vol'], data_adv)
    # 7. 计算 log(divide(vol, adv(20)))
    data_log = log(data_divide)
    # 8. 计算 ts_rank(ts_delta(close, 3), 10) * inverse(ts_std_dev(close, 20)) * log(divide(vol, adv(20)))
    factor = data_ts_rank * data_inverse * data_log

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()