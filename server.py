from flask import Flask, json, request
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

import scipy as sp
from sklearn.metrics.pairwise import cosine_similarity

api = Flask(__name__)


plt.style.use('ggplot')
pd.set_option('display.max_columns', 2)

file_dir = 'C:/Users/heide/OneDrive/Desktop/recommenders/IMB-dataset/'

ratings_ = pd.read_csv(file_dir + 'ratings.csv')
movies_ = pd.read_csv(file_dir + 'movies.csv')
rated_movies = ratings_.merge(movies_, left_on='movieId', right_on='movieId')[['userId', 'movieId', 'title', 'rating']]

ratings_pivot = rated_movies.pivot_table(index='userId', columns='title', values='rating', aggfunc=np.mean)
ratings_pivot.fillna(0, inplace=True)

sparse_ratings = sp.sparse.csr_matrix(ratings_pivot.values)

user_similarity = cosine_similarity(sparse_ratings)
item_similarity = cosine_similarity(sparse_ratings.T)

user_similarity_df = pd.DataFrame(user_similarity, index=ratings_pivot.index, columns=ratings_pivot.index)
item_similarity_df = pd.DataFrame(item_similarity, index=ratings_pivot.columns, columns=ratings_pivot.columns)

@api.route('/api/top-resources', methods=['POST'])
def top_movies():
    title = json.loads(request.data)
    count = 0
    results = []
    print('Similar shows to {} include'.format(title))
    for movie in item_similarity_df.sort_values(by=title, ascending=False).index[1:11]:
        print('No: {}: {}'.format(count, movie))
        count += 1
        results.append(title)
    return json.dumps(results)

@api.route('/api/top-users', methods=['POST'])
def top_user():
    user = json.loads(request.data)
    count = 0
    print('Similar show to {} include'.format(user))
    similar_indexes = user_similarity_df.sort_values(by=user, ascending=False).index[1:11]
    similar_values =  user_similarity_df.sort_values(by=user, ascending=False).loc[:, user].tolist()[1:11]
    results = []
    for user, sim in zip(similar_indexes, similar_values):
        print('No: {}: {} Similarity {}'.format(count, user, sim))
        count += 1
        results.append(user)
    return json.dumps(results)
   

if __name__ == '__main__':
    api.run(debug=True)