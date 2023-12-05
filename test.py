import os
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.base import BaseCallbackManager,BaseCallbackHandler
from langchain.schema import HumanMessage, SystemMessage

os.environ["OPENAI_API_KEY"] = "sk-83oW8ytjMFgzbSCY2a90Ee8355974d33B1289f7eA657882e"
os.environ["OPENAI_API_BASE"] = "https://api.xbbdkj.com/v1"
class StreamOnlyCallbackHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs: any) -> any:
        print("")
        # return token
# 初始化 ChatOpenAI 对象
chat = ChatOpenAI(
    model_name="gpt-4-1106-preview",
    # gpt-3.5-turbo,
    streaming=True,
    verbose=True,
    callback_manager=BaseCallbackManager([StreamOnlyCallbackHandler()])
)

# 定义要发送给模型的消息
messages = [
    # SystemMessage(content='You are an AI friend.'),
    HumanMessage(content="你是什么模型"),
]

chat(messages)

# 调用模型并直接打印到控制台
for response in chat(messages):
    # print(111)
    print(response)
