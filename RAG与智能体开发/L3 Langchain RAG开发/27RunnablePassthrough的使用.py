from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import DashScopeEmbeddings


model = ChatTongyi(model="qwen3-max")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system","以我提供的已知参考资料为主,简洁和专业的回答用户问题.参考资料如下:{content}."),
        ("human","用户提问:{input}")
    ]
)
vector_store = InMemoryVectorStore(embedding=DashScopeEmbeddings(model="text-embedding-v4"))

# 准备资料,简单加些str
# add_texts 传入一个list[str]
vector_store.add_texts(["减肥就是要少吃多练","在减肥期间吃东西很重要,清淡少油控制卡路里摄入并运动起来","跑步是很好的运动哦"])

input_text = "怎么减肥?"

def print_prompt(prompt):
    print(prompt.to_string())
    print("="*20)
    return prompt

# 向量检索入链,但VectorStore不是Runable子类无法入链
# langchain中向量存储对象,有一个方法as_retriever,可以返回一个Runnable接口的子类实例对象
retriever = vector_store.as_retriever(search_kwargs={"k":2})

def format_func(docs:list[Document]):
    if not docs:
        print("无相关资料")
    formatted_docs =""
    for doc in docs:
        formatted_docs += doc.page_content
        formatted_docs += ","
    return formatted_docs

# 字典是否可以入链? 可以,字典的顶级父类是Mapping
rag_chain = ({"input":RunnablePassthrough(),"content":retriever|format_func } | prompt | print_prompt | model | StrOutputParser())
res = rag_chain.invoke(input_text)
print(res)
"""
retriever:
    -输入:用户提问input        input: str
    -输出:向量库的检索结果      list[Document]
    retriever的输入和输出都要给prompt,用户的提问要同时给retriever和prompt,
    且retriever的输出类型list[Document]要转为dict
prompt:
    -输入:用户输入+向量库的检索结果   input: dict
    -输出:完整的提示词              PromptValue
"""