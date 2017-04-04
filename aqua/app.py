from datetime import datetime

from flask import Flask, jsonify, request, abort

app = Flask(__name__)


class HTTPDictionary:
    def __init__(self):
        self._dict = {}

    def get(self, key):
        value = self._dict.get(key)
        if not value:
            abort(404)
        return value, 200

    def post(self, key, value):
        if not key or not value:
            abort(400)

        if key in self._dict:
            abort(409)

        self._dict[key] = value

        return '', 200

    def put(self, key, value):
        if not key or not value:
            abort(400)

        if not self._dict.get(key):
            abort(404)

        self._dict[key] = value

        return '', 200

    def delete(self, key):
        value = self._dict.get(key)
        if not value:
            result = None
        else:
            result = value
            del self._dict[key]

        return jsonify({'result': result, 'time': datetime.now().strftime("%Y-%m-%d %H:%M")}), 200


GLOBAL_DICTIONARY = HTTPDictionary()


@app.route('/dictionary/<key>', methods=['GET', 'PUT', 'DELETE'])
def dictionary(key):
    if request.method == 'GET':
        return GLOBAL_DICTIONARY.get(key)
    elif request.method == 'PUT':
        data = request.get_json()
        value = data.get('value')
        return GLOBAL_DICTIONARY.put(key, value)
    else:
        return GLOBAL_DICTIONARY.delete(key)

@app.route('/dictionary', methods=['POST'])
def dictionaries():
    data = request.get_json()
    key = data.get('key')
    value = data.get('value')
    return GLOBAL_DICTIONARY.post(key, value)


