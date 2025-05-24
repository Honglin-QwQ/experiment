from typing import Union

import pandas as pd
from czsc.objects import RawBar,Freq
from chanlun.exchange.exchange_db import ExchangeDB

freq_transfer = {
    "Tick": "tick",
    "1分钟": "1m",
    "5分钟": "5m",
    "10分钟": "10m",
    "15分钟": "15m",
    "30分钟": "30m",
    "60分钟": "60m",
    "2小时":"2h",
    "4小时": "4h",
    "6小时":"6h",
    "8小时":"8h",
    "12小时":"12h",
    "日线": "d",
    "周线": "w",
}




def klines_format_hl(symbol, freq, sdt, edt, data='spot', fq='前复权', **kwargs):
    kwargs['fq'] = fq
    freq_1 = Freq(freq)
    freq_2 = freq_transfer[freq]
    delta = pd.Timedelta(0)  # 默认值
    if "分钟" in freq:
        minutes = int(''.join(filter(str.isdigit, freq)))
        delta = pd.Timedelta(minutes=minutes)
    elif "小时" in freq:
        hours = int(''.join(filter(str.isdigit, freq)))
        delta = pd.Timedelta(hours=hours)
    elif freq == "日线":
        delta = pd.Timedelta(days=1)
    elif freq == "周线":
        delta = pd.Timedelta(days=7)
    if data=='spot':
        exchange = ExchangeDB("currency_spot")
    elif data=='future':
        exchange = ExchangeDB("currency")
    sdt=pd.to_datetime(sdt).strftime("%Y-%m-%d %H:%M:%S")
    edt=pd.to_datetime(edt).strftime("%Y-%m-%d %H:%M:%S")
    if "/" in symbol:
        symbol=symbol
    elif"_" in symbol:
        symbol = symbol.split("_")[0]
        symbol = f"{symbol}/USDT"
    elif "USDT" in symbol:
        symbol = symbol.split("USDT")[0]
        symbol = f"{symbol}/USDT"
    elif "BTC" in symbol:
        symbol = symbol.split("BTC")[0]
        symbol = f"{symbol}/BTC"
    print(symbol)



    bars = exchange.klines(code=symbol, frequency=freq_2, start_date=sdt, end_date=edt)
    i = 0
    bars = bars.to_dict('records')
    raw_bars = []
    for bar in bars:
        raw_bar = RawBar(
            symbol=bar["code"],
            dt=pd.to_datetime(bar["date"]).tz_localize(None)+delta,
            id=i,
            freq=freq_1,
            open=bar["open"],
            close=bar["close"],
            high=bar["high"],
            low=bar["low"],
            vol=bar["volume"],
            amount=bar["amount"],
            trades=bar["trades"],
            tbase=bar["taker_buy_volume"],
            tquote=bar["taker_buy_quote_volume"],
        )
        i = i + 1
        raw_bars.append(raw_bar)
    return raw_bars