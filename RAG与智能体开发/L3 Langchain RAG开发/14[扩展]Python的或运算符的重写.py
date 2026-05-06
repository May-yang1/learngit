class Test(object):
    def __init__(self,name):
        self.name = name

    def __or__(self,other):
        return MySequence(self,other)

    def __str__(self):
        return self.name

class MySequence(object):
    def __init__(self,*args):
        self.Sequence = []
        for arg in args:
            self.Sequence.append(arg)

    def __or__(self,other):
        self.Sequence.append(other)
        return self

    def run(self):
        for i in self.Sequence:
            print(i)

if __name__ == "__main__":
    a = Test("a")
    b = Test("b")
    c = Test("c")

    d = a | b | c
    d.run()
    print(type(d))
