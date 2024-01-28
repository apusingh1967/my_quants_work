import yfinance as yf
import numpy as np 
from scipy.optimize import minimize
import matplotlib.pyplot as plt

def get_data(tickers):
    data = yf.download(tickers)
    data = data['Adj Close']
    data = data.dropna().pct_change(1).dropna()
    return data 

def mv(wts, data):
    # λ: A higher risk aversion parameter leads to a greater penalty for risk in the utility function
    risk_aversion = 3 # risk_aversion
    wealth = 1
    risk_free_ret = 1 + 0.25/100
    p_ret = np.multiply(data, np.transpose(wts)).sum(axis=1)
    mean = np.mean(p_ret, axis=0)
    std = np.std(p_ret, axis=0)

    mv_criterion =  risk_free_ret**(1 - risk_aversion) / (1 + risk_aversion) + \
                    risk_free_ret**(-risk_aversion) * wealth * mean - \
                    risk_aversion / 2 * risk_free_ret ** (-1 - risk_aversion) * wealth ** 2 * std ** 2
    return -1 * mv_criterion # func is to minimize, so negate it

def calculate_mv(tickers):
    data = get_data(tickers)
    split = int(0.7 * len(data))
    train_set = data.iloc[:split, :]
    test_set = data.iloc[split:, :]
    number_of_assets = data.shape[1]
    initial_val_of_wts = np.ones(number_of_assets)
    constraints = {'type': 'eq', 'fun': lambda x: sum(abs(x)) - 1}
    bounds = [(0, 1) for _ in range(0, number_of_assets)]
    return minimize(mv, initial_val_of_wts, method='SLSQP', args=train_set,  \
                    bounds=bounds, constraints=constraints, options={'disp': True}), test_set

def plot(mv_res, test_set):
    returns = np.multiply(test_set, np.transpose(mv_res))
    returns_sum = returns.sum(axis=1)
    plt.figure(figsize=(15, 8))
    plt.plot(np.cumsum(returns_sum) * 100, color='#035593', linewidth=3)
    plt.ylabel("Cumulative returns %", size=15, fontweight='bold')
    plt.xticks(size=15, fontweight='bold')
    plt.yticks(size=15, fontweight='bold')
    plt.title('Cumulative returns of MV portfolio', size=20)
    plt.axhline(0, color='r', linewidth=3)
    plt.show()
    
if __name__ == '__main__':
    tickers = ['META', 'NFLX', 'TSLA']
    mv_res, test_set = calculate_mv(tickers)
    plot(mv_res.x, test_set)

