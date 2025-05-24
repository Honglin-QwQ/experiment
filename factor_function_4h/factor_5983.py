import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_delta, ts_rank, divide, multiply

def factor_5983(data, **kwargs):
    """
    因子名称: Volatility_Rank_Weighted_Price_Change_35551
    数学表达式: multiply(ts_std_dev(ts_delta(low, 3), 66), ts_rank(divide(ts_delta(close, 1), open), 5))
    中文描述: 该因子结合了市场低价波动率和短期价格变化排名。首先，计算每日最低价在过去3天内的变化，并计算这些变化在过去66天内的标准差，作为市场波动率的度量。然后，计算每日收盘价相对于开盘价的短期变化（收益率），并计算其在过去5天内的排名。最后，将波动率度量与短期价格变化排名相乘。该因子的创新点在于将长期波动率与短期价格变化排名相结合，试图捕捉波动性背景下的短期价格动量或反转机会。高波动率且短期价格变化排名靠前的股票可能预示着强劲的上涨动能，而高波动率且短期价格变化排名靠后的股票可能预示着下跌风险或潜在反弹。该因子可用于识别波动市场中的交易机会。
    因子应用场景：
    1. 波动性交易：在波动率较高的市场中，该因子可以帮助识别短期价格动量或反转的机会。
    2. 动量交易：结合波动率和价格变化排名，可以发现具有上涨动能的股票。
    3. 反转交易：识别高波动率下价格排名靠后的股票，可能预示着潜在的反弹机会。
    """
    # 1. 计算 ts_delta(low, 3)
    data_ts_delta_low = ts_delta(data['low'], 3)
    # 2. 计算 ts_std_dev(ts_delta(low, 3), 66)
    data_ts_std_dev = ts_std_dev(data_ts_delta_low, 66)
    # 3. 计算 ts_delta(close, 1)
    data_ts_delta_close = ts_delta(data['close'], 1)
    # 4. 计算 divide(ts_delta(close, 1), open)
    data_divide = divide(data_ts_delta_close, data['open'])
    # 5. 计算 ts_rank(divide(ts_delta(close, 1), open), 5)
    data_ts_rank = ts_rank(data_divide, 5)
    # 6. 计算 multiply(ts_std_dev(ts_delta(low, 3), 66), ts_rank(divide(ts_delta(close, 1), open), 5))
    factor = multiply(data_ts_std_dev, data_ts_rank)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()