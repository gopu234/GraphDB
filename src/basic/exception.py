a = 10
b = 0 

try:
    c = a / b 
    print ("last line of try block")
except Exception as e:
    print(e)
finally:
    print("in the finally block")