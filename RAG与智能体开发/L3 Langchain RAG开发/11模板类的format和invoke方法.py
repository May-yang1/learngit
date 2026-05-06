from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate
from langchain_core.prompts import ChatPromptTemplate

"""
PromptTemplate -> StringPromptTemplate -> BasePromptTemplate -> RunnableSerializable -> Runnable
FewShotPromptTemplate -> StringPromptTemplate -> BasePromptTemplate -> RunnableSerializable -> Runnable
ChatPromptTemplate -> BaseChatPromptTemplate -> BasePromptTemplate -> RunnableSerializable -> Runnable
"""
template = PromptTemplate.from_template("我的名字是{name},最喜欢{hobby}")

res = template.format(name = "张大明",hobby = "钓鱼")
print(res,type(res))

res2 = template.invoke({"name":"周杰伦","hobby":"唱歌"})
print(res2,type(res2)) #StringPromptValue