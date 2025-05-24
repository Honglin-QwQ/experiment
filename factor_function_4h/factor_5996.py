import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import ts_corr, ts_entropy, ts_delta

def factor_5996(data, **kwargs):
    """
    因子名称: VolumeEntropyPriceDeltaCorrelation_28648
    数学表达式: ts_corr(ts_entropy(ts_delta(vol, 2), 8), ts_delta(vwap, 4), 6)
    中文描述: 该因子基于对历史因子评估结果的分析和改进建议，旨在捕捉成交量变化率的随机性（熵）与成交量加权平均价格（VWAP）短期动量之间的关系。
    首先，计算过去8天成交量变化率的香农熵，衡量成交量变动模式的不可预测性。然后，计算当前VWAP与4天前VWAP的差值，代表短期VWAP变化。
    最后，计算这两个时间序列在过去6天内的滚动相关性。相较于原始因子，创新点在于：1. 计算熵的对象从原始成交量转变为成交量变化率，旨在捕捉波动率加速或减速的信息。
    2. 价格变化指标从简单的收盘价差值替换为VWAP的差值，引入了成交量信息来衡量价格变动的强度。3. 调整了计算熵、价格变化和相关性的时间窗口，以期找到更优的参数组合。
    高相关性可能表明VWAP趋势伴随着成交量变动模式的复杂性增加，可能预示着趋势的不可持续性或潜在的波动加剧；低相关性则可能指向更稳定的市场环境。
    这个因子提供了一个新的维度来理解成交量变动模式与价格行为之间的复杂相互作用，有助于识别不同市场阶段的特征，并尝试通过捕捉波动率变化率的熵来提高因子的预测能力。
    因子应用场景：
    1. 波动率预测：高因子值可能预示着市场波动性增加。
    2. 趋势分析：结合因子值与价格趋势，判断趋势的稳定性和可持续性。
    3. 市场阶段识别：用于区分不同的市场阶段，如稳定期、波动期等。
    """
    # 1. 计算 ts_delta(vol, 2)
    data_ts_delta_vol = ts_delta(data['vol'], 2)
    # 2. 计算 ts_entropy(ts_delta(vol, 2), 8)
    data_ts_entropy = ts_entropy(data_ts_delta_vol, 8)
    # 3. 计算 ts_delta(vwap, 4)
    data_ts_delta_vwap = ts_delta(data['vwap'], 4)
    # 4. 计算 ts_corr(ts_entropy(ts_delta(vol, 2), 8), ts_delta(vwap, 4), 6)
    factor = ts_corr(data_ts_entropy, data_ts_delta_vwap, 6)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()