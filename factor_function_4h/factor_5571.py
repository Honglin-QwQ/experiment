import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_zscore, multiply, ts_rank, log, divide

def factor_5571(data, **kwargs):
    """
    数学表达式: ts_zscore(multiply(ts_rank(close, d=5), log(divide(high, low))), d=20)
    中文描述: 该因子结合了收盘价的短期排名、日内高低价格比率的对数以及时间序列Z-score。首先，计算过去5天收盘价的排名，然后计算每日最高价与最低价之比的自然对数，并将两者相乘。最后，计算这个乘积在过去20天内的Z-score。该因子旨在捕捉价格动量和波动率的结合，通过Z-score标准化，使其更具可比性。
    因子应用场景：
    1. 动量分析：用于识别价格动量较强且波动率较高的股票。
    2. 波动率交易：结合价格排名和波动率信息，辅助判断市场情绪和潜在的交易机会。
    3. 风险调整：通过Z-score标准化，使不同股票的因子值更具可比性，便于风险调整。
    """
    # 1. 计算 ts_rank(close, d=5)
    data_ts_rank = ts_rank(data['close'], d=5)
    # 2. 计算 divide(high, low)
    data_divide = divide(data['high'], data['low'])
    # 3. 计算 log(divide(high, low))
    data_log = log(data_divide)
    # 4. 计算 multiply(ts_rank(close, d=5), log(divide(high, low)))
    data_multiply = multiply(data_ts_rank, data_log)
    # 5. 计算 ts_zscore(multiply(ts_rank(close, d=5), log(divide(high, low))), d=20)
    factor = ts_zscore(data_multiply, d=20)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()