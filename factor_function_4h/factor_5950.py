import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_corr, divide, ts_delta, rank, ts_std_dev

def factor_5950(data, **kwargs):
    """
    因子名称: Volume_Weighted_Price_Trend_Strength_13766
    数学表达式: ts_rank(ts_corr(divide(close, vwap), ts_delta(vol, 1), 10), 5) - rank(ts_std_dev(amount, 5))
    中文描述: 该因子旨在捕捉收盘价与VWAP比值（衡量价格相对于成交量加权均价的偏离）与成交量日变化之间的短期相关性强度，并结合交易额的短期波动性。
            首先，计算过去10天收盘价/VWAP与成交量日变化（ts_delta(vol, 1)）的时间序列相关性，并对该相关性在过去5天内进行排名（ts_rank）。
            这部分创新性地使用了收盘价与VWAP的比值来代替简单的价格变化，更好地反映了价格在当日交易中的相对位置与成交量的配合。
            然后，该因子减去过去5天交易额（amount）标准差的横截面排名（rank）。交易额标准差反映了资金流动的波动性，其排名衡量了这种波动性在所有股票中的相对位置。
            通过将价格相对强度与成交量变化的短期相关性时间序列排名，与交易额短期波动性的横截面排名相结合，该因子试图识别那些在短期内表现出特定价格-成交量配合模式，并且伴随相对较高或较低资金波动性的股票。
            相较于参考因子，创新点在于使用close/vwap比值作为价格动量代理，并引入了交易额的波动性而非单纯变化量，提供了更丰富的市场信息。
            改进方向参考了对原因子复杂性、相关性不稳定以及成分相关性弱的诊断，尝试简化相关性计算的输入，并引入波动性指标以期提高稳定性。
    因子应用场景：
    1. 价格与成交量配合分析：用于识别价格变动与成交量变化之间存在特定模式的股票。
    2. 资金波动性考量：结合交易额波动性，筛选出在资金流动性变化下表现出特定价格行为的股票。
    """
    # 1. 计算 divide(close, vwap)
    data_divide = divide(data['close'], data['vwap'])
    # 2. 计算 ts_delta(vol, 1)
    data_ts_delta = ts_delta(data['vol'], 1)
    # 3. 计算 ts_corr(divide(close, vwap), ts_delta(vol, 1), 10)
    data_ts_corr = ts_corr(data_divide, data_ts_delta, 10)
    # 4. 计算 ts_rank(ts_corr(divide(close, vwap), ts_delta(vol, 1), 10), 5)
    data_ts_rank = ts_rank(data_ts_corr, 5)
    # 5. 计算 ts_std_dev(amount, 5)
    data_ts_std_dev = ts_std_dev(data['amount'], 5)
    # 6. 计算 rank(ts_std_dev(amount, 5))
    data_rank = rank(data_ts_std_dev, 2)
    # 7. 计算 ts_rank(ts_corr(divide(close, vwap), ts_delta(vol, 1), 10), 5) - rank(ts_std_dev(amount, 5))
    factor = data_ts_rank - data_rank

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()