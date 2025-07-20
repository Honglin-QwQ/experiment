import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank, ts_corr, ts_delta, sign, adv, multiply, add, subtract, signed_power,indneutralize
import pandas as pd

def factor_0079(data, **kwargs):
    """
    数学表达式: ((rank(Sign(ts_delta(indneutralize(((open * 0.868128) + (high * (1 - 0.868128))), IndClass.industry), 4.04545)))^ts_rank(ts_corr(high, adv10, 5.11456), 5.53756)) * -1) 
    中文描述: 这个因子首先计算开盘价的86.8128%加上最高价的剩余百分比，然后对结果进行行业中性化处理，再计算结果序列的4.04545期差分，并取差分结果的符号，然后计算这个符号序列的排序。同时，计算最高价和10日平均成交额在过去5.11456天内的相关性，并计算这个相关性序列的5.53756期排名。最后，将符号排序的结果乘以相关性排名，取负数作为最终因子值。该因子可以捕捉短期价格动量和成交额相关性的反转效应，可以用于短线择时，识别超买超卖机会，或者作为其他复杂量化模型的输入特征。
    因子应用场景：
    1. 短线择时：捕捉短期价格动量和成交额相关性的反转效应，辅助短线交易决策。
    2. 超买超卖识别：识别市场中的超买超卖机会，辅助判断价格回调或反弹的可能性。
    3. 特征工程：作为其他复杂量化模型的输入特征，提升模型的预测能力。
    """
    # 1. 计算 (open * 0.868128)
    open_weighted = multiply(data['open'], 0.868128)
    # 2. 计算 (high * (1 - 0.868128))
    high_weighted = multiply(data['high'], (1 - 0.868128))
    # 3. 计算 ((open * 0.868128) + (high * (1 - 0.868128)))
    temp = add(open_weighted, high_weighted)

    # 4. 行业中性化


    temp_neutralized = indneutralize(temp,data['industry'])
    temp_neutralized.name = 'temp_neutralized'

    # 5. 计算 ts_delta(indneutralize(((open * 0.868128) + (high * (1 - 0.868128))), IndClass.industry), 4.04545)
    delta = ts_delta(temp_neutralized, d = 4)
    # 6. 计算 Sign(ts_delta(indneutralize(((open * 0.868128) + (high * (1 - 0.868128))), IndClass.industry), 4.04545))
    sign_delta = sign(delta)
    # 7. 计算 rank(Sign(ts_delta(indneutralize(((open * 0.868128) + (high * (1 - 0.868128))), IndClass.industry), 4.04545)))
    rank_sign_delta = rank(sign_delta)

    # 8. 计算 adv10
    adv10 = adv(data['amount'])
    # 9. 计算 ts_corr(high, adv10, 5.11456)
    corr = ts_corr(data['high'], adv10, d = 5)
    # 10. 计算 ts_rank(ts_corr(high, adv10, 5.11456), 5.53756)
    rank_corr = rank(corr)

    # 11. 计算 (rank(Sign(ts_delta(indneutralize(((open * 0.868128) + (high * (1 - 0.868128))), IndClass.industry), 4.04545)))^ts_rank(ts_corr(high, adv10, 5.11456), 5.53756))
    power = signed_power(rank_sign_delta, rank_corr)
    # 12. 计算 ((rank(Sign(ts_delta(indneutralize(((open * 0.868128) + (high * (1 - 0.868128))), IndClass.industry), 4.04545)))^ts_rank(ts_corr(high, adv10, 5.11456), 5.53756)) * -1)
    factor = multiply(power, -1)

    # 删除中间变量


    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()