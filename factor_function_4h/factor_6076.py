import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import rank
from operators import ts_delta
from operators import ts_std_dev
from operators import ts_corr
from operators import ts_decay_exp_window
import pandas as pd

def factor_6076(data, **kwargs):
    """
    因子名称: VolStdDevDeltaRankPlusTSCorrDecay_74073
    数学表达式: rank(ts_delta(ts_std_dev(vol, 180), 1)) + ts_decay_exp_window(ts_corr(vol, close, 60), 15, 0.7)
    中文描述: 该因子结合了长期成交量标准差的变化率排名和短期成交量与收盘价相关性的指数衰减加权平均。第一部分计算了过去180天成交量标准差的日变化量，并对其进行截面排名。这旨在捕捉长期成交量波动性的短期趋势变化，并对窗口期进行了调整以探索更优参数。第二部分计算了成交量与收盘价在过去60天内的相关性，并对过去15天的相关性进行指数衰减加权平均，衰减因子为0.7。这旨在识别当前成交量与价格走势的关联程度，并赋予近期关联性更高的权重，同时调整了窗口期和衰减因子。将这两部分相加，旨在构建一个同时考虑长期波动性变化和短期量价关联性及其近期趋势的综合因子。相较于参考因子，创新点在于：1. 对长期成交量波动性进行了差分处理，关注其变化率。2. 第二部分引入了成交量与收盘价的ts_corr，而非简单的Zscore，关注量价关系而非单一量能的异常。3. 对短期量价相关性使用了指数衰减加权平均，更强调近期量价关系的影响，并对衰减窗口和因子进行了调整。4. 结合了变化率排名和指数衰减加权平均的量价相关性，提供了更动态的交易量和价格分析视角。该因子参考了历史输出的结构，并根据改进建议，尝试调整了窗口期参数（180, 60, 15）和衰减因子（0.7），并引入了ts_corr操作符来捕捉量价关系，以期提升因子的预测能力和稳定性。
    因子应用场景：
    1. 波动性趋势跟踪：捕捉成交量波动性的短期趋势变化，辅助判断市场活跃度和潜在风险。
    2. 量价关系分析：识别成交量与价格走势的关联程度，辅助验证价格趋势的可靠性。
    3. 综合信号：结合波动性变化和量价关联性，提供更全面的市场分析视角。
    """
    # 1. 计算 ts_std_dev(vol, 180)
    data_ts_std_dev_vol = ts_std_dev(data['vol'], 180)
    # 2. 计算 ts_delta(ts_std_dev(vol, 180), 1)
    data_ts_delta = ts_delta(data_ts_std_dev_vol, 1)
    # 3. 计算 rank(ts_delta(ts_std_dev(vol, 180), 1))
    factor1 = rank(data_ts_delta, 2)
    # 4. 计算 ts_corr(vol, close, 60)
    data_ts_corr = ts_corr(data['vol'], data['close'], 60)
    # 5. 计算 ts_decay_exp_window(ts_corr(vol, close, 60), 15, 0.7)
    factor2 = ts_decay_exp_window(data_ts_corr, 15, 0.7)
    # 6. 计算 rank(ts_delta(ts_std_dev(vol, 180), 1)) + ts_decay_exp_window(ts_corr(vol, close, 60), 15, 0.7)
    factor = factor1 + factor2

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()