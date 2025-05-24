import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd

def factor_5877(data, **kwargs):
    """
    因子名称: VolumeChangeVolatilityRatio_22294
    数学表达式: divide(ts_mean(ts_delta(volume, 5), 3), ts_std_dev(amount, 10))
    中文描述: 该因子计算过去3天内交易量5日变动的平均值，并将其除以过去10天的交易额标准差。它结合了交易量的短期平均变化和交易额的长期波动性。因子逻辑在于捕捉短期交易量平均变化相对于整体市场活跃度波动性的信号。如果短期交易量平均变动较大且为正（平均增长），同时相对于交易额波动性较高，可能预示着资金的积极流入和潜在的上涨动能。反之，如果平均变动为负（平均下降）或相对于交易额波动性较低，则可能表明市场兴趣减弱或资金流出。创新点在于将交易量的短期平均变化与交易额的长期波动性相结合，形成一个相对指标，更全面地衡量市场活跃度和资金流向的稳定性。相较于历史输出，我们将分子中的乘积替换为平均值，以减少噪声放大，并将分母中的均值替换为标准差，以衡量市场活跃度的波动性，从而提高因子的稳健性和预测能力。
    因子应用场景：
    1. 市场活跃度分析：用于衡量市场短期交易量变化相对于长期交易额波动性的活跃程度。
    2. 资金流向判断：辅助判断资金流入流出情况，交易量增加且交易额波动大可能预示资金流入。
    3. 趋势判断：结合其他因子，辅助判断股票上涨或下跌趋势。
    """
    # 1. 计算 ts_delta(volume, 5)
    data_ts_delta_volume = ts_delta(data['vol'], 5)
    # 2. 计算 ts_mean(ts_delta(volume, 5), 3)
    data_ts_mean = ts_mean(data_ts_delta_volume, 3)
    # 3. 计算 ts_std_dev(amount, 10)
    data_ts_std_dev = ts_std_dev(data['amount'], 10)
    # 4. 计算 divide(ts_mean(ts_delta(volume, 5), 3), ts_std_dev(amount, 10))
    factor = divide(data_ts_mean, data_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()