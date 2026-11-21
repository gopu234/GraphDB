#list , tuple, set and dict are the main data structures in python

my_list = []
my_list.append(2)
my_list.append("hello")
my_list.append(3.14)
my_list.append([1,2,3])

my_list.insert(2, "new added")

print(my_list)
print(type(my_list))

my_list.pop(2)

print(my_list) 


#tuple immutable datastructure
my_tuple = (1,2,3,4,"hello")

print(my_tuple)
print(my_tuple[2])
print(type(my_tuple))

#set
my_set = {1,2,3,4,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5}
print(my_set)
print(type(my_set))

my_set.add(6)
print(my_set)

#dictionary
my_dict = {"name":"John", "age":30, "city":"New York"}

print(my_dict)
print(type(my_dict))

my_dict["age"] = 31
print(my_dict)