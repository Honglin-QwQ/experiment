import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, divide, subtract, ts_weighted_decay, adv

def factor_5674(data, **kwargs):
    """
    数学表达式: rank(divide(subtract(close, ts_weighted_decay(close, k = 0.3)), adv(vol, d = 30)))
    中文描述: 该因子在历史因子VolumeWeightedOpenPriceDeviation的基础上进行了改进，首先，将开盘价替换为收盘价，以更好地反映市场对股票价值的最终评估。其次，调整了ts_weighted_decay的k值和adv的d值，k值设置为0.3，d值设置为30，以寻找更优的参数组合。最后，使用rank函数对因子值进行排序，以消除异常值的影响，提高因子的鲁棒性。该因子的设计思路是衡量收盘价相对于其近期趋势的偏离程度，并结合成交量进行调整，以反映市场活跃度对价格偏离的影响。创新点在于结合了价格的时间序列加权衰减和成交量信息，并使用rank函数进行排序，可以更有效地识别价格的短期异动。
    因子应用场景：
    1. 短期异动识别：该因子可以帮助识别短期内价格出现异常波动的股票，从而辅助投资者进行短线交易决策。
    2. 趋势反转预测：通过观察因子值的变化，可以辅助判断股票价格趋势是否可能发生反转。
    3. 市场活跃度分析：结合成交量信息，可以评估市场活跃度对价格偏离的影响，从而更全面地了解市场动态。
    """
    # 1. 计算 ts_weighted_decay(close, k = 0.3)
    data_ts_weighted_decay = ts_weighted_decay(data['close'], k = 0.3)
    # 2. 计算 subtract(close, ts_weighted_decay(close, k = 0.3))
    data_subtract = subtract(data['close'], data_ts_weighted_decay)
    # 3. 计算 adv(vol, d = 30)
    data_adv = adv(data['vol'], d = 30)
    # 4. 计算 divide(subtract(close, ts_weighted_decay(close, k = 0.3)), adv(vol, d = 30))
    data_divide = divide(data_subtract, data_adv)
    # 5. 计算 rank(divide(subtract(close, ts_weighted_decay(close, k = 0.3)), adv(vol, d = 30)))
    factor = rank(data_divide, 2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()