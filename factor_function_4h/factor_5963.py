import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
from operators import rank
from operators import ts_skewness
from operators import adv
from operators import ts_std_dev
from operators import divide
import pandas as pd

def factor_5963(data, **kwargs):
    """
    因子名称: VolumeVolatilitySkewRatio_94693
    数学表达式: divide(rank(ts_skewness(adv(vol, 10), 20)), rank(ts_std_dev(adv(vol, 10), 20)))
    中文描述: 该因子计算过去20天内，过去10天平均成交量的偏度排名，并将其除以过去20天内过去10天平均成交量的标准差排名。在参考因子 VolatilityAdjustedVolumeRankRatio 的基础上，本因子将 'ts_max' 替换为 'ts_skewness'，引入了成交量分布形态的信息。通过比较成交量偏度和标准差的排名，该因子旨在识别成交量分布不对称且波动性相对较低的交易机会。高因子值表示在成交量分布偏度较高（可能意味着有大单或集中交易）时期，成交量的波动性排名相对较低，可能预示着更稳定的价格趋势或潜在的交易机会。该因子结合了成交量信息、时间序列偏度和波动性，并通过排名化处理增强了其稳定性和预测能力，适用于识别成交量分布特征显著且波动性相对较低的交易机会。
    因子应用场景：
    1. 识别成交量分布不对称且波动性相对较低的交易机会。
    2. 辅助判断价格趋势的稳定性。
    3. 寻找潜在的交易机会。
    """
    # 1. 计算 adv(vol, 10)
    data_adv = adv(data['vol'], d = 10)
    # 2. 计算 ts_skewness(adv(vol, 10), 20)
    data_ts_skewness = ts_skewness(data_adv, d = 20)
    # 3. 计算 rank(ts_skewness(adv(vol, 10), 20))
    data_rank_skewness = rank(data_ts_skewness, rate = 2)
    # 4. 计算 ts_std_dev(adv(vol, 10), 20)
    data_ts_std_dev = ts_std_dev(data_adv, d = 20)
    # 5. 计算 rank(ts_std_dev(adv(vol, 10), 20))
    data_rank_std_dev = rank(data_ts_std_dev, rate = 2)
    # 6. 计算 divide(rank(ts_skewness(adv(vol, 10), 20)), rank(ts_std_dev(adv(vol, 10), 20)))
    factor = divide(data_rank_skewness, data_rank_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()