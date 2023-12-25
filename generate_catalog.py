from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackManager, BaseCallbackHandler
from langchain.prompts import PromptTemplate
from flask_socketio import emit
import os
os.environ["OPENAI_API_KEY"] = "sk-83oW8ytjMFgzbSCY2a90Ee8355974d33B1289f7eA657882e"
os.environ["OPENAI_API_BASE"] = "https://api.xbbdkj.com/v1"


class StreamOnlyCallbackHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs: any) -> any:
        # print(token)
        emit('my_response', {'token': token})


chat = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        # model_name="gpt-4-1106-preview",
        streaming=True,
        verbose=True,
        callback_manager=BaseCallbackManager([StreamOnlyCallbackHandler()]),
)



def catalog_output(content):
    with open('/home/ubuntu/llm_paper/prompt/catalog.txt', 'r') as file:
        file_contents = file.read()
    prompt = PromptTemplate(
        input_variables=["paper_level", "academic_area", "research_objectives", "title", "paper_length",
                         "specific_requirement"],
        template=file_contents
    )
    chain = LLMChain(llm=chat, prompt=prompt)
    chain.run(content)
def catalog_follow(content):
    with open('/home/ubuntu/llm_paper/prompt/catalog_follow.txt', 'r') as file:
        file_contents = file.read()
    prompt = PromptTemplate(
        input_variables=[ "title", "catalog","click_title"],
        template=file_contents
    )
    chain = LLMChain(llm=chat, prompt=prompt)
    # chain.run(content)
    print(chain.run(content))




