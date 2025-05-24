import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import rank, add, ts_delta, ts_std_dev

def factor_5954(data, **kwargs):
    """
    数学表达式: rank(add(ts_delta(ts_std_dev(vwap, 15), 3), ts_delta(ts_std_dev(volume, 15), 3)))
    中文描述: 该因子计算短期（15天）VWAP标准差的3日变化与短期（15天）成交量标准差的3日变化的加总，并对其进行横截面排名。它旨在捕捉VWAP和成交量波动率短期变化的综合强度，并将其标准化到排名空间。当VWAP和成交量短期波动率同时出现显著变化时，该因子值会较高或较低，可能预示着市场情绪的短期转变或潜在的趋势形成。通过计算变化率加总和排名，因子值被映射到0到1之间，便于跨资产比较和策略构建。这结合了原始参考因子的VWAP、标准差和时间序列分位数概念，通过计算VWAP和成交量波动性变化率的加总并进行排名处理的创新结构，提供了对市场动态更细致且具有相对意义的洞察，并根据历史评估结果调整了时间窗口以尝试提高预测能力和稳定性。
    因子应用场景：
    1. 波动率变化识别：用于识别VWAP和成交量波动率短期变化的综合强度。
    2. 市场情绪转变：捕捉市场情绪的短期转变或潜在趋势形成。
    3. 跨资产比较：将因子值映射到0到1之间，便于跨资产比较和策略构建。
    """
    # 1. 计算 ts_std_dev(vwap, 15)
    data_ts_std_dev_vwap = ts_std_dev(data['vwap'], 15)
    # 2. 计算 ts_delta(ts_std_dev(vwap, 15), 3)
    data_ts_delta_ts_std_dev_vwap = ts_delta(data_ts_std_dev_vwap, 3)
    # 3. 计算 ts_std_dev(volume, 15)
    data_ts_std_dev_volume = ts_std_dev(data['vol'], 15)
    # 4. 计算 ts_delta(ts_std_dev(volume, 15), 3)
    data_ts_delta_ts_std_dev_volume = ts_delta(data_ts_std_dev_volume, 3)
    # 5. 计算 add(ts_delta(ts_std_dev(vwap, 15), 3), ts_delta(ts_std_dev(volume, 15), 3))
    data_add = add(data_ts_delta_ts_std_dev_vwap, data_ts_delta_ts_std_dev_volume)
    # 6. 计算 rank(add(ts_delta(ts_std_dev(vwap, 15), 3), ts_delta(ts_std_dev(volume, 15), 3)))
    factor = rank(data_add, 2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()