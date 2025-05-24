import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, ts_std_dev, divide

def factor_5825(data, **kwargs):
    """
    因子名称: Volume_Volatility_Skew_Ratio_36118
    数学表达式: divide(ts_skewness(vol, 20), ts_std_dev(vol, 60))
    中文描述: 该因子计算了过去20天交易量偏度与过去60天交易量标准差之比。偏度衡量交易量分布的对称性，标准差衡量交易量的波动性。高偏度（正偏）表示交易量分布右侧有较长的尾部，即存在大量异常高的交易量；低偏度（负偏）表示交易量分布左侧有较长的尾部，即存在大量异常低的交易量。将短期交易量偏度与中期交易量波动性结合，旨在捕捉交易量分布形态的变化相对于整体波动水平的强度。相较于参考因子，该因子引入了偏度这一统计量，提供了关于交易量分布形态的新信息，而不仅仅是简单的波动性或变化率。通过将偏度与标准差结合，可以识别在不同波动环境下，交易量异常变动的相对重要性。例如，在低波动环境下出现显著正偏度，可能预示着资金的异常流入和潜在的价格变动。该因子可用于识别市场情绪的变化、资金流动的异常情况，并可能预示着短期价格趋势的变化。
    因子应用场景：
    1. 识别市场情绪的变化。
    2. 识别资金流动的异常情况。
    3. 预测短期价格趋势的变化。
    """
    # 1. 计算 ts_skewness(vol, 20)
    data_ts_skewness = ts_skewness(data['vol'], 20)
    # 2. 计算 ts_std_dev(vol, 60)
    data_ts_std_dev = ts_std_dev(data['vol'], 60)
    # 3. 计算 divide(ts_skewness(vol, 20), ts_std_dev(vol, 60))
    factor = divide(data_ts_skewness, data_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()