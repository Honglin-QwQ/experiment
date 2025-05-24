import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import log_diff, ts_rank, adv, sigmoid, ts_delta, ts_zscore, multiply

def factor_5635(data, **kwargs):
    """
    因子名称: factor_0002_81798
    数学表达式: ts_zscore(log_diff(high), ts_rank(adv(vol, 20), 10)) * sigmoid(ts_delta(close, 5))
    中文描述: 该因子结合了高价波动率的Z分数、成交量平均排名的Z分数以及收盘价动量的Sigmoid函数。首先计算高价的对数差分并进行Z分数标准化，然后乘以收盘价5日差分的Sigmoid函数值。Sigmoid函数将收盘价的动量转化为0到1之间的权重，从而调节高价波动率对因子值的影响。该因子旨在捕捉高价异常波动且伴随收盘价趋势变化的股票。
    因子应用场景：
    1. 捕捉高价异常波动且伴随收盘价趋势变化的股票。
    """
    # 1. 计算 log_diff(high)
    data['log_diff_high'] = log_diff(data['high'])

    # 2. 计算 adv(vol, 20)
    data['adv_vol_20'] = adv(data['vol'], d=20)

    # 3. 计算 ts_rank(adv(vol, 20), 10)
    data['ts_rank_adv_vol_20'] = ts_rank(data['adv_vol_20'], d=10)

    # 4. 计算 ts_zscore(log_diff(high), ts_rank(adv(vol, 20), 10))
    data['ts_zscore_log_diff_high'] = ts_zscore(data['log_diff_high'], d=6)
    data['ts_zscore_ts_rank_adv_vol_20'] = ts_zscore(data['ts_rank_adv_vol_20'], d=6)
    factor_left = data['ts_zscore_log_diff_high']

    # 5. 计算 ts_delta(close, 5)
    data['ts_delta_close_5'] = ts_delta(data['close'], d=5)

    # 6. 计算 sigmoid(ts_delta(close, 5))
    data['sigmoid_ts_delta_close_5'] = sigmoid(data['ts_delta_close_5'])

    # 7. 计算 ts_zscore(log_diff(high), ts_rank(adv(vol, 20), 10)) * sigmoid(ts_delta(close, 5))
    factor = multiply(factor_left, data['sigmoid_ts_delta_close_5'])

    # 删除中间变量
    del data['log_diff_high']
    del data['adv_vol_20']
    del data['ts_rank_adv_vol_20']
    del data['ts_zscore_log_diff_high']
    del data['ts_zscore_ts_rank_adv_vol_20']
    del data['ts_delta_close_5']
    del data['sigmoid_ts_delta_close_5']

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()