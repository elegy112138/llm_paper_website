import os
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import BaseCallbackManager, BaseCallbackHandler
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from flask_socketio import  emit
# 环境变量设置
os.environ["OPENAI_API_KEY"] = "sk-83oW8ytjMFgzbSCY2a90Ee8355974d33B1289f7eA657882e"
os.environ["OPENAI_API_BASE"] = "https://api.xbbdkj.com/v1"


class StreamOnlyCallbackHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs: any) -> any:
        emit('my_response', {'token': token})


# 初始化 ChatOpenAI 对象
chat = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    streaming=True,
    verbose=True,
    callback_manager=BaseCallbackManager([StreamOnlyCallbackHandler()]),
)

# 读取文件内容并将其添加为系统消息
with open('/home/ubuntu/llm_paper/prompt/subject.txt', 'r') as file:
    file_contents = file.read()

# Prompt
prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(file_contents),
        # The `variable_name` here is what must align with memory
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{answer}"),
    ]
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
conversation = LLMChain(llm=chat, prompt=prompt, verbose=True, memory=memory)


