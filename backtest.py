import numpy as np
import pandas as pd
from tqdm import tqdm
from loguru import logger
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor
from collections import Counter


def cal_break_even_point(seq) -> float:
    """计算单笔收益序列的盈亏平衡点

    :param seq: 单笔收益序列，数据样例：[0.01, 0.02, -0.01, 0.03, 0.02, -0.02, 0.01, -0.01, 0.02, 0.01]
    :return: 盈亏平衡点
    """
    if sum(seq) < 0:
        return 1.0
    seq = np.cumsum(sorted(seq))  # type: ignore
    return (np.sum(seq < 0) + 1) / len(seq)  # type: ignore
def daily_performance(daily_returns, **kwargs):
    """采用单利计算日收益数据的各项指标

    函数计算逻辑：

    1. 首先，将传入的日收益率数据转换为NumPy数组，并指定数据类型为float64。
    2. 然后，进行一系列判断：如果日收益率数据为空或标准差为零或全部为零，则返回字典，其中所有指标的值都为零。
    3. 如果日收益率数据满足要求，则进行具体的指标计算：

        - 年化收益率 = 日收益率列表的和 / 日收益率列表的长度 * 252
        - 夏普比率 = 日收益率的均值 / 日收益率的标准差 * 标准差的根号252
        - 最大回撤 = 累计日收益率的最高累积值 - 累计日收益率
        - 卡玛比率 = 年化收益率 / 最大回撤（如果最大回撤不为零，则除以最大回撤；否则为10）
        - 日胜率 = 大于零的日收益率的个数 / 日收益率的总个数
        - 年化波动率 = 日收益率的标准差 * 标准差的根号252
        - 下行波动率 = 日收益率中小于零的日收益率的标准差 * 标准差的根号252
        - 非零覆盖 = 非零的日收益率个数 / 日收益率的总个数
        - 回撤风险 = 最大回撤 / 年化波动率；一般认为 1 以下为低风险，1-2 为中风险，2 以上为高风险

    4. 将所有指标的值存储在字典中，其中键为指标名称，值为相应的计算结果。

    :param daily_returns: 日收益率数据，样例：
        [0.01, 0.02, -0.01, 0.03, 0.02, -0.02, 0.01, -0.01, 0.02, 0.01]
    :param kwargs: 其他参数
        - yearly_days: int, 252, 一年的交易日数
    :return: dict
    """
    daily_returns = np.array(daily_returns, dtype=np.float64)
    yearly_days = kwargs.get("yearly_days", 252)

    if len(daily_returns) == 0 or np.std(daily_returns) == 0 or all(x == 0 for x in daily_returns):
        return {
            "绝对收益": 0,
            "年化": 0,
            "夏普": 0,
            "最大回撤": 0,
            "卡玛": 0,
            "日胜率": 0,
            "日盈亏比": 0,
            "日赢面": 0,
            "年化波动率": 0,
            "下行波动率": 0,
            "非零覆盖": 0,
            "盈亏平衡点": 0,
            "新高间隔": 0,
            "新高占比": 0,
            "回撤风险": 0,
        }

    annual_returns = np.sum(daily_returns) / len(daily_returns) * yearly_days
    sharpe_ratio = np.mean(daily_returns) / np.std(daily_returns) * np.sqrt(yearly_days)
    cum_returns = np.cumsum(daily_returns)
    dd = np.maximum.accumulate(cum_returns) - cum_returns
    max_drawdown = np.max(dd)
    kama = annual_returns / max_drawdown if max_drawdown != 0 else 10
    win_pct = len(daily_returns[daily_returns >= 0]) / len(daily_returns)
    daily_mean_loss = np.mean(daily_returns[daily_returns < 0]) if len(daily_returns[daily_returns < 0]) > 0 else 0
    daily_ykb = np.mean(daily_returns[daily_returns >= 0]) / abs(daily_mean_loss) if daily_mean_loss != 0 else 5

    annual_volatility = np.std(daily_returns) * np.sqrt(yearly_days)
    none_zero_cover = len(daily_returns[daily_returns != 0]) / len(daily_returns)

    downside_volatility = np.std(daily_returns[daily_returns < 0]) * np.sqrt(yearly_days)

    # 计算最大新高间隔
    max_interval = Counter(np.maximum.accumulate(cum_returns).tolist()).most_common(1)[0][1]

    # 计算新高时间占比
    high_pct = len([i for i, x in enumerate(dd) if x == 0]) / len(dd)

    def __min_max(x, min_val, max_val, digits=4):
        if x < min_val:
            x1 = min_val
        elif x > max_val:
            x1 = max_val
        else:
            x1 = x
        return round(x1, digits)

    sta = {
        "绝对收益": round(np.sum(daily_returns), 4),
        "年化": round(annual_returns, 4),
        "夏普": __min_max(sharpe_ratio, -100, 100, 2),
        "最大回撤": round(max_drawdown, 4),
        "卡玛": __min_max(kama, -100, 100, 2),
        "日胜率": round(win_pct, 4),
        "日盈亏比": round(daily_ykb, 4),
        "日赢面": round(win_pct * daily_ykb - (1 - win_pct), 4),
        "年化波动率": round(annual_volatility, 4),
        "下行波动率": round(downside_volatility, 4),
        "非零覆盖": round(none_zero_cover, 4),
        "盈亏平衡点": round(cal_break_even_point(daily_returns), 4),
        "新高间隔": max_interval,
        "新高占比": round(high_pct, 4),
        "回撤风险": round(max_drawdown / annual_volatility, 4),
    }
    return sta
def evaluate_pairs(pairs: pd.DataFrame, trade_dir: str = "多空") -> dict:
    """评估开平交易记录的表现

    :param pairs: 开平交易记录，数据样例如下：

        ==========  ==========  ===================  ===================  ==========  ==========  ===========  ============  ==========  ==========
        标的代码     交易方向     开仓时间              平仓时间              开仓价格    平仓价格     持仓K线数    事件序列        持仓天数     盈亏比例
        ==========  ==========  ===================  ===================  ==========  ==========  ===========  ============  ==========  ==========
        DLi9001     多头        2019-02-25 21:36:00  2019-02-25 21:51:00     1147.8      1150.72           16  开多 -> 平多           0       25.47
        DLi9001     多头        2021-09-15 14:06:00  2021-09-15 14:09:00     3155.88     3153.61            4  开多 -> 平多           0       -7.22
        DLi9001     多头        2019-08-29 21:01:00  2019-08-29 22:54:00     1445.86     1454.55          114  开多 -> 平多           0       60.09
        DLi9001     多头        2021-10-11 21:46:00  2021-10-11 22:11:00     3631.77     3622.66           26  开多 -> 平多           0      -25.08
        DLi9001     多头        2020-05-13 09:16:00  2020-05-13 09:26:00     1913.13     1917.64           11  开多 -> 平多           0       23.55
        ==========  ==========  ===================  ===================  ==========  ==========  ===========  ============  ==========  ==========

    :param trade_dir: 交易方向，可选值 ['多头', '空头', '多空']
    :return: 交易表现
    """



    assert trade_dir in [
        "多头",
        "空头",
        "多空",
    ], "trade_dir 参数错误，可选值 ['多头', '空头', '多空']"

    pairs = pairs.copy()

    p = {
        "交易方向": trade_dir,
        "交易次数": 0,
        "累计收益": 0,
        "单笔收益": 0,
        "盈利次数": 0,
        "累计盈利": 0,
        "单笔盈利": 0,
        "亏损次数": 0,
        "累计亏损": 0,
        "单笔亏损": 0,
        "交易胜率": 0,
        "累计盈亏比": 0,
        "单笔盈亏比": 0,
        "盈亏平衡点": 1,
        "持仓天数": 0,
        "持仓K线数": 0,
    }

    if len(pairs) == 0:
        return p

    if trade_dir in ["多头", "空头"]:
        pairs = pairs[pairs["交易方向"] == trade_dir]
        if len(pairs) == 0:
            return p

    pairs = pairs.to_dict(orient="records")
    p["交易次数"] = len(pairs)
    p["盈亏平衡点"] = round(cal_break_even_point([x["盈亏比例"] for x in pairs]), 4)
    p["累计收益"] = round(sum([x["盈亏比例"] for x in pairs]), 2)
    p["单笔收益"] = round(p["累计收益"] / p["交易次数"], 2)
    p["持仓天数"] = round(sum([x["持仓天数"] for x in pairs]) / len(pairs), 2)
    p["持仓K线数"] = round(sum([x["持仓K线数"] for x in pairs]) / len(pairs), 2)

    win_ = [x for x in pairs if x["盈亏比例"] >= 0]
    if len(win_) > 0:
        p["盈利次数"] = len(win_)
        p["累计盈利"] = sum([x["盈亏比例"] for x in win_])
        p["单笔盈利"] = round(p["累计盈利"] / p["盈利次数"], 4)
        p["交易胜率"] = round(p["盈利次数"] / p["交易次数"], 4)

    loss_ = [x for x in pairs if x["盈亏比例"] < 0]
    if len(loss_) > 0:
        p["亏损次数"] = len(loss_)
        p["累计亏损"] = sum([x["盈亏比例"] for x in loss_])
        p["单笔亏损"] = round(p["累计亏损"] / p["亏损次数"], 4)

        p["累计盈亏比"] = round(p["累计盈利"] / abs(p["累计亏损"]), 4)
        p["单笔盈亏比"] = round(p["单笔盈利"] / abs(p["单笔亏损"]), 4)

    return p

class WeightBacktest:

    def __init__(self, dfw, digits=2, weight_type="ts", **kwargs) -> None:

        self.kwargs = kwargs
        self.dfw = dfw.copy()
        self.dfw["dt"] = pd.to_datetime(self.dfw["dt"])
        if self.dfw.isnull().sum().sum() > 0:
            raise ValueError("dfw 中存在空值, 请先处理")

        self.digits = digits
        self.weight_type = weight_type.lower()
        self.fee_rate = kwargs.get("fee_rate", 0.0002)
        self.dfw["weight"] = self.dfw["weight"].astype("float").round(digits)
        self.symbols = list(self.dfw["symbol"].unique().tolist())
        self._dailys = None
        self.yearly_days = kwargs.pop("yearly_days", 252)
        self.results = self.backtest(n_jobs=kwargs.pop("n_jobs", 1))

    @property
    def stats(self):
        """回测绩效评价"""
        return self.results.get("绩效评价", {})

    @property
    def alpha(self) -> pd.DataFrame:
        """策略超额收益

        columns = ['date', '策略', '基准', '超额']
        """
        if self._dailys is None:
            return pd.DataFrame()
        df1 = self._dailys.groupby("date").agg({"return": "mean", "n1b": "mean"})
        df1["alpha"] = df1["return"] - df1["n1b"]
        df1.rename(columns={"return": "策略", "n1b": "基准", "alpha": "超额"}, inplace=True)
        df1 = df1.reset_index()
        return df1


    def get_symbol_daily(self, symbol):
        """获取某个合约的每日收益率

        函数计算逻辑：

        1. 从实例变量self.dfw中筛选出交易标的为symbol的数据，并复制到新的DataFrame dfs。
        2. 计算每条数据的收益（edge）：权重乘以下一条数据的价格除以当前价格减1。
        3. 计算每条数据的手续费（cost）：当前权重与前一条数据权重之差的绝对值乘以实例变量self.fee_rate。
        4. 计算每条数据扣除手续费后的收益（edge_post_fee）：收益减去手续费。
        5. 根据日期进行分组，并对每组进行求和操作，得到每日的总收益、总扣除手续费后的收益和总手续费。
        6. 重置索引，并将交易标的符号添加到DataFrame中。
        7. 重命名列名，将'edge_post_fee'列改为 return，将'dt'列改为 date。
        8. 选择需要的列，并返回包含日期、交易标的、收益、扣除手续费后的收益和手续费的DataFrame。

        :param symbol: str，合约代码
        :return: pd.DataFrame，品种每日收益率，

            columns = ['date', 'symbol', 'edge', 'return', 'cost', 'n1b']
            其中
                date        交易日，
                symbol      合约代码，
                n1b         品种每日收益率，
                edge        策略每日收益率，
                long_edge   多头每日收益率，
                short_edge  空头每日收益率，
                return      策略每日收益率减去交易成本后的真实收益，
                cost        交易成本
                turnover    当日的单边换手率

            数据样例如下：

                ==========  ========  ============  ============  =======
                date        symbol            edge        return     cost
                ==========  ========  ============  ============  =======
                2019-01-02  DLi9001    0.00230261    0.00195919   0.00085
                2019-01-03  DLi9001    0.00425589    0.00310589   0.00115
                2019-01-04  DLi9001   -0.0014209    -0.0024709    0.00105
                2019-01-07  DLi9001    0.000988305  -0.000111695  0.0011
                2019-01-08  DLi9001   -0.0004743    -0.0016243    0.00115
                ==========  ========  ============  ============  =======
        """
        dfs = self.dfw[self.dfw["symbol"] == symbol].copy()
        dfs["n1b"] = dfs["price"].shift(-1) / dfs["price"] - 1
        dfs["edge"] = dfs["weight"] * dfs["n1b"]
        dfs["turnover"] = abs(dfs["weight"].shift(1) - dfs["weight"])
        dfs["cost"] = dfs["turnover"] * self.fee_rate
        dfs["return"] = dfs["edge"] - dfs["cost"]

        # 分别计算多头和空头的收益
        dfs["long_weight"] = np.where(dfs["weight"] > 0, dfs["weight"], 0)
        dfs["short_weight"] = np.where(dfs["weight"] < 0, dfs["weight"], 0)
        dfs["long_edge"] = dfs["long_weight"] * dfs["n1b"]
        dfs["short_edge"] = dfs["short_weight"] * dfs["n1b"]

        dfs["long_turnover"] = abs(dfs["long_weight"].shift(1) - dfs["long_weight"])
        dfs["short_turnover"] = abs(dfs["short_weight"].shift(1) - dfs["short_weight"])
        dfs["long_cost"] = dfs["long_turnover"] * self.fee_rate
        dfs["short_cost"] = dfs["short_turnover"] * self.fee_rate

        dfs["long_return"] = dfs["long_edge"] - dfs["long_cost"]
        dfs["short_return"] = dfs["short_edge"] - dfs["short_cost"]

        daily = (
            dfs.groupby(dfs["dt"].dt.date)
            .agg(
                {
                    "edge": "sum",
                    "return": "sum",
                    "cost": "sum",
                    "n1b": "sum",
                    "turnover": "sum",
                    "long_edge": "sum",
                    "short_edge": "sum",
                    "long_cost": "sum",
                    "short_cost": "sum",
                    "long_turnover": "sum",
                    "short_turnover": "sum",
                    "long_return": "sum",
                    "short_return": "sum",
                }
            )
            .reset_index()
        )
        daily["symbol"] = symbol
        daily.rename(columns={"dt": "date"}, inplace=True)
        cols = [
            "date",
            "symbol",
            "edge",
            "return",
            "cost",
            "n1b",
            "turnover",
            "long_edge",
            "long_cost",
            "long_return",
            "long_turnover",
            "short_edge",
            "short_cost",
            "short_return",
            "short_turnover",
        ]

        daily = daily[cols].copy()
        return daily

    def get_symbol_pairs(self, symbol):
        """获取某个合约的开平交易记录

        函数计算逻辑：

        1. 从实例变量self.dfw中筛选出交易标的为symbol的数据，并复制到新的DataFrame dfs。
        2. 将权重乘以10的self.digits次方，并转换为整数类型，作为volume列的值。
        3. 生成bar_id列，从1开始递增，与行数对应。
        4. 创建一个空列表operates，用于存储开平仓交易记录。
        5. 定义内部函数__add_operate，用于向operates列表中添加开平仓交易记录。
           函数接受日期dt、bar_id、交易量volume、价格price和操作类型operate作为参数。
           函数根据交易量的绝对值循环添加交易记录到operates列表中。
        6. 将dfs转换为字典列表rows。
        7. 处理第一个行记录。
           - 如果volume大于0，则调用__add_operate函数添加"开多"操作的交易记录。
           - 如果volume小于0，则调用__add_operate函数添加"开空"操作的交易记录。
        8. 处理后续的行记录。
           - 使用zip函数遍历rows[:-1]和rows[1:]，同时获取当前行row1和下一行row2。
           - 根据volume的正负和变化情况，调用__add_operate函数添加对应的开平仓交易记录。
        9. 创建空列表pairs和opens，用于存储交易对和开仓记录。
        10. 遍历operates列表中的交易记录。
            - 如果操作类型为"开多"或"开空"，将交易记录添加到opens列表中，并继续下一次循环。
            - 如果操作类型为"平多"或"平空"，将对应的开仓记录从opens列表中弹出。
              根据开仓和平仓的价格计算盈亏比例，并创建一个交易对字典，将其添加到pairs列表中。
        11. 将pairs列表转换为DataFrame，并返回包含交易标的的开平仓交易记录的DataFrame。

        """

        dfs = self.dfw[self.dfw["symbol"] == symbol].copy()

        dfs["volume"] = (dfs["weight"] * pow(10, self.digits)).astype(int)
        dfs["bar_id"] = list(range(1, len(dfs) + 1))

        # 根据权重变化生成开平仓记录
        operates = []

        def __add_operate(dt, bar_id, volume, price, operate):
            for _ in range(abs(volume)):
                _op = {"bar_id": bar_id, "dt": dt, "price": price, "operate": operate}
                operates.append(_op)

        rows = dfs.to_dict(orient="records")

        # 处理第一个 row
        if rows[0]["volume"] > 0:
            __add_operate(rows[0]["dt"], rows[0]["bar_id"], rows[0]["volume"], rows[0]["price"], operate="开多")
        elif rows[0]["volume"] < 0:
            __add_operate(rows[0]["dt"], rows[0]["bar_id"], rows[0]["volume"], rows[0]["price"], operate="开空")

        # 处理后续 rows
        for row1, row2 in zip(rows[:-1], rows[1:]):
            if row1["volume"] >= 0 and row2["volume"] >= 0:
                # 多头仓位变化对应的操作
                if row2["volume"] > row1["volume"]:
                    __add_operate(
                        row2["dt"], row2["bar_id"], row2["volume"] - row1["volume"], row2["price"], operate="开多"
                    )
                elif row2["volume"] < row1["volume"]:
                    __add_operate(
                        row2["dt"], row2["bar_id"], row1["volume"] - row2["volume"], row2["price"], operate="平多"
                    )

            elif row1["volume"] <= 0 and row2["volume"] <= 0:
                # 空头仓位变化对应的操作
                if row2["volume"] > row1["volume"]:
                    __add_operate(
                        row2["dt"], row2["bar_id"], row1["volume"] - row2["volume"], row2["price"], operate="平空"
                    )
                elif row2["volume"] < row1["volume"]:
                    __add_operate(
                        row2["dt"], row2["bar_id"], row2["volume"] - row1["volume"], row2["price"], operate="开空"
                    )

            elif row1["volume"] >= 0 >= row2["volume"]:
                # 多头转换成空头对应的操作
                __add_operate(row2["dt"], row2["bar_id"], row1["volume"], row2["price"], operate="平多")
                __add_operate(row2["dt"], row2["bar_id"], row2["volume"], row2["price"], operate="开空")

            elif row1["volume"] <= 0 <= row2["volume"]:
                # 空头转换成多头对应的操作
                __add_operate(row2["dt"], row2["bar_id"], row1["volume"], row2["price"], operate="平空")
                __add_operate(row2["dt"], row2["bar_id"], row2["volume"], row2["price"], operate="开多")

        pairs, opens = [], []
        for op in operates:
            # print(op)
            if op["operate"] in ["开多", "开空"]:
                opens.append(op)
                continue

            assert op["operate"] in ["平多", "平空"]
            open_op = opens.pop()
            if open_op["operate"] == "开多":
                p_ret = round((op["price"] - open_op["price"]) / open_op["price"] * 10000, 2)
                p_dir = "多头"
            else:
                p_ret = round((open_op["price"] - op["price"]) / open_op["price"] * 10000, 2)
                p_dir = "空头"
            pair = {
                "标的代码": symbol,
                "交易方向": p_dir,
                "开仓时间": open_op["dt"],
                "平仓时间": op["dt"],
                "开仓价格": open_op["price"],
                "平仓价格": op["price"],
                "持仓K线数": op["bar_id"] - open_op["bar_id"] + 1,
                "事件序列": f"{open_op['operate']} -> {op['operate']}",
                "持仓天数": (op["dt"] - open_op["dt"]).total_seconds() / (24 * 3600),
                "盈亏比例": p_ret,
            }
            pairs.append(pair)
        df_pairs = pd.DataFrame(pairs)
        return df_pairs



    def process_symbol(self, symbol):
        """处理某个合约的回测数据"""
        daily = self.get_symbol_daily(symbol)
        pairs = self.get_symbol_pairs(symbol)
        return symbol, {"daily": daily, "pairs": pairs}

    def backtest(self, n_jobs=1):

        n_jobs = min(n_jobs, cpu_count())
        logger.info(f"n_jobs={n_jobs}，将使用 {n_jobs} 个进程进行回测")

        symbols = self.symbols
        res = {}
        if n_jobs <= 1:
            for symbol in tqdm(sorted(symbols), desc="WBT进度", leave=False):
                res[symbol] = self.process_symbol(symbol)[1]
        else:
            with ProcessPoolExecutor(n_jobs) as pool:
                for symbol, res_symbol in tqdm(
                    pool.map(self.process_symbol, sorted(symbols)), desc="WBT进度", total=len(symbols), leave=False
                ):
                    res[symbol] = res_symbol

        self._dailys = pd.concat([v["daily"] for k, v in res.items() if k in symbols], ignore_index=True)

        dret = pd.concat([v["daily"] for k, v in res.items() if k in symbols], ignore_index=True)
        dret = pd.pivot_table(dret, index="date", columns="symbol", values="return").fillna(0)

        if self.weight_type == "ts":
            # 时序策略每日收益为各品种收益的等权
            dret["total"] = dret[list(res.keys())].mean(axis=1)
        elif self.weight_type == "cs":
            # 截面策略每日收益为各品种收益的和
            dret["total"] = dret[list(res.keys())].sum(axis=1)
        else:
            raise ValueError(f"weight_type {self.weight_type} not supported, should be 'ts' or 'cs'")

        # dret 中的 date 对应的是上一日；date 后移一位，对应的才是当日收益
        dret = dret.round(4).reset_index()
        res["品种等权日收益"] = dret

        stats = {"开始日期": dret["date"].min().strftime("%Y%m%d"), "结束日期": dret["date"].max().strftime("%Y%m%d")}
        stats.update(daily_performance(dret["total"], yearly_days=self.yearly_days))
        dfp = pd.concat([v["pairs"] for k, v in res.items() if k in symbols], ignore_index=True)
        pairs_stats = evaluate_pairs(dfp)

        pairs_stats = {k: v for k, v in pairs_stats.items() if k in ["单笔收益", "持仓K线数", "交易胜率", "持仓天数"]}
        stats.update(pairs_stats)

        dfw = self.dfw.copy()
        long_rate = dfw[dfw["weight"] > 0].shape[0] / dfw.shape[0]
        short_rate = dfw[dfw["weight"] < 0].shape[0] / dfw.shape[0]
        stats.update({"多头占比": round(long_rate, 4), "空头占比": round(short_rate, 4)})

        alpha = self.alpha.copy()
        stats["波动比"] = round(alpha["策略"].std() / alpha["基准"].std(), 4)
        stats["与基准波动相关性"] = round(alpha["策略"].corr(alpha["基准"].abs()), 4)
        stats["与基准相关性"] = round(alpha["策略"].corr(alpha["基准"]), 4)
        alpha_short = alpha[alpha["基准"] < 0].copy()
        stats["与基准空头相关性"] = round(alpha_short["策略"].corr(alpha_short["基准"]), 4)
        stats["品种数量"] = len(symbols)

        res["绩效评价"] = stats
        return res


