# 定义一个字典
dict = {"name": "张三", "age": 20, "sex": "男"}

# 常见操作
# len():测量字典中的键值对
print(len(dict))
# keys():返回所有的key
print(dict.keys())
# values():返回包含value的列表
print(dict.values())
# items():返回包含(键值,实值)元组的列表
print(dict.items())
# in  not in
if 20 in dict.values():
    print("我是年龄")
if "李四" not in dict.values():
    print("李四不存在")
