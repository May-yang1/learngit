"""
基于Streamlit框架完成WEB网页上传服务

❤ ❤ ❤ Streamlit: 当WEB页面元素发生变化,则代码重新执行一遍,会造成状态的丢失,用session_state(字典)来记录状态
"""
import time

import streamlit as st
from knowledge_base import KnowledgeBaseService

# 添加网页标题
st.header("数据库更新服务")
uploader_file = st.file_uploader(
    "请上传TXT文件",
    type=['txt'],
    accept_multiple_files=False,        # False表示仅接受一个文件的上传
)

# service = KnowledgeBaseService()
# 第一次创建实例化对象,后只是调用upload_by_str方法,指向同一个chroma数据库
if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()


if uploader_file is not None:
    # 提取文件的信息
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024   # KB

    st.subheader(file_name)
    st.write(f'格式:{file_type} | 大小:{file_size:.2f} KB')

    # .getvalue() -> bytes -> decode('utf-8')
    text = uploader_file.getvalue().decode('utf-8')

    with st.spinner("载入知识库中..."):             # 在spinner内的代码执行过程中,会有一个转圈动画
        time.sleep(1)
        result = st.session_state["service"].upload_by_str(text,file_name)
        st.write(result)