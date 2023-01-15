def cta(a):
    a = list(a)
    hD.oZ(a, 43)
    hD.oe(a, 1)
    hD.zt(a)
    return "".join(a)

class hD:
    @staticmethod
    def oe(a, b):
        del a[:b]
        
    @staticmethod
    def oZ(a, b):
        c = a[0]
        a[0] = a[b % len(a)]
        a[b % len(a)] = c

    @staticmethod
    def zt(a):
        a.reverse()