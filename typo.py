import os
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import BaseCallbackManager, BaseCallbackHandler
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.chains import LLMChain
from flask_socketio import  emit


os.environ["OPENAI_API_KEY"] = "sk-pvGAarypv3x3Sqly83E255206a3e4052Bf5674252e4045Bc"
os.environ["OPENAI_API_BASE"] = "https://api.xbbdkj.com/v1"

class StreamOnlyCallbackHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs: any) -> any:
        emit('my_response', {'token': token})

with open('/home/ubuntu/llm_paper/prompt/follow.txt', 'r') as file:
    file_contents = file.read()

chat = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    streaming=True,
    verbose=True,
    callback_manager=BaseCallbackManager([StreamOnlyCallbackHandler()]),
)
prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(file_contents),
        HumanMessagePromptTemplate.from_template("{answer}"),
    ]
)
conversation = LLMChain(llm=chat, prompt=prompt, verbose=True)


