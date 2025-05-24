import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import inverse, rank, divide, ts_delta, ts_std_dev

def factor_6042(data, **kwargs):
    """
    因子名称: InverseRankedVolumeVolatilityDeltaRatio_42995
    数学表达式: inverse(rank(divide(ts_delta(ts_std_dev(volume, 10), 5), ts_delta(ts_std_dev(volume, 5), 10))))
    中文描述: 该因子基于对历史因子表现的分析和改进建议，旨在捕捉成交量波动性变化率的相对强弱。它首先计算过去10天成交量标准差在过去5天的变化率，以及过去5天成交量标准差在过去10天的变化率。然后，计算这两个变化率的比值，并对该比值进行排名。最后，取排名的倒数。通过取倒数，将原本可能与未来收益率负相关的排名转化为正相关。该因子通过比较不同时间窗口下成交量波动性变化的速度，试图识别市场活跃度的加速或减速，并在排名后取倒数，可能用于捕捉潜在的上涨机会。相较于原始因子，创新点在于引入了两个变化率的比值，并对排名结果取倒数，以期提升预测能力和反转负相关性。
    因子应用场景：
    1. 市场活跃度识别：用于识别市场活跃度的加速或减速。
    2. 潜在上涨机会捕捉：通过比较不同时间窗口下成交量波动性变化的速度，并在排名后取倒数，可能用于捕捉潜在的上涨机会。
    """
    # 1. 计算 ts_std_dev(volume, 10)
    data_ts_std_dev_10 = ts_std_dev(data['vol'], 10)
    # 2. 计算 ts_delta(ts_std_dev(volume, 10), 5)
    data_ts_delta_1 = ts_delta(data_ts_std_dev_10, 5)
    # 3. 计算 ts_std_dev(volume, 5)
    data_ts_std_dev_5 = ts_std_dev(data['vol'], 5)
    # 4. 计算 ts_delta(ts_std_dev(volume, 5), 10)
    data_ts_delta_2 = ts_delta(data_ts_std_dev_5, 10)
    # 5. 计算 divide(ts_delta(ts_std_dev(volume, 10), 5), ts_delta(ts_std_dev(volume, 5), 10))
    data_divide = divide(data_ts_delta_1, data_ts_delta_2)
    # 6. 计算 rank(divide(ts_delta(ts_std_dev(volume, 10), 5), ts_delta(ts_std_dev(volume, 5), 10)))
    data_rank = rank(data_divide, 2)
    # 7. 计算 inverse(rank(divide(ts_delta(ts_std_dev(volume, 10), 5), ts_delta(ts_std_dev(volume, 5), 10))))
    factor = inverse(data_rank)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()