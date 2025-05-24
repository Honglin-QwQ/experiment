import inspect
import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from operators import divide, ts_std_dev, abs, ts_returns

def factor_5806(data, **kwargs):
    """
    因子名称: Vol_StdDev_Returns_Ratio_12775
    数学表达式: divide(ts_std_dev(vol, 240), abs(ts_returns(vol, 22)))
    中文描述: 该因子计算了交易量的长期波动性（过去240天的标准差）与短期交易量变化率（过去22天的收益率）的绝对值之比。高值可能表明尽管交易量长期波动较大，但近期交易量变化相对平缓，或反之。这可以用来衡量交易量波动与近期动量之间的关系，识别潜在的市场情绪变化或流动性模式的转变。相较于单独使用交易量波动性或收益率，该因子结合了长期稳定性和短期变化的视角，提供了更全面的交易量动态分析。
    因子应用场景：
    1. 波动性与动量背离：识别交易量波动性与近期动量之间存在背离的股票，可能预示着趋势反转。
    2. 市场情绪分析：通过观察因子值的变化，可以洞察市场参与者对特定股票或板块的情绪变化。
    3. 流动性风险评估：高因子值可能意味着流动性风险较高，因为交易量波动较大但近期变化不大，可能导致交易执行困难。
    """
    # 1. 计算 ts_std_dev(vol, 240)
    data_ts_std_dev_vol = ts_std_dev(data['vol'], 240)
    # 2. 计算 ts_returns(vol, 22)
    data_ts_returns_vol = ts_returns(data['vol'], 22)
    # 3. 计算 abs(ts_returns(vol, 22))
    data_abs_ts_returns_vol = abs(data_ts_returns_vol)
    # 4. 计算 divide(ts_std_dev(vol, 240), abs(ts_returns(vol, 22)))
    factor = divide(data_ts_std_dev_vol, data_abs_ts_returns_vol)

    tag = kwargs.get("tag", "DEFAULT")
    factor_name = inspect.currentframe().f_code.co_name
    factor_col = f"F#{factor_name}#{tag}"
    data[factor_col] = factor
    return data.sort_index()