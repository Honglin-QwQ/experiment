import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import *
import pandas as pd

def factor_6017(data, **kwargs):
    """
    因子名称: VolatilityFractionalVolumeRatio_Adjusted_82473
    数学表达式: divide(ts_std_dev(fraction(vol), 15), ts_std_dev(ts_delay(vol, 20), 25)) * ts_rank(change(close, 10), 20)
    中文描述: 该因子计算当前成交量小数部分的短期波动率（15天窗口）与20天前成交量的长期波动率（25天窗口）之比，并乘以过去10天收盘价变化率在过去20天内的排名。它结合了对成交量微观结构（小数部分）的关注、对历史整体成交量波动性的考量以及近期价格变化率的动量信息。创新的地方在于调整了时间窗口以探索更优参数，并引入了收盘价变化率的排名作为乘数，旨在捕捉微观交易行为波动性与历史整体成交量波动性之间的相对强弱，并结合价格动量信息，可能用于识别由微小交易行为驱动的市场情绪变化或趋势的潜在信号。相较于历史输出，该因子调整了波动率计算的时间窗口和延迟期，并加入了价格变化率的排名，试图增强因子的预测能力和稳定性，利用了改进建议中提到的调整时间窗口和引入其他变量（价格信息）以及使用排序类操作符的思路。
    因子应用场景：
    1. 波动率比率分析：用于识别成交量微观结构波动性与历史成交量波动性之间的关系，判断市场活跃度和潜在风险。
    2. 价格动量结合：结合价格变化率排名，可能用于发现由微观交易行为驱动的市场情绪变化或趋势信号。
    3. 参数优化：通过调整时间窗口，探索更优的参数组合，提高因子的预测能力。
    """
    # 1. fraction(vol)
    data['fraction_vol'] = fraction(data['vol'])
    # 2. ts_std_dev(fraction(vol), 15)
    data['ts_std_dev_fraction_vol'] = ts_std_dev(data['fraction_vol'], 15)
    # 3. ts_delay(vol, 20)
    data['ts_delay_vol'] = ts_delay(data['vol'], 20)
    # 4. ts_std_dev(ts_delay(vol, 20), 25)
    data['ts_std_dev_ts_delay_vol'] = ts_std_dev(data['ts_delay_vol'], 25)
    # 5. divide(ts_std_dev(fraction(vol), 15), ts_std_dev(ts_delay(vol, 20), 25))
    data['divide_std_dev'] = divide(data['ts_std_dev_fraction_vol'], data['ts_std_dev_ts_delay_vol'])
    # 6. change(close, 10)
    data['change_close'] = data['close'].diff(10)
    # 7. ts_rank(change(close, 10), 20)
    data['ts_rank_change_close'] = ts_rank(data['change_close'], 20)
    # 8. divide(ts_std_dev(fraction(vol), 15), ts_std_dev(ts_delay(vol, 20), 25)) * ts_rank(change(close, 10), 20)
    factor = data['divide_std_dev'] * data['ts_rank_change_close']

    data = data.drop(columns=['fraction_vol', 'ts_std_dev_fraction_vol', 'ts_delay_vol', 'ts_std_dev_ts_delay_vol', 'divide_std_dev', 'change_close', 'ts_rank_change_close'])

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()