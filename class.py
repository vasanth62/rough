class Base(object):
    attr1 = ''
    attr2 = ''

    def virtual(self):
        pass               # doesn't do anything in the parent class

    def func(self):
        print "%s, %s" % (self.attr1, self.attr2)
        self.virtual()

class Derived(Base):
    attr1 = 'I am in class Derived'
    attr2 = 'blah blah'

    def virtual(self):
        print 'Virtual in derived'

d = Derived()
d.func()

