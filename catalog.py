from  llm_api import chatglm_turbo
import json
class PaperDirectoryGenerator:


    async def generate_directory(self, queue,data):
        prompt = (
            "直接列出论文的目录结构，不包括'论文目录'等任何额外标题或介绍性的文字。只提供章节和子章节的标题。\n"
            "论文级别：{paper_level}\n"
            "学科领域：{academic_area}\n"
            "研究目标：{research_objectives}\n"
            "论文题目：{paper_subject}\n"
            "论文长度：{paper_length}\n"
            "具体需求：{specific_requirement}\n"
            "格式要求：章节号后直接跟章节标题，子章节同样只列出编号和标题。\n"
            "结束后请不要有任何说明，尤其是‘注意’，谢谢"
            "请以markdown格式返回给我"
        ).format(
            paper_level=data['paper_level'],
            academic_area=data['academic_area'],
            research_objectives=data['research_objectives'],
            paper_subject=data['paper_subject'],
            paper_length=data['paper_length'],
            specific_requirement=data['specific_requirement']
        )

        async for response in chatglm_turbo(prompt):
            if response['event'] == 'add':
                queue.put(f"data: {json.dumps(response['data'], ensure_ascii=False)}\n\n")
            elif response['event'] == 'finish':
                # response['data'] = 'finish'
                # queue.put(f"data: {json.dumps(response['data'], ensure_ascii=False)}\n\n")
                queue.put("STOP")
                break
            # 一定要在生成器结束时发送STOP信号
        # queue.put("STOP")

    # def format_directory(self,text):
    #     # 将文本拆分成行并去除空格
    #     lines = [line.strip() for line in text.split('\n') if line.strip()]
    #
    #     tree = []
    #     current_parent = None
    #
    #     for line in lines:
    #         # 删除子标题前的破折号
    #         if line.startswith('- '):
    #             line = line[2:]
    #
    #         # 检查是否是主标题，例如 "1. 引言"
    #         if line.count('.') == 1 and line.split('.')[0].isdigit() and not line.split('.')[1][0].isdigit():
    #             current_parent = {
    #                 "key": line.split('.')[0],
    #                 "title": line,
    #                 "children": []
    #             }
    #             tree.append(current_parent)
    #         # 检查是否是子标题，例如 "2.1 量子加密的基本原理"
    #         elif line.count('.') == 1 and line.split('.')[0].isdigit() and line.split('.')[1][0].isdigit():
    #             if current_parent and line.startswith(current_parent["key"] + '.'):
    #                 sub_key, sub_title = line.split(' ', 1)
    #                 sub_key = sub_key.split('.')[1]  # 只保留子标题的部分
    #                 current_parent['children'].append({
    #                     "key": f"{current_parent['key']}-{sub_key}",
    #                     "title": line
    #                 })
    #
    #     return  tree






