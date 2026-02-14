import requests, pandas as pd

# Fetch recent BTC-USD hourly prices from CoinGecko (public, no key)
resp = requests.get("https://api.coingecko.com/api/v3/coins/bitcoin/market_chart",
                    params={"vs_currency": "usd", "days": 3, "interval": "hourly"})
prices = resp.json()["prices"]  # [timestamp_ms, price]

df = pd.DataFrame(prices, columns=["ts", "price"])
df["ts"] = pd.to_datetime(df["ts"], unit="ms")

# Simulate: buy at first price, sell at last price, include a 0.1% fee each way
buy_price = df.iloc[0].price
sell_price = df.iloc[-1].price
fee_rate = 0.001  # 0.1% per trade

size_btc = 0.01  # paper position size
cost = buy_price * size_btc
fees = (buy_price + sell_price) * size_btc * fee_rate
proceeds = sell_price * size_btc

pnl = proceeds - cost - fees

print(f"Bought {size_btc} BTC at ${buy_price:,.2f}, sold at ${sell_price:,.2f}")
print(f"Fees: ${fees:,.2f}")
print(f"P&L: ${pnl:,.2f}")