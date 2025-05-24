import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, ts_std_dev, divide

def factor_5864(data, **kwargs):
    """
    因子名称: Volume_Volatility_Skewness_Ratio_50784
    数学表达式: divide(ts_skewness(volume, 20), ts_std_dev(close, 10))
    中文描述: 该因子衡量了近期交易量分布的偏度与短期收盘价波动的相对强度。分子计算过去20天内交易量的偏度，反映了交易量分布的对称性，正偏度表示极端高交易量出现的频率较高，负偏度表示极端低交易量出现的频率较高。分母计算过去10天内收盘价的标准差，反映了价格的波动程度。通过将交易量偏度除以价格波动，因子试图捕捉在价格波动相对稳定时，交易量是否呈现出明显的偏态分布。如果比值较高，可能意味着在价格波动不大的情况下，交易量出现了异常的单边放量或缩量，这可能预示着市场情绪的潜在变化。如果比值较低，则表明交易量分布相对对称或者价格波动较大。相较于参考因子，该因子引入了统计学中的偏度概念，从交易量分布的形态而非简单的波动幅度来分析市场行为，提供了一个更细致的视角来捕捉潜在的市场异动。同时，结合了价格的短期波动性作为分母进行标准化，使得因子更具可比性。参考历史输出和改进建议，该因子尝试通过引入偏度这一新的统计量，并结合价格波动进行比值计算，希望能捕捉到更有效的市场信号，并且通过调整窗口期参数（volume 20天，close 10天）来探索不同的时间尺度效应。同时，使用了'divide'操作符，并且在概念上与历史输出的'Volume_Price_Volatility_Ratio'因子有所关联，但通过偏度的引入实现了创新。
    因子应用场景：
    1. 市场情绪识别：通过偏度衡量交易量分布，判断市场是趋于一致看涨或看跌，还是存在分歧。
    2. 波动率标准化：将交易量偏度与价格波动率结合，可以更好地识别在低波动率时期出现的异常交易量行为。
    3. 潜在趋势预警：因子值异常升高可能预示着市场潜在趋势的变化，例如价格波动不大但交易量偏度极高，可能意味着市场正在积蓄力量。
    """
    # 1. 计算 ts_skewness(volume, 20)
    volume_skewness = ts_skewness(data['vol'], d=20)
    # 2. 计算 ts_std_dev(close, 10)
    close_std_dev = ts_std_dev(data['close'], d=10)
    # 3. 计算 divide(ts_skewness(volume, 20), ts_std_dev(close, 10))
    factor = divide(volume_skewness, close_std_dev)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()