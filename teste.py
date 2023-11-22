
from syntactic import Grammar, Production, Syntactic

def f0(a, b):
    a.val = b.val + 1
    print(a.val)

def f1(a, _):
    a.val = 0
    print(a.val)

cfg = Grammar([
    Production("A", ["B"], after_run=f0),
    Production("B", ["C"], after_run=f0),
    Production("C", ["D"], after_run=f0),
    Production("D", ["a"], after_run=f1),
])


syn = Syntactic(cfg)
tokens = 'a'
syn.analyze(tokens)



# from functools import partial

# a = []

# def append_2(lista):
#     lista.append(2)
# class test(partial):
#     pass

# bla = test(append_2, a)

# bla()
# bla()
# bla()

# print(a)
