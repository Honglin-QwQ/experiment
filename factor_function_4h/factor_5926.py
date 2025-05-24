import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_rank, divide

def factor_5926(data, **kwargs):
    """
    因子名称: VolumeVolatility_PriceRankRatio_73289
    数学表达式: divide(ts_std_dev(vol, 15), ts_rank(close, 10))
    中文描述: 该因子旨在衡量成交量波动性与收盘价短期相对位置的关系。它计算过去15天成交量的标准差，并将其除以当前收盘价在过去10天内的排名。高因子值可能表明在收盘价处于较低排名时，成交量波动剧烈，这可能预示着潜在的买入机会。相较于参考因子，创新点在于将价格与近期支撑位的距离替换为价格在近期内的排名，更侧重于捕捉价格的相对强度，并通过比率形式结合成交量波动性进行分析。根据历史评估结果，该因子调整了时间窗口，并尝试通过价格排名来捕捉与未来收益率可能存在的负相关关系。
    因子应用场景：
    1. 波动性分析：用于识别成交量波动较大且价格排名较低的股票，可能预示着市场关注度提升。
    2. 短期交易：高因子值可能提示潜在的买入机会，尤其是在市场调整期间。
    """
    # 1. 计算 ts_std_dev(vol, 15)
    data_ts_std_dev_vol = ts_std_dev(data['vol'], d = 15)
    # 2. 计算 ts_rank(close, 10)
    data_ts_rank_close = ts_rank(data['close'], d = 10)
    # 3. 计算 divide(ts_std_dev(vol, 15), ts_rank(close, 10))
    factor = divide(data_ts_std_dev_vol, data_ts_rank_close)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()