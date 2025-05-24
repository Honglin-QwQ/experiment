import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_std_dev, sign, ts_delta, multiply

def factor_5892(data, **kwargs):
    """
    因子名称: Volatility_Volume_Trend_Rank_93254
    数学表达式: ts_rank(multiply(ts_std_dev(close, 10), sign(ts_delta(vol, 5))), 20)
    中文描述: 该因子名为“Volatility Volume Trend Rank”，旨在捕捉股票价格波动性与近期成交量变化趋势相结合的相对强度。
    它首先计算过去10天收盘价的标准差（ts_std_dev(close, 10)），衡量价格波动性；
    然后计算过去5天成交量的变化方向（sign(ts_delta(vol, 5))），如果成交量增加则为1，减少则为-1，不变则为0。
    接着，将价格波动性与成交量变化方向相乘，得到一个结合了波动性和成交量趋势的指标。
    最后，计算这个指标在过去20天内的排名（ts_rank(..., 20)）。
    该因子创新性地将波动性与成交量趋势相结合，试图识别那些在波动加剧且成交量呈现特定趋势（例如，波动加剧伴随成交量放大）时表现出相对强劲的股票。
    相较于参考因子，创新点在于引入了成交量变化趋势的方向，并将其与波动性相乘，以捕捉更复杂的价量关系，并通过时间序列排名来衡量其相对强度。
    这借鉴了历史输出的改进建议中关于考虑成交量变化方向的思路，并使用了sign和ts_delta操作符来实现。
    因子应用场景：
    1. 识别波动性加剧且成交量呈现特定趋势的股票。
    2. 辅助判断股票的相对强度。
    """
    # 1. 计算 ts_std_dev(close, 10)
    data_std = ts_std_dev(data['close'], d=10)
    # 2. 计算 ts_delta(vol, 5)
    data_delta = ts_delta(data['vol'], d=5)
    # 3. 计算 sign(ts_delta(vol, 5))
    data_sign = sign(data_delta)
    # 4. 计算 multiply(ts_std_dev(close, 10), sign(ts_delta(vol, 5)))
    data_multiply = multiply(data_std, data_sign)
    # 5. 计算 ts_rank(multiply(ts_std_dev(close, 10), sign(ts_delta(vol, 5))), 20)
    factor = ts_rank(data_multiply, d=20)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()