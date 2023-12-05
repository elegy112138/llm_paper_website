from llm_api import chatglm_pro,chatglm_turbo
import json

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

    async def generate_follow(self, queue,data):
        prompt = (
            f"请在所提供的文本后续写，而不改变原文。您的续写应该紧接着原文的最后一个词开始，并且平滑地扩展文字。并且需要以markdown格式续写。您应该从这句话的末尾开始续写，请确保您的续写内容与原文在逻辑上连贯，并且自然地衔接上文。续写文本如下：'{data['text']}'。请你以markdown格式返回续写内容")
        async for response in chatglm_turbo(prompt):
            if response['event'] == 'add':
                queue.put(f"data: {json.dumps(response['data'], ensure_ascii=False)}\n\n")
            elif response['event'] == 'finish':
                response['data'] = ' ```'
                queue.put(f"data: {json.dumps(response['data'], ensure_ascii=False)}\n\n")
                queue.put("STOP")
                break
            # 一定要在生成器结束时发送STOP信号
        # queue.put("STOP")

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

