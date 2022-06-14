from flask import Flask, json, request
from recommender import top_user, top_resources

api = Flask(__name__)

@api.route('/api/recommender/user', methods=['POST'])
def recommender_user():
    data = json.loads(request.data)
    return top_user(data)

@api.route('/api/recommender/resources', methods=['POST'])
def recommender_resources():
    data = json.loads(request.data)
    return top_resources(data)

@api.route('/api/recommender/dataset/update', methods=['POST'])
def write_dataset():
    data = json.loads(request.data)
    return write_dataset(data)

if __name__ == '__main__':
    api.run(debug=True)
    