# my_list = [1, 2, 3]

# for v in my_list:
#     print(v, end=" ")
# print()

# my_list2 = [x * x for x in range(5)]

# for v in my_list2:
#     print(v, end=" ")

# my_generator = (x * x for x in range(5))


# print(type(my_generator))
# for v in my_generator:
#     print(v, end=" ")
## yeild
def generator_even(max):
    for i in range(0, max + 1):
        if i % 2 == 0:
            yield i


even_generator = generator_even(10)

for n in even_generator:
    print(n, end=" ")
