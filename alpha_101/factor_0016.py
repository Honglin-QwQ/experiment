import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_rank, ts_delta, adv, divide, multiply

def factor_0016(data, **kwargs):
    """
    数学表达式: (((-1 * rank(ts_rank(close, 10))) * rank(ts_delta(ts_delta(close, 1), 1))) * rank(ts_rank((volume / adv20), 5))) 
    中文描述: 该因子首先计算过去10天收盘价的时间序列排名，然后取负并再次进行横截面排名；接着计算收盘价两次一阶差分的时间序列差分，再进行横截面排名；然后计算过去20天成交量的平均值，用当日成交量除以该平均值，再计算过去5天该比率的时间序列排名，最后进行横截面排名；将这三个排名值相乘。该因子试图捕捉价格动量和成交量变化的组合效应，可能反映了市场情绪、趋势强度和交易活跃度。
    因子应用场景包括：
    1. 趋势跟踪策略：结合其他技术指标，判断趋势的启动或反转。
    2. 量价关系分析：识别成交量异动配合价格变化的股票，寻找潜在的交易机会。
    3. 短线交易：在量化模型中作为输入特征，预测股票短期内的超额收益。
    """
    # 1. 计算 ts_rank(close, 10)
    data_ts_rank_close_10 = ts_rank(data['close'], 10)
    # 2. 计算 rank(ts_rank(close, 10))
    data_rank_ts_rank_close_10 = rank(data_ts_rank_close_10, 2)
    # 3. 计算 -1 * rank(ts_rank(close, 10))
    data_neg_rank_ts_rank_close_10 = multiply(-1, data_rank_ts_rank_close_10, filter=False)
    # 4. 计算 ts_delta(close, 1)
    data_ts_delta_close_1 = ts_delta(data['close'], 1)
    # 5. 计算 ts_delta(ts_delta(close, 1), 1)
    data_ts_delta_ts_delta_close_1_1 = ts_delta(data_ts_delta_close_1, 1)
    # 6. 计算 rank(ts_delta(ts_delta(close, 1), 1))
    data_rank_ts_delta_ts_delta_close_1_1 = rank(data_ts_delta_ts_delta_close_1_1, 2)
    # 7. 计算 adv20
    data_adv20 = adv(data['vol'], d = 20)
    # 8. 计算 volume / adv20
    data_volume_div_adv20 = divide(data['vol'], data_adv20)
    # 9. 计算 ts_rank((volume / adv20), 5)
    data_ts_rank_volume_div_adv20_5 = ts_rank(data_volume_div_adv20, 5)
    # 10. 计算 rank(ts_rank((volume / adv20), 5))
    data_rank_ts_rank_volume_div_adv20_5 = rank(data_ts_rank_volume_div_adv20_5, 2)
    # 11. 计算 (-1 * rank(ts_rank(close, 10))) * rank(ts_delta(ts_delta(close, 1), 1))
    data_part1 = multiply(data_neg_rank_ts_rank_close_10, data_rank_ts_delta_ts_delta_close_1_1, filter=False)
    # 12. 计算 ((-1 * rank(ts_rank(close, 10))) * rank(ts_delta(ts_delta(close, 1), 1))) * rank(ts_rank((volume / adv20), 5))
    factor = multiply(data_part1, data_rank_ts_rank_volume_div_adv20_5, filter=False)

    # 删除中间变量
    del data_ts_rank_close_10
    del data_rank_ts_rank_close_10
    del data_neg_rank_ts_rank_close_10
    del data_ts_delta_close_1
    del data_ts_delta_ts_delta_close_1_1
    del data_rank_ts_delta_ts_delta_close_1_1
    del data_adv20
    del data_volume_div_adv20
    del data_ts_rank_volume_div_adv20_5
    del data_rank_ts_rank_volume_div_adv20_5
    del data_part1

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()