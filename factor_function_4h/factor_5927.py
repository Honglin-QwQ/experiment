import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import sqrt, ts_std_dev, adv, sigmoid, divide, multiply

def factor_5927(data, **kwargs):
    """
    数学表达式: divide(sqrt(ts_std_dev(vol, 20)), multiply(adv(vol, 60), sigmoid(open)))
    中文描述: 该因子旨在捕捉交易量的波动性相对于长期平均交易量与开盘价经过Sigmoid函数缩放后的乘积的比率。首先计算过去20天交易量的标准差，衡量短期交易量波动。然后计算过去60天的平均交易量，作为长期交易量水平的参考。同时，将开盘价通过Sigmoid函数进行非线性缩放，使其值介于0到1之间，反映开盘价的市场情绪强度。最后，用短期交易量标准差除以长期平均交易量与开盘价Sigmoid缩放值的乘积。创新点在于结合了短期交易量波动、长期交易量水平以及开盘价的市场情绪，通过Sigmoid函数引入非线性关系，构建了一个多维度的交易量和价格综合因子。高因子值可能表示短期交易量波动剧烈，相对于长期平均水平和开盘情绪显得异常活跃，可能预示着潜在的价格变动或市场关注度变化。
    因子应用场景：
    1. 交易量异常检测：识别交易量波动异常的股票，可能预示着市场关注度或潜在风险。
    2. 市场情绪量化：结合开盘价的Sigmoid缩放值，量化市场情绪对交易量的影响。
    3. 多因子策略：与其他因子结合，构建更稳健的量化交易策略。
    """
    # 1. 计算 ts_std_dev(vol, 20)
    data_ts_std_dev_vol = ts_std_dev(data['vol'], d=20)
    # 2. 计算 sqrt(ts_std_dev(vol, 20))
    data_sqrt_ts_std_dev_vol = sqrt(data_ts_std_dev_vol)
    # 3. 计算 adv(vol, 60)
    data_adv_vol = adv(data['vol'], d=60)
    # 4. 计算 sigmoid(open)
    data_sigmoid_open = sigmoid(data['open'])
    # 5. 计算 multiply(adv(vol, 60), sigmoid(open))
    data_multiply_adv_vol_sigmoid_open = multiply(data_adv_vol, data_sigmoid_open)
    # 6. 计算 divide(sqrt(ts_std_dev(vol, 20)), multiply(adv(vol, 60), sigmoid(open)))
    factor = divide(data_sqrt_ts_std_dev_vol, data_multiply_adv_vol_sigmoid_open)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()