from langchain_community.llms.tongyi import Tongyi
from langchain_community.chat_models.tongyi import ChatTongyi

# qwen-max是LLMs大语言模型,而qwen3-max是聊天模型
# llm = Tongyi(model = "qwen-max")
# res = llm.invoke("你是谁,能做什么")
# print(res)

model = ChatTongyi(model = "qwen3-max")
res2 = model.invoke("你是谁,能做什么")
print(res2)