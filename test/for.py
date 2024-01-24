APIS = {"a": "A", "b": "B"}

# for k in APIS:
#     print(k)

# for v in APIS.values():
#     print(v)


# for k, v in APIS.items():
#     print(k, v)

# for item in APIS.items():
#     print(item[0], item[1])

# print(list(APIS.keys()))

apis_temp = {k: v + "1" for k, v in APIS.items()}
print(apis_temp)
