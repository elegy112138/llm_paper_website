# app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO
from flask_socketio import disconnect
from src.subject.generate_subject import subject_response
from src.catalog.generate_catalog import catalog_output
from generate_suject import handle_respose, dispaly_history, clear_history
from src.save.save_acticle import *
from src.follow.follow import follow_output, typo_output, polish_output
from login import UserAuthenticator

app = Flask(__name__)
# 创建 SocketIO 实例
socketio = SocketIO()
# 将 SocketIO 实例与 Flask 应用关联，并设置跨域请求的来源
socketio.init_app(app, cors_allowed_origins='*')


@app.route('/api/login', methods=['POST'])
def login():
    user_login = UserAuthenticator("user_tabel")
    data = request.json
    phonenumber, password = data.get("phonenumber"), data.get("password")
    response, status = user_login.check_login(phonenumber, password)
    return jsonify(response), status

@app.route('/api/subject', methods=['POST'])
def subject():
    data = request.json
    response, status=subject_response(data)
    return jsonify(response), status

@app.route('/api/content', methods=['POST'])
def content():
    data = request.json
    response, status = catalog_output(data)
    return jsonify(response), status

@app.route('/api/save', methods=['POST'])
def save():
    data = request.json
    response, status = save_article(data)
    return jsonify(response), status

@app.route('/api/article', methods=['GET'])
def article():
    data = request.args
    response, status = display_article(data)
    return jsonify(response), status

@app.route('/api/articleContent', methods=['GET'])
def article_content():
    data = request.args
    response, status = display_article_content(data)
    return jsonify(response), status

@app.route('/api/Delarticle', methods=['GET'])
def delarticle():
    data = request.args
    response, status = delete_article(data)
    return jsonify(response), status

@app.route('/api/Upatearticle', methods=['POST'])
def updatearticle():
    data = request.json
    response, status = update_article(data)
    return jsonify(response), status




'''生成后续'''

# 处理 WebSocket 连接事件
@socketio.on('connect', namespace='/follow')
def connected_msg():
    # 打印提示信息
    print('client connected.')


# 处理 WebSocket 断开连接事件
@socketio.on('disconnect', namespace='/follow')
def disconnect_msg():
    disconnect(request.sid, namespace='/follow')
    # 打印提示信息
    print('client disconnected.')


# 处理来自客户端的特定事件（my_event）
@socketio.on('my_event', namespace='/follow')
def test_message(message):
    if(message['type']=='typo'):
        typo_output(message['data'])
    elif(message['type']=='follow'):
        follow_output(message['data'])
    elif(message['type']=='polish'):
        polish_output(message['data'])

    # 断开连接

'''生成后续'''


'''静态资源'''


@app.route('/essaywriter-head.svg')
def serve_svg():
    return send_from_directory('static', 'essaywriter-head.svg')


'''静态资源'''

'''对话系统选选题'''


# 处理 WebSocket 连接事件
@socketio.on('connect', namespace='/subject')
def connected_msg():
    # 打印提示信息
    print('client connected.')


# 处理 WebSocket 断开连接事件
@socketio.on('disconnect', namespace='/subject')
def disconnect_msg():
    # 打印提示信息
    print('client disconnected.')


# 处理来自客户端的特定事件（my_event）
@socketio.on('my_event', namespace='/subject')
def test_message(message):
    handle_respose(message['data'])
    # 断开连接
    disconnect(request.sid, namespace='/subject')


@app.route('/api/clear_history', methods=['GET'])
def clear():
    data = request.args
    response, status = clear_history(data)
    return jsonify(response), status


@app.route('/api/dispaly_history', methods=['GET'])
def dispaly():
    data = request.args
    response, status = dispaly_history(data)
    return jsonify(response), status


'''对话系统选选题'''

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True,allow_unsafe_werkzeug=True)
