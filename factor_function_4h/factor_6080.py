import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import log, divide, ts_rank, add, ts_std_dev, subtract, scale
import pandas as pd

def factor_6080(data, **kwargs):
    """
    因子名称: VolumeRank_PriceVolatility_Ratio_Scaled_Improved_52870
    数学表达式: scale(divide(ts_rank(log(add(vol, 1)), 10), ts_std_dev(divide(subtract(high, low), close), 10)))
    中文描述: 该因子是基于对历史因子评估报告的分析和改进建议生成的。原始因子预测能力弱且不稳定。改进后的因子旨在通过更精细的处理和更短的窗口期来捕捉成交量活跃度与标准化日内价格波动率之间的关系。因子表达式为：scale(divide(ts_rank(log(add(vol, 1)), 10), ts_std_dev(divide(subtract(high, low), close), 10)))。其中，ts_rank(log(add(vol, 1)), 10)计算过去10天成交量取对数加1后的时间序列排名，用于衡量短期交易活跃度。对成交量取对数并加1（避免log(0)）可以平滑数据，减少异常值的影响，并捕捉成交量变化率的趋势，窗口期缩短至10天以捕捉更近期的市场情绪。ts_std_dev(divide(subtract(high, low), close), 10)计算过去10天日内价格波动率（(high-low)/close）的标准差，用于衡量日内价格波动的稳定性，窗口期同样缩短至10天。将平滑后的成交量排名除以价格波动率的标准差，旨在识别在相对活跃的交易环境下，价格波动是否稳定。最后使用scale操作符对结果进行缩放。创新点在于对成交量进行了对数变换以平滑数据，并根据历史评估结果将两个时间窗口都调整为更短的10天，尝试在更短的时间尺度上发现更有效的量价关系模式，并结合了对数变换和更短的窗口期，以提高因子的预测能力和稳定性。
    因子应用场景：
    1. 量价关系分析：该因子用于识别成交量活跃度与价格波动率之间的关系，可以辅助判断市场情绪和趋势。
    2. 短期交易活跃度：通过成交量的对数处理和排名，可以更敏感地捕捉短期交易活跃度的变化。
    3. 风险评估：价格波动率的标准差可以用于评估市场风险，结合成交量信息可以更全面地评估交易风险。
    """
    # 1. 计算 add(vol, 1)
    data_add = add(data['vol'], 1)
    # 2. 计算 log(add(vol, 1))
    data_log = log(data_add)
    # 3. 计算 ts_rank(log(add(vol, 1)), 10)
    data_ts_rank = ts_rank(data_log, d=10)
    # 4. 计算 subtract(high, low)
    data_subtract = subtract(data['high'], data['low'])
    # 5. 计算 divide(subtract(high, low), close)
    data_divide = divide(data_subtract, data['close'])
    # 6. 计算 ts_std_dev(divide(subtract(high, low), close), 10)
    data_ts_std_dev = ts_std_dev(data_divide, d=10)
    # 7. 计算 divide(ts_rank(log(add(vol, 1)), 10), ts_std_dev(divide(subtract(high, low), close), 10))
    data_divide_final = divide(data_ts_rank, data_ts_std_dev)
    # 8. 计算 scale(divide(ts_rank(log(add(vol, 1)), 10), ts_std_dev(divide(subtract(high, low), close), 10)))
    factor = scale(data_divide_final)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()