import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_min_max_diff, ts_delta, ts_decay_exp_window, ts_corr

def factor_5785(data, **kwargs):
    """
    数学表达式: divide(ts_min_max_diff(ts_delta(vol, 5), 10, 0.4), ts_decay_exp_window(ts_corr(low, vol, 15), 7, 0.6))
    中文描述: 该因子旨在捕捉成交量变化的极值波动与价量关系衰减趋势的相对强度。首先，计算过去5天成交量(vol)的差值，并对该差值序列应用10天窗口、比例因子为0.4的最小值最大值差异运算。这部分衡量了短期成交量变化的极值波动。然后，计算过去15天最低价(low)与成交量(vol)的相关性，并对该相关性序列应用7天窗口、衰减因子为0.6的指数衰减加权平均。这部分捕捉了近期价量关系的衰减趋势。最终因子值是成交量变化极值波动部分除以价量关系衰减趋势部分。这个因子通过结合成交量趋势的极值分析和衰减的价量相关性，试图识别市场中潜在的能量积聚或释放。创新点在于将成交量的短期极值波动与价量关系的衰减趋势相结合，并通过除法操作构建新的关系，同时在参数和窗口期上进行了调整以期提升预测能力，并使用了divide运算符。
    因子应用场景：
    1. 市场能量识别： 用于识别市场中能量积聚或释放的潜在机会。
    2. 成交量波动分析： 评估成交量变化的极值波动强度。
    3. 价量关系趋势分析： 捕捉近期价量关系的衰减趋势。
    """
    # 1. 计算 ts_delta(vol, 5)
    data_ts_delta_vol = ts_delta(data['vol'], 5)
    # 2. 计算 ts_min_max_diff(ts_delta(vol, 5), 10, 0.4)
    data_ts_min_max_diff = ts_min_max_diff(data_ts_delta_vol, 10, 0.4)
    # 3. 计算 ts_corr(low, vol, 15)
    data_ts_corr = ts_corr(data['low'], data['vol'], 15)
    # 4. 计算 ts_decay_exp_window(ts_corr(low, vol, 15), 7, 0.6)
    data_ts_decay_exp_window = ts_decay_exp_window(data_ts_corr, 7, 0.6)
    # 5. 计算 divide(ts_min_max_diff(ts_delta(vol, 5), 10, 0.4), ts_decay_exp_window(ts_corr(low, vol, 15), 7, 0.6))
    factor = divide(data_ts_min_max_diff, data_ts_decay_exp_window)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()