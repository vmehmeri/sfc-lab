#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, send_from_directory #url_for
from nsd_parser import NsdParser, clean_up
import codecs
import os

app = Flask(__name__, static_url_path="")
app.config['UPLOAD_FOLDER'] = 'yaml'
app.config['DOWNLOAD_FOLDER'] = 'result'

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


#nsd = {   }
#vnfds = [{ 'id' : 0 }]

#@app.route('/tosca-parser/api/nsd', methods=['GET'])
#def get_nsd():
#    return jsonify({'nsd': nsd})

#@app.route('/tosca-parser/api/vnfd', methods=['GET'])
#def get_vnfds():
#    return jsonify({'vnfds': vnfds})

#@app.route('/tosca-parser/api/vnfd/<int:vnfd_id>', methods=['GET'])
#def get_vnfd(vnfd_id):
#    vnfd = filter(lambda t: t['id'] == vnfd_id, vnfds)
#    if len(vnfd) == 0:
#        abort(404)
#    return jsonify({'vnfd': vnfd[0]})


@app.route('/tosca-parser/api/vnfd', methods=['POST'])
def create_vnfd():
    file = request.files['file']

    if not file:
        print("Something wrong with the file")
        abort(400)

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    return jsonify({'result': 'OK'})

@app.route('/tosca-parser/api/nsd', methods=['POST'])
def create_nsd():
    file = request.files['file']

    if not file:
        print("Something wrong with the file")
        abort(400)

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    return jsonify({'result': 'OK'})

#@app.route('/tosca-parser/api/vnfd/<int:vnfd_id>', methods=['PUT'])
#def update_vnfd(vnfd_id):
#    vnfd = filter(lambda t: t['id'] == vnfd_id, vnfds)
#    if len(vnfd) == 0:
#        abort(404)
#    if not request.json:
#        abort(400)
#    if 'descriptor' in request.json and type(request.json['description']) is not unicode:
#        abort(400)
#
#    vnfd[0]['descriptor'] = request.json.get('descriptor', vnfd[0]['descriptor'])
#    return jsonify({'vnfd': vnfd[0]})

#@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
#def delete_task(vnfd_id):
#    vnfd = filter(lambda t: t['id'] == vnfd_id, vnfds)
#    if len(vnfd) == 0:
#        abort(404)
#    vnfds.remove(vnfd[0])
#    return jsonify({'result': True})


@app.route('/tosca-parser/api/operations/parse', methods=['POST'])
def parse():
    #if not request.json:
    #    abort(400)

    nsd_parser = NsdParser()
    tree = nsd_parser.parse_all()
    print(tree)
    return jsonify({'result': 'OK'}), 201

@app.route('/tosca-parser/api/results/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    uploads = os.path.join(app.config['DOWNLOAD_FOLDER'])
    try:
        return send_from_directory(directory=uploads, filename=filename)
    finally:
        clean_up()

if __name__ == '__main__':
    app.run(debug=True)