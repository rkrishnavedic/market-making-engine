# Market Making Engine

A quantitative market-making framework designed to simulate liquidity provision using stochastic control models. The engine processes raw market events (limit/market orders) to manage inventory risk and price discovery in real-time.

## Features

### 1. Market Data & Order Book Engine [Done]

* **Events:** Real-time processing of Limit, Cancel, and Market order events.
* **Microstructure Signals:**
  * **Micro-price:** Volume-weighted fair value calculation to lead mid-price movements.
  * **Order Book Imbalance (OBI):** Predictive signaling of short-term buy/sell pressure.
  * **Kyle’s Lambda ($\lambda$):** Real-time estimation of price impact and "toxic" order flow.


### 2. Pricing & Risk Engine (Avellaneda-Stoikov) [Done]

* **Reservation Price ($r$):** Dynamic skewing of the mid-price based on current inventory position ($q$) and risk aversion ($\gamma$).
* **Optimal Spread ($\delta$):** Volatility-adjusted spread calculation incorporating market liquidity ($\kappa$) and realized variance ($\sigma^2$).
* **Inventory Management:** Automated "leaning" of quotes to neutralize directional exposure and mitigate drawdown.

### 3. Portfolio & Backtesting Suite [In Progress]

* **Real-time Ledger:** Tracking of cash, net inventory position, and realized/unrealized PnL.
* **Execution Simulator:** A matching engine that simulates "passive fills" against historical market aggressor flow.


### 4. Integration & Performance Analytics [Planned]

* **Full Engine Loop:** Integrating the data ingestor, pricing brain, and portfolio ledger into a single execution thread.
* **Performance Metrics:** Implementation of Sharpe Ratio, Maximum Drawdown, and PnL visualization scripts.


---

## Setup & Usage

### 1. Environment Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run Notebook Environment

```bash
pip install jupyterlab
jupyter lab
```

---
