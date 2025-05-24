import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_corr, ts_delta, divide, ts_std_dev
import pandas as pd

def factor_5884(data, **kwargs):
    """
    因子名称: Volume_Weighted_Price_Momentum_Divergence_95367
    数学表达式: ts_corr(ts_delta(divide(amount, vol), 10), ts_std_dev(close, 20), 30)
    中文描述: 该因子旨在捕捉成交量加权平均价格（VWAP的简化形式，用交易额/成交量近似）的短期变化与收盘价波动性之间的关系。
    它首先计算近似VWAP的10日差值，反映短期价格动量。然后计算过去20天收盘价的标准差，反映价格波动性。
    最后，计算这两者在过去30天的滚动相关性。正相关可能表明短期价格动量与波动性同向变动，预示趋势的延续或强化；
    负相关则可能表明价格动量与波动性背离，可能预示趋势的减弱或反转。相较于参考因子和历史输出因子，该因子引入了交易额和成交量计算的近似VWAP，
    更能反映真实交易成本和市场情绪对价格的影响，并结合价格动量和波动性相关性，具有更强的市场行为捕捉能力和创新性。
    同时，根据历史评估结果和改进建议，适当调整了时间窗口参数，并替换了主动买卖比率为交易额/成交量，以期提高因子的预测能力和稳定性。
    特别地，我们尝试了改进建议中提到的优化时间窗口和重新定义相对价格变化的思路，使用交易额/成交量作为价格的代理，并调整了ts_delta和ts_corr的周期。

    因子应用场景：
    1. 趋势识别：通过相关性判断价格动量与波动性是否同向变动，辅助识别趋势的延续或反转。
    2. 背离分析：负相关可能预示价格动量与波动性背离，可能预示趋势的减弱或反转。
    3. 市场情绪捕捉：使用交易额/成交量近似VWAP，更能反映真实交易成本和市场情绪对价格的影响。
    """
    # 1. 计算 divide(amount, vol)
    data_divide = divide(data['amount'], data['vol'])
    # 2. 计算 ts_delta(divide(amount, vol), 10)
    data_ts_delta = ts_delta(data_divide, 10)
    # 3. 计算 ts_std_dev(close, 20)
    data_ts_std_dev = ts_std_dev(data['close'], 20)
    # 4. 计算 ts_corr(ts_delta(divide(amount, vol), 10), ts_std_dev(close, 20), 30)
    factor = ts_corr(data_ts_delta, data_ts_std_dev, 30)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()