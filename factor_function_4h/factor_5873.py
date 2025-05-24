import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import divide, ts_mean, subtract, ts_std_dev
import pandas as pd

def factor_5873(data, **kwargs):
    """
    因子名称: VolatilityAdjustedTradePressure_46507
    数学表达式: divide(ts_mean(subtract(tbase, tquote), 5), ts_std_dev(amount, 10))
    中文描述: 该因子衡量了短期内主动买卖压力的平均值相对于中期交易额波动性的比例。具体而言，它计算了过去5天主动买入量与主动卖出量差值的平均值，并将其除以过去10天交易额的标准差。当主动买入压力持续存在且交易额波动较低时，因子值可能为正且较大，表明买方力量稳定且市场风险较低。反之，当主动卖出压力占主导且交易额波动较高时，因子值可能为负且较小，表明卖方力量强大且市场风险较高。这可能用于识别在相对稳定市场环境下的资金流向和交易压力。创新点在于结合了主动买卖量（tbase和tquote）来衡量真实的交易压力，并与交易额的波动性相结合，以更全面地评估市场情绪和风险。参考了原始因子中对价格波动和开盘收盘关系的关注，以及对交易量波动性的衡量，但通过引入主动买卖量和交易额波动性，提供了新的视角。同时考虑了历史输出中因子预测能力弱和稳定性差的问题，尝试通过更直接的交易压力指标和波动性调整来提升因子的有效性。改进建议中提到的Rank操作符和标准化操作可以在后续进一步优化中考虑。
    因子应用场景：
    1. 衡量市场买卖压力：用于识别市场中主动买入和卖出力量的强弱，判断市场情绪。
    2. 评估市场风险：结合交易额波动性，评估市场的稳定性和风险水平。
    3. 资金流向分析：识别资金在相对稳定市场环境下的流向。
    """
    # 1. 计算 subtract(tbase, tquote)
    data_subtract = subtract(data['tbase'], data['tquote'])
    # 2. 计算 ts_mean(subtract(tbase, tquote), 5)
    data_ts_mean = ts_mean(data_subtract, 5)
    # 3. 计算 ts_std_dev(amount, 10)
    data_ts_std_dev = ts_std_dev(data['amount'], 10)
    # 4. 计算 divide(ts_mean(subtract(tbase, tquote), 5), ts_std_dev(amount, 10))
    factor = divide(data_ts_mean, data_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()