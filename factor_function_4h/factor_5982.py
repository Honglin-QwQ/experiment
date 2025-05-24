import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_rank, adv, arc_tan, floor

def factor_5982(data, **kwargs):
    """
    因子名称: VolRank_OpenFloor_arctan_Ratio_66099
    数学表达式: divide(ts_rank(adv(vol, 20), 23), arc_tan(floor(open)))
    中文描述: 该因子结合了成交量排名、开盘价向下取整和反正切函数。首先计算过去20天的平均成交量，并在过去23天内对其进行时间序列排名。然后，对开盘价进行向下取整并应用反正切函数。最后，用成交量排名除以反正切处理后的开盘价。这个因子旨在捕捉市场流动性与价格离散化处理后的非线性关系的相对强度。当成交量排名较高而反正切处理后的开盘价相对较低时，因子值会增大，可能指示市场对该股票的关注度高且价格波动相对平缓，或存在其他非线性关系。相较于参考因子，该因子通过引入开盘价的非线性变换并与成交量排名进行比率计算，增加了因子的复杂性和创新性，试图捕捉更深层次的市场动态。
    因子应用场景：
    1. 市场流动性分析：用于识别成交量较高且开盘价相对平缓的股票，可能表明市场关注度较高。
    2. 非线性关系捕捉：通过反正切函数处理开盘价，捕捉价格的非线性特征与成交量的关系。
    """
    # 1. 计算 adv(vol, 20)
    data_adv = adv(data['vol'], d=20)
    # 2. 计算 ts_rank(adv(vol, 20), 23)
    data_ts_rank = ts_rank(data_adv, d=23)
    # 3. 计算 floor(open)
    data_floor = floor(data['open'])
    # 4. 计算 arc_tan(floor(open))
    data_arc_tan = arc_tan(data_floor)
    # 5. 计算 divide(ts_rank(adv(vol, 20), 23), arc_tan(floor(open)))
    factor = divide(data_ts_rank, data_arc_tan)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()