import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_delay, sign, ts_sum, subtract, divide, add, multiply

def factor_0029(data, **kwargs):
    """
    数学表达式: (((1.0 - rank(((sign((close - ts_delay(close, 1))) + sign((ts_delay(close, 1) - ts_delay(close, 2)))) + sign((ts_delay(close, 2) - ts_delay(close, 3)))))) * ts_sum(volume, 5)) / ts_sum(volume, 20)) 
    中文描述: 详细描述：该因子首先计算过去三天收盘价变化趋势的加总，如果连续两天上涨或下跌，则对应部分为正或负，然后用1减去该趋势和的排序百分比，得到一个趋势反转的信号，再将该信号乘以过去5天成交量的总和，最后除以过去20天成交量的总和，得到一个成交量加权的趋势反转指标，表明近期成交量相对活跃时，短期趋势反转的强度。
    因子应用场景：
    1. 短线反转策略：当因子值较高时，可能预示着短期下跌趋势即将结束，可以考虑买入；
    2. 趋势跟踪策略的过滤条件：避免在因子值较高时追涨，降低趋势跟踪策略的风险；
    3. 量价关系分析：结合成交量和价格趋势，判断市场情绪和潜在的买卖压力。
    """
    # 计算 ts_delay(close, 1)
    ts_delay_close_1 = ts_delay(data['close'], 1)
    # 计算 (close - ts_delay(close, 1))
    close_diff_1 = subtract(data['close'], ts_delay_close_1)
    # 计算 sign(close - ts_delay(close, 1))
    sign_close_diff_1 = sign(close_diff_1)
    # 计算 ts_delay(close, 2)
    ts_delay_close_2 = ts_delay(data['close'], 2)
    # 计算 (ts_delay(close, 1) - ts_delay(close, 2))
    close_diff_2 = subtract(ts_delay_close_1, ts_delay_close_2)
    # 计算 sign(ts_delay(close, 1) - ts_delay(close, 2))
    sign_close_diff_2 = sign(close_diff_2)
    # 计算 ts_delay(close, 3)
    ts_delay_close_3 = ts_delay(data['close'], 3)
    # 计算 (ts_delay(close, 2) - ts_delay(close, 3))
    close_diff_3 = subtract(ts_delay_close_2, ts_delay_close_3)
    # 计算 sign(ts_delay(close, 2) - ts_delay(close, 3))
    sign_close_diff_3 = sign(close_diff_3)
    # 计算 (sign((close - ts_delay(close, 1))) + sign((ts_delay(close, 1) - ts_delay(close, 2))))
    sum_sign_1_2 = add(sign_close_diff_1, sign_close_diff_2)
    # 计算 ((sign((close - ts_delay(close, 1))) + sign((ts_delay(close, 1) - ts_delay(close, 2)))) + sign((ts_delay(close, 2) - ts_delay(close, 3))))
    sum_sign_1_3 = add(sum_sign_1_2, sign_close_diff_3)
    # 计算 rank(((sign((close - ts_delay(close, 1))) + sign((ts_delay(close, 1) - ts_delay(close, 2)))) + sign((ts_delay(close, 2) - ts_delay(close, 3)))))
    rank_sum_sign = rank(sum_sign_1_3)
    # 计算 (1.0 - rank(((sign((close - ts_delay(close, 1))) + sign((ts_delay(close, 1) - ts_delay(close, 2)))) + sign((ts_delay(close, 2) - ts_delay(close, 3))))))
    factor_1 = subtract(1.0, rank_sum_sign)
    # 计算 ts_sum(volume, 5)
    ts_sum_volume_5 = ts_sum(data['vol'], 5)
    # 计算 ((1.0 - rank(((sign((close - ts_delay(close, 1))) + sign((ts_delay(close, 1) - ts_delay(close, 2)))) + sign((ts_delay(close, 2) - ts_delay(close, 3)))))) * ts_sum(volume, 5))
    factor_2 = multiply(factor_1, ts_sum_volume_5)
    # 计算 ts_sum(volume, 20)
    ts_sum_volume_20 = ts_sum(data['vol'], 20)
    # 计算 (((1.0 - rank(((sign((close - ts_delay(close, 1))) + sign((ts_delay(close, 1) - ts_delay(close, 2)))) + sign((ts_delay(close, 2) - ts_delay(close, 3)))))) * ts_sum(volume, 5)) / ts_sum(volume, 20))
    factor = divide(factor_2, ts_sum_volume_20)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()