from openai import OpenAI

# 1.获取client对象,OpenAI类对象
client = OpenAI(base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1")

# 2.调用模型
response = client.chat.completions.create(
    model = "qwen3-max",
    messages = [
       {"role":"system","content":"你是AI助手,回答简练"},
       {"role":"user","content":"小明有三条宠物狗"},
       {"role":"assistant","content":"好的"},
       {"role":"user","content":"小红有两条宠物猫"},
       {"role":"assistant","content":"好的"},
       {"role":"user","content":"总共有几个宠物"}
    ],
    stream = True
)
# 3.处理结果
for chunk in response:
    print(
        chunk.choices[0].delta.content,
        end=" ",    # 每一段以空格间隔
        flush=True # 立刻刷新缓冲区
   )
