import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_rank, adv, ts_delta, log

def factor_5998(data, **kwargs):
    """
    数学表达式: divide(ts_rank(adv(vol, 15), 20), ts_delta(log(open), 5))
    中文描述: 该因子结合了成交量排名、开盘价对数和时间序列差分。首先计算过去15天的平均成交量，并在过去20天内对其进行时间序列排名。然后，对开盘价取自然对数，并计算其与5期前值的差值。最后，用成交量排名除以开盘价对数的时间序列差分。这个因子旨在捕捉市场流动性与开盘价平滑处理后短期变化率的相对强度。相较于参考因子，该因子通过引入开盘价的对数变换和时间序列差分计算，增加了因子的复杂性和创新性，试图捕捉更深层次的市场动态，并根据评估报告的建议，替换了意义不明确的反正切和向下取整操作，并引入了时间序列差分来衡量短期变化，同时调整了窗口期参数以尝试提升预测能力和稳定性。
    因子应用场景：
    1. 市场流动性分析：通过成交量排名评估股票的流动性水平。
    2. 开盘价短期变化率：利用开盘价对数的时间序列差分捕捉开盘价的短期变化。
    3. 相对强度分析：结合流动性和开盘价变化率，评估市场动态。
    """
    # 1. 计算 adv(vol, 15)
    data_adv_vol = adv(data['vol'], d = 15)
    # 2. 计算 ts_rank(adv(vol, 15), 20)
    data_ts_rank = ts_rank(data_adv_vol, d = 20)
    # 3. 计算 log(open)
    data_log_open = log(data['open'])
    # 4. 计算 ts_delta(log(open), 5)
    data_ts_delta = ts_delta(data_log_open, d = 5)
    # 5. 计算 divide(ts_rank(adv(vol, 15), 20), ts_delta(log(open), 5))
    factor = divide(data_ts_rank, data_ts_delta)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()