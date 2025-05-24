import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_exp_window, ts_co_skewness, ts_std_dev

def factor_6010(data, **kwargs):
    """
    因子名称: Volatility_Volume_Skew_Decay_61518
    数学表达式: ts_decay_exp_window(ts_co_skewness(ts_std_dev(close, 10), vol, 20), 0.7)
    中文描述: 该因子旨在捕捉短期收盘价波动率与成交量之间协偏度的指数衰减趋势。首先，计算过去10天收盘价的标准差，衡量短期价格波动。然后，计算这个短期波动率与当日成交量在过去20天内的滚动协偏度。协偏度衡量两个变量共同偏离其均值的程度，可以捕捉波动率和成交量异常变动的同步性。最后，对这个协偏度序列应用指数衰减加权平均，给予近期数据更高的权重。因子创新性在于结合了短期波动率、成交量以及协偏度，并引入指数衰减，试图识别在不同市场阶段下，波动率和成交量异常变动的同步性及其持续性。较高的因子值可能表明短期波动率和成交量存在持续的、同方向的异常偏离，而较低的值可能指向反方向或不显著的异常偏离。
    因子应用场景：
    1. 市场情绪分析：用于识别市场波动率和成交量之间的联动关系，辅助判断市场情绪。
    2. 风险预警：当因子值异常升高时，可能预示着市场风险的增加。
    3. 交易策略：可以作为量化交易策略中的一个特征，辅助判断买卖时机。
    """
    # 1. 计算 ts_std_dev(close, 10)
    data_ts_std_dev = ts_std_dev(data['close'], d = 10)
    # 2. 计算 ts_co_skewness(ts_std_dev(close, 10), vol, 20)
    data_ts_co_skewness = ts_co_skewness(data_ts_std_dev, data['vol'], d = 20)
    # 3. 计算 ts_decay_exp_window(ts_co_skewness(ts_std_dev(close, 10), vol, 20), 0.7)
    factor = ts_decay_exp_window(data_ts_co_skewness, d = 6, factor = 0.7)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()