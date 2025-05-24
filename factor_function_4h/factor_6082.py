import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_std_dev, adv, rank

def factor_6082(data, **kwargs):
    """
    因子名称: Volume_Volatility_Ratio_Ranked_79539
    数学表达式: rank(divide(ts_std_dev(volume, d=15), adv(volume, d=25)))
    中文描述: 该因子计算了过去15天成交量的标准差与过去25天平均成交量的比值，并对结果进行排名。它旨在衡量成交量的波动性相对于其平均水平的强度，并将其在整个市场中进行比较。分子（成交量标准差）捕捉了成交量的短期波动程度；分母（平均成交量）提供了长期成交量的基准。通过计算比值并进行排名，该因子能够识别出那些在近期成交量波动相对于其平均水平异常活跃或沉寂的股票。这可能用于捕捉市场情绪的剧烈变化或潜在的交易机会。相较于参考因子，创新点在于结合了成交量的波动性（标准差）和平均水平，并通过排名操作进行横截面比较，提供了更丰富的成交量信息和相对强度评估。
    因子应用场景：
    1. 波动性识别：识别成交量波动较大的股票，可能预示着市场关注度高或存在潜在机会。
    2. 异常交易量检测：通过排名，可以发现成交量波动相对于平均水平异常的股票，可能存在异常交易行为。
    """
    # 1. 计算 ts_std_dev(volume, d=15)
    data_ts_std_dev = ts_std_dev(data['vol'], d=15)
    # 2. 计算 adv(volume, d=25)
    data_adv = adv(data['vol'], d=25)
    # 3. 计算 divide(ts_std_dev(volume, d=15), adv(volume, d=25))
    data_divide = divide(data_ts_std_dev, data_adv)
    # 4. 计算 rank(divide(ts_std_dev(volume, d=15), adv(volume, d=25)))
    factor = rank(data_divide, rate = 2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()