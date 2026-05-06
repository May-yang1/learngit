from langchain_ollama import OllamaLLM

llm = OllamaLLM(model = "deepseek-r1:1.5b")
res = llm.invoke("你是谁,能做什么")
print(res)