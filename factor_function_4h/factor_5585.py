import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_delta, ts_std_dev, ts_corr, rank

def factor_5585(data, **kwargs):
    """
    因子名称: factor_volume_price_oscillator_66349
    数学表达式: ts_delta(vwap, 3) * ts_std_dev(vol, 5) * rank(ts_corr(close, vol, 5) * ts_delta(vol, 1))
    中文描述: 该因子结合了VWAP的短期动量、成交量的波动性和价格变化与成交量之间的相关性，并引入成交量冲击的概念。
            首先，计算VWAP的3日差值来捕捉短期价格动量；然后，计算过去5天成交量的标准差来衡量成交量的波动性；
            最后，计算收盘价与成交量的相关性，并乘以成交量的一阶差分（成交量冲击）进行排序。
            成交量冲击反映了市场情绪的突然变化，旨在寻找成交量放大且与价格走势一致（正相关）或相反（负相关）的股票。
            该因子可能适用于寻找短期内具有爆发性增长潜力的股票。
    因子应用场景：
    1. 寻找短期内具有爆发性增长潜力的股票。
    2. 辅助判断市场情绪的突然变化。
    """
    # 1. 计算 ts_delta(vwap, 3)
    data_ts_delta_vwap = ts_delta(data['vwap'], 3)
    # 2. 计算 ts_std_dev(vol, 5)
    data_ts_std_dev_vol = ts_std_dev(data['vol'], 5)
    # 3. 计算 ts_corr(close, vol, 5)
    data_ts_corr_close_vol = ts_corr(data['close'], data['vol'], 5)
    # 4. 计算 ts_delta(vol, 1)
    data_ts_delta_vol = ts_delta(data['vol'], 1)
    # 5. 计算 ts_corr(close, vol, 5) * ts_delta(vol, 1)
    data_multiply = data_ts_corr_close_vol * data_ts_delta_vol
    # 6. 计算 rank(ts_corr(close, vol, 5) * ts_delta(vol, 1))
    data_rank = rank(data_multiply, 2)
    # 7. 计算 ts_delta(vwap, 3) * ts_std_dev(vol, 5) * rank(ts_corr(close, vol, 5) * ts_delta(vol, 1))
    factor = data_ts_delta_vwap * data_ts_std_dev_vol * data_rank

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()