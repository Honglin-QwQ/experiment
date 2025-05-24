import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_exp_window, ts_entropy, ts_std_dev, divide

def factor_5865(data, **kwargs):
    """
    因子名称: WeightedVolumeEntropyVolatilityRatio_85126
    数学表达式: divide(ts_decay_exp_window(ts_entropy(vol, 20), 31, factor = 0.7), ts_std_dev(vol, 31))
    中文描述: 该因子计算过去31天内经过指数衰减加权处理的成交量时间序列熵与成交量标准差的比值。相较于参考因子，该因子在计算熵时使用了更短的时间窗口（20天），并对熵值进行了指数衰减加权处理（衰减因子0.7），使得因子对近期成交量分布的复杂性变化更加敏感。标准差仍沿用31天窗口。这旨在捕捉近期成交量波动模式中包含的信息量相对于其整体波动水平的相对强度，并赋予近期信息更高的权重。高比值可能表明近期成交量波动模式复杂且信息丰富，且这种复杂性正在衰减，而低比值可能表明近期成交量波动相对简单或随机，或者复杂性正在增强。这可以用于识别市场情绪变化或潜在的价格变动驱动因素，并对近期市场行为赋予更高的关注度。
    因子应用场景：
    1. 市场情绪识别：高比值可能表明市场情绪复杂，信息丰富，适用于识别市场情绪变化。
    2. 波动性分析：捕捉成交量波动模式中包含的信息量相对于其整体波动水平的相对强度。
    3. 短期趋势预测：对近期成交量分布的复杂性变化更加敏感，可用于短期趋势预测。
    """

    # 1. 计算 ts_entropy(vol, 20)
    data_ts_entropy = ts_entropy(data['vol'], 20)

    # 2. 计算 ts_decay_exp_window(ts_entropy(vol, 20), 31, factor = 0.7)
    data_ts_decay_exp_window = ts_decay_exp_window(data_ts_entropy, 31, factor = 0.7)

    # 3. 计算 ts_std_dev(vol, 31)
    data_ts_std_dev = ts_std_dev(data['vol'], 31)

    # 4. 计算 divide(ts_decay_exp_window(ts_entropy(vol, 20), 31, factor = 0.7), ts_std_dev(vol, 31))
    factor = divide(data_ts_decay_exp_window, data_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()