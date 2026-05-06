from openai import OpenAI
import json

client = OpenAI(base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1")

examples = [
    {
        "content":"2025年第88期，开好红球10 14 17 24 27 30 篮球 05，一等奖中奖为4注。",
        "answer":{
            "期数":"202588",
            "中奖号码":[10,14,17,24,27,30,5],
            "一等奖":"4注"
        }
    },
    {
        "content":"2025年89期，有5注一等奖，18注二等奖，开号篮球09，中奖红球02、08、15、19、23、28。",
        "answer":{
            "期数":"202589",
            "中奖号码":[2,8,15,19,23,28,9],
            "一等奖":"5注"
        }
    }
]
questions = [
    "2025年第100期,开好红球22 21 06 01 03 11 篮球 07,一等奖中奖为2注.",
    "2025101期,有3注1等奖,10注2等奖,开号篮球11,中奖红球3、5、7、11、12、16."
]
message = [{"role":"system","content":"你帮我信息抽取,我给你句子,你抽取信息,按照JSON字符串输出,如果某些信息不存在,用'原文未提及'表示,请参考如下示例:"}]

for example in examples:
    message.append({"role":"user","content":example["content"]}),
    message.append({"role":"assistant","content":json.dumps(example["answer"],ensure_ascii=False)})

for q in questions:
    response = client.chat.completions.create(
        model = "qwen3-max",
        messages = message + [{"role":"user","content":f"按照上述示例,现在抽取这个句子的信息:{q}"}]
    )
    print(response.choices[0].message.content)