from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    file_path = "./data/stu.csv",
    csv_args={
        "delimiter":",",        # 指定分隔符,如","
        "quotechar":'"'        # 指定带分隔符文本的引号是单引号还是双引号
        #"fieldnames":["name","age","gender","hobby"]  # 表头,如若.csv中有表头就不需要加
    },
    encoding = "utf-8"
)

# 批量加载.load()         ->  [Document,Document,...]
# for document in loader.load():
#     print(type(document),document)

# 懒加载.lazy_load()      ->  [Document]
for document in loader.lazy_load():
    print(type(document),document)