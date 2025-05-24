import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, multiply, ts_std_dev, ts_mean

def factor_6037(data, **kwargs):
    """
    数学表达式: ts_skewness(multiply(close, vol), 20) * ts_std_dev(close, 60) / ts_mean(vol, 10)
    中文描述: 该因子结合了价格、成交量、波动性和偏度信息。首先计算收盘价与成交量乘积在过去20天的偏度，捕捉价量关系的非对称性。然后乘以收盘价在过去60天的标准差，衡量长期价格波动性。最后除以成交量在过去10天的平均值，对成交量进行标准化。该因子旨在识别那些在近期价量关系呈现特定偏度、同时具有一定长期价格波动性且近期成交量适中的股票。创新点在于结合了价量乘积的偏度、长期价格波动性和短期成交量均值，形成一个综合性的市场情绪和流动性指标。
    因子应用场景：
    1. 市场情绪分析：识别市场情绪偏离正常状态的股票。
    2. 波动性分析：结合价格波动性和成交量变化，辅助判断市场风险。
    3. 流动性评估：通过成交量均值标准化，评估股票的流动性状况。
    """
    # 1. 计算 multiply(close, vol)
    close_vol = multiply(data['close'], data['vol'])
    # 2. 计算 ts_skewness(multiply(close, vol), 20)
    skewness = ts_skewness(close_vol, d=20)
    # 3. 计算 ts_std_dev(close, 60)
    std_dev = ts_std_dev(data['close'], d=60)
    # 4. 计算 ts_mean(vol, 10)
    mean_vol = ts_mean(data['vol'], d=10)
    # 5. 计算 ts_skewness(multiply(close, vol), 20) * ts_std_dev(close, 60) / ts_mean(vol, 10)
    factor = skewness * std_dev / mean_vol

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()