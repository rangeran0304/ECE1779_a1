import base64
from flask import render_template, url_for, request
from app import memcache
from flask import json
from app import webapp


class Base64Encoder(json.JSONEncoder):
    # pylint: disable=method-hidden
    def default(self, o):
        if isinstance(o, bytes):
            return base64.b64encode(o).decode()
        return json.JSONEncoder.default(self, o)

@webapp.route('/')
def main():
    return render_template("main.html")

@webapp.route('/get',methods=['POST'])
def GET():
    key = request.form.get('key')
    if memcache.get(key):
        file = memcache.get(key)
        decoded_file = base64.b64decode(file)
        response = webapp.response_class(
            response=
            json.dumps(decoded_file,cls=Base64Encoder),
            status=200,
            mimetype='application/json'
        )
    else:
        response = webapp.response_class(
            response=json.dumps("Unknown key"),
            status=400,
            mimetype='application/json'
        )

    return response

@webapp.route('/put',methods=['POST'])
def PUT():
    key = request.form.get('key')
    file = request.files['file']
    file_64_encode = base64.b64encode(file.read())
    #put a value, if already exists, overwrite it
    if memcache.get(key):
        memcache[key] = file_64_encode
        response = webapp.response_class(
             response=json.dumps("overwrite the previous value"),
             status=200,
             mimetype='application/json'
    )
    else:
        memcache[key] = file_64_encode
        response = webapp.response_class(
            response=json.dumps("new cache file"),
            status=200,
            mimetype='application/json'
        )

    return response

@webapp.route('/delete',methods=['POST'])
def invalidateKey():
    key = request.form.get('key')
    if memcache.get(key):
        memcache.pop(key)
        response = webapp.response_class(
            response=
            json.dumps("successfully deleted"),
            status=200,
            mimetype='application/json'
        )
    else:
        response = webapp.response_class(
            response=json.dumps("Unknown key"),
            status=400,
            mimetype='application/json'
        )

    return response
@webapp.route('/clear',methods=['POST'])
def CLEAR():
    memcache.clear()
    response = webapp.response_class(
        response=
        json.dumps("successfully cleared"),
        status=200,
        mimetype='application/json'
    )
    return response