import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, adv, multiply, subtract

def factor_0024(data, **kwargs):
    """
    数学表达式: rank(((((-1 * returns) * adv20) * vwap) * (high - close)))
    中文描述: 首先计算收益率的负值，然后乘以过去20天平均成交额，再乘以成交量加权平均价，最后乘以最高价减去收盘价的差值，得到一个综合数值，对这个数值在所有股票中进行排序，得到每只股票的排序百分比。这个因子衡量的是成交活跃的股票中，当日收益率低且收盘价接近当日最低价的股票的相对强度。
    应用场景包括：
    1. 识别短期内可能反弹的超卖股票：因子值较低的股票可能被过度抛售，存在反弹机会。
    2. 构造量化反转策略：买入因子值低的股票，卖出因子值高的股票，期望获得反转收益。
    3. 风险控制：避免持有因子值持续走高的股票，这些股票可能面临进一步下跌的风险。
    """
    # 1. 计算 -1 * returns
    neg_returns = multiply(-1, data['returns'])
    # 2. 计算 adv20
    adv20 = adv(data['vol'], d=20)
    # 3. 计算 (-1 * returns) * adv20
    step1 = multiply(neg_returns, adv20)
    # 4. 计算 ((-1 * returns) * adv20) * vwap
    step2 = multiply(step1, data['vwap'])
    # 5. 计算 high - close
    high_minus_close = subtract(data['high'], data['close'])
    # 6. 计算 (((-1 * returns) * adv20) * vwap) * (high - close)
    step3 = multiply(step2, high_minus_close)
    # 7. 计算 rank(((((-1 * returns) * adv20) * vwap) * (high - close)))
    factor = rank(step3, rate = 2)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()