#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.get(id)
    
    if animal:
        response_body = f'''
            <ul>
                <li>ID: {animal.id}</li>
                <li>Name: {animal.name}</li>
                <li>Species: {animal.species}</li>
                <li>Zookeeper: {animal.zookeeper.name}</li>
                <li>Enclosure: {animal.enclosure.environment}</li>
            </ul>
    
        '''
        response = make_response(response_body, 200)
    else:
        response_body = '<h1>404 Animal not found</h1>'
        response = make_response(response_body, 404)
    
    return response


@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.get(id)
    if zookeeper:
        response_body = f'''
           <ul>
                <li>ID: {zookeeper.id}</li>
                <li>Birthday: {zookeeper.birthday}</li>
                <li>Animals:</li>
            '''
        response_body += '<ul>'
        for animal in zookeeper.animals:
            response_body += f'<li>{animal.name} - {animal.species}</li>'
        response_body += '</ul>'
        response = make_response(response_body, 200)
    else:
        response_body = '<h1>404 Zookeeper not found</h1>'
        response = make_response(response_body, 404)
    
    return response

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.get(id)
    if enclosure:
        response_body = f'''
            <ul>
                <li>ID: {enclosure.id}</li>
                <li>Environment: {enclosure.environment}</li>
                <li>Open to Visitors: {enclosure.open_to_visitors}</li>
                <li>Animals:</li>
            '''
        response_body += '<ul>'
        for animal in enclosure.animals:
            response_body += f'<li>{animal.name} - {animal.species}</li>'
        response_body += '</ul>'
        response = make_response(response_body, 200)
    else:
        response_body = '<h1>404 Enclosure not found</h1>'
        response = make_response(response_body, 404)
    
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
