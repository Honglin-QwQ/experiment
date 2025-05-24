import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_std_dev, ts_rank, ts_decay_linear, multiply

def factor_5889(data, **kwargs):
    """
    数学表达式: rank(ts_std_dev(vwap, 10)) * ts_rank(ts_decay_linear(ts_std_dev(amount, 15), 10), 5)
    中文描述: 该因子旨在捕捉成交量加权平均价格（VWAP）的短期波动性，并结合交易额波动性的线性衰减排名。具体来说，因子计算了过去10天VWAP的标准差，并对其进行横截面排名。然后，乘以过去15天交易额标准差的过去10天线性衰减值的过去5天时间序列排名。该因子结合了价格和交易额的波动性特征，通过VWAP标准差捕捉价格波动，通过交易额标准差捕捉市场活跃度波动，并通过线性衰减和双重排名（横截面和时间序列）来捕捉相对强度和趋势，试图识别波动性特征的持续性和相对强度。创新点在于结合了VWAP的波动性、交易额波动性的线性衰减以及双重排名，以更精细地捕捉市场波动结构的变化，并根据历史评估报告，尝试通过乘法组合两个相对独立的波动性度量，并利用线性衰减和双重排名来提高因子的稳定性和预测能力。
    因子应用场景：
    1. 波动性分析：用于识别价格和交易额波动性均较高的股票。
    2. 趋势跟踪：结合线性衰减和排名，捕捉波动性趋势。
    3. 市场活跃度评估：通过交易额波动性评估市场活跃度。
    """
    # 1. 计算 ts_std_dev(vwap, 10)
    data_ts_std_dev_vwap = ts_std_dev(data['vwap'], 10)
    # 2. 计算 rank(ts_std_dev(vwap, 10))
    factor1 = rank(data_ts_std_dev_vwap, 2)
    # 3. 计算 ts_std_dev(amount, 15)
    data_ts_std_dev_amount = ts_std_dev(data['amount'], 15)
    # 4. 计算 ts_decay_linear(ts_std_dev(amount, 15), 10)
    data_ts_decay_linear = ts_decay_linear(data_ts_std_dev_amount, 10)
    # 5. 计算 ts_rank(ts_decay_linear(ts_std_dev(amount, 15), 10), 5)
    factor2 = ts_rank(data_ts_decay_linear, 5)
    # 6. 计算 rank(ts_std_dev(vwap, 10)) * ts_rank(ts_decay_linear(ts_std_dev(amount, 15), 10), 5)
    factor = multiply(factor1, factor2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()