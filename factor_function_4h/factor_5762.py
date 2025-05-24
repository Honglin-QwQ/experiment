import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_corr, rank, ts_std_dev

def factor_5762(data, **kwargs):
    """
    数学表达式: ts_rank(ts_corr(low, vol, 15), 100) - rank(ts_std_dev(close, 20))
    中文描述: 该因子结合了价格与交易量的短期相关性排名和收盘价的长期波动性排名。首先计算过去15天最低价与交易量的相关性，并对其在过去100天内进行时间序列排名。然后计算过去20天收盘价的标准差，并对其进行横截面排名。最终因子值为前者减去后者。该因子旨在捕捉那些在短期内价量关系稳定且长期价格波动相对较小的股票，可能用于识别具有潜在稳定增长趋势的标的。创新点在于结合了时间序列排名和横截面排名，以及使用最低价而非收盘价与交易量进行相关性分析，以更精细地捕捉价格底部区域的交易行为。
    因子应用场景：
    1. 稳定增长趋势识别：用于识别短期价量关系稳定，长期价格波动较小的股票，这些股票可能具有稳定增长的潜力。
    2. 底部区域交易行为分析：通过最低价与交易量的相关性，捕捉价格底部区域的交易行为，辅助判断潜在的支撑位。
    3. 风险评估：结合波动率排名，可以帮助评估股票的风险水平，选择风险调整后收益较高的标的。
    """
    # 1. 计算 ts_corr(low, vol, 15)
    data_ts_corr = ts_corr(data['low'], data['vol'], 15)
    # 2. 计算 ts_rank(ts_corr(low, vol, 15), 100)
    data_ts_rank = ts_rank(data_ts_corr, 100)
    # 3. 计算 ts_std_dev(close, 20)
    data_ts_std_dev = ts_std_dev(data['close'], 20)
    # 4. 计算 rank(ts_std_dev(close, 20))
    data_rank = rank(data_ts_std_dev, 2)
    # 5. 计算 ts_rank(ts_corr(low, vol, 15), 100) - rank(ts_std_dev(close, 20))
    factor = data_ts_rank - data_rank

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()