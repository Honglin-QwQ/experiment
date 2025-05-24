import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_delta, ts_std_dev, ts_returns

def factor_5913(data, **kwargs):
    """
    因子名称: Volatility_Weighted_Price_Change_Ratio_48192
    数学表达式: divide(ts_delta(close, 1), ts_std_dev(ts_returns(close, 1), 20))
    中文描述: 该因子计算了每日收盘价的变化与过去20天收盘价日收益率标准差的比值。它衡量了当前价格变动相对于近期价格波动性的强度。创新点在于将日收益率的标准差作为波动性度量，并用其对日价格变化进行标准化。这可以用于识别在低波动环境下出现显著价格变动的股票，或者在高波动环境下价格变动相对较小的股票，可能预示着趋势的形成或反转。适用于捕捉价格变化与波动性之间的动态关系，可用于趋势跟踪或反转策略。
    因子应用场景：
    1. 识别在低波动环境下出现显著价格变动的股票。
    2. 识别在高波动环境下价格变动相对较小的股票，可能预示着趋势的形成或反转。
    3. 捕捉价格变化与波动性之间的动态关系，可用于趋势跟踪或反转策略。
    """
    # 1. 计算 ts_delta(close, 1)
    data_ts_delta_close = ts_delta(data['close'], 1)
    # 2. 计算 ts_returns(close, 1)
    data_ts_returns_close = ts_returns(data['close'], 1)
    # 3. 计算 ts_std_dev(ts_returns(close, 1), 20)
    data_ts_std_dev = ts_std_dev(data_ts_returns_close, 20)
    # 4. 计算 divide(ts_delta(close, 1), ts_std_dev(ts_returns(close, 1), 20))
    factor = divide(data_ts_delta_close, data_ts_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()