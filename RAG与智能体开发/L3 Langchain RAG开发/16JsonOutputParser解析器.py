from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi

# 创建字符串和JSON格式解释器
str_parser = StrOutputParser()
json_parser = JsonOutputParser()

# 创建模型
model = ChatTongyi(model = "qwen3-max")

# 第一个提示词模版
first_prompt = PromptTemplate.from_template(
    "我的邻居姓{lastname},刚生了{gender},帮我起个名字,并封装为JSON格式返回给我,"
    "要求key是name,value是起的名字.请严格遵守格式要求"
)
# 第二个提示词模版
second_prompt = PromptTemplate.from_template(
    "姓名{name},请帮我解析含义"
)
# 创建链
# AI 返回的 JSON 字符串 → Python 字典
chain = first_prompt | model | json_parser | second_prompt | model |str_parser

for chunk in chain.stream({"lastname":"杨","gender":"女儿"}):
    print(chunk,end="",flush=True)