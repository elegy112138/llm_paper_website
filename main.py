# app.py
from flask import Flask, request, jsonify, send_from_directory,Response,stream_with_context
from generate_suject import PaperSubjectGenerator
from follow import paper_md
from login import  UserAuthenticator
from  thread import start_background_task
paper_md=paper_md()
paper_subject=PaperSubjectGenerator()

app = Flask(__name__)



@app.route('/api/login', methods=['POST'])
def login():
    user_login = UserAuthenticator("user_tabel")
    data = request.json
    phonenumber, password = data.get("phonenumber"), data.get("password")
    response, status = user_login.check_login(phonenumber, password)
    return jsonify(response), status

@app.route('/api/content', methods=['POST'])
def content():
    data = request.json
    generate = start_background_task(data, 'catalog')
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@app.route('/api/follow', methods=['POST'])
def follow():
    data = request.json
    generate = start_background_task(data, 'follow')
    return Response(stream_with_context(generate()), mimetype='text/event-stream')


@app.route('/api/typo', methods=['POST'])
def typo():
    data = request.json
    response, status = paper_md.check_typo(data)
    return jsonify(response), status

@app.route('/api/subject', methods=['POST'])
def subject():
    data = request.json
    response, status = paper_subject.generate_subject(data)
    return jsonify(response), status

@app.route('/essaywriter-head.svg')
def serve_svg():
    return send_from_directory('static', 'essaywriter-head.svg')



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

