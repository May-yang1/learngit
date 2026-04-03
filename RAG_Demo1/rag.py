from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from langchain_core.documents import Document
from file_history_store import get_history

import config_data as config
from vector_stores import VectorStoreService
def print_prompt(prompt):
    print("="*20)
    print(prompt.to_string())
    print("="*30)
    return prompt

class RagService(object):
    def __init__(self):
        self.vector_store = VectorStoreService(DashScopeEmbeddings(model=config.embedding_model_name))
        self.chat_model = ChatTongyi(model = config.chat_model_name)
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system","以我提供的已知参考资料为主,间接和专业的回答用户问题,参考资料:{content}"),
                MessagesPlaceholder("history"),
                ("user","请回答用户提问:{input}")
            ]
        )
        self.chain = self.__get_chain()

    def __get_chain(self):
        """获取最终的执行链"""
        retriever = self.vector_store.get_retriever()

        def format_func(docs:list[Document]):
            if not docs:
                return "无相关资料"
            formatted_str = ""
            for doc in docs:
                formatted_str += f"文档内容:{doc.page_content}"
            return formatted_str

        def format_for_retriever(value):
            return value['input']
        def format_for_prompt_template(value):
            new_value = {}
            new_value['input'] = value['input']['input']
            new_value['history'] = value['input']['history']
            new_value['content'] = value['content']
            return new_value

        chain = (
                {
                    "input": RunnablePassthrough(),
                    "content":RunnableLambda(format_for_retriever) |retriever | format_func
                } | RunnableLambda(format_for_prompt_template) |self.prompt_template | print_prompt | self.chat_model | StrOutputParser()
        )

        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key = "input",
            history_messages_key = "history"
        )
        return conversation_chain

if __name__ == "__main__":
    session_config = {
        "configurable":{
            "session_id":config.session_id
        }
    }
    res = RagService().chain.invoke({"input":"春天应该穿什么颜色"},session_config)
    print(res)