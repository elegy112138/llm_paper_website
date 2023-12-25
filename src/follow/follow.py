from config.base import ChatModelWrapper
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


def follow_output(content):
    # 读取文件内容并将其添加为系统消息
    wrapper = ChatModelWrapper("gpt-3.5-turbo-16k", True,'my_response')
    file_contents = wrapper.read_prompt_file("follow.txt")
    prompt = PromptTemplate(
        input_variables=["title","subtitle"],
        template=file_contents
    )
    chain = LLMChain(llm=wrapper.chat, prompt=prompt)
    print(chain.run(content))

def typo_output(content):
    wrapper = ChatModelWrapper("gpt-3.5-turbo", True,'typo_response')
    file_contents = wrapper.read_prompt_file("typo.txt")
    prompt = PromptTemplate(
        input_variables=["text"],
        template=file_contents
    )
    chain = LLMChain(llm=wrapper.chat, prompt=prompt)
    print(chain.run(content))

def polish_output(content):
    wrapper = ChatModelWrapper("gpt-3.5-turbo", True,'polish_response')
    file_contents = wrapper.read_prompt_file("polish.txt")
    prompt = PromptTemplate(
        input_variables=["text"],
        template=file_contents
    )
    chain = LLMChain(llm=wrapper.chat, prompt=prompt)
    print(chain.run(content))
