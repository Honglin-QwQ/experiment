import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_returns, ts_std_dev, ts_mean, divide, rank

def factor_5569(data, **kwargs):
    """
    因子名称: factor_ATR_volatility_ratio_rank_65002
    数学表达式: rank(divide(ts_std_dev(ts_returns(high, 5), 20), ts_mean(vol, 20)))
    中文描述: 该因子旨在衡量过去20天内，5日收益率标准差与过去20天平均成交量的比率的排名。因子首先计算过去5天最高价的收益率，并计算其20日标准差作为价格波动率的衡量，然后除以过去20天的平均成交量，得到一个波动率/成交量的比率，最后对这个比率进行排名。创新点在于使用最高价的收益率标准差来衡量波动率，并对波动率/成交量的比率进行排名，使得因子更具可比性。这可能用于识别成交量较低、价格波动较大，且排名较高的股票。
    因子应用场景：
    1. 识别成交量较低、价格波动较大，且排名较高的股票。
    """
    # 1. 计算 ts_returns(high, 5)
    data_ts_returns = ts_returns(data['high'], 5)
    # 2. 计算 ts_std_dev(ts_returns(high, 5), 20)
    data_ts_std_dev = ts_std_dev(data_ts_returns, 20)
    # 3. 计算 ts_mean(vol, 20)
    data_ts_mean = ts_mean(data['vol'], 20)
    # 4. 计算 divide(ts_std_dev(ts_returns(high, 5), 20), ts_mean(vol, 20))
    data_divide = divide(data_ts_std_dev, data_ts_mean)
    # 5. 计算 rank(divide(ts_std_dev(ts_returns(high, 5), 20), ts_mean(vol, 20)))
    factor = rank(data_divide, 2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()