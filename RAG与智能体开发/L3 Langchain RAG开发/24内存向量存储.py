from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader

vector_store = InMemoryVectorStore(
    embedding = DashScopeEmbeddings()
)
loader = CSVLoader(
    file_path = "./data/info.csv",
    encoding = "utf-8",
    source_column = "source"
)
docs = loader.load()
# id1 id2 id3 id4 ..
# 向量存储的  新增,删除,检索
vector_store.add_documents(
    documents = docs,           # 被添加的文档,list[Document,Document,...]
    ids = ["id"+str(i) for i in range(1,len(docs)+1)]  # 给添加的文档提供id (字符串)  list[str,str,...]
)
# 删除 传入id
vector_store.delete(["id1","id2"])
# 检索
result = vector_store.similarity_search(
    query = "Python是不是简单易学啊",
    k = 3
)
print(result)