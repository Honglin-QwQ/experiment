import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import scale
from operators import divide
from operators import ts_rank
from operators import adv
from operators import ts_min_diff

def factor_6034(data, **kwargs):
    """
    数学表达式: scale(divide(ts_rank(adv(vol, 25), 28), ts_min_diff(open, 55)))
    中文描述: 该因子是基于历史输出和改进建议生成的新因子。它计算了过去25天平均成交量在过去28天内的排名，并将其除以当前开盘价与过去55天最低开盘价的差值。最后对结果进行标准化处理。相较于历史输出，该因子调整了参数窗口，并保留了核心的排名与差值比率结构，但去除了倒数操作，以避免放大极端值的影响。较高的因子值可能表明成交量排名相对较高，同时开盘价相对于近期最低点上涨有限，或者成交量排名较低但开盘价相对于近期最低点有显著上涨。创新点在于参数的调整和倒数操作的移除，旨在提高因子的稳定性和预测能力。
    因子应用场景：
    1. 成交量分析：用于识别成交量变化对股票价格的影响。
    2. 价格趋势分析：结合成交量排名和开盘价差值，辅助判断价格趋势。
    3. 风险管理：通过标准化处理，控制因子暴露，降低投资组合风险。
    """
    # 1. 计算 adv(vol, 25)
    data_adv = adv(data['vol'], d=25)
    # 2. 计算 ts_rank(adv(vol, 25), 28)
    data_ts_rank = ts_rank(data_adv, d=28)
    # 3. 计算 ts_min_diff(open, 55)
    data_ts_min_diff = ts_min_diff(data['open'], d=55)
    # 4. 计算 divide(ts_rank(adv(vol, 25), 28), ts_min_diff(open, 55))
    data_divide = divide(data_ts_rank, data_ts_min_diff)
    # 5. 计算 scale(divide(ts_rank(adv(vol, 25), 28), ts_min_diff(open, 55)))
    factor = scale(data_divide)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()