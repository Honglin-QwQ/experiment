import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, ts_decay_linear, multiply, ts_delta, divide

def factor_5974(data, **kwargs):
    """
    因子名称: PriceVolumeVolatilityRatio_DecayWeighted_39021
    数学表达式: divide(ts_std_dev(ts_decay_linear(multiply(close, vol), 10), 10), ts_std_dev(ts_decay_linear(multiply(ts_delta(close, 1), vol), 10), 10))
    中文描述: 该因子计算过去10天内收盘价乘以成交量的线性衰减加权标准差与过去10天内日收盘价变化乘以成交量的线性衰减加权标准差之比。相较于参考因子，创新点在于使用线性衰减加权（ts_decay_linear）来处理价格和成交量的乘积，使得近期数据对标准差的贡献更大，而非简单平均。同时，保留了成交量作为加权因子，关注成交量活跃度对价格波动的影响。分子反映了成交量加权下收盘价绝对水平波动的衰减加权标准差，分母反映了成交量加权下日价格变动波动的衰减加权标准差。高因子值可能表明近期成交量加权下的价格水平波动相对更强，或者近期成交量加权下的日价格变动相对更弱。这可能用于识别近期成交量驱动下价格波动模式的变化，捕捉短期趋势的加速或减缓信号。结合了线性衰减加权和成交量加权，并计算其波动性比率，提供了对近期市场动能和波动结构的新视角，特别关注了近期成交量活跃度的驱动作用。根据历史评估结果和改进建议，该因子将时间窗口调整为10天，并引入线性衰减加权，旨在增强因子对近期市场变化的敏感性，并尝试通过衰减加权优化参数，提高预测能力。同时，保留了成交量作为加权因子，旨在增强因子对市场情绪和交易活跃度变化的敏感性，从而提升统计显著性和稳定性。
    因子应用场景：
    1. 波动性分析：用于衡量价格和成交量共同作用下的市场波动程度。
    2. 趋势识别：高因子值可能预示着价格趋势的变化或加速。
    3. 市场情绪感知：成交量加权有助于捕捉市场情绪对价格波动的影响。
    """
    # 1. 计算 multiply(close, vol)
    close_vol = multiply(data['close'], data['vol'])
    # 2. 计算 ts_decay_linear(multiply(close, vol), 10)
    decay_close_vol = ts_decay_linear(close_vol, d = 10)
    # 3. 计算 ts_std_dev(ts_decay_linear(multiply(close, vol), 10), 10)
    std_decay_close_vol = ts_std_dev(decay_close_vol, d = 10)
    # 4. 计算 ts_delta(close, 1)
    delta_close = ts_delta(data['close'], d = 1)
    # 5. 计算 multiply(ts_delta(close, 1), vol)
    delta_close_vol = multiply(delta_close, data['vol'])
    # 6. 计算 ts_decay_linear(multiply(ts_delta(close, 1), vol), 10)
    decay_delta_close_vol = ts_decay_linear(delta_close_vol, d = 10)
    # 7. 计算 ts_std_dev(ts_decay_linear(multiply(ts_delta(close, 1), vol), 10), 10)
    std_decay_delta_close_vol = ts_std_dev(decay_delta_close_vol, d = 10)
    # 8. 计算 divide(ts_std_dev(ts_decay_linear(multiply(close, vol), 10), 10), ts_std_dev(ts_decay_linear(multiply(ts_delta(close, 1), vol), 10), 10))
    factor = divide(std_decay_close_vol, std_decay_delta_close_vol)

    # 删除中间变量
    del close_vol, decay_close_vol, std_decay_close_vol, delta_close, delta_close_vol, decay_delta_close_vol, std_decay_delta_close_vol

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()