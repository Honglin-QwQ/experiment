import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_max_diff, ts_std_dev
import pandas as pd

def factor_5703(data, **kwargs):
    """
    数学表达式: rank(ts_corr(ts_max_diff(open, 104), ts_std_dev(close, 20), 10))
    中文描述: 该因子结合了参考因子中的开盘价最大差（ts_max_diff(open, 104)）和收盘价的波动率（ts_std_dev(close, 20)），计算这两者在过去10天内的滚动相关系数，并对这个相关系数进行截面排名。

    创新点在于：
    1. 结构创新：将一个基于价格偏离历史高点的因子与基于收盘价的波动率因子相结合，通过计算它们的时间序列相关性，来捕捉价格偏离与市场波动性之间的动态关系。
    2. 逻辑创新：不再只关注价格偏离本身或与成交量的关系，而是引入波动率作为衡量市场不确定性的指标。高相关性可能意味着价格偏离历史高点时伴随着市场波动性的增加，这可能预示着趋势的加强或潜在的反转。
    3. 元素组成创新：在参考因子使用'open'和'vol'的基础上，引入了'close'来计算波动率。

    改进方向的体现：
    1. 因子计算逻辑的改进：引入了波动率（ts_std_dev(close, 20)）作为新的元素，替代了原因子中的成交量，旨在捕捉价格偏离与市场不确定性之间的关系，这比单纯与成交量关联更具经济学意义。
    2. 参数优化方向：调整了ts_corr的窗口期从5天到10天，尝试捕捉更中期的相关性。
    3. 通过什么类型的操作符可以提升因子：继续使用了rank操作符进行截面排名，以消除量纲差异并提高稳定性。

    该因子可能用于识别那些在价格大幅偏离历史高点时伴随有市场波动性显著变化的股票。高排名可能预示着市场情绪的剧烈变化，可用于动量或反转策略，同时考虑了风险因素（波动率）。
    
    因子应用场景：
    1. 识别价格大幅偏离历史高点且伴随市场波动性显著变化的股票。
    2. 用于动量或反转策略，结合风险因素（波动率）进行决策。
    """
    # 1. 计算 ts_max_diff(open, 104)
    data_ts_max_diff_open = ts_max_diff(data['open'], d=104)
    # 2. 计算 ts_std_dev(close, 20)
    data_ts_std_dev_close = ts_std_dev(data['close'], d=20)
    # 3. 计算 ts_corr(ts_max_diff(open, 104), ts_std_dev(close, 20), 10)
    data_ts_corr = ts_corr(data_ts_max_diff_open, data_ts_std_dev_close, d=10)
    # 4. 计算 rank(ts_corr(ts_max_diff(open, 104), ts_std_dev(close, 20), 10))
    factor = rank(data_ts_corr, rate=2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()