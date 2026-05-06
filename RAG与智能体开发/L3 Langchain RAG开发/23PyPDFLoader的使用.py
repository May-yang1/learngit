from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(
    file_path="./data/pdf1.pdf", #pdf1无密,pdf2有密码
    mode = "page",        # 默认是page模式,每个页面生成一个Document对象,
                            # single模式,不管多少页,只返回一个Document对象
 #   password = "itheima"
)

count = 0
for doc in loader.lazy_load():
    count += 1
    print(doc)
    print("="*20,count)