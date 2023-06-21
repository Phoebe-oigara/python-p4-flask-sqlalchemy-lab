#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()
    
    if animal:
        response_body = f''

        response_body += f'<ul>ID: {animal.id}</ul>'
        response_body += f'<ul>Name: {animal.name}</ul>'
        response_body += f'<ul>Species: {animal.species}</ul>'
        response_body += f'<ul>Zookeeper: {animal.zookeeper.name}</ul>'
        response_body += f'<ul>Enclosure: {animal.enclosure.environment}</ul>'

    
        response = make_response(response_body, 200)
    else:
        response_body = '<h1>404 Animal not found</h1>'
        response = make_response(response_body, 404)
    
    return response


@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.filter(Zookeeper.id == id).first()
    if zookeeper:
        response_body = f''

        response_body += f'ID: {zookeeper.id}</ul>'
        response_body += f'<ul>Name: {zookeeper.name}</ul>'
        response_body += f'<ul>Birthday: {zookeeper.birthday}</ul>'
        response_body += f'<ul>Animals:</ul>'
            
        response_body += '<ul>'

        for animal in zookeeper.animals:
            response_body += f'<ul>{animal.name} - {animal.species}</ul>'
        response_body += '</ul>'
        response = make_response(response_body, 200)
    else:
        response_body = '<h1>404 Zookeeper not found</h1>'
        response = make_response(response_body, 404)
    
    return response

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.filter(Enclosure.id == id).first()
    if enclosure:
        response_body = f''

        response_body += f'<ul>ID: {enclosure.id}</ul>'
        response_body += f'<ul>Environment: {enclosure.environment}</ul>'
        response_body += f'<ul>Open to Visitors: {enclosure.open_to_visitors}</ul>'
        response_body += f'<ul>Animals:</ul>'
            
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
