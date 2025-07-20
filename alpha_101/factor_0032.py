import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, subtract, divide, multiply

def factor_0032(data, **kwargs):
    """
    数学表达式: rank((-1 * ((1 - (open / close))^1)))
    中文描述: 描述：首先计算每日开盘价与收盘价的比率，然后用1减去这个比率，再取结果的1次方（实际上没有改变数值），接着将这个结果乘以-1，最后计算这个数值在所有股票中的排序百分比。这个因子衡量的是当日开盘价和收盘价之间的相对关系，数值越小代表股票表现越好（收盘价相对于开盘价越高），排序百分比则反映了该股票在所有股票中表现的相对强弱。
    应用场景：
    1. 选股策略：选取rank值较低的股票，即当日收盘价相对于开盘价涨幅较大的股票，预期这些股票可能具有较强的上涨动能。
    2. 动量策略：结合其他动量因子，例如过去一段时间的收益率，构建综合动量指标，选取综合动量指标排名靠前的股票。
    3. 短线交易：在日内交易中，可以观察该因子值的变化，寻找因子值快速下降的股票，这些股票可能存在短线交易机会。
    """
    # 1. 计算 open / close
    open_close_ratio = divide(data['open'], data['close'])
    # 2. 计算 1 - (open / close)
    one_minus_ratio = subtract(1, open_close_ratio)
    # 3. 计算 (1 - (open / close))^1
    powered_ratio = one_minus_ratio # 任何数的1次方等于它本身
    # 4. 计算 -1 * ((1 - (open / close))^1)
    negated_ratio = multiply(-1, powered_ratio)
    # 5. 计算 rank((-1 * ((1 - (open / close))^1)))
    factor = rank(negated_ratio, 2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()