from config.db_connect import get_collection
from datetime import datetime
from bson.objectid import ObjectId
import json


def save_article(data):
    # 保存文章
    collection = get_collection("article_table")
    # Generate a timestamp and format it as specified (YYYY-MM-DD HH:MM:SS)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data['PublishDate'] = timestamp
    result = collection.insert_one(data)
    if result.inserted_id:
        return {"message": "success insert", "status": 1, "data": {"article_id": str(result.inserted_id)}}, 200
    else:
        return {"message": "faliled insert", "status": 0, }, 200


def display_article(data):
    # 根据User_ID展示文章
    collection = get_collection("article_table")
    result = collection.find({"UserID": data['UserID']})

    articles = []  # 用于存储处理后的文章

    for doc in result:
        # 删除每个文档的Content字段
        if 'Content' in doc:
            del doc['Content']

        # 替换_id字段为article_id
        doc['article_id'] = str(doc.pop('_id', None))

        # 将处理后的文档添加到列表中
        articles.append(doc)

    # 根据结果返回不同的消息
    if articles:
        return {"message": "success", "status": 1, "data": articles}, 200
    else:
        return {"message": "No articles found", "status": 0}, 200


def display_article_content(data):
    collection = get_collection("article_table")
    result = collection.find_one({"_id": ObjectId(data['article_id'])})
    if result:
        # 转换ObjectId为字符串
        result = json.loads(json.dumps(result, default=str))
        # 添加或更新article_id字段
        result['article_id'] = result.pop('_id', None)

        return {"message": "success", "status": 1, "data": result}, 200
    else:
        return {"message": "Article not found", "status": 0}, 200


def delete_article(data):
    collection = get_collection("article_table")
    # 尝试找到文章
    result = collection.find_one({"_id": ObjectId(data['article_id'])})
    if result:
        # 如果找到了文章，执行删除操作
        delete_result = collection.delete_one({"_id": ObjectId(data['article_id'])})

        if delete_result.deleted_count > 0:
            return {"message": "Article deleted successfully", "status": 1}, 200
        else:
            return {"message": "Article deletion failed", "status": 0}, 200
    else:
        # 如果没找到文章
        return {"message": "Article not found", "status": 0}, 200


def update_article(data):
    collection = get_collection("article_table")

    # 从data中提取article_id，并将其转换为ObjectId
    article_id = ObjectId(data['article_id'])

    # 构造更新操作的内容
    new_values = {"$set": {
        "Title": data['Title'],
        "Content": data['Content']
    }}

    # 根据article_id执行更新操作
    result = collection.update_one({"_id": article_id}, new_values)

    if result.matched_count > 0:
        # 如果找到并更新了文章
        if result.modified_count > 0:
            return {"message": "Article updated successfully", "status": 1}, 200
        else:
            return {"message": "Article already up-to-date", "status": 1}, 200
    else:
        # 如果没有找到文章
        return {"message": "Article not found", "status": 0}, 200
