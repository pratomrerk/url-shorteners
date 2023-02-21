import os
from flask import Flask, redirect, jsonify, request, abort
from flask_cors import CORS
from redis import Redis
import datetime as dt
import string
import random
import json
from urllib.parse import urlparse

# pratomrerk
# Update 21/02/2023

app = Flask(__name__)
CORS(app)
redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = os.environ.get('REDIS_PORT', 6379)
redis_db = os.environ.get('REDIS_DB', 8)
redis_password = os.environ.get('REDIS_PASSWORD', '')
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:7788')

def random_string(length):
    all_chars = string.digits + string.ascii_letters + string.ascii_uppercase
    return ''.join(random.choice(all_chars) for m in range(length))

def connect_redis():
    return Redis(host=redis_host, port=redis_port, db=redis_db, password=redis_password) 

@app.route('/', methods=['GET'])
def index():
    return abort(404)

@app.route('/<url_key>', methods=['GET'])
def get(url_key):
    r = connect_redis()
    v = r.get(url_key)
    if v is not None:
        v = json.loads(v)
        url = v['url']
        v['count'] += 1
        r.set(url_key, json.dumps(v))
        r.close()
        return redirect(url)
    else:
        return jsonify({
            'error': 'Not found or expired'
        }), 404


@app.route('/new-url', methods=['GET'])
def new_url():

    url = request.args.get('url', None)
    expire = request.args.get('expire', 60*60*24*30) # 30 days by default
    if url is None:
        return jsonify({
            'error': 'URL is required'
        }), 400

    # check url is valid
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            return jsonify({
                'error': 'Invalid URL'
            }), 400

    except ValueError:
        return jsonify({
            'error': 'Invalid URL'
        }), 400

    if expire is not None:
        try:
            expire = int(expire)
        except ValueError:
            return jsonify({
                'error': 'Expire must be integer'
            }), 400
    
    r = connect_redis()

    while True:
        url_key = random_string(8)
        if not r.get(url_key):
            break
    
    expired = int(dt.datetime.now().timestamp()) + expire
    data = {
        'short_url': f'{BASE_URL}/{url_key}',
        'url': url,
        'count': 0,
        'expire': expired
    }
    #print(data)
    r.set(url_key, json.dumps(data), ex=expire)

    r.close()
    data['check'] = f'{BASE_URL}/check?url-key={url_key}'
    return jsonify(data)

@app.route('/check', methods=['GET'])
def check_count():
    url_key = request.args.get('url-key', None)
    if url_key is None:
        return jsonify({
            'error': 'url-key is required'
        }), 400

    r = connect_redis()
    v = r.get(url_key)
    r.close()
    if v:
        data = json.loads(v)
        return jsonify(data)
    else:
        return jsonify({
            'error': 'Not found or expired'
        }), 404

if __name__ == '__main__':
    app.run(port=7788, debug=True)