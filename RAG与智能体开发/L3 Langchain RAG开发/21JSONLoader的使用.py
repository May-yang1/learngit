from langchain_community.document_loaders import JSONLoader
import json
loader = JSONLoader(
    file_path = "./data/stu.json",
    jq_schema = '.', # jq_schema语法 .表示根
    text_content=False, # 只有完全是字符串时,才能是True,其它复合结构等用False
    json_lines = False,
)
documents = loader.load()
# text_content=False JSONLoader 会将提取到的 Python 对象（如字典）通过 json.dumps() 序列化为字符串。
# 而 json.dumps() 默认开启 ensure_ascii=True，会强制把所有非 ASCII 字符（中文）转义为 \uXXXX 格式的 Unicode 编码
# 所以为了得到字符串
for document in documents:
    data = json.loads(document.page_content)   # 得到字典
    document.page_content = json.dumps(data,ensure_ascii=False) #

print(len(documents))  # 1
print(documents)
