from langchain.agents.middleware import (before_agent, after_agent, before_model, after_model, wrap_model_call, \
    wrap_tool_call)
from langchain_core.tools import tool
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain.agents import create_agent, AgentState
from langgraph.runtime import Runtime


@tool(description="查询天气,传入城市名称字符串,返回字符串天气")
def get_weather(city: str) -> str:
    return f"{city}大雨"

@before_agent
def log_before_agent(state: AgentState, runtime: Runtime) -> None:
    print(f"[before_agent]agent启动,并附带{len(state['messages'])}消息")

@after_agent
def log_after_agent(state: AgentState, runtime: Runtime) -> None:
    print(f"[after_agent]agent结束,并附带{len(state['messages'])}消息")

@before_model
def log_before_model(state: AgentState, runtime: Runtime) -> None:
    print(f"[before_model]模型即将调用,并附带{len(state['messages'])}消息")

@after_model
def log_after_model(state: AgentState, runtime: Runtime) -> None:
    print(f"[after_model]模型调用结束,并附带{len(state['messages'])}消息")

@wrap_model_call
def model_call_hook(request,handler):
    print("模型调用啦")
    return handler(request)

@wrap_tool_call
def monitor_tool(request,handler):
    print(f"工具执行:{request.tool_call['name']}")
    print(f"工具执行传入参数:{request.tool_call['args']}")

    return handler(request)

agent = create_agent(
    model=ChatTongyi(model="qwen3-max"),
    tools=[get_weather],
    middleware=[log_before_agent,log_after_agent,log_before_model,log_after_model,model_call_hook,monitor_tool]
)
res = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "今天深圳天气如何, 如何穿衣?"}
        ]
    }
)
print("************************")
for msg in res['messages']:
    print(type(msg).__name__,msg.content)