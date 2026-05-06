from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_community.llms.tongyi import Tongyi

example_template = PromptTemplate.from_template("单词:{word},反义词:{antonym}")
examples_data = [
    {"word":"上","antonym":"下"},
    {"word":"大","antonym":"小"}
]

few_shot_prompt = FewShotPromptTemplate(
    example_prompt = example_template,
    examples = examples_data,
    prefix = "我给你单词,你帮我生成反义词,有如下示例:",
    suffix = "基于上述示例,告诉我{input_word}的反义词是什么?",
    input_variables = ['input_word']
)

prompt_text = few_shot_prompt.invoke({"input_word":"左"}).to_string()
print(prompt_text,type(prompt_text))

llm = Tongyi(model="qwen-max")
print(llm.invoke(prompt_text))

# chain = few_shot_prompt | llm
# res = chain.invoke({"input_word":"左"})
# print(res)