from flask import Flask, jsonify, abort, make_response, request, url_for

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': 'Test',
        'done': False
    },
    {
        'id': 2,
        'title': 'Test Two',
        'done': False
    },
]


# Function that creates URI to identify our tasks

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_tasks', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


# curl -i -H "Content-Type: application/json" -X GET \
# http://127.0.0.1:5000/test/api/v1.0/tasks

@app.route('/test/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': [make_public_task(task) for task in tasks]})


# curl -i -H "Content-Type: application/json" -X GET \
# http://127.0.0.1:5000/test/api/v1.0/tasks/{taskId}

@app.route('/test/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_tasks_by_id(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


# curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Test Three"}' \
# http://127.0.0.1:5000/test/api/v1.0/tasks

@app.route('/test/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(404)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'done': False,
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


# curl -i -H "Content-Type: application/json" -X PUT -d '{"done":true}' \
# http://127.0.0.1:5000/test/api/v1.0/tasks/{taskId}

@app.route('/test/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})


# curl -i -H "Content-Type: application/json" -X DELETE \
# http://127.0.0.1:5000/test/api/v1.0/tasks/{taskId}

@app.route('/test/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': str(error)}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': str(error)}), 400)

if __name__ == '__main__':
    app.run(debug=True)
