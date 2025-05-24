import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_sum, ts_corr, abs, ts_delta, log, ts_rank, signed_power, sigmoid, adv

def factor_5693(data, **kwargs):
    """
    因子名称: factor_0008_64403
    数学表达式: ts_sum(ts_corr(abs(ts_delta(log(close), 1)), ts_rank(signed_power(vol, 0.5), 10), 5), 10) * sigmoid(ts_delta(adv(vol, 20), 5))
    中文描述: 该因子是factor_0007的改进版本，旨在增强其对市场成交量变化的敏感性，并利用sigmoid函数对成交量变化进行平滑和约束。它结合了对数收益率动量、成交量排名和相关性分析，并引入了成交量变化的Sigmoid加权。首先计算收盘价对数的一阶差分，反映价格的瞬时变化率；然后对成交量取0.5次幂，并计算过去10天成交量幂函数的排名，衡量市场活跃度；接着计算这两个序列在过去5天的相关性，捕捉价格变化与成交量之间的关系；然后对过去10天的相关性进行求和，平滑短期波动，从而识别长期趋势；最后乘以成交量变化率的sigmoid值，目的是为了根据成交量的变化程度对因子进行加权，当成交量迅速增加时，sigmoid函数会趋近于1，因子权重增加，反之则趋近于0，因子权重降低。创新点在于引入了sigmoid函数对成交量变化进行加权，使得因子对成交量的变化更加敏感，从而可能提高因子的预测能力。该因子旨在发现价格动量与成交量之间的联动效应，可用于量化选股，识别具有持续上涨潜力的股票。
    因子应用场景：
    1. 量化选股：识别具有持续上涨潜力的股票。
    2. 市场成交量变化敏感性分析：增强因子对市场成交量变化的敏感性。
    """
    # 1. 计算 log(close)
    log_close = log(data['close'])
    # 2. 计算 ts_delta(log(close), 1)
    ts_delta_log_close = ts_delta(log_close, 1)
    # 3. 计算 abs(ts_delta(log(close), 1))
    abs_ts_delta_log_close = abs(ts_delta_log_close)
    # 4. 计算 signed_power(vol, 0.5)
    signed_power_vol = signed_power(data['vol'], 0.5)
    # 5. 计算 ts_rank(signed_power(vol, 0.5), 10)
    ts_rank_signed_power_vol = ts_rank(signed_power_vol, 10)
    # 6. 计算 ts_corr(abs(ts_delta(log(close), 1)), ts_rank(signed_power(vol, 0.5), 10), 5)
    ts_corr_factor = ts_corr(abs_ts_delta_log_close, ts_rank_signed_power_vol, 5)
    # 7. 计算 ts_sum(ts_corr(abs(ts_delta(log(close), 1)), ts_rank(signed_power(vol, 0.5), 10), 5), 10)
    ts_sum_ts_corr_factor = ts_sum(ts_corr_factor, 10)
    # 8. 计算 adv(vol, 20)
    adv_vol = adv(data['vol'], 20)
    # 9. 计算 ts_delta(adv(vol, 20), 5)
    ts_delta_adv_vol = ts_delta(adv_vol, 5)
    # 10. 计算 sigmoid(ts_delta(adv(vol, 20), 5))
    sigmoid_ts_delta_adv_vol = sigmoid(ts_delta_adv_vol)
    # 11. 计算 ts_sum(ts_corr(abs(ts_delta(log(close), 1)), ts_rank(signed_power(vol, 0.5), 10), 5), 10) * sigmoid(ts_delta(adv(vol, 20), 5))
    factor = ts_sum_ts_corr_factor * sigmoid_ts_delta_adv_vol

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()