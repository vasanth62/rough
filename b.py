from test.a import *

class A(A):
    def __init__(self):
        print 'b.A'
        import test.a
        test.a.A.__init__(self)

x = A()
x.p()
