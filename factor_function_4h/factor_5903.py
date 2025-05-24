import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_decay_linear, divide, ts_delay

def factor_5903(data, **kwargs):
    """
    数学表达式: rank(ts_decay_linear(divide(amount, vol), 15)) / rank(ts_decay_linear(divide(vol, amount), 15)) - rank(ts_decay_linear(divide(close, ts_delay(close, 1)), 10))
    中文描述: 该因子旨在捕捉价格变化率与成交额/成交量比率（平均价格）之间的动态关系。它在原始因子的基础上进行了多方面的创新和改进。首先，它计算了成交额/成交量比率和成交量/成交额比率（即平均价格及其倒数）的过去15天的线性衰减加权平均，并对它们进行排名。与原始因子直接相减不同，这里使用了排名之间的比率，以放大两者的相对差异。其次，因子引入了过去10天收盘价日收益率的线性衰减加权平均的排名，并将其从前面的比率中减去。这部分创新地结合了价格变化的信息，旨在捕捉价格动量对量价关系的影响。当平均价格的衰减排名与单位交易额成交量的衰减排名差异较大（比率较高），并且近期价格上涨动量较弱时，因子值可能较高，反之亦然。这可能有助于识别市场中量价背离或协同的信号，为交易决策提供更丰富的视角。参数15和10是根据历史评估建议调整的，以尝试寻找更优的时间窗口。
    因子应用场景：
    1. 量价关系分析：用于识别市场中量价背离或协同的信号。
    2. 趋势判断：结合价格动量信息，辅助判断市场趋势的强弱。
    3. 交易决策：为交易决策提供更丰富的视角，辅助识别潜在的交易机会。
    """
    # 1. 计算 divide(amount, vol)
    data_divide_amount_vol = divide(data['amount'], data['vol'])
    # 2. 计算 ts_decay_linear(divide(amount, vol), 15)
    data_ts_decay_linear_amount_vol = ts_decay_linear(data_divide_amount_vol, d=15)
    # 3. 计算 rank(ts_decay_linear(divide(amount, vol), 15))
    data_rank_ts_decay_linear_amount_vol = rank(data_ts_decay_linear_amount_vol, rate = 2)
    # 4. 计算 divide(vol, amount)
    data_divide_vol_amount = divide(data['vol'], data['amount'])
    # 5. 计算 ts_decay_linear(divide(vol, amount), 15)
    data_ts_decay_linear_vol_amount = ts_decay_linear(data_divide_vol_amount, d=15)
    # 6. 计算 rank(ts_decay_linear(divide(vol, amount), 15))
    data_rank_ts_decay_linear_vol_amount = rank(data_ts_decay_linear_vol_amount, rate = 2)
    # 7. 计算 divide(close, ts_delay(close, 1))
    data_ts_delay_close = ts_delay(data['close'], d=1)
    data_divide_close_ts_delay_close = divide(data['close'], data_ts_delay_close)
    # 8. 计算 ts_decay_linear(divide(close, ts_delay(close, 1)), 10)
    data_ts_decay_linear_close_ts_delay_close = ts_decay_linear(data_divide_close_ts_delay_close, d=10)
    # 9. 计算 rank(ts_decay_linear(divide(close, ts_delay(close, 1)), 10))
    data_rank_ts_decay_linear_close_ts_delay_close = rank(data_ts_decay_linear_close_ts_delay_close, rate = 2)
    # 10. 计算 rank(ts_decay_linear(divide(amount, vol), 15)) / rank(ts_decay_linear(divide(vol, amount), 15)) - rank(ts_decay_linear(divide(close, ts_delay(close, 1)), 10))
    factor = data_rank_ts_decay_linear_amount_vol / data_rank_ts_decay_linear_vol_amount - data_rank_ts_decay_linear_close_ts_delay_close

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()