def calnumGenerator(num):
    for x in range(num):
        square=x*x
        yield square


val = calnumGenerator(10)
for v in val:
    print(v)
    
# print(next(val))    
# print(next(val))    
# print(next(val))    