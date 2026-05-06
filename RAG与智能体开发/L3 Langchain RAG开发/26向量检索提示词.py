from langchain_core.output_parsers import StrOutputParser
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import DashScopeEmbeddings

model = ChatTongyi(model="qwen3-max")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system","以我提供的已知参考资料为主,简洁和专业的回答用户问题.参考资料如下{content}."),
        ("human","用户提问:{input}")
    ]
)
vector_store = InMemoryVectorStore(embedding=DashScopeEmbeddings(model="text-embedding-v4"))

# 准备资料,简单加些str
# add_texts 传入一个list[str]
vector_store.add_texts(["减肥就是要少吃多练","在减肥期间吃东西很重要,清淡少油控制卡路里摄入并运动起来","跑步是很好的运动哦"])

input_text = "怎么减肥?"
# 参考资料  检索向量库[Document,Document,Document]
res = vector_store.similarity_search(input_text,2)
# print(res)
reference_text = "["
# 遍历出来的doc是一个一个的document
for doc in res:
    reference_text += doc.page_content
reference_text += "]"

def print_prompt(prompt):
    print(prompt.to_string())
    print("="*20)
    return prompt

chain = prompt | print_prompt | model | StrOutputParser()
result = chain.invoke({"input":input_text,"content":reference_text})
print(result)