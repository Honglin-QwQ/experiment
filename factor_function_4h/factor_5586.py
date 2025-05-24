import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_std_dev, ts_rank, ts_delta, multiply

def factor_5586(data, **kwargs):
    """
    因子名称: factor_dynamic_volatility_rank_30019
    数学表达式: rank(ts_std_dev(high-low, 10))*ts_rank(ts_delta(amount,5),15)
    中文描述: 该因子结合了波动率和成交额变化的信息。首先，计算过去10天最高价和最低价之差的标准差，反映了价格的短期波动性。然后，计算过去5天成交额的变化，并通过ts_rank计算其在过去15天的排名。最后，将波动率的排名与成交额变化排名的乘积作为最终因子值。该因子旨在捕捉价格波动性与成交额变化之间的关系，可能用于识别价格趋势的潜在反转点或加速点。
    因子应用场景：
    1. 波动性分析：用于衡量股票价格的波动程度，并结合成交额的变化来判断市场活跃度。
    2. 趋势反转识别：当波动率排名较高且成交额变化排名也较高时，可能预示着趋势的反转。
    """

    # 1. 计算 high-low
    high_low_diff = data['high'] - data['low']

    # 2. 计算 ts_std_dev(high-low, 10)
    std_dev = ts_std_dev(high_low_diff, d=10)

    # 3. 计算 rank(ts_std_dev(high-low, 10))
    volatility_rank = rank(std_dev, rate=2)

    # 4. 计算 ts_delta(amount, 5)
    amount_delta = ts_delta(data['amount'], d=5)

    # 5. 计算 ts_rank(ts_delta(amount,5), 15)
    amount_rank = ts_rank(amount_delta, d=15)

    # 6. 计算 rank(ts_std_dev(high-low, 10))*ts_rank(ts_delta(amount,5),15)
    factor = multiply(volatility_rank, amount_rank)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()