# app.py
from flask import Flask, request, jsonify, send_from_directory,Response,stream_with_context
from flask_socketio import SocketIO, emit
from flask_socketio import disconnect
from test import conversation
from generate_suject import PaperSubjectGenerator
from follow import paper_md
from login import  UserAuthenticator
from  thread import start_background_task
paper_md=paper_md()
paper_subject=PaperSubjectGenerator()

app = Flask(__name__)
# 创建 SocketIO 实例
socketio = SocketIO()
# 将 SocketIO 实例与 Flask 应用关联，并设置跨域请求的来源
socketio.init_app(app, cors_allowed_origins='*')
# 定义一个命名空间
name_space = '/subject'

@app.route('/api/login', methods=['POST'])
def login():
    user_login = UserAuthenticator("user_tabel")
    data = request.json
    phonenumber, password = data.get("phonenumber"), data.get("password")
    response, status = user_login.check_login(phonenumber, password)
    return jsonify(response), status


@app.route('/api/content', methods=['GET'])
def content():
    # data = request.json
    generate = start_background_task(request.args, 'catalog')
    response = Response(stream_with_context(generate()), mimetype='text/event-stream')

    # 设置 CORS 头，允许所有来源访问
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response


@app.route('/api/follow', methods=['GET'])
def follow():
    generate = start_background_task(request.args, 'follow')
    response = Response(stream_with_context(generate()), mimetype='text/event-stream')

    # 设置 CORS 头，允许所有来源访问
    response.headers['Access-Control-Allow-Origin'] = '*'

    return response


@app.route('/api/typo', methods=['POST'])
def typo():
    data = request.json
    response, status = paper_md.check_typo(data)
    return jsonify(response), status


@app.route('/essaywriter-head.svg')
def serve_svg():
    return send_from_directory('static', 'essaywriter-head.svg')


@app.route('/api/subject')
def subject():
    # response, status = paper_subject.generate_subject(data)
    # 定义要广播的事件名称
    event_name = 'echo'
    # 定义要广播的数据
    broadcasted_data = {'data': "test message!"}
    # 使用 SocketIO 实例发送消息，但不进行广播（只发送给发起请求的客户端）
    socketio.emit(event_name, broadcasted_data, broadcast=False, namespace=name_space)
    return 'done!'

# 处理 WebSocket 连接事件
@socketio.on('connect', namespace=name_space)
def connected_msg():
    # 打印提示信息
    print('client connected.')

# 处理 WebSocket 断开连接事件
@socketio.on('disconnect', namespace=name_space)
def disconnect_msg():
    # 打印提示信息
    print('client disconnected.')

# 处理来自客户端的特定事件（my_event）
@socketio.on('my_event', namespace=name_space)
def test_message(message):
    conversation(message['data'])
    disconnect(sid=request.sid)



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

