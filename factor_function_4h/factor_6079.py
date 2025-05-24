import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_decay_exp_window, divide, ts_std_dev

def factor_6079(data, **kwargs):
    """
    数学表达式: ts_decay_exp_window(divide(vol, ts_std_dev(vol, 20)), 30, factor=0.8)
    中文描述: 该因子计算了当前成交量与其过去20日标准差的比率的指数衰减加权平均值。它通过计算每日成交量与过去20日成交量标准差的比值，然后对这个比值计算过去30天的指数衰减加权平均值（衰减因子为0.8）。高因子值表明近期成交量相对于其自身的波动性较高，可能预示着市场活跃度增加或潜在的价格变动。相较于参考因子，该因子将波动率计算应用于成交量本身，并使用了指数衰减加权，使得近期成交量的相对波动情况对因子值影响更大，更能捕捉成交量的短期异常变化。这可能用于识别成交量驱动的市场异动或趋势的早期信号。
    因子应用场景：
    1. 市场活跃度分析：用于识别成交量相对于历史波动率显著增加的股票，可能表明市场关注度提升。
    2. 异常交易量检测：可以帮助发现成交量异常波动的股票，这些股票可能存在潜在的市场操纵或重大事件影响。
    3. 趋势确认：结合价格走势，验证成交量放大是否伴随价格上涨，从而确认趋势的有效性。
    """
    # 1. 计算 ts_std_dev(vol, 20)
    data_ts_std_dev = ts_std_dev(data['vol'], 20)
    # 2. 计算 divide(vol, ts_std_dev(vol, 20))
    data_divide = divide(data['vol'], data_ts_std_dev)
    # 3. 计算 ts_decay_exp_window(divide(vol, ts_std_dev(vol, 20)), 30, factor=0.8)
    factor = ts_decay_exp_window(data_divide, 30, factor=0.8)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()