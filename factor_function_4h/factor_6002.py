import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_mean, rank, ts_std_dev, ts_rank, ts_delta, multiply

def factor_6002(data, **kwargs):
    """
    因子名称: VWAP_Volatility_Trend_Interaction_67008
    数学表达式: ts_mean(rank(ts_std_dev(vwap, 15)) * ts_rank(ts_delta(vwap, 7), 20), 10)
    中文描述: 该因子旨在捕捉VWAP波动性排名与VWAP短期趋势排名之间的交互作用，并通过时间序列平均来平滑结果。
            首先，计算过去15天VWAP的标准差并对其进行排名，衡量波动性的相对水平。
            然后，计算过去7天VWAP的变化量，并对其在过去20天内进行排名，反映短期趋势的相对强度。
            将这两个排名相乘，得到一个结合波动性和趋势的交互项。
            最后，计算该交互项在过去10天内的平均值，以降低噪音并识别更持续的模式。
            创新点在于将波动性和趋势的相对排名进行乘积组合，并通过时间序列平均进一步提炼信号，旨在发现高波动性且具有明确短期趋势的市场状态。
    因子应用场景：
    1. 波动性与趋势结合： 适用于需要同时考虑资产波动性和趋势的交易策略。
    2. 短期交易： 适用于捕捉短期市场状态，例如日内或短线交易。
    3. 风险管理： 可用于识别高波动且趋势明显的资产，从而进行风险控制。
    """
    # 1. 计算 ts_std_dev(vwap, 15)
    data_ts_std_dev_vwap = ts_std_dev(data['vwap'], 15)
    # 2. 计算 rank(ts_std_dev(vwap, 15))
    data_rank_ts_std_dev_vwap = rank(data_ts_std_dev_vwap, 2)
    # 3. 计算 ts_delta(vwap, 7)
    data_ts_delta_vwap = ts_delta(data['vwap'], 7)
    # 4. 计算 ts_rank(ts_delta(vwap, 7), 20)
    data_ts_rank_ts_delta_vwap = ts_rank(data_ts_delta_vwap, 20)
    # 5. 计算 rank(ts_std_dev(vwap, 15)) * ts_rank(ts_delta(vwap, 7), 20)
    data_multiply = multiply(data_rank_ts_std_dev_vwap, data_ts_rank_ts_delta_vwap)
    # 6. 计算 ts_mean(rank(ts_std_dev(vwap, 15)) * ts_rank(ts_delta(vwap, 7), 20), 10)
    factor = ts_mean(data_multiply, 10)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()