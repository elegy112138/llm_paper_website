from config.base import ChatModelWrapper
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def catalog_output(content):
    wrapper = ChatModelWrapper("gpt-3.5-turbo", False)

    file_contents = wrapper.read_prompt_file("catalog.txt")
    prompt = PromptTemplate(
        input_variables=[ "academic_area", "research_objectives", "title" ],
        template=file_contents
    )
    chain = LLMChain(llm=wrapper.chat, prompt=prompt)
    response=chain.run(content)
    response=format_chapters(response)
    return {"message": "success to generate catalog", "status": 1,"data":response}, 200



def format_chapters(text):
    # Split the text into lines
    lines = text.split('\n')

    # Define a list to hold the formatted chapter structure
    formatted_chapters = []

    # Iterate through each line to process the chapters and subchapters
    for line in lines:
        # Remove leading and trailing spaces
        line = line.strip()

        # Check the format of the line (1, 1.1, 1.1.1, etc.)
        parts = line.split(' ')
        numbers = parts[0].split('.')
        # Remove empty strings from the list
        numbers = [num for num in numbers if num]

        # Major chapter (e.g., "1. 引言")
        if len(numbers) == 1:
            formatted_chapters.append({'title': line, 'key': numbers[0], 'children': []})

        # Subchapter (e.g., "1.1 研究背景")
        elif len(numbers) == 2:
            if formatted_chapters:
                chapter_key = f"{numbers[0]}-{numbers[1]}"
                formatted_chapters[-1]['children'].append({'title': line, 'key': chapter_key})

        # Sub-subchapter (e.g., "2.1.1 量子比特")
        elif len(numbers) == 3:
            if formatted_chapters and formatted_chapters[-1]['children']:
                subchapter_key = f"{numbers[0]}-{numbers[1]}-{numbers[2]}"
                last_subchapter = formatted_chapters[-1]['children'][-1]
                last_subchapter.setdefault('children', []).append({'title': line, 'key': subchapter_key})

    return formatted_chapters




