import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import multiply, floor, ts_std_dev
import pandas as pd

def factor_5725(data, **kwargs):
    """
    因子名称: VolumeVolatilityFloorProduct_65790
    数学表达式: multiply(volume, floor(ts_std_dev(volume, 5)))
    中文描述: 该因子结合了当前交易量和过去5天交易量标准差的向下取整值。首先计算过去5天交易量的标准差，然后向下取整，最后将当前交易量与这个取整后的标准差相乘。这个因子旨在捕捉在近期交易量波动较大的情况下，当前交易量的绝对水平。当近期交易量波动剧烈且当前交易量较高时，因子值会显著增大，可能预示着市场情绪的剧烈变化或潜在的价格大幅波动。这与参考因子'volume*floor(volume)'和'volume*ts_mean(volume,3)'有相似之处，都强调了交易量的重要性，但通过引入交易量波动性（标准差）并进行向下取整，增加了因子的复杂性和对市场异常活跃的敏感性。它可用于识别那些在交易量上既活跃又波动剧烈的股票，适合用于短期交易策略或捕捉市场热点。
    因子应用场景：
    1. 识别交易量波动性：用于识别交易量波动较大的股票，尤其是在短期内。
    2. 市场情绪判断：因子值增大可能预示市场情绪的剧烈变化或潜在的价格大幅波动。
    3. 短期交易策略：适用于短期交易策略，捕捉市场热点。
    """
    # 1. 计算 ts_std_dev(volume, 5)
    volume = data['vol']
    data_ts_std_dev = ts_std_dev(volume, d=5)
    # 2. 计算 floor(ts_std_dev(volume, 5))
    data_floor = floor(data_ts_std_dev)
    # 3. 计算 multiply(volume, floor(ts_std_dev(volume, 5)))
    factor = multiply(volume, data_floor)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()