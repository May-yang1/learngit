from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi

chat_prompt_template = ChatPromptTemplate.from_messages(
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
# ChatPromptValue    to_string()
#prompt = chat_prompt_template.format(history = history_data)
#print(type(prompt))
prompt_text = chat_prompt_template.invoke({"history":history_data}).to_string()

print(prompt_text,type(prompt_text))

model = ChatTongyi(model = "qwen3-max")
res = model.invoke(prompt_text)
print('\n'+res.content,type(res))

# chain = chat_prompt_template | model
# res = chain.invoke({"history":history_data})
# print(res.content,type(res))