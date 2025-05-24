import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_corr, ts_std_dev, divide, ts_delta, sign

import pandas as pd

def factor_6070(data, **kwargs):
    """
    因子名称: Volatility_Price_Change_Interaction_Rank_83758
    数学表达式: ts_rank(ts_corr(ts_std_dev(close, 90), divide(ts_delta(close, 45), close), 15) * sign(ts_std_dev(low, 180)), 8)
    中文描述: 该因子旨在捕捉收盘价波动率与标准化收盘价变化之间的短期相关性，并结合长期最低价波动率的方向进行加权，最后进行排名。它首先计算过去90天收盘价的标准差，衡量中期价格波动性。然后，计算当前收盘价与45天前收盘价的百分比变化，衡量中期价格变化。接着，计算这两个指标在过去15天内的相关系数。创新点在于，将这个相关系数乘以过去180天最低价标准差的符号（正负），以引入长期波动率的方向信息。最后，计算该加权相关系数在过去8天内的排名。高排名可能表明中期价格变化与波动率之间存在特定方向的强相关性，并得到长期波动率方向的印证，低排名则反之。相较于参考因子，该因子：1. 使用收盘价波动率代替最低价波动率，更直接反映整体价格波动；2. 使用标准化价格变化，消除价格水平差异的影响；3. 引入长期最低价波动率的符号作为权重，增加长期市场情绪的考量；4. 调整了所有时间窗口参数，并引入了乘法和符号操作符，以尝试捕捉更复杂的非线性关系和市场动态。这些改进是基于历史评估报告中关于参数优化、使用非线性操作符以及引入更多市场信息的建议。
    因子应用场景：
    1. 波动率与价格变化关系：该因子可用于识别波动率与价格变化之间存在特定关系（正相关或负相关）的股票。
    2. 趋势确认：结合长期波动率方向，可辅助判断当前趋势的可靠性。
    3. 市场情绪分析：长期最低价波动率的符号可作为市场情绪的指标，影响因子值。
    """
    # 1. 计算 ts_std_dev(close, 90)
    data_ts_std_dev_close = ts_std_dev(data['close'], 90)
    # 2. 计算 ts_delta(close, 45)
    data_ts_delta_close = ts_delta(data['close'], 45)
    # 3. 计算 divide(ts_delta(close, 45), close)
    data_divide = divide(data_ts_delta_close, data['close'])
    # 4. 计算 ts_corr(ts_std_dev(close, 90), divide(ts_delta(close, 45), close), 15)
    data_ts_corr = ts_corr(data_ts_std_dev_close, data_divide, 15)
    # 5. 计算 ts_std_dev(low, 180)
    data_ts_std_dev_low = ts_std_dev(data['low'], 180)
    # 6. 计算 sign(ts_std_dev(low, 180))
    data_sign = sign(data_ts_std_dev_low)
    # 7. 计算 ts_corr(ts_std_dev(close, 90), divide(ts_delta(close, 45), close), 15) * sign(ts_std_dev(low, 180))
    data_multiply = data_ts_corr * data_sign
    # 8. 计算 ts_rank(ts_corr(ts_std_dev(close, 90), divide(ts_delta(close, 45), close), 15) * sign(ts_std_dev(low, 180)), 8)
    factor = ts_rank(data_multiply, 8)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()