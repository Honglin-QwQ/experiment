import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_max_diff, ts_std_dev, ts_min, divide

def factor_6038(data, **kwargs):
    """
    因子名称: VWAP_Price_Momentum_Volatility_Ratio_78185
    数学表达式: divide(ts_max_diff(vwap, 73), ts_std_dev(ts_min(returns, 4), 6))
    中文描述: 该因子综合考虑了VWAP的长期动量、短期收益率的下行风险以及短期收益率的波动性。它计算了当前VWAP与过去73天VWAP最大值的差值，并将其除以过去6天短期最小收益率的标准差。分子反映了价格从近期高点回落的幅度，可能预示着价格的潜在反转或回调；分母则衡量了短期收益率的波动性，代表了下行风险的不确定性。这个因子通过将价格动量与短期风险波动性相结合，旨在捕捉那些在经历一定程度价格回落后，短期收益率波动性较低的股票，可能预示着相对稳定的潜在反弹机会。创新点在于结合了长期VWAP动量和短期收益率波动性，构建了一个反映价格回落与风险波动的比率，提供了更全面的视角来评估潜在的交易机会。
    因子应用场景：
    1. 寻找潜在反弹机会：该因子可以帮助识别那些价格从高点回落，但短期收益率波动性较低的股票，这些股票可能具有潜在的反弹机会。
    2. 风险评估：通过结合价格动量和收益率波动性，该因子可以提供更全面的风险评估，帮助投资者更好地管理投资组合的风险。
    """
    # 1. 计算 ts_max_diff(vwap, 73)
    data_ts_max_diff_vwap = ts_max_diff(data['vwap'], 73)
    # 2. 计算 ts_min(returns, 4)
    data_ts_min_returns = ts_min(data['returns'], 4)
    # 3. 计算 ts_std_dev(ts_min(returns, 4), 6)
    data_ts_std_dev = ts_std_dev(data_ts_min_returns, 6)
    # 4. 计算 divide(ts_max_diff(vwap, 73), ts_std_dev(ts_min(returns, 4), 6))
    factor = divide(data_ts_max_diff_vwap, data_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()