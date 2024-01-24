class _Base:
    name = ""

    @classmethod
    def Pr():
        raise NotImplementedError


class A(_Base):
    name = "A"

    @classmethod
    def Pr():
        print("这是$name")


class B(_Base):
    name = "A"

    @classmethod
    def Pr():
        print("这是$name")


APIS = {"A": A, "B": B}


urls = {k: {"index": -1, "values": []} for k in APIS}

value = list(APIS.keys())[0]
print(value)
