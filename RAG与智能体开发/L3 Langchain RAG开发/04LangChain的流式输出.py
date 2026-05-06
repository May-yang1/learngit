from langchain_community.llms.tongyi import Tongyi

llm = Tongyi(model = "qwen-max")
res = llm.stream("你是谁,能做什么?")
for chunk in res:
    print(chunk,end="",flush=True)

# from langchain_ollama import OllamaLLM
# llm = OllamaLLM(model = "deepseek-r1:1.5b")
# res = llm.stream("你是谁,能做什么?")
#
# for chunk in res:
#     print(chunk,end="",flush=True)