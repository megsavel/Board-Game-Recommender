import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import base
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.neighbors import NearestNeighbors
from sklearn.linear_model import RidgeCV, LinearRegression, SGDRegressor, Ridge
from sklearn.decomposition import TruncatedSVD
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

#Opening csvs
rankings = pd.read_csv('rankings_cleaned', sep='\t', lineterminator='\n')
games = pd.read_csv('games', sep='\t', lineterminator='\n')


#Formatting the csvs so column names will appear in a logical fashion
games.columns = ['name', 'image', 'year_published', 'item_number', 'max_players', 'min_players', 'min_playtime', 'num_owned', 'rating_average', 'complete_type']
rankings.drop(rankings.iloc[:, 0:2], inplace = True, axis = 1)

#All boardgames are listed as being from the category "boardgame", removing boardgame as a category type
games['complete_type'] = games['complete_type'].str.replace("'boardgame',|'boardgame'", '')

#Choosing to report games created before 0 AD as NA
games['year_published'] = pd.to_datetime(games['year_published'], format='%Y.0',errors='coerce')

#For simplicitity's sake concerning graphing later on, creating data set of only when games were published
just_dates = games['year_published']

#For simplicitity's sake concerning graphing later on, creating data set of only when games were published after 1960
games_new = games[games['year_published'] > '1960']
games_new2 = games_new['year_published']

#Creating a plot that displays how many games were created in each year.
#Note: there is not a sudden drop-off in games creation, rather that boardgamers are less likely to have brand new
#games that were published in 2019 in their collections just yet.
figure = just_dates.groupby(just_dates.dt.year).count().plot(kind="line")
plt.title('Total games created/published for a given year')
plt.xlabel('Year');

#Zooming in on more recent decades
figure = games_new2.groupby(games_new2.dt.year).count().plot(kind="line")
plt.title('Total games created/published for a given year')
plt.xlabel('Year');

#Popular categories: Creating a dataset that only contains categories of games and a corresponding count of number
#of games
types = games.groupby(games.complete_type).count()
types2 = types['name']
types2 = types2.reset_index()
types2.sort_values("name", inplace=True)
#Wanting just the top 10 most popular categories, while eliminating gamees classified only as "boardgame".
top = types2[28:38]

#Creating bar chart of total number of games in each category
plt.bar(top.complete_type, top.name)
plt.xticks(fontsize=8, rotation=90)
plt.title('Number of Games by Cateogry');

#Creating Recommender
#Wanting to use the feature categories for the recommender. I don't know the categories a priori, so I will use
#the DictVectorizer to help. This transformer takes in a list of dictionaries. Each key in the dictionaries
#gets mapped to a column, and the values for those keys are placed in the appropriate column. Columns for keys
#that are not present in a particular row are filled with zeros.In order to use this, I need to transform the list
#of categories in to a dictionary, with values of one.

class DictEncoder(base.BaseEstimator, base.TransformerMixin):

    def __init__(self, col):
        self.col = col

    def fit(self, X, y=None):
        return self

    def transform(self, X):

        def to_dict(l):
            try:
                return {x: 1 for x in l}
            except TypeError:
                return {}

        return X[self.col].apply(to_dict)

#A pipeline helps me chain transformers together. Since the pipeline doesn't end in an estimator, it acts as a
#transformer instead.

cat_pipe = Pipeline([('encoder', DictEncoder('complete_type')),
                     ('vectorizer', DictVectorizer())])
features = cat_pipe.fit_transform(games)
features

#Nearest Neighbors
#Now that I have a way to describe a game, I want to be able to find other games that are nearby in feature space.
#This is the nearest neighbors problem, and Scikit Learn provides a class to handle this.

nn = NearestNeighbors(n_neighbors=40).fit(features)

#I will be finding recommendations for someone who likes a family game, "Sushi Go", and someone who likes a family
#game that involves a little strategy "Catan". I am confirming that they are row 546 and row 200 in my dataset.
games.iloc[[546, 200]]

#Starting with Catan first

dists, indices = nn.kneighbors(features[200])
CatanRecommendations = games.iloc[indices[0]]

#My recommender suggests 40 games that are similar to Catan (they are all stategygames that are light enough to also
#be designated as family games). I have sorted those games by highest average rating of users. If I knew that the
#boardgamer had particular tastes, I could also sort by playtime or number of players.
CatanRecommendations.sort_values('rating_average', ascending=False )

#Now for Sushi Go!
dists, indices = nn.kneighbors(features[546])
SushiGoRecommendations = games.iloc[indices[0]]
#My recommender suggests 40 games that are similar to Sushi Go! (they are similar to those recommended for Catan, as
#one would expect, but noticeably lighter). I have sorted those games by highest average rating of users. If I knew
#that the boardgamer had particular tastes, I could also sort by playtime or number of players.
SushiGoRecommendations.sort_values('rating_average', ascending=False )