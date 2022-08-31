from flask import Flask, json, request
# from recommender import top_user, top_resources, write_dataset
import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
import json
import scipy as sp
from sklearn.metrics.pairwise import cosine_similarity
import os

api = Flask(__name__)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

plt.style.use('ggplot')
pd.set_option('display.max_columns', 6)

file_dir_datasets_base = ROOT_DIR + '/data/datasets/'
file_dir_dynamics_datasets = ROOT_DIR + '/datasets/'

resources_ = pd.read_csv(file_dir_datasets_base + 'resources.csv')

def top_resources(user, name, learningStyle, lesson):

    ratings_ = pd.read_csv(file_dir_dynamics_datasets + name + '.csv')

    rated_resources = ratings_.merge(resources_, left_on='resourceId', right_on='resourceId')[['userId', 'resourceId', 'title', 'rating', 'learningStyle', 'structure']]

    results = rated_resources[(rated_resources['userId'] == user) & (rated_resources['learningStyle'] == learningStyle) & (rated_resources['title'].str.contains(lesson))]
    
    return results.to_json(orient='records')

def top_user(user, name):
    if(os.path.exists(file_dir_dynamics_datasets + name +  '.csv') == False):
        create_dataset(name)

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
        with open(file_dir_dynamics_datasets + data['name'] +  '.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(body)
            file.close()
    else:
        create_dataset(data['name'])

    return json.dumps("done")

def create_dataset(name):
    df = pd.read_csv(file_dir_datasets_base + '/ratings.csv')
    df.to_csv(file_dir_dynamics_datasets + name + '.csv', index=False)

    return json.dumps("done")

@api.route("/") 
def hello(): 
    return "Hello, I love Digital Ocean!"

@api.route('/api/recommender/user', methods=['GET'])
def recommender_user():
    id = int(request.args['id'])
    if id > 20: 
        id = 20
    name = request.args['name']
    return top_user(id, name)

@api.route('/api/recommender/resources', methods=['GET'])
def recommender_resources():
    id = int(request.args['id'])
    name = request.args['name']
    learningStyle = int(request.args['learningStyle'])
    lesson = request.args['lesson']
    return top_resources(id, name, learningStyle, lesson)

@api.route('/api/recommender/dataset/update', methods=['POST'])
def override_dataset():
    data = json.loads(request.data)
    return write_dataset(data)

if __name__ == '__main__':
    api.run(debug=True)
    