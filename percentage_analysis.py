import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

import os
import plotly.graph_objects as go
import plotly.offline as pyo
from scipy import signal
import scipy.cluster.hierarchy as spc
from pandas import read_excel
from ipywidgets import widgets
from ipywidgets import interactive, HBox, VBox
import plotly.io as pio
from sklearn.cluster import KMeans
from sklearn import linear_model
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score
from plotly.graph_objs import *
from plotly.subplots import make_subplots
import plotly.express as px
import json


def plot_distrib(df_weekly_all, dataset):
    #before meetoo is from 2015 (0) to september 2017 (week 152)
    percent_b4_metoo = df_weekly_all.iloc[0:152].percent_women
    #after meetoo is from september 2017 till 2020
    percent_post_metoo = df_weekly_all.iloc[152:].percent_women

    #plots
    plt.figure(figsize=(11.7,8.27))
    _, bins_, _ = plt.hist(percent_b4_metoo, bins=30, fc=(0, 0, 1, 0.7))
    plt.hist(percent_post_metoo, bins=bins_, fc=(1, 0, 0, 0.7))
    plt.axvline(x=percent_b4_metoo.mean(), ls='--',c=(0,0,1,1))
    plt.axvline(x=percent_post_metoo.mean(), ls='--',c=(0.5,0,0,1))
    plt.legend(['Before September 2017 (mean)', 'After September 2017 (mean)', 'Before September 2017', 'After September 2017'])
    plt.title(f'Weekly percentage of women speakers on {dataset} dataset')
    plt.ylabel('frequency')
    plt.xlabel('percentage of women speaker')
    
    mean_b4 = round(percent_b4_metoo.mean(), 3)
    std_b4 = round(percent_b4_metoo.std(), 3)
    mean_post = round(percent_post_metoo.mean(), 3)
    std_post = round(percent_post_metoo.std(), 3)
    p_value = stats.ttest_ind(percent_b4_metoo, percent_post_metoo, nan_policy="omit").pvalue


    print(f'*************Graph {dataset}*************')
    print(f'mean before #MeToo = {mean_b4}')
    print(f'mean after #MeToo = {mean_post}')
    print(f'std before #MeToo = {std_b4}')
    print(f'std after #MeToo = {std_post}')
    print(f'p-value {p_value}')


def plotly_distrib(df, datasets):

    fig = go.Figure()
    name = ['General (entire quotebank)', 'When talking about women', 'When talking about #MeToo']

    for i in range(len(datasets)):
        #for country in df_weekly_all:
        slope, intercept, r_value, p_value, std_err=stats.linregress(df[i].index,df[i].percent_women)
        line = slope*df[i].index+intercept
        fig.add_trace(go.Scatter(
            x=df[i].date,
            y=df[i].percent_women*100,
            fill='tozeroy',
            mode='none',
            #color='Area',
            name=name[i],
        ))
        fig.add_trace(go.Scatter(
                x=df[i].date,
                y=line*100,
                mode='lines',
                #fillcolor='black',
                marker=go.Marker(),
                name=f'Fitted line'
                ))

    # Reduce opacity to see both histograms
    fig.update_traces(opacity=0.9)
    fig.update_layout()

    # Add range slider
    fig.update_layout(
        xaxis=go.layout.XAxis(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label="1m",
                        step="month",
                        stepmode="backward"),
                    dict(count=6,
                        label="6m",
                        step="month",
                        stepmode="backward"),
                    dict(count=1,
                        label="YTD",
                        step="year",
                        stepmode="todate"),
                    dict(count=1,
                        label="1y",
                        step="year",
                        stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        ), 
        yaxis_title="Percentage of women speakers [%]",
        xaxis_title="Date",
        title_text='Percentage of women speakers through time',
        title_x=0.5
    )

    RESULT_PATH = './data/HTML/'
    FIG_NAME = 'percent_graph.html'

    fig.show()
    pio.write_html(fig, file=RESULT_PATH + FIG_NAME, auto_open=False)