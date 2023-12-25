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
from langchain.memory import MongoDBChatMessageHistory

connection_string = "mongodb://localhost:27017"
# 环境变量设置
os.environ["OPENAI_API_KEY"] = "sk-pvGAarypv3x3Sqly83E255206a3e4052Bf5674252e4045Bc"
os.environ["OPENAI_API_BASE"] = "https://api.xbbdkj.com/v1"
os.environ["SERPAPI_API_KEY"] = "91bbedfd776ce5d52f703a4a33405c4cdad4066161179f6e03aa82a3f607d066"


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
def handle_respose(data):
    # 初始化 MongoDBChatMessageHistory
    message_history = initialize_message_history(session_id=data["session_id"])
    memory = ConversationBufferMemory(
        memory_key="chat_history", chat_memory=message_history, return_messages=True
    )
    # tools = load_tools(["serpapi", "llm-math"], llm=chat)
    # memory.save_context({"system": file_contents},{})
    # agent_chain = initialize_agent(
    #     tools,
    #     llm=chat,
    #     agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    #     verbose=True,
    #     memory=memory,
    # )
    # agent_chain.run(file_contents)
    conversation = LLMChain(llm=chat, prompt=prompt, verbose=True, memory=memory)
    conversation(data["text"])
def clear_history(data):
    message_history = initialize_message_history(session_id=data["session_id"])
    message_history.clear()
    return {"message": "success to clear history text", "status": 1}, 200

def dispaly_history(data):
    message_history = initialize_message_history(session_id=data["session_id"])
    if len(message_history.messages) == 0:
        return {"message": "no history text", "status": 0}, 200
    contents = [message.content for message in message_history.messages]
    contents.pop(0)  # 使用pop()方法删除索引为0的元素
    return {"message": "success to dispaly history text", "status": 1,"data":{"text":contents}}, 200

def initialize_message_history(session_id):
    # 使用传入的 session_id 初始化 MongoDBChatMessageHistory
    message_history = MongoDBChatMessageHistory(
        connection_string=connection_string, session_id=session_id
    )
    return message_history



