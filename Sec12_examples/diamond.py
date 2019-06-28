# example - classes A, B, C, and D form the graph as featured on page 378

class A:
    def ping(self):
        print('ping: ', self)

class B(A):
    def pong(self):
        print('pong: ', self)

class C(A):
    def pong(self):
        print('PONG: ', self)

class D(B, C):
    def ping(self):
        # super().ping()
        # when calling an instance method directly on a class, you must pass self EXPLICITLY because you are accessing an unbound method
        A.ping(self) # alternative to super().ping()
        print('post-ping: ', self)

    def pingpong(self):
        self.ping()
        super().ping()
        self.pong()
        super().pong()
        C.pong(self)