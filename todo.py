from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

client = MongoClient('mongodb://mongo:27017/')
db = client.todo_db
todos = db.todos

@app.route('/') 
def index():
    all_todos = todos.find()
    return render_template('index.html', todos=all_todos)

@app.route('/add', methods=['POST'])
def add_todo():
    new_todo = request.form.get('todo')
    todo_id = ObjectId()
    todos.insert_one({'_id': todo_id, 'text': new_todo})
    return ''

@app.route('/delete/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todos.delete_one({'_id': ObjectId(todo_id)})
    return ''

@app.route('/list', methods=['GET'])
def list():
    res = todos.find()
    result= []
    for e in res:
        result.append({'id': str(e['_id']), 'text': e['text']})
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)