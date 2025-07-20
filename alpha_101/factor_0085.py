import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_sum, subtract, add, ts_rank, adv

def factor_0085(data, **kwargs):
    """
    数学表达式: ((ts_rank(ts_corr(close, ts_sum(adv20, 14.7444), 6.00049), 20.4195) < rank(((open + close) - (vwap + open)))) * -1)
    中文描述: 该因子首先计算收盘价与过去14.7444天平均成交额之和的相关性，窗口期为6.00049天，然后计算该相关性在过去20.4195天内的排名。
             接着，计算（开盘价+收盘价）与（平均成交价+开盘价）的差值，并计算该差值的排名。
             如果相关性排名的值小于差值排名的值，则结果为-1，否则为0。
             该因子试图捕捉成交量与价格之间的关系，如果近期成交量与价格之和的相关性排名较低，同时价格变化（开盘价和收盘价与成交均价和开盘价的差值）的排名较高，则该因子输出-1。
    因子应用场景：
    1. 可以用于识别价格与成交量背离的股票，例如，当价格上涨但成交量没有相应增加时，该因子可能发出信号。
    2. 可以作为短线反转策略的一部分，当因子值为-1时，可能预示着股票价格即将下跌。
    3. 可以与其他因子结合使用，例如，与动量因子或超买超卖指标结合，以提高选股的准确性。
    """

    # 计算 ts_sum(adv20, 14.7444)
    adv20 = adv(data['vol'],20)
    data['adv20'] = adv20
    data_ts_sum = ts_sum(data['adv20'], d = 15)

    # 计算 ts_corr(close, ts_sum(adv20, 14.7444), 6.00049)
    data_ts_corr = ts_corr(data['close'], data_ts_sum, d = 6)

    # 计算 ts_rank(ts_corr(close, ts_sum(adv20, 14.7444), 6.00049), 20.4195)
    data_ts_rank1 = ts_rank(data_ts_corr, d = 20)

    # 计算 (open + close)
    data_add1 = add(data['open'], data['close'])

    # 计算 (vwap + open)
    data_add2 = add(data['vwap'], data['open'])

    # 计算 ((open + close) - (vwap + open))
    data_subtract = subtract(data_add1, data_add2)

    # 计算 rank(((open + close) - (vwap + open)))
    data_rank = rank(data_subtract, rate = 2)

    # 计算 (ts_rank(ts_corr(close, ts_sum(adv20, 14.7444), 6.00049), 20.4195) < rank(((open + close) - (vwap + open))))
    condition = data_ts_rank1 < data_rank

    # 计算 ((ts_rank(ts_corr(close, ts_sum(adv20, 14.7444), 6.00049), 20.4195) < rank(((open + close) - (vwap + open)))) * -1)
    factor = condition.astype(int) * -1

    del data['adv20']

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()