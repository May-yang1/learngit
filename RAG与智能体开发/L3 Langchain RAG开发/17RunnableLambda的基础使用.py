from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables import RunnableLambda

# 创建字符串解释器
str_parser = StrOutputParser()

# 创建模型
model = ChatTongyi(model = "qwen3-max")

# 第一个提示词模版
first_prompt = PromptTemplate.from_template(
    "我的邻居姓{lastname},刚生了{gender},帮我起个名字,不要额外信息"
)
# 第二个提示词模版
second_prompt = PromptTemplate.from_template(
    "姓名{name},请帮我解析含义"
)
# 函数的入参:AIMessage -> dict  ({"name":"xxxxx"})
my_func = RunnableLambda(lambda ai_msg:{"name":ai_msg.content})
chain = first_prompt | model | my_func | second_prompt | model | str_parser

# # 自定义函数是Callable接口,内部会自己转到RunnableLambda类对象
# chain = first_prompt | model | (lambda ai_msg:{"name":ai_msg.content}) | second_prompt | model | str_parser

for chunk in chain.stream({"lastname":"何","gender":"男孩"}):
    print(chunk,end="",flush=True)