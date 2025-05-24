import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_skewness, rank, ts_decay_linear, divide, subtract

def factor_6009(data, **kwargs):
    """
    因子名称: VolatilitySkew_VolumeDecay_RankDiff_40403
    数学表达式: subtract(ts_skewness(divide(high, low), 25), rank(ts_decay_linear(vol, 20)))
    中文描述: 该因子旨在捕捉价格波动的不对称性（偏度）与近期成交量衰减特征的结合，并通过计算两者排名差异来衡量相对强度。
    因子首先计算过去25天最高价/最低价比率的时间序列偏度，反映价格波动向上或向下的倾向。
    然后计算过去20天成交量的线性衰减值的排名。
    最后，用价格波动偏度减去成交量衰减的排名。
    高因子值可能表明价格波动更倾向于向上，且近期成交量衰减相对较弱，这可能预示着潜在的上涨动能。
    相较于参考因子，创新点在于使用了减法而不是乘法结合价格偏度和成交量衰减，并对成交量衰减进行了排名处理，以突出其相对强度，并移除了收盘价标准差的排名项，简化了因子结构，并根据评估报告的负相关性问题，调整了计算逻辑，使其可能呈现正向预测能力。
    因子应用场景：
    1. 波动率偏度与成交量衰减的相对强度分析：用于识别价格波动偏度较高但成交量衰减较弱的股票，这些股票可能具有潜在的上涨动能。
    2. 趋势反转识别：当因子值显著变化时，可能预示着市场趋势的反转。
    """
    # 1. 计算 divide(high, low)
    data_divide = divide(data['high'], data['low'])
    # 2. 计算 ts_skewness(divide(high, low), 25)
    data_ts_skewness = ts_skewness(data_divide, 25)
    # 3. 计算 ts_decay_linear(vol, 20)
    data_ts_decay_linear = ts_decay_linear(data['vol'], 20)
    # 4. 计算 rank(ts_decay_linear(vol, 20))
    data_rank = rank(data_ts_decay_linear, 2)
    # 5. 计算 subtract(ts_skewness(divide(high, low), 25), rank(ts_decay_linear(vol, 20)))
    factor = subtract(data_ts_skewness, data_rank)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()