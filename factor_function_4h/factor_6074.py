import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import reverse
from operators import log
from operators import divide
import pandas as pd

def factor_6074(data, **kwargs):
    """
    因子名称: ReverseLogVolPriceRatio_65422
    数学表达式: reverse(log(divide(vol, close)))
    中文描述: 该因子计算成交量与收盘价之比的自然对数，并取反。成交量与收盘价之比可以近似反映单位价格下的交易活跃度。对其取自然对数可以平滑极端值的影响。最后取反，使得因子值越高，单位价格下的交易活跃度越低。这与原始因子对成交量进行Sigmoid变换并相乘的逻辑有所不同，通过简单的除法和对数变换，尝试捕捉价格和成交量之间的反向关系。相较于参考因子，该因子结构更简洁，并直接利用了成交量和价格信息，通过对数变换和取反，尝试找到与未来收益率的负相关关系。
    因子应用场景：
    1. 衡量市场活跃度：可以用于衡量股票市场的活跃程度，因子值越高，表明市场交易活跃度越低。
    2. 风险预警：当因子值异常升高时，可能预示着市场流动性风险的增加。
    """
    # 1. 计算 divide(vol, close)
    data_divide = divide(data['vol'], data['close'])
    # 2. 计算 log(divide(vol, close))
    data_log = log(data_divide)
    # 3. 计算 reverse(log(divide(vol, close)))
    factor = reverse(data_log)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()