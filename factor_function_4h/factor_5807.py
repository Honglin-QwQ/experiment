import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_rank, ts_std_dev

def factor_5807(data, **kwargs):
    """
    因子名称: Volatility_Weighted_Volume_Rank_Ratio_69301
    数学表达式: divide(ts_rank(vol, 10), ts_std_dev(close, 10))
    中文描述: 该因子计算过去10天成交量的时间序列排名与过去10天收盘价标准差的比值。成交量排名反映了近期交易活跃度在一段时间内的相对位置，而收盘价标准差衡量了近期的价格波动性。将成交量排名除以波动性，旨在识别在相对较低波动性时期伴随较高相对成交量的股票，这可能预示着在市场平静期内资金的悄然流入。该因子创新性地结合了时间序列排名和波动性指标，通过比值关系捕捉市场在不同波动环境下的交易行为特征，为投资者提供一个衡量成交量强度相对于价格波动风险的新视角。
    因子应用场景：
    1. 识别潜在的资金流入：当成交量排名较高且波动性较低时，可能表明资金正在悄然流入该股票。
    2. 衡量成交量强度：通过将成交量排名与波动性进行比较，可以更准确地衡量成交量的强度。
    3. 风险调整的成交量分析：该因子提供了一个风险调整的视角来分析成交量，有助于识别在承担较小风险的情况下具有较高交易活跃度的股票。
    """
    # 1. 计算 ts_rank(vol, 10)
    data_ts_rank_vol = ts_rank(data['vol'], 10)
    # 2. 计算 ts_std_dev(close, 10)
    data_ts_std_dev_close = ts_std_dev(data['close'], 10)
    # 3. 计算 divide(ts_rank(vol, 10), ts_std_dev(close, 10))
    factor = divide(data_ts_rank_vol, data_ts_std_dev_close)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()