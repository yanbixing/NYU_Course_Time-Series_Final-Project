# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 13:46:00 2018

@author: Jinze Chen
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import  linregress
import seaborn as sns
from cycler import cycler
from IPython.display import display, HTML
#import pandas_market_calendars as mcal

#plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b', 'y']) )))
plt.style.use('ggplot')

def get_hitrate(wt_df, fwd_rtn, thred = 0, axis = 1):
    """ Compute the hitrate
    Args:
        wt_df: the dataframe of the portfolio weight
        fwd_rtn: 
        thred: the threshold that rtn must be greater than to mark as positive bet

    """
    rtn = wt_df.fillna(0) * fwd_rtn.fillna(0)
    
    rtn = rtn[wt_df.fillna(0) != 0]
    all_bet = rtn.count(axis=axis)
    
    rtn = rtn[rtn > thred]
    pos_bet = rtn.count(axis=axis)
    
    return pos_bet / all_bet


def get_max_dd(value_df):
    value = value_df.ffill().fillna(1)
    cum_max = value.apply(np.maximum.accumulate,axis=0)
    dd = 1. - value/cum_max
    return dd.max().apply(lambda x: x if x<1. else 1.)
    

def get_turnover(wt_df):
    thruput = abs(wt_df - wt_df.shift(1)).apply(sum, axis = 1)
    return thruput / 2.

def get_gross_leverage(wt_df):
    gross_leverage = wt_df.abs().sum(axis = 1)
    return gross_leverage

        
def compute_rtn_multiple(p_wt_dfs, fwd_rtn):
    
    if "Long-only" in p_wt_dfs:
        p_nms = sorted(p_wt_dfs.keys(),key=lambda s:len(s))
    elif "Q1" in p_wt_dfs:
        p_nms = sorted(p_wt_dfs.keys(),key=lambda s:str(len(s))+s)
    else :
        p_nms = sorted(p_wt_dfs.keys())
    
    r_dfs = []
    hr_dfs = []
    to_dfs = []
    gl_dfs = []
    for p_nm in p_nms :

        wt_df = p_wt_dfs[p_nm].reindex(fwd_rtn.index)
        # compute performance measure
        gl = get_gross_leverage(wt_df)
        to = get_turnover(wt_df)
        hr = get_hitrate(wt_df, fwd_rtn)
        
        rs = (wt_df.fillna(value=0) * fwd_rtn.fillna(value=0)).fillna(0)
        r = rs.apply(sum, axis=1)
        
        r_dfs.append(r)
        hr_dfs.append(hr)
        to_dfs.append(to)
        gl_dfs.append(gl)    

    r_df = pd.concat(r_dfs, axis = 1, join = 'outer')
    r_df.columns = p_nms   
    
    hr_df = pd.concat(hr_dfs, axis = 1, join = 'outer')
    hr_df.columns = p_nms  
    
    to_df = pd.concat(to_dfs, axis = 1, join = 'outer')
    to_df.columns = p_nms 
    
    gl_df = pd.concat(gl_dfs, axis = 1, join = 'outer')
    gl_df.columns = p_nms   
    
    return r_df, hr_df, to_df, gl_df


def compute_rtn_ls(wt_df, fwd_rtn):
    if type(wt_df) is pd.Series and type(fwd_rtn) is pd.Series:
        wt_df = pd.DataFrame(wt_df)
        wt_df.columns = ["asset0"]
        fwd_rtn = pd.DataFrame(fwd_rtn)
        fwd_rtn.columns = ["asset0"]
    
    wt_df = wt_df.loc[fwd_rtn.index]

    wt_long_df = wt_df.copy(deep = True)
    wt_long_df[wt_long_df < 0] = 0
    
    wt_short_df = wt_df.copy(deep = True)
    wt_short_df[wt_short_df > 0] = 0
    
    wt_buy_and_hold = wt_df.copy(deep = True)
    wt_buy_and_hold = wt_buy_and_hold*0.+1
    
    p_wt_dfs = {"Long-only":wt_long_df,"Short-only":wt_short_df,
                "Long-Short ":wt_df,"Buy and Hold":wt_buy_and_hold}
    
    return compute_rtn_multiple(p_wt_dfs, fwd_rtn)

def backtest_ls(wt_df, fwd_rtn, initial_cash):
    r_df, hr_df, to_df, gl_df = compute_rtn_ls(wt_df, fwd_rtn)
    return backtest_plot(r_df, hr_df, to_df, gl_df,initial_capital=initial_cash)
    
def match_index_dropna(series1, series2):
    idx = series1.dropna().index.intersection(series2.dropna().index)
    return series1.loc[idx], series2.loc[idx]

def backtest_plot(r_df, hr_df, to_df, gl_df,initial_capital=1.):
    # annualize
    af = 252

    # backtest
    #value_df = (1.+r_df).cumprod(axis = 0)*initial_capital
    
    value_df = (1.+r_df.cumsum(axis = 0))*initial_capital
    fig, axs = plt.subplots(3,1,figsize = (16,16))
    #fig.subplots_adjust(hspace=.3)
    #ir = (pnl - bm).mean()/(pnl - bm).std()*af
    ax = axs[0]
    ax.set_title("Wealth")
    value_df.ffill().plot(ax=ax)
    ax.set_ylabel("Value")
    ax.set_xlabel("Date")
    ax.legend()
    
    ax = axs[1]
    ax.set_title("Position")
    value_df.ffill().plot(ax=ax)
    ax.set_ylabel("Value")
    ax.set_xlabel("Date")
    ax.legend()
            
    ax = axs[2]
    years = r_df.apply(lambda x:x.name.year, axis =1)
    (r_df[gl_df.abs()>1e-6].groupby(years).mean()*af*100).plot(kind="bar",ax = ax )
    ax.set_title("Annual PnL")
    ax.set_ylabel("Annualized Return(%)")
    ax.set_xlabel("Year")  
    plt.show()
    
    return compute_stats(r_df, hr_df, to_df, gl_df,initial_capital)


def backtest_single_asset(wt_df, fwd_rtn, initial_capital=1., plot= True):
    fwd_rtn = fwd_rtn.reindex(wt_df.index)
    
    
    r_df, hr_df, to_df, gl_df = compute_rtn_ls(wt_df, fwd_rtn)
    # annualize
    af = 252
   
    # backtest
    #value_df = (1.+r_df).cumprod(axis = 0)*initial_capital
    value_df = (1.+r_df.cumsum(axis = 0))*initial_capital
    if plot:
        fig, axs = plt.subplots(3,1,figsize = (16,12))
        #fig.subplots_adjust(hspace=.3)
        #ir = (pnl - bm).mean()/(pnl - bm).std()*af
        ax = axs[0]
        ax.set_title("Wealth")
        value_df.ffill().plot(ax=ax)
        ax.set_ylabel("Value")
        ax.set_xlabel("Date")
        ax.legend()
        
        ax = axs[1]
        ax.set_title("Position")
        (wt_df*100).plot(ax=ax)
        ax.set_ylabel("Position(%)")
        ax.set_xlabel("Date")
        ax.legend()
                
        ax = axs[2]
        years = r_df.apply(lambda x:x.name.year, axis =1)
        (r_df[gl_df.abs()>1e-6].groupby(years).mean()*af*100).plot(kind="bar",ax = ax )
        ax.set_title("Annual PnL")
        ax.set_ylabel("Annualized Return(%)")
        ax.set_xlabel("Year")  
        
        plt.show()
    
    
    return compute_stats(r_df, hr_df, to_df, gl_df,initial_capital)
    
    
def compute_stats(r_df, hr_df, to_df, gl_df,initial_capital):

    # annualize
    af = 252

    value_df = (1.+r_df.cumsum(axis = 0))*initial_capital
    
    df_summary = pd.DataFrame(index = r_df.columns, columns=["annualized return","annualized vol","sharp ratio",'hit rate', "gross leverage", "turnover"])
    df_summary.loc[:,"gross leverage"] = (100.*gl_df[gl_df.abs()>1e-6].mean()).apply(lambda x :"%.2f%%"%x)
    df_summary.loc[:,"turnover"] = (100.*to_df[gl_df.abs()>1e-6].mean() * af).apply(lambda x :"%.2f%%"%(x))
    
    hr_out = pd.Series(index = gl_df.columns)
    for c in gl_df.columns:
        gl,hr = match_index_dropna(gl_df.loc[:,c],hr_df.loc[:,c])
        hr_out[c] = (gl*hr).sum()/(gl.sum())
        
    df_summary.loc[:,"hit rate"] = hr_out.apply(lambda x :"%.2f%%"%(x*100.))
    rtn = r_df.mean()
    vol = r_df.std()
    df_summary.loc[:,"sharp ratio"] = (rtn/vol*np.sqrt(af)).apply(lambda x :"%.2f"%x)
    df_summary.loc[:,"annualized return"] = (rtn*af*100.).apply(lambda x :"%.2f%%"%x)
    df_summary.loc[:,"annualized vol"] = (vol*np.sqrt(af)*100.).apply(lambda x :"%.2f%%"%x)
    df_summary.loc[:,"max drawdown"] = (get_max_dd(value_df)*100.).apply(lambda x :"%.2f%%"%x)
    plt.show()
    return df_summary
        