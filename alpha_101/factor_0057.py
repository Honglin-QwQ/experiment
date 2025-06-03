import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import ts_rank, ts_decay_linear, ts_corr, indneutralize, multiply

def factor_0057(data, **kwargs):
    """
    数学表达式: (-1 * ts_rank(ts_decay_linear(ts_corr(indneutralize(vwap, IndClass.sector), volume, 3.92795), 7.89291), 5.50322))
    中文描述: 描述：该因子首先计算每个股票的成交量加权平均价(VWAP)相对于其所属行业的超额收益，然后计算该超额收益与成交量在过去3.92天的相关性，接着对该相关性进行7.89天的线性衰减，再计算衰减值的5.50天排名，最后取负值。该因子试图捕捉行业中成交量与价格趋势相关性较弱的股票，可能反映了市场关注度低或者价格发现机制不健全的股票。
    应用场景：1. 可以用于构建反转策略，预期相关性低迷的股票未来可能出现价格回归。2. 可以用于量化选股，选择因子值较低的股票构建投资组合，预期获得超额收益。3. 可以作为风险管理指标，识别市场关注度较低、价格波动可能较大的股票，降低投资组合的风险敞口。
    """
    # 1. 计算 indneutralize(vwap, IndClass.sector)
    data_indneutralize_vwap_sector = indneutralize(data['vwap'], data['industry'])
    # 2. 计算 ts_corr(indneutralize(vwap, IndClass.sector), volume, 3.92795)
    data_ts_corr = ts_corr(data_indneutralize_vwap_sector, data['vol'], 3.92795)
    # 3. 计算 ts_decay_linear(ts_corr(indneutralize(vwap, IndClass.sector), volume, 3.92795), 7.89291)
    data_ts_decay_linear = ts_decay_linear(data_ts_corr, 7.89291)
    # 4. 计算 ts_rank(ts_decay_linear(ts_corr(indneutralize(vwap, IndClass.sector), volume, 3.92795), 7.89291), 5.50322)
    data_ts_rank = ts_rank(data_ts_decay_linear, 5.50322)
    # 5. 计算 -1 * ts_rank(ts_decay_linear(ts_corr(indneutralize(vwap, IndClass.sector), volume, 3.92795), 7.89291), 5.50322)
    factor = multiply(-1, data_ts_rank)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()