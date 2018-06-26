from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from collections import Counter
from textblob import TextBlob, Word
import nltk
from nltk.corpus import stopwords
import string
import spacy
import seaborn as sns
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import plotly.graph_objs as go


def load_articles(articles_list):
    """
    Read files from articles_list into memory and return two dictionaries - one which maps title to the raw text and
    one that maps title to date of article. In addition return list of article titles.
    """
    file_title = articles_list.article_urls.apply(lambda x: x.replace("/", "").replace(".", ""))
    article_date = articles_list.date

    title_date_dict = dict(zip(file_title, article_date))

    title_text_dict = dict()

    for article in file_title:
        with open(f'nyt_scrape/articles/{article}.txt') as f:
            title_text_dict[article] = f.read().replace('’', '').replace('”', '').replace('“', '').replace('—',
                                                                                                           '').split(
                '\n')

    return title_date_dict, title_text_dict, file_title


def compute_sentiment(title_date_dict, title_text_dict, file_title, team_name, team_city):
    """
    Input dictionaries of title-date and title-text, list of file titles and create:
        (title, Total Sentiment Score, Total Mentions, Date)

    These tuples then transformed to dataframe to output.
    """
    vader = SentimentIntensityAnalyzer()

    title_sentiment_warriors = defaultdict(list)
    article_tuples = []

    for article in file_title:
        for para in title_text_dict[article]:
            if (team_name in para or team_city in para):
                title_sentiment_warriors[article].append(vader.polarity_scores(para)['compound'])
        if len(title_sentiment_warriors[article]) > 0:
            article_tuples.append((article, np.sum(title_sentiment_warriors[article]),
                                   len(title_sentiment_warriors[article]),
                                   title_date_dict[article]))
        else:
            article_tuples.append((article, 0, 0, title_date_dict[article]))

    sentiment_track = pd.DataFrame(article_tuples,columns = ['Title','Total Sentiment','Mentions','Date']).sort_values('Date')

    sentiment_track['Cumulative Sentiment'] = sentiment_track['Total Sentiment'].cumsum()
    sentiment_track['Cumulative Mentions'] = sentiment_track['Mentions'].cumsum()

    return sentiment_track


def plotly_plotting(sentiment_track, gsw_results, gsw_results_postseason=None):
    """
    Take sentiment and two results DFs and return plotly figure to plot
    """
    trace0 = go.Scatter(
        x=gsw_results.Date,
        y=gsw_results.net_wins,
        mode='lines+markers',
        name='Net Wins (Regular Season)',
        text=gsw_results.text,
        hoverinfo='text'
    )

    trace1 = go.Scatter(
        x=sentiment_track.Date,
        y=sentiment_track['Cumulative Sentiment'],
        mode='lines',
        name='Cumulative Sentiment'
    )



    trace3 = go.Bar(
        x=sentiment_track.Date,
        y=sentiment_track['Mentions'],
        name='Daily Mentions'
    )

    layout = dict(title='Comparison of cumulative sentiment against Record',
                  xaxis=dict(title='Date')
                  )

    if gsw_results_postseason is not None:
        trace2 = go.Scatter(
            x=gsw_results_postseason.Date,
            y=gsw_results_postseason.net_wins,
            mode='lines+markers',
            name='Net Wins (Postseason)',
            text=gsw_results_postseason.text,
            hoverinfo='text'
        )

        return dict(data=[trace0, trace2, trace1, trace3], layout=layout)

    else:
        return dict(data=[trace0, trace1, trace3], layout=layout)



