class Father():
    def __init__(self,house=20) :
        self.house = house
        print('Father has a house.')

class Son(Father): 
    def __init__(self, car=10):
        super(Son,self).__init__() ##调用父类的函数
        self.car = car
        print('Son has a car')
son = Son(30)

print(son.house)