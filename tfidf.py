from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from itertools import combinations
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import sqlite3
import os.path

def genre_recommendations(movie_title, k=5):
    """
    Recommends movies based on a similarity dataframe

    Parameters
    ----------
    i : str
        Movie (index of the similarity dataframe)
    M : pd.DataFrame
        Similarity dataframe, symmetric, with movies as indices and columns
    items : pd.DataFrame
        Contains both the title and some other features used to define similarity
    k : int
        Amount of recommendations to return
        :param k:
        :param movie_data:
        :param similarity_matrix:
        :param movie_title:

    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_dir = (BASE_DIR + '\\db.sqlite3')
    cnx = sqlite3.connect(db_dir)
    movies = pd.read_sql_query("SELECT * FROM movie", cnx)

    tf = TfidfVectorizer(analyzer=lambda s: (c for i in range(1, 4)
                                             for c in combinations(s.split('|'), r=i)))
    tfidf_matrix = tf.fit_transform(movies['genres'])
    cosine_sim = cosine_similarity(tfidf_matrix)
    cosine_sim_df = pd.DataFrame(cosine_sim, index=movies['title'], columns=movies['title'])
    cosine_sim_df.sample(5, axis=1).round(2)
    movie_row = similarity_matrix.loc[movie_title]
    similar_movies = movie_row.sort_values(ascending=False)[1:k + 1].index.tolist()
    return similar_movies

print(genre_recommendations('Saving Private Ryan (1998)'))