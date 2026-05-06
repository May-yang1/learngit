from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi

chat_prompt_template = ChatPromptTemplate(
    [
        ("system","你是一个边塞诗人,可以作诗"),
        MessagesPlaceholder("history"),
        ("human","请再来一首唐诗")
    ]
)
history_data = [
    ("human","你来写一首唐诗"),
    ("ai","床前明月光,疑是地上霜,举头望明月,低头思故乡"),
    ("human","好诗再来一首"),
    ("ai","锄禾日当午,汗滴禾下土,谁知盘中餐,粒粒皆幸苦")
]
model = ChatTongyi(model = "qwen3-max")

# 组成链,要求每一个组件都是Runnable接口的之类
chain = chat_prompt_template | model
print(type(chain))

# 通过链来调用invoke或stream
# res = chain.invoke({"history":history_data})
# print(res.content,type(res))

for chunk in chain.stream({"history":history_data}):
    print(chunk.content,end="",flush=True)
