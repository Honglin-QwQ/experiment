import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_std_dev, multiply, ts_scale

def factor_5914(data, **kwargs):
    """
    因子名称: ScaledVolumeWeightedPriceVolatilityRatio_34043
    数学表达式: divide(ts_std_dev(multiply(vwap, ts_scale(vol, 100, constant = 0)), 10), ts_std_dev(vwap, 10))
    中文描述: 该因子计算成交量加权价格（VWAP）乘以经过时间序列缩放的成交量的标准差，与VWAP自身标准差的比值。在参考因子基础上，创新性地引入了ts_scale对成交量进行缩放，将其归一化到[0,1]区间，以减少极端成交量对因子计算的直接影响，使因子更能反映相对成交量下的价格波动性。高值可能表明相对活跃的成交量在价格波动中扮演了更重要的角色，可能预示着趋势的加强或反转。因子改进了对成交量的处理方式，使其更具鲁棒性。
    因子应用场景：
    1. 波动性分析：用于衡量成交量缩放后对价格波动的影响。
    2. 趋势判断：高值可能预示趋势的加强或反转。
    """
    # 1. 计算 ts_scale(vol, 100, constant = 0)
    data_ts_scale = ts_scale(data['vol'], d = 100, constant = 0)
    # 2. 计算 multiply(vwap, ts_scale(vol, 100, constant = 0))
    data_multiply = multiply(data['vwap'], data_ts_scale)
    # 3. 计算 ts_std_dev(multiply(vwap, ts_scale(vol, 100, constant = 0)), 10)
    data_ts_std_dev_1 = ts_std_dev(data_multiply, d = 10)
    # 4. 计算 ts_std_dev(vwap, 10)
    data_ts_std_dev_2 = ts_std_dev(data['vwap'], d = 10)
    # 5. 计算 divide(ts_std_dev(multiply(vwap, ts_scale(vol, 100, constant = 0)), 10), ts_std_dev(vwap, 10))
    factor = divide(data_ts_std_dev_1, data_ts_std_dev_2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()