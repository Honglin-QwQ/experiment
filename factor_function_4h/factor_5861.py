import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_std_dev, adv, ts_mean, divide

def factor_5861(data, **kwargs):
    """
    因子名称: LiquidityVolatilityRatio_33404
    数学表达式: divide(ts_std_dev(adv(vol, 20), 10), ts_mean(adv(vol, 20), 10))
    中文描述: 该因子计算过去10天内20天平均交易量（adv20）的标准差与过去10天内adv20均值的比值。它衡量了股票流动性（以adv20衡量）在短期内的波动性。较高的因子值表示流动性波动较大，可能预示着市场不确定性增加或交易环境变化。这结合了参考因子中对流动性的关注（adv20）和时间序列统计量（ts_std_dev, ts_mean），通过比率的形式提供了一种创新的流动性波动衡量方法。
    因子应用场景：
    1. 衡量股票流动性在短期内的波动性。
    2. 预示市场不确定性增加或交易环境变化。
    """
    # 1. 计算 adv(vol, 20)
    data_adv = adv(data['vol'], d = 20)
    # 2. 计算 ts_std_dev(adv(vol, 20), 10)
    data_ts_std_dev = ts_std_dev(data_adv, d = 10)
    # 3. 计算 ts_mean(adv(vol, 20), 10)
    data_ts_mean = ts_mean(data_adv, d = 10)
    # 4. 计算 divide(ts_std_dev(adv(vol, 20), 10), ts_mean(adv(vol, 20), 10))
    factor = divide(data_ts_std_dev, data_ts_mean)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()