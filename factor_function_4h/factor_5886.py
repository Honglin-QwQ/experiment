import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_mean, multiply, densify, ts_std_dev

def factor_5886(data, **kwargs):
    """
    因子名称: VolumeMomentumDensityRatio_33147
    数学表达式: divide(ts_mean(vol, 5), multiply(densify(vol), ts_std_dev(vol, 10)))
    中文描述: 该因子计算短期平均成交量与成交量密集化和长期成交量标准差乘积的比值。它结合了成交量的短期动量（通过短期均值衡量）和长期波动性（通过长期标准差衡量），并引入了成交量密集化作为一种对成交量分布的调整。因子值较高可能表明当前成交量相对较高且波动性适中，并且经过密集化处理的成交量分布相对集中，这可能预示着市场活跃度和趋势的持续性。这是一种创新性的结合方式，将时间序列统计量与密集化操作符相结合，以捕捉更复杂的成交量特征。
    因子应用场景：
    1. 动量确认：因子值高可能确认了成交量的短期上升动量，暗示当前趋势的持续。
    2. 波动性评估：结合成交量标准差，可以评估当前成交量水平相对于其历史波动性的情况。
    3. 密集化调整：通过成交量密集化，可以调整成交量分布，从而更准确地反映市场活跃度。
    """
    # 1. 计算 ts_mean(vol, 5)
    data_ts_mean_vol = ts_mean(data['vol'], 5)
    # 2. 计算 densify(vol)
    data_densify_vol = densify(data['vol'])
    # 3. 计算 ts_std_dev(vol, 10)
    data_ts_std_dev_vol = ts_std_dev(data['vol'], 10)
    # 4. 计算 multiply(densify(vol), ts_std_dev(vol, 10))
    data_multiply = multiply(data_densify_vol, data_ts_std_dev_vol)
    # 5. 计算 divide(ts_mean(vol, 5), multiply(densify(vol), ts_std_dev(vol, 10)))
    factor = divide(data_ts_mean_vol, data_multiply)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()