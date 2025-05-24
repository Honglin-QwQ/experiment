import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_linear, ts_std_dev, ts_delta

def factor_6005(data, **kwargs):
    """
    因子名称: VolumeVolatilityAcceleration_76846
    数学表达式: ts_decay_linear(delta(ts_std_dev(vol, 15), 2), 20)
    中文描述: 该因子旨在捕捉成交量波动性变化的加速度，并对其进行线性衰减加权平均。首先计算过去15天的成交量标准差，衡量短期成交量波动性。然后计算这个波动性指标的2日差分，反映波动性变化的速率。最后，对这个速率的每日变化（即加速度）计算过去20天的线性衰减加权平均，给予近期变化更高的权重。这可以用来识别成交量波动性加速或减速的趋势，可能预示着市场情绪的快速变化或潜在的价格拐点。相较于参考因子直接寻找波动性峰值，本因子关注波动性变化的速率和加速度，并引入线性衰减，提供了对市场动态更精细的捕捉能力，并参考了改进建议中提到的使用delta和decay_linear操作符来提升因子的表现。
    因子应用场景：
    1. 识别成交量波动性加速或减速的趋势。
    2. 预示市场情绪的快速变化或潜在的价格拐点。
    """
    # 1. 计算 ts_std_dev(vol, 15)
    data_ts_std_dev = ts_std_dev(data['vol'], 15)
    # 2. 计算 delta(ts_std_dev(vol, 15), 2)
    data_delta = ts_delta(data_ts_std_dev, 2)
    # 3. 计算 ts_decay_linear(delta(ts_std_dev(vol, 15), 2), 20)
    factor = ts_decay_linear(data_delta, 20)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()