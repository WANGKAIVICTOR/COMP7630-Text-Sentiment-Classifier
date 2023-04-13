import pandas as pd
from bs4 import BeautifulSoup
import numpy as np

# remove html
def remove_html(data):
    soup = BeautifulSoup(data, 'html.parser')
    return soup.get_text()

# combination of all operations
def process_data(df,col_name):
    df = df.astype(str)
    df[col_name] = df[col_name].apply(remove_html) # remove html
    df[col_name].replace('',np.nan,inplace=True) # replace the empty content to nan
    df.dropna(axis=0, how='any') # remove row with nan value
    df.replace(['\ +', '"'], [' ',' '], regex=True , inplace=True) # spaces to single space, Remove quotation marks
    return df

def info(df):
    pass

# print dataframe info
def print_info(df):
    print(df.shape)
    print(df.dtypes)
    print(df.head())

# read csv
games = pd.read_csv("games.csv", header=0)
movies = pd.read_csv("movies.csv", header=0)

# # read and process data
# games = process_data(games,"game_comment")
# movies = process_data(movies,"movie_comment")

print_info(games)
# games = games.astype(str)
# games["game_comment"] = games["game_comment"].apply(remove_html) # remove html
# games['game_comment'].replace('',np.nan,inplace=True) # replace the empty content to nan
# games.dropna(axis=0, how='any') # remove row with nan value
# games.replace(['\ +', '"'], [' ',' '], regex=True , inplace=True) # spaces to single space, Remove quotation marks
games = process_data(games,'game_comment')

print_info(games)

print(games.iloc[211])
print(games.iloc[210])
print(games.iloc[209])

