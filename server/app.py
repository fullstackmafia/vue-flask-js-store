from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

COURSES = [
    {
         'id': uuid.uuid4().hex,
        'title': 'Effective JavaScript: 68 Specific Ways to Harness the Power of JavaScript ',
        'author': 'David Herman',
        'paperback': True,
        'price': '46.99'
    },
    {
         'id': uuid.uuid4().hex,
        'title': 'JavaScript: The Good Parts',
        'author': 'Douglas Crockford',
        'paperback': False,
        'price': '29.23'
    },
    {
         'id': uuid.uuid4().hex,
        'title': 'Eloquent JavaScript: A Modern Introduction to Programming',
        'author': 'Marijn Haverbeke',
        'paperback': True,
        'price': '26.23'
    }
]

@app.route('/courses', methods=['GET', 'POST'])
def all_courses():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        COURSES.append({
             'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'paperback': post_data.get('paperback'),
            'price': post_data.get('price')
        })
        response_object['message'] = 'Course added!'
    else:
        response_object['courses'] = COURSES
    return jsonify(response_object)

@app.route('/courses/<course_id>', methods=['GET', 'PUT', 'DELETE'])
def single_course(course_id):
    response_object = {'status': 'success'}
    if request.method == 'GET':
        return_course = ''
        for course in COURSES:
            if course['id'] == course_id:
                return_course = course
        response_object['course'] = return_course
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_course(course_id)
        COURSES.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'paperback': post_data.get('paperback'),
            'price': post_data.get('price')
        })
        response_object['message'] = 'Course updated!'
    if request.method == 'DELETE':
        remove_course(course_id)
        response_object['message'] = 'Course removed!'
    return jsonify(response_object)

def remove_course(course_id):
    for course in COURSES:
        if course['id'] == course_id:
            COURSES.remove(course)
            return True
    return False

if __name__ == '__main__':
    app.run()