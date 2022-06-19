from operator import contains
from definitions import ROOT_DIR
import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
import json
import scipy as sp
from sklearn.metrics.pairwise import cosine_similarity
import os

plt.style.use('ggplot')
pd.set_option('display.max_columns', 5)

file_dir_datasets_base = ROOT_DIR + '/data/datasets/'
file_dir_dynamics_datasets = ROOT_DIR + '/datasets/'

resources_ = pd.read_csv(file_dir_datasets_base + 'resources.csv')

def top_resources(user, name, learningStyle, lesson):

    title = 'R1_E1_L1_Act'

    ratings_ = pd.read_csv(file_dir_dynamics_datasets + name + '.csv')

    rated_resources = ratings_.merge(resources_, left_on='resourceId', right_on='resourceId')[['userId', 'resourceId', 'title', 'rating', 'learningStyle']]

    rr = rated_resources[rated_resources['learningStyle'] == learningStyle & rated_resources['title'].str.contains(lesson)]
    
    ratings_pivot = rr.pivot_table(index='userId', columns='title', values='rating', aggfunc=np.mean)
    ratings_pivot.fillna(0, inplace=True)

    sparse_ratings = sp.sparse.csr_matrix(ratings_pivot.values)
    item_similarity = cosine_similarity(sparse_ratings.T)

    item_similarity_df = pd.DataFrame(item_similarity, index=ratings_pivot.columns, columns=ratings_pivot.columns)

    count = 0
    results = []
    print('Similar shows to {} include'.format(title))
    similar_indexes = item_similarity_df.sort_values(by=title, ascending=False).index[1:11]
    similar_values =  item_similarity_df.sort_values(by=title, ascending=False).loc[:, title].tolist()[1:11]
    for resource, sim in zip(similar_indexes, similar_values):
        print('No: {}: {} Similarity {}'.format(count, resource, sim))
        count += 1
        results.append(resource)
    return json.dumps(results)

def top_user(user, name):
    ratings_ = pd.read_csv(file_dir_dynamics_datasets + name + '.csv')

    rated_resources = ratings_.merge(resources_, left_on='resourceId', right_on='resourceId')[['userId', 'resourceId', 'title', 'rating']]
    
    ratings_pivot = rated_resources.pivot_table(index='userId', columns='title', values='rating', aggfunc=np.mean)
    ratings_pivot.fillna(0, inplace=True)
    
    sparse_ratings = sp.sparse.csr_matrix(ratings_pivot.values)

    user_similarity = cosine_similarity(sparse_ratings)
    user_similarity_df = pd.DataFrame(user_similarity, index=ratings_pivot.index, columns=ratings_pivot.index)

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

def write_dataset(data):
    body = data['body']

    if(os.path.exists(file_dir_dynamics_datasets + data['name'] +  '.csv')):
        with open(file_dir_dynamics_datasets + data['name'] +  '.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(body)
    else:
        create_dataset(data)

    return json.dumps("done")

def create_dataset(data):
    df = pd.read_csv(ROOT_DIR + 'ratings.csv')
    df.to_csv(file_dir_dynamics_datasets + data['name'] + '.csv')

    return json.dumps("done")
