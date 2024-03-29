from sklearn.feature_extraction.text import TfidfVectorizer
from itertools import combinations
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import sqlite3
import os.path


def genre_recommendations(movie_title, k=5):
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
    movie_row = cosine_sim_df.loc[movie_title]
    similar_movies = movie_row.sort_values(ascending=False)[1:k + 1].index.tolist()
    return similar_movies


def average_rating(rating_list):
    if not rating_list:
        return 0

    return round(sum(rating_list) / len(rating_list))
