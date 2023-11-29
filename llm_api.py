import zhipuai

def chatglm_pro(prompt):
    zhipuai.api_key = "a4c0eae52f6c07d423a8714ad5b1804c.ypACGm6JR6Ujjgal"
    response = zhipuai.model_api.sse_invoke(
        model="chatglm_turbo",
        prompt=prompt,
        temperature=0.95,
        top_p=0.7,
        incremental=True
    )
    output = []  # 用来累积输出

    for event in response.events():
        if event.event == "add":
            output.append(event.data)
        elif event.event == "error" or event.event == "interrupted":
            print(event.data)
        elif event.event == "finish":
            full_output = "".join(output)  # 一次性获取完整的输出
            print(event.meta)
            return full_output  # 返回完整的输出
        else:
            print(event.data)

async def chatglm_turbo(prompt):
    zhipuai.api_key = "a4c0eae52f6c07d423a8714ad5b1804c.ypACGm6JR6Ujjgal"
    response = zhipuai.model_api.sse_invoke(
        model="chatglm_turbo",
        prompt=prompt,
        temperature=0.95,
        top_p=0.7,
        incremental=True
    )
    for event in response.events():
        if event.event == "add":
            yield {"event": "add", "data": event.data}
        elif event.event == "error" or event.event == "interrupted":
            yield {"event": "error", "data": event.data}
        elif event.event == "finish":
            yield {"event": "finish"}
            break
        else:
            yield {"event": "other", "data": event.data}

