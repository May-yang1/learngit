from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

str_parser = StrOutputParser()
# prompt = PromptTemplate.from_template(
#     "你需要根据会话历史记录回答用户问题.会话历史记录:{chat_history},用户提问:{input},请回答:"
# )
prompt = ChatPromptTemplate.from_messages(
    [
        ("system","你需要根据会话历史记录回答用户问题.会话历史记录:"),
        MessagesPlaceholder("chat_history"),
        ("human","请回答如下问题:{input}")
    ]
)
def print_prompt(full_prompt):
    print("="*20,full_prompt.to_string(),"="*20)
    return full_prompt

model = ChatTongyi(model = "qwen3-max")
base_chain = prompt | print_prompt | model | str_parser

chat_history_store = {}
# 实现通过会话id获取InMemoryChatMessageHistory类对象
def get_history(session_id):
    if session_id not in chat_history_store:
        chat_history_store[session_id] = InMemoryChatMessageHistory()
    return chat_history_store[session_id]

# 被增强的chain(携带会话记录)
conversation_chain = RunnableWithMessageHistory(
    base_chain,         # 被附加历史消息的Runnable链
    get_history,        # 通过会话id获取InMemoryChatMessageHistory类对象
    input_messages_key = "input",       # 用户输入消息的占位符
    history_messages_key = "chat_history"
)

if __name__ == "__main__":
    # 固定格式,添加LangChain的配置,为当前程序配置所属的session_id
    session_config = {
        "configurable":{
            "session_id":"user_001"
        }
    }
    res = conversation_chain.invoke({"input":"小红有5只猫"},session_config)
    print("第1次执行",res)

    res = conversation_chain.invoke({"input": "小蓝有7只狗"}, session_config)
    print("第2次执行", res)

    res = conversation_chain.invoke({"input": "总共有多少只宠物"}, session_config)
    print("第3次执行", res)