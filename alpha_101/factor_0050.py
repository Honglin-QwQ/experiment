import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_delay, subtract, divide, multiply

def factor_0050(data, **kwargs):
    """
    数学表达式: (((((ts_delay(close, 20) - ts_delay(close, 10)) / 10) - ((ts_delay(close, 10) - close) / 10)) < (-1 * 0.05)) ? 1 : ((-1 * 1) * (close - ts_delay(close, 1))))
    中文描述: 因子描述：该因子首先计算过去20天到过去10天收盘价的变化率，再计算过去10天到今天的收盘价变化率，然后求这两个变化率之差。如果这个差值小于-0.05，则因子值为1，否则因子值为负的（今天收盘价减去昨天收盘价的差值）。这个因子试图捕捉价格变化趋势的加速或减速。
    因子应用场景：
    1. 短期反转策略：当因子值为1时，表明价格下跌速度加快，可能预示着超卖，可以考虑买入；当因子值为负且绝对值较大时，表明价格上涨，可能预示着超买，可以考虑卖出。
    2. 趋势跟踪策略：结合其他趋势指标，当因子值为1时，确认下跌趋势，可以做空；当因子值为负时，确认上涨趋势，可以做多。
    3. 波动率预测：因子值频繁在1和负值之间切换可能预示着市场波动性增加。
    """
    # ts_delay(close, 20)
    ts_delay_close_20 = ts_delay(data['close'], 20)
    # ts_delay(close, 10)
    ts_delay_close_10 = ts_delay(data['close'], 10)
    # (ts_delay(close, 20) - ts_delay(close, 10))
    sub_1 = subtract(ts_delay_close_20, ts_delay_close_10)
    # ((ts_delay(close, 20) - ts_delay(close, 10)) / 10)
    div_1 = divide(sub_1, 10)
    # (ts_delay(close, 10) - close)
    sub_2 = subtract(ts_delay_close_10, data['close'])
    # ((ts_delay(close, 10) - close) / 10)
    div_2 = divide(sub_2, 10)
    # (((ts_delay(close, 20) - ts_delay(close, 10)) / 10) - ((ts_delay(close, 10) - close) / 10))
    sub_3 = subtract(div_1, div_2)
    # (-1 * 0.05)
    mult_1 = multiply(-1, 0.05)

    # ts_delay(close, 1)
    ts_delay_close_1 = ts_delay(data['close'], 1)
    # (close - ts_delay(close, 1))
    sub_4 = subtract(data['close'], ts_delay_close_1)
    # ((-1 * 1) * (close - ts_delay(close, 1)))
    mult_2 = multiply(-1, 1, sub_4)



    factor = (sub_3 < mult_1).astype(int).where(lambda x: x != 0, mult_2)


    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()