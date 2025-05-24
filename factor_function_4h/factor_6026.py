import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_std_dev

def factor_6026(data, **kwargs):
    """
    因子名称: VolumeVolatilityCorrelation_76101
    数学表达式: ts_corr(vol, ts_std_dev(close, 20), 10)
    中文描述: 该因子计算过去10天内成交量与过去20天收盘价标准差（波动率）之间的相关性。它旨在捕捉交易量与价格波动之间的动态关系。高相关性可能表明交易量的变化与市场波动性紧密相关，例如在波动加剧时交易活跃度也随之增加。创新点在于结合了成交量和不同时间窗口的波动率，并使用时间序列相关性来衡量其相互影响，这可能揭示出更深层次的市场情绪和交易行为模式。
    因子应用场景：
    1. 市场情绪分析：通过观察成交量与波动率的相关性，可以推断市场情绪。例如，高相关性可能出现在市场恐慌或乐观时期。
    2. 风险管理：该因子可以帮助识别交易量和波动率同步增加的股票，这些股票可能具有较高的风险。
    3. 交易策略：可以根据成交量和波动率的相关性设计交易策略，例如在两者相关性较高时进行趋势交易。
    """
    # 1. 计算 ts_std_dev(close, 20)
    data_ts_std_dev = ts_std_dev(data['close'], 20)
    # 2. 计算 ts_corr(vol, ts_std_dev(close, 20), 10)
    factor = ts_corr(data['vol'], data_ts_std_dev, 10)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()