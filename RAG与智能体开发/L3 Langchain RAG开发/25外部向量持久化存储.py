from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader

vector_store = Chroma(
    collection_name = "test",                       # 当前向量存储起个名字,类似于数据库的表名称
    embedding_function = DashScopeEmbeddings(),     # 嵌入模型
    persist_directory="./chroma_db"                 # 指定数据存放的文件夹
)
loader = CSVLoader(
    file_path = "./data/info.csv",
    encoding = "utf-8",
    source_column = "source"                        # 指定本条数据的来源是哪里
)
docs = loader.load()
# id1 id2 id3 id4 ..
# 向量存储的  新增,删除,检索
#vector_store.add_texts()
vector_store.add_documents(
    documents = docs,           # 被添加的文档,list[Document,Document,...]
    ids = ["id"+str(i) for i in range(1,len(docs)+1)]  # 给添加的文档提供id (字符串)  list[str,str,...]
)
# 删除 传入id
vector_store.delete(["id1","id2"])
# 检索 [Document,Document,Document]
result = vector_store.similarity_search(
    query = "Python是不是简单易学啊",
    k = 3,
    filter = {'source': '黑马程序员'}
)
print(result)