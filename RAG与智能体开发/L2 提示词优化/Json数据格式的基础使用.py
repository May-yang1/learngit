import json
# json.dumps转json  json中的key是用双引号""
d = {"name":"周杰轮","age":11}
print(d)
# 字典转换为json
print(json.dumps(d,ensure_ascii=False))

l = [
    {"name":"周杰轮","age":11},
    {"name":"蔡依临","age":12},
    {"name":"小明","age":16}
]
# 列表转换为json
print(json.dumps(l,ensure_ascii=False))
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# json.loads转列表和字典
json_str = '{"name": "周杰轮", "age": 11}'
json_arry_str = '[{"name": "周杰轮", "age": 11}, {"name": "蔡依临", "age": 12}, {"name": "小明", "age": 16}]'

res_dict = json.loads(json_str)
print(res_dict,type(res_dict)) #<class 'dict'>

res_list = json.loads(json_arry_str)
print(res_list,type(res_list)) # <class 'list'>