from  llm_api import chatglm_pro
import json
import os

class PaperSubjectGenerator:
    def generate_subject(self,data):
        with open('/home/ubuntu/llm_paper/example.txt', 'r', encoding='utf-8') as file:
            file_content = file.read()
        prompt = (
            "作为一个论文助手，你的任务是根据我提供的信息，生成五个相关的论文标题。我会给你三篇文章的标题和摘要供参考。请你根据以下信息，以数组的格式返回给我五个标题\n"
            "论文级别：{paper_level}\n"
            "学科领域：{academic_area}\n"
            "研究目标：{research_objectives}\n"
            "候选论文题目：{paper_subject}\n"
            f"参考论文：{file_content}\n"
            "请按照这种格式给出答案，不需要添加任何额外的说明或注释。"
        ).format(
            paper_level=data['paper_level'],
            academic_area=data['academic_area'],
            research_objectives=data['research_objectives'],
            paper_subject=data['paper_subject'],
            file_content=file_content
        )
        subjects_str = chatglm_pro(prompt)
        subjects_str = subjects_str.replace("，", ",")
        subjects = json.loads(subjects_str)
        if subjects:
            return {"message": "sucesss to generate subjects","status": 1,"data":{"list":subjects}}, 200
        else:
            return {"message": "failed to generate subjects", "status": 0}, 401