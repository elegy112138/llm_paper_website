from config.base import ChatModelWrapper
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json


def subject_response(data):
    wrapper = ChatModelWrapper("gpt-4-1106-preview", False)
    file_contents = wrapper.read_prompt_file("subject.txt")
    prompt = PromptTemplate(
        input_variables=["paper_level", "academic_area", "research_objectives", "paper_subject"],
        template=file_contents
    )
    # tools = load_tools(
    #     ["arxiv"],
    # )

    # agent_chain = initialize_agent(
    #     tools,
    #     llm=wrapper.chat,
    #     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    #     verbose=True,
    #     handle_parsing_errors=True
    # )
    # prompt = prompt.format(**data)
    # agent_chain.run("What's the paper 1605.08386 about?",)
    # agent_chain.run(prompt )
    chain = LLMChain(llm=wrapper.chat, prompt=prompt)
    response=json.loads(chain.run(data))
    return {"message": "success to generate subject", "status": 1,"data":response}, 200
