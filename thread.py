from queue import Queue
import threading
import asyncio
from catalog import PaperDirectoryGenerator
from follow import paper_md
catalog=PaperDirectoryGenerator()
paper_md=paper_md()
def background_task(queue, data,type):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    if type == 'catalog':
        loop.run_until_complete(catalog.generate_directory(queue, data))
    elif type == 'follow':
        loop.run_until_complete(paper_md.generate_follow(queue, data))
    loop.close()

def start_background_task(data, task_type):
    q = Queue()

    # 在一个新线程中运行异步生成器
    thread = threading.Thread(target=background_task, args=(q, data, task_type))
    thread.start()

    def generate():
        while True:
            message = q.get()
            print(message)
            if message == "STOP":
                break
            yield message

    return generate