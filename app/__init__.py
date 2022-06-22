from flask import Flask, json, request
from recommender import top_user, top_resources, write_dataset

api = Flask(__name__)

@api.route('/api/recommender/user', methods=['GET'])
def recommender_user():
    id = int(request.args['id'])
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
    