import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_corr, ts_delta, ts_mean, divide

def factor_5966(data, **kwargs):
    """
    因子名称: VolumeWeightedPriceReversalSignal_71312
    数学表达式: ts_rank(ts_corr(volume, close, 20), 120) * ts_delta(ts_mean(divide(amount, volume), 5), 10)
    中文描述: 该因子旨在捕捉成交量加权平均价（VWAP）的短期变化与成交量和收盘价长期相关性趋势的结合。首先，计算过去20天成交量与收盘价的相关性，并对这个相关性在过去120天内进行时间序列排名，反映价量关系的长期趋势。然后，计算过去5天VWAP（交易额/交易量）的平均值，并计算这个平均值在过去10天内的差分，捕捉短期VWAP的变化。将这两个分量相乘，生成一个综合信号。高值可能预示着长期价量关系支持的趋势在短期VWAP变化中得到确认，潜在的买入机会；低值可能预示着反转或卖出机会。相较于参考因子，创新点在于引入了VWAP这一更贴近实际交易成本的指标，并结合了长期价量相关性排名和短期VWAP变化差分，试图捕捉更复杂的市场动态。同时，根据改进建议，我们尝试了不同的时间窗口参数，并使用了ts_corr和ts_mean等操作符来提升因子的表达能力。
    因子应用场景：
    1. 趋势识别：高值可能预示着长期价量关系支持的趋势在短期VWAP变化中得到确认，潜在的买入机会。
    2. 反转识别：低值可能预示着反转或卖出机会。
    """
    # 1. 计算 ts_corr(volume, close, 20)
    data_ts_corr = ts_corr(data['vol'], data['close'], d = 20)
    # 2. 计算 ts_rank(ts_corr(volume, close, 20), 120)
    data_ts_rank = ts_rank(data_ts_corr, d = 120)
    # 3. 计算 divide(amount, volume)
    data_divide = divide(data['amount'], data['vol'])
    # 4. 计算 ts_mean(divide(amount, volume), 5)
    data_ts_mean = ts_mean(data_divide, d = 5)
    # 5. 计算 ts_delta(ts_mean(divide(amount, volume), 5), 10)
    data_ts_delta = ts_delta(data_ts_mean, d = 10)
    # 6. 计算 ts_rank(ts_corr(volume, close, 20), 120) * ts_delta(ts_mean(divide(amount, volume), 5), 10)
    factor = data_ts_rank * data_ts_delta

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()