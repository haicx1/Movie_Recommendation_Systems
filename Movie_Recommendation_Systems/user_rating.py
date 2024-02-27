import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
import seaborn as sns
import sqlite3
import os.path
from sklearn.metrics.pairwise import cosine_similarity
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_dir = (BASE_DIR + '\\db.sqlite3')
cnx = sqlite3.connect(db_dir)
movies = pd.read_sql_query("SELECT * FROM movie", cnx)
ratings = pd.read_csv(r"C:\Users\Admin\Documents\DAP391m\Movie_Recommendation_Systems\ratings.csv", sep='\t', encoding='latin-1', usecols=['user_id', 'movie_id', 'rating'])
user_item_m = ratings.pivot('user_id', 'movie_id', 'rating').fillna(0)
X_user = cosine_similarity(user_item_m)
X_item = cosine_similarity(user_item_m.T)
def movie_recommender(user_item_m, X_user, user, k=20, top_n=10):
    # Get location of the actual movie in the User-Items matrix
    user_ix = user_item_m.index.get_loc(user)
    # Use it to index the User similarity matrix
    user_similarities = X_user[user_ix]
    # obtain the indices of the top k most similar users
    most_similar_users = user_item_m.index[user_similarities.argpartition(-k)[-k:]]
    # Obtain the mean ratings of those users for all movies
    rec_movies = user_item_m.loc[most_similar_users].mean(0).sort_values(ascending=False)
    # Discard already seen movies
    m_seen_movies = user_item_m.loc[user].gt(0)
    seen_movies = m_seen_movies.index[m_seen_movies].tolist()
    rec_movies = rec_movies.drop(seen_movies).head(top_n)
    # return recommendations - top similar users rated movies
    return rec_movies.index.to_frame().reset_index(drop=True).merge(movies)


class CfRec():
    def __init__(self, M, X, items, k=20, top_n=10):
        self.X = X
        self.M = M
        self.k = k
        self.top_n = top_n
        self.items = items

    def recommend_user_based(self, user):
        ix = self.M.index.get_loc(user)
        # Use it to index the User similarity matrix
        u_sim = self.X[ix]
        # obtain the indices of the top k most similar users
        most_similar = self.M.index[u_sim.argpartition(-(self.k + 1))[-(self.k + 1):]]
        # Obtain the mean ratings of those users for all movies
        rec_items = self.M.loc[most_similar].mean(0).sort_values(ascending=False)
        # Discard already seen movies
        # already seen movies
        seen_mask = self.M.loc[user].gt(0)
        seen = seen_mask.index[seen_mask].tolist()
        rec_items = rec_items.drop(seen).head(self.top_n)
        # return recommendations - top similar users rated movies
        return (rec_items.index.to_frame()
                .reset_index(drop=True)
                .merge(self.items))

    def recommend_item_based(self, item):
        liked = self.items.loc[self.items.movie_id.eq(item), 'title'].item()
        print(f"Because you liked {liked}, we'd recommend you to watch:")
        # get index of movie
        ix = self.M.columns.get_loc(item)
        # Use it to index the User similarity matrix
        i_sim = self.X[ix]
        # obtain the indices of the top k most similar users
        most_similar = self.M.columns[i_sim.argpartition(-(self.k + 1))[-(self.k + 1):]]
        return (most_similar.difference([item])
                .to_frame()
                .reset_index(drop=True)
                .merge(self.items)
                .head(self.top_n))
def because_user_liked(user_item_m, movies, ratings, user):
    ix_user_seen = user_item_m.loc[user]>0.
    seen_by_user = user_item_m.columns[ix_user_seen]
    return (seen_by_user.to_frame()
                 .reset_index(drop=True)
                 .merge(movies)
                 .assign(user_id=user)
                 .merge(ratings[ratings.user_id.eq(user)])
                 .sort_values('rating', ascending=False).head(10))

rec = CfRec(user_item_m, X_user, movies)

print(rec.recommend_user_based(12))