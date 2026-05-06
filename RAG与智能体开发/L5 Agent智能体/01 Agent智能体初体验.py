from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_community.chat_models.tongyi import ChatTongyi

@tool(description="查询天气")
def get_weather() -> str:
    return "大雨"

agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),
    tools=[get_weather],
    system_prompt="你是一个聊天助手,可以回答用户问题"
)
res = agent.invoke(
    {
        "messages":[
            {"role":"user","content":"明天深圳天气如何?"}
        ]
    }
)
for msg in res["messages"]:
    # 不加__name__,得到<class 'langchain_core.messages.human.HumanMessage'>,加了得到HumanMessage
    print(type(msg).__name__,msg.content)
