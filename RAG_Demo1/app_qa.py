import streamlit as st
from rag import RagService
import config_data as config

st.title("智能客服")
st.divider()      # 分隔符

prompt = st.chat_input()

if "message" not in st.session_state:
    st.session_state["message"] = [{"role":"assistant","content":"你好,有什么可以帮您的?"}]
for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role":"user","content":prompt})

    ai_res_list=[]
    with st.spinner("AI思考中..."):
        # res_stream = st.session_state["rag"].chain.stream({"input": prompt}, config.session_config)
        # res = st.chat_message("assistant").write_stream(res_stream)
        # st.session_state["message"].append({"role": "assistant", "content": res})   # res_stream是迭代器,无法存入content中(要求是字符串)

        # yield 返回迭代器
        res_stream = st.session_state["rag"].chain.stream({"input": prompt}, config.session_config)
        def capture(generator,cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk

        st.chat_message("assistant").write_stream(capture(res_stream,ai_res_list))
        st.session_state["message"].append({"role": "assistant", "content": "".join(ai_res_list)})
# 将列表list转为字符串的方式
# ['a','b','c']        "".join(list)   -> abc
# ['a','b','c']        ",".join(list)   -> a,b,c