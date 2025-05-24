import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_entropy

def factor_5748(data, **kwargs):
    """
    因子名称: VWAP_Trades_Entropy_Ratio_31742
    数学表达式: divide(ts_entropy(vwap, 106), ts_entropy(trades, 106))
    中文描述: 该因子计算了VWAP在过去106天的时间序列熵与交易笔数(trades)在过去106天的时间序列熵的比值。VWAP的熵衡量成交量加权平均价格的波动性和不确定性，而交易笔数的熵衡量交易活动的波动性和不确定性。通过计算两者的比值，该因子试图捕捉价格波动与交易活跃度之间的相对不确定性关系。高比值可能表明价格波动的不确定性相对于交易活动的波动性更高，反之亦然。这可以用于识别市场情绪、流动性变化以及潜在的价格趋势反转信号。创新点在于结合了两个不同维度的熵度量，并计算它们的比值来捕捉更深层次的市场结构信息。
    因子应用场景：
    1. 市场情绪识别：通过比较价格和交易量熵，识别市场情绪的变化。
    2. 风险管理：评估价格和交易量的不确定性，辅助风险管理。
    3. 趋势反转信号：寻找价格波动与交易活跃度之间关系的变化，捕捉潜在的价格趋势反转信号。
    """
    # 1. 计算 ts_entropy(vwap, 106)
    data_ts_entropy_vwap = ts_entropy(data['vwap'], 106)
    # 2. 计算 ts_entropy(trades, 106)
    data_ts_entropy_trades = ts_entropy(data['trades'], 106)
    # 3. 计算 divide(ts_entropy(vwap, 106), ts_entropy(trades, 106))
    factor = divide(data_ts_entropy_vwap, data_ts_entropy_trades)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()