import pandas as pd
import scipy.stats as stats

import plotly.graph_objects as go
import plotly.offline as pyo
from scipy import signal
import scipy.cluster.hierarchy as spc
import plotly.io as pio
from plotly.graph_objs import *
import plotly.express as px
import json
import numpy as np



def compute_error(mean, count, alpha=0.05):
    '''
    Input: mean, count and the significance level
    Return: standard error * z_score
    '''
    z_score = stats.t.ppf(q=1-alpha/2, df=count-1)
    mean = np.abs(mean)
    std_err = np.sqrt(mean*(1-mean)/count)

    return z_score*std_err

def plotly_barplot(years, df_compounds1, df_compounds2, df_compounds3, df_metoo_compounds1, df_metoo_compounds2, df_metoo_compounds3):
    '''
    Generate a plotly barplot with error bars for the weekly compound it  and export as compound_bar.html.
        '''
    fig = go.Figure()
    for i, year in enumerate(years):

        fig.add_trace(go.Bar(
            name=f"Woman's day (08/03)",
            x=['< 40 (women)', '40-60 (women)', '> 60 (women)','< 40 (men)', '40-60 (men)', '> 60 (men)'], y=df_compounds1[i]['mean'],
            error_y=dict(type='data', array=df_compounds1[i].error)
        ))

        fig.add_trace(go.Bar(
            name=f"#MeToo (15/10)",
            x=['< 40 (women)', '40-60 (women)', '> 60 (women)','< 40 (men)', '40-60 (men)', '> 60 (men)'], y=df_compounds2[i]['mean'],
            error_y=dict(type='data', array=df_compounds2[i].error)
        ))

        fig.add_trace(go.Bar(
            name=f'Overall average (all year)',
            x=['< 40 (women)', '40-60 (women)', '> 60 (women)','< 40 (men)', '40-60 (men)', '> 60 (men)'], y=df_compounds3[i]['mean'],
            error_y=dict(type='data', array=df_compounds3[i].error)
        ))

        fig.add_trace(go.Bar(
            name=f"Woman's day (08/03)",
            x=['< 40 (women)', '40-60 (women)', '> 60 (women)','< 40 (men)', '40-60 (men)', '> 60 (men)'], y=df_metoo_compounds1[i]['mean'],
            error_y=dict(type='data', array=df_metoo_compounds1[i].error)
        ))

        fig.add_trace(go.Bar(
            name=f"#MeToo (15/10)",
            x=['< 40 (women)', '40-60 (women)', '> 60 (women)','< 40 (men)', '40-60 (men)', '> 60 (men)'], y=df_metoo_compounds2[i]['mean'],
            error_y=dict(type='data', array=df_metoo_compounds2[i].error)
        ))

        fig.add_trace(go.Bar(
            name=f'Overall average (all year)',
            x=['< 40 (women)', '40-60 (women)', '> 60 (women)','< 40 (men)', '40-60 (men)', '> 60 (men)'], y=df_metoo_compounds3[i]['mean'],
            error_y=dict(type='data', array=df_metoo_compounds3[i].error)
        ))





    # Make 10th trace visible
    for i in range(len(fig.data)):
        fig.data[i].visible = True if i < 3 else False

    # Add dropdown
    fig.update_layout(
        yaxis_title="Mean compound value",
        title_text='Percentage of women speakers through time',
        title_x=0.45,

        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(label="Women, 2015",
                        method="update",
                        args=[{"visible": [True, True, True, False, False, False, False, False, False,
                        False, False, False, False, False, False, False, False, False]},
                            ]),
                    dict(label="Women, 2017",
                        method="update",
                        args=[{"visible": [False, False, False, False, False, False, True, True, True,
                        False, False, False, False, False, False, False, False, False]},
                            ]),
                    dict(label="Women, 2019",
                        method="update",
                        args=[{"visible": [False, False, False, False, False, False, False, False, False,
                        False, False, False, True, True, True, False, False, False]},
                            ]),
                    dict(label="Metoo, 2015",
                        method="update",
                        args=[{"visible": [False, False, False, True, True, True, False, False, False,
                        False, False, False, False, False, False, False, False, False]},
                            ]),
                    dict(label="Metoo, 2017",
                        method="update",
                        args=[{"visible": [False, False, False, False, False, False, False, False, False,
                        True, True, True, False, False, False, False, False, False,]},
                            ]),
                    dict(label="Metoo, 2019",
                        method="update",
                        args=[{"visible": [False, False, False, False, False, False, False, False, False,
                        False, False, False, False, False, False, True, True, True]},
                            ]),
                ]),
                x=0.62,
                y=1.15,
            ),
        ])
    fig.update_layout(
        annotations=[
            dict(text='Subject, Year', x=0.42,xref='paper', yref='paper', y=1.12, showarrow=False)])
    
    fig.show()
    RESULT_PATH = './data/HTML/'
    FIG_NAME = 'compound_bar.html'
    pio.write_html(fig, file=RESULT_PATH + FIG_NAME, auto_open=False)


def generate_barplot(PATH_DATA, datasets, years):
    '''
    Preprocess the data to be plotted on the bar plot with plotly_barplot().
    Files from line 144 to 149 must be downloaded and added to the right folder.
     '''
    datasets = ['women', 'metoo']
    years = [2015, 2017, 2019]
    df_compounds1, df_compounds2, df_compounds3 = [], [], []
    df_metoo_compounds1, df_metoo_compounds2, df_metoo_compounds3 = [], [], []

    for year in years:
        QUOTES_FILE = PATH_DATA + f'/quotes-{year}-filtered_sentiment_age_compounds_per_gender_age_8_3.json.bz2'
        QUOTES_FILE2 = PATH_DATA + f'/quotes-{year}-filtered_sentiment_age_compounds_per_gender_age_15_10.json.bz2'
        QUOTES_FILE3 = PATH_DATA + f'/quotes-{year}-filtered_sentiment_age_compounds_per_gender_age.json.bz2'

        QUOTES_metoo_FILE = PATH_DATA + f'/quotes-{year}-filtered_metoo_sentiment_age_compounds_per_gender_age_8_3.json.bz2'
        QUOTES_metoo_FILE2 = PATH_DATA + f'/quotes-{year}-filtered_metoo_sentiment_age_compounds_per_gender_age_15_10.json.bz2'
        QUOTES_metoo_FILE3 = PATH_DATA + f'/quotes-{year}-filtered_metoo_sentiment_age_compounds_per_gender_age.json.bz2'

        df_compound1 = pd.read_json(QUOTES_FILE, lines=True, compression='bz2', typ='frame')
        df_compound1['error'] = df_compound1.apply(lambda x: compute_error(x['mean'], x['count']), axis=1)
        df_compound2 = pd.read_json(QUOTES_FILE2, lines=True, compression='bz2', typ='frame')
        df_compound2['error'] = df_compound2.apply(lambda x: compute_error(x['mean'], x['count']), axis=1)
        df_compound3 = pd.read_json(QUOTES_FILE3, lines=True, compression='bz2', typ='frame')
        df_compound3['error'] = df_compound3.apply(lambda x: compute_error(x['mean'], x['count']), axis=1)

        df_metoo_compound1 = pd.read_json(QUOTES_metoo_FILE, lines=True, compression='bz2', typ='frame')
        df_metoo_compound1['error'] = df_metoo_compound1.apply(lambda x: compute_error(x['mean'], x['count']), axis=1)
        df_metoo_compound2 = pd.read_json(QUOTES_metoo_FILE2, lines=True, compression='bz2', typ='frame')
        df_metoo_compound2['error'] = df_metoo_compound2.apply(lambda x: compute_error(x['mean'], x['count']), axis=1)
        df_metoo_compound3 = pd.read_json(QUOTES_metoo_FILE3, lines=True, compression='bz2', typ='frame')
        df_metoo_compound3['error'] = df_metoo_compound3.apply(lambda x: compute_error(x['mean'], x['count']), axis=1)

        df_compounds1.append(df_compound1)
        df_compounds2.append(df_compound2)
        df_compounds3.append(df_compound3)

        df_metoo_compounds1.append(df_metoo_compound1)
        df_metoo_compounds2.append(df_metoo_compound2)
        df_metoo_compounds3.append(df_metoo_compound3)

    plotly_barplot(years, df_compounds1, df_compounds2, df_compounds3, df_metoo_compounds1, df_metoo_compounds2, df_metoo_compounds3)
