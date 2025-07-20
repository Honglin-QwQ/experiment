import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, divide, adv, ts_delta, multiply

def factor_0042(data, **kwargs):
    """
    数学表达式: (ts_rank((volume / adv20), 20) * ts_rank((-1 * ts_delta(close, 7)), 8))
    中文描述: 该因子首先计算过去20天成交量与过去20天平均成交量的比率，然后计算这个比率在过去20天内的排序，排序值越高代表最近成交量相对于平均成交量越大；同时，计算过去7天收盘价的变化量，并取负数，然后计算这个负变化量在过去8天内的排序，排序值越高代表最近收盘价下跌越多；最后，将这两个排序值相乘，得到最终的因子值。该因子试图捕捉成交量放大且价格下跌的股票，可能表明市场抛售压力较大，或者有资金在逢低吸纳。
    因子应用场景：
    1. 选股策略：选择因子值较高的股票，可能预示着短期内价格反弹的机会。
    2. 风险预警：因子值持续升高可能表明股票风险增加，需要谨慎对待。
    3. 量化对冲：结合其他因子，构建多因子模型，进行量化对冲交易。
    """
    # 1. 计算 adv20
    adv20 = adv(data['vol'], d=20)
    # 2. 计算 volume / adv20
    volume_adv_ratio = divide(data['vol'], adv20)
    # 3. 计算 ts_rank((volume / adv20), 20)
    rank_volume = ts_rank(volume_adv_ratio, d=20)
    # 4. 计算 ts_delta(close, 7)
    delta_close = ts_delta(data['close'], d=7)
    # 5. 计算 -1 * ts_delta(close, 7)
    negative_delta_close = multiply(-1, delta_close)
    # 6. 计算 ts_rank((-1 * ts_delta(close, 7)), 8)
    rank_price = ts_rank(negative_delta_close, d=8)
    # 7. 计算 (ts_rank((volume / adv20), 20) * ts_rank((-1 * ts_delta(close, 7)), 8))
    factor = multiply(rank_volume, rank_price)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()