import os, json
from typing import Sequence

from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

# message_to_dict: 单个消息对象(BaseMessage类实例) -> 字典
# messages_from_dict: [字典、字典...] -> [消息、消息...]
# AIMessage HumanMessage SystemMessage 都是BaseMessage的子类

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self,session_id,storage_path):
        self.session_id = session_id        # 会话id
        self.storage_path = storage_path    # 不同会话id的存储文件,所在的文件夹路径
        # 完整文件路径
        self.file_path = os.path.join(self.storage_path,self.session_id)
        # 确保文件夹是存在的
        os.makedirs(os.path.dirname(self.file_path),exist_ok=True)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        # Sequence序列 类似list,tuple
        all_messages = list(self.messages) # 已有的消息列表
        all_messages.extend(messages) # 新的和已有的融合成一个list

        # 将数据同步写入到本地文件中
        # 类对象写入文件 -> 一堆二进制
        # 为了方便,可以将BaseMessage消息转为字典(借助json模块以json字符串写入文件)
        # 官方message_to_dict: 单个消息对象(BaseMessage类实例) -> 字典
        # all_messages=[消息,消息..]      new_messages = [字典,字典..]
        new_messages = [message_to_dict(message) for message in all_messages]

        with open(self.file_path,'w',encoding='utf-8') as f:
            json.dump(new_messages,f)

    @property # @property装饰器将messages方法变成成员属性用,转化为属性,每次访问都会自动执行方法里的代码(动态读取)
    def messages(self) -> list[BaseMessage]:
        # 当前文件内: list[字典]
        try:
            with open(self.file_path,'r',encoding='utf-8') as f:
                message_data = json.load(f)
                return messages_from_dict(message_data)
        except FileNotFoundError:
            return []

    def clear(self) -> None:
        with open(self.file_path,'w',encoding='utf-8') as f:
            json.dump([],f)

def get_history(session_id):
    return FileChatMessageHistory(session_id,"./chat_history")

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

conversation_chain = RunnableWithMessageHistory(
    base_chain,         # 被附加历史消息的Runnable链
    get_history,        # 通过会话id获取FileChatMessageHistory类对象
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
    # res = conversation_chain.invoke({"input":"小红有5只猫"},session_config)
    # print("第1次执行",res)
    #
    # res = conversation_chain.invoke({"input": "小蓝有7只狗"}, session_config)
    # print("第2次执行", res)

    res = conversation_chain.invoke({"input":"总共有多少只宠物"}, session_config)

    print("第3次执行", res)





