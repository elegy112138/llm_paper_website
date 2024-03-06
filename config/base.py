import os
from langchain.callbacks.base import BaseCallbackManager, BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from flask_socketio import emit

class ChatModelWrapper:
    def __init__(self, model_name,stream,response_name='my_event'):
        # 固定的环境变量值
        api_key = "sk-YXXtQVrIHMmEeHT4148a98D03cEf404392E546C482962978"
        api_base = "https://api.rcouyi.com/v1"

        # 设置环境变量
        os.environ["OPENAI_API_KEY"] = api_key
        os.environ["OPENAI_API_BASE"] = api_base
        if(stream):
            # 初始化 ChatOpenAI
            self.chat = ChatOpenAI(
                model_name=model_name,
                streaming=True,
                verbose=True,
                callback_manager=BaseCallbackManager([self.StreamOnlyCallbackHandler(response_name)])
            )
        else:
            self.chat = ChatOpenAI(
                model_name=model_name,
                verbose=True,
            )
    class StreamOnlyCallbackHandler(BaseCallbackHandler):
        def __init__(self, response_name):
            self.response_name = response_name
        def on_llm_new_token(self, token: str, chunk, run_id, parent_run_id=None, **kwargs):
            # 这里可以根据需要进行操作
            if token:
                emit(self.response_name, {'token': token})
            else:
                emit(self.response_name, {'token': 'finished'})
    def read_prompt_file(self, file_path):
        with open('/home/ubuntu/llm_paper/prompt/'+file_path, 'r') as file:
            file_contents = file.read()
        return file_contents
        # 在这里处理文件内容
        # 比如启动聊天模型或其他操作

# 使用示例
# wrapper = ChatModelWrapper("gpt-3.5-turbo",True)