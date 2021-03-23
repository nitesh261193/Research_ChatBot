def get5():
    for i in range(5):
        yield i

gen = get5()
print(gen)
print(next(gen))
#lkjdalfdj
print(next(gen))