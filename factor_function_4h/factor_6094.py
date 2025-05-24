import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_mean, subtract, ts_skewness, ts_corr, ts_decay_exp_window, rank

def factor_6094(data, **kwargs):
    """
    数学表达式: rank(ts_decay_exp_window(ts_corr(ts_mean(subtract(high, low), 5), ts_skewness(close, 10), 10), 0.7))
    中文描述: 该因子计算过去5天日内波动率（high-low的平均值）与过去10天收盘价偏度在过去10天内的相关性，然后对这个相关性结果应用指数衰减加权平均（衰减因子0.7），最后对衰减后的结果进行排名。
    这个因子在参考因子的基础上进行了多方面的创新：1. 使用日内波动率的平均值（ts_mean(subtract(high, low), 5)）替代标准差，以降低对极端值的敏感性；
    2. 扩展了收盘价偏度的计算窗口（从5天到10天），以捕捉更稳定的偏度信息；3. 对相关性结果应用指数衰减加权平均，赋予近期数据更大的权重，从而更好地反映当前市场动态；
    4. 最终对衰减后的结果进行排名，以消除绝对值的影响并进行横截面比较。高排名可能表示近期市场波动特征之间的关系正在加强，且这种关系在近期数据中更为突出，可能预示着市场情绪或趋势的变化。
    因子应用场景：
    1. 市场情绪分析：用于识别市场情绪的变化，高排名可能预示着市场情绪的转变。
    2. 趋势预测：用于辅助判断市场趋势，尤其是在市场波动特征关系加强时。
    """
    # 1. 计算 subtract(high, low)
    data_subtract = subtract(data['high'], data['low'])
    # 2. 计算 ts_mean(subtract(high, low), 5)
    data_ts_mean = ts_mean(data_subtract, 5)
    # 3. 计算 ts_skewness(close, 10)
    data_ts_skewness = ts_skewness(data['close'], 10)
    # 4. 计算 ts_corr(ts_mean(subtract(high, low), 5), ts_skewness(close, 10), 10)
    data_ts_corr = ts_corr(data_ts_mean, data_ts_skewness, 10)
    # 5. 计算 ts_decay_exp_window(ts_corr(ts_mean(subtract(high, low), 5), ts_skewness(close, 10), 10), 0.7)
    data_ts_decay_exp_window = ts_decay_exp_window(data_ts_corr, d = 10, factor = 0.7)
    # 6. 计算 rank(ts_decay_exp_window(ts_corr(ts_mean(subtract(high, low), 5), ts_skewness(close, 10), 10), 0.7))
    factor = rank(data_ts_decay_exp_window, rate = 2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()