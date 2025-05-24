import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_zscore, ts_std_dev, divide

def factor_5605(data, **kwargs):
    """
    因子名称: VolatilityAdjustedReturnsZScore_39070
    数学表达式: divide(ts_zscore(returns, 79), ts_std_dev(vol, 20))
    中文描述: 该因子是对时间序列标准分数（Z分数）因子的改进，通过将收益率的Z分数除以成交量的标准差，来调整收益率的波动性。原始的Z分数因子衡量了收益率相对于历史平均水平的偏差，而本因子进一步考虑了成交量的波动情况。当成交量波动较大时，收益率的Z分数会被相应地缩小，从而降低了高波动时期信号的强度；反之，当成交量波动较小时，收益率的Z分数会被放大，从而提高了低波动时期信号的强度。这种调整可以帮助投资者更好地识别具有持续性的价格趋势，并降低因市场噪音造成的误判风险。
    因子应用场景：
    1. 波动性调整： 调整收益率Z分数，降低高波动时期信号强度，提高低波动时期信号强度。
    2. 趋势识别： 帮助识别具有持续性的价格趋势，降低因市场噪音造成的误判风险。
    """
    # 1. 计算 ts_zscore(returns, 79)
    data_ts_zscore_returns = ts_zscore(data['returns'], d=79)
    # 2. 计算 ts_std_dev(vol, 20)
    data_ts_std_dev_vol = ts_std_dev(data['vol'], d=20)
    # 3. 计算 divide(ts_zscore(returns, 79), ts_std_dev(vol, 20))
    factor = divide(data_ts_zscore_returns, data_ts_std_dev_vol)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()