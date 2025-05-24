import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_exp_window, ts_corr, divide, rank

def factor_5920(data, **kwargs):
    """
    因子名称: ts_decay_exp_window_ts_corr_price_vol_rank_75610
    数学表达式: ts_decay_exp_window(ts_corr(divide(high, low), vol, 15), factor=0.8) * rank(vol)
    中文描述: 该因子旨在捕捉价格波动与成交量之间的动态关系，并结合成交量的相对强度。首先，计算过去15天最高价与最低价之比（代表价格波动）与成交量之间的滚动相关性。然后，对该相关性应用衰减因子为0.8的指数衰减加权平均，使得近期的数据对相关性影响更大。最后，将衰减后的相关性与当前成交量的横截面排名相乘。这个因子可能用于识别在价格波动加剧或减缓时，成交量的配合程度，以及成交量在市场中的相对活跃度，从而辅助判断趋势的持续性或潜在反转。相较于参考因子，创新点在于使用了最高价与最低价之比作为价格波动的代理，并结合了指数衰减加权平均和成交量排名，形成一个更细致刻画量价关系的因子。改进方向上，参考了评估报告中关于引入非线性变换和关注价格与成交量关系的建议，使用了价格波动的比值和成交量排名，并调整了时间窗口和衰减系数。
    因子应用场景：
    1. 量价关系分析：识别价格波动与成交量之间的相关性，判断趋势的可靠性。
    2. 市场活跃度评估：结合成交量的排名，评估股票在市场中的活跃程度。
    3. 趋势反转预测：辅助判断趋势的持续性或潜在反转。
    """
    # 1. 计算 divide(high, low)
    data_divide = divide(data['high'], data['low'])
    # 2. 计算 ts_corr(divide(high, low), vol, 15)
    data_ts_corr = ts_corr(data_divide, data['vol'], d=15)
    # 3. 计算 ts_decay_exp_window(ts_corr(divide(high, low), vol, 15), factor=0.8)
    data_ts_decay_exp_window = ts_decay_exp_window(data_ts_corr, factor=0.8)
    # 4. 计算 rank(vol)
    data_rank = rank(data['vol'])
    # 5. 计算 ts_decay_exp_window(ts_corr(divide(high, low), vol, 15), factor=0.8) * rank(vol)
    factor = data_ts_decay_exp_window * data_rank

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()