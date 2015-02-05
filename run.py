#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request 

app = Flask(__name__)

items = [
    {
        'id': 1,
        'title': u'DN12345',
        'address': u'12 main road', 
        'type': u'dealing'
    },
    {
        'id': 2,
        'title': u'DN56789',
        'address': u'34 high street', 
        'type': u'TP'
    }
]

@app.route('/BGREST/api/data', methods=['GET'])
def get_all_items():
    return jsonify({'items': items})

@app.route('/BGREST/api/data/<int:item_id>', methods=['GET'])
def get_one_item(item_id):
    item = [item for item in items if item['id'] == item_id]
    if len(item) == 0:
        abort(404)
    return jsonify({'item': item[0]})

@app.route('/BGREST/api/data', methods=['POST'])
def create_item():
    if not request.json or not 'title' in request.json:
        abort(400)
    item = {
        'id': items[-1]['id'] + 1,
        'title': request.json['title'],
        'address': request.json.get('address', ""),
        'type': request.json.get('type', "")
    }
    #file_body[items[-1]['id'] + 1] = request.args['file'][0]
    items.append(item)
    return jsonify({'New item created, id': items[-1]['id']}), 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)