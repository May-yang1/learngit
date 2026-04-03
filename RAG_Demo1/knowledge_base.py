"""
知识库维护
"""
import hashlib
import os
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

import config_data as config

def check_md5(md5_str:str):
    """检查传入的md5字符串是否已经处理过了
    return False (md5未处理过)  True (已经处理过,已有记录)"""
    if not os.path.exists(config.md5_path):
        # if进入表示文件不存在,那肯定没有处理过这个md5了
        # open函数,以'w'模式打开,如果文件不存在,就会自动创建
        # with open() as f  写with是为了防止不关文件而出错,这里手动关了
        open(config.md5_path,'w',encoding='utf-8').close()
        return False
    else:
        with open(config.md5_path,'r',encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            line = line.strip()     # 处理字符串前后的空格和回车,否则会被当作字符串一起处理
            if line == md5_str:
                return True
        return False


def save_md5(md5_str:str):
    """将传入的md5字符串,记录到文件内保存"""
    with open(config.md5_path,'a',encoding='utf-8') as f:
        f.write(md5_str + '\n')

def get_string_md5(input_str:str,encoding='utf-8'):
    # 创建md5对象   md5 是一种哈希算法，能把任意大小的文件、文本，算出一串固定长度的「数字指纹」,结果是一段32位的16进制字符
    # 比如5ebf03ecc559cc74347557a3ac3ab52d

    # 将传入的字符串转换为bytes字节数组
    input_bytes = input_str.encode(encoding = encoding)

    md5 = hashlib.md5()        # 得到md5对象
    md5.update(input_bytes)    # 更新内容(传入即将要转换的字节数组)
    return md5.hexdigest()

class KnowledgeBaseService(object):
    def __init__(self):
        self.chroma = Chroma(
            collection_name=config.collection_name,
            embedding_function=DashScopeEmbeddings(model = "text-embedding-v4"),
            persist_directory=config.persist_directory,
        ) # 向量存储实例, Chroma向量库对象
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,  # 分割后的文本段最大长度
            chunk_overlap=config.chunk_overlap,  # 连续文本段之间的字符重叠数量
            # 文本自然段落分割的依据符号
            separators=config.separators,
            length_function=len  # 统计字符的依据函数
        ) # 文本分割器对象


    def upload_by_str(self,data:str,filename):
        """将传入的字符串,进行向量化,存入向量数据库中"""
        # 1.得到md5对象
        md5 = get_string_md5(data)

        # 2.判断是否存在于知识库中,是,直接返回
        if check_md5(md5):
            return "[跳过]内容已经存在知识库中"

        # 3.切分chunk
        if len(data) > config.max_split_char_number:
            knowledge_chunks:list[str] = self.splitter.split_text(data)
        else:
            knowledge_chunks = [data]

        # 4.加载内容到向量库中
        metadata = {
            "source":filename,
            # 2026-03-31 22:43:01
            "create_time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator":"杨安其"
        }

        self.chroma.add_texts(
            # Iterable 迭代器  eg.list  tuple
            knowledge_chunks,
            metadatas = [metadata for _ in knowledge_chunks], # 给每一份数据赋予一份metedata元数据
        )
        # 5.将处理过的文件保存md5
        save_md5(md5)

        return "[成功]内容已经成功载入向量库中"

if __name__ == "__main__":
    service = KnowledgeBaseService()
    # r = service.upload_by_str("周杰轮","test")
    # r = service.upload_by_str("蔡依临","test")
    # print(r)

