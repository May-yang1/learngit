from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi

# zero-shot思想
prompt_template = PromptTemplate.from_template("我的邻居姓{lastname},刚生了{gender},你帮我取个名字,要求简单回答")

# 调用.format方法注入信息即可
prompt_text = prompt_template.format(lastname="张",gender="女儿")
llm = Tongyi(model="qwen-max")
res = llm.invoke(prompt_text)
print(res)

llm = Tongyi(model="qwen-max")
chain = prompt_template | llm
res = chain.invoke({"lastname":"张","gender":"女儿"})
print(res)
