#!flask/bin/python
from os.path import abspath, dirname, join

from flask import flash, Flask, Markup, redirect, render_template, url_for, jsonify, abort, make_response, request 
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import fields
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from sqlalchemy import desc
from sqlalchemy.sql import exists

_cwd = dirname(abspath(__file__))

SECRET_KEY = 'insecure-secret-key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(_cwd, 'Items.db')
SQLALCHEMY_ECHO = True
WTF_CSRF_SECRET_KEY = 'this-should-be-more-random'


app = Flask(__name__)
app.config.from_object(__name__)

db = SQLAlchemy(app)

class Item(db.Model):
    __tablename__ = 'Post_Item'

    item_Id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String)
    address = db.Column(db.String)
    application_Type = db.Column(db.String)

    def __repr__(self):
        return '<Item %r - %r>' % (self.item_Id)

@app.route('/BGREST/api/data', methods=['GET'])
def get_all_items():
    return jsonify({'items': items})

@app.route('/BGREST/api/data/<int:item_id>', methods=['GET'])
def get_one_item(item_id):
    query = Item.query.order_by(desc(Item.item_Id)).first()

    highestItem = query.item_Id
    if (highestItem > 0) and (item_id <= highestItem) :
        query = Item.query.filter(Item.item_Id == item_id).first()

        return jsonify({'id': query.item_Id, 'title': query.title, 'address': query.address, 'type': query.application_Type}), 202
    else:
        abort(404)

@app.route('/BGREST/api/data', methods=['POST'])
def create_item():
    if not request.json or not 'title' in request.json:
        abort(400)
    item = Item()
    query = Item.query.order_by(desc(Item.item_Id)).first()

    highestItem = query.item_Id
    item.item_Id = highestItem+1
    item.title = request.json['title']
    if item.title == '':
        abort(400)
    item.address = request.json.get('address', "")
    item.application_Type = request.json.get('type', "")
        
    db.session.add(item)
    db.session.commit()

    return jsonify({'id': item.item_Id}), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'No Title'}), 404)

if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.run(host='0.0.0.0', debug=True)