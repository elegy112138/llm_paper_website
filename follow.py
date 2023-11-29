from llm_api import chatglm_pro


class paper_md:
    def __init__(self):
        pass

    def check_typo(self, data):
        prompt = (
            f"作为我的论文助手，你的任务包括两个方面：第一，检查输入文本是否为Markdown格式。如果不是，请将其转换成Markdown格式并返回给我。第二，检查文本段落中是否有错别字或语法问题，并进行相应的更正。请注意，你的输出应该仅包括转换后的Markdown格式文本，不需要包含其他多余的信息。下面是需要你处理的文本：\n"
            f"({data["text"]})\n"
            f"请仅执行上述任务，并以Markdown格式返回修改后的文本。")
        text=chatglm_pro(prompt)
        print(text)
        text = self.format_text(text)

        if text:
            return {"message": "success to check text", "data":{"text":text},"status": 1}, 200
        else:
            return {"message": "failed check text", "status": 0}, 401

    def generate_follow(self, data):
        prompt = (
            f"作为我的论文助手，你的任务是继续撰写我提供的论文内容。我将给你一个论文结构的草稿，格式为 Markdown。请根据我提供的 Markdown 内容 '{data['text']}' 继续写作，要求是从我给出的文本后面开始写作，而且不要给出多余的标题，保证续写就好。在你的回答中，请确保只包含所需的后续内容，，并避免包含任何不必要的信息。")
        text = chatglm_pro(prompt)
        text = self.format_text(text)
        if text:
            return {"message": "success to generate text", "data":{"text":text},"status": 1}, 200
        else:
            return {"message": "failed generate text", "status": 0}, 401

    def format_text(self,text):
        # 移除可能存在的空白字符
        text = text.strip()

        # 检查是否以```markdown或```开头
        if text.startswith("```markdown") or text.startswith("```"):
            # 移除开头的```markdown或```并提取直到下一个```之前的内容
            start = text.find("\n") + 1 if text.startswith("```markdown") else 3
            end = text.find("```", start)
            return text[start:end].strip() if end != -1 else text[start:].strip()
        return text

