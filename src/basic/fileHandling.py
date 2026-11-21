def file_read(filename):    
    try:
        with open(filename, "r") as file:
            print(file.read())
    except FileNotFoundError:
        print("File not found")
        
def file_write(filename, data):
    try:
        with open(filename, "w") as file:
            file.write(data)
    except FileNotFoundError:
        print("File not found")

def file_append(filename, data):
    try:
        with open(filename, "a") as file:
            file.write(data)
    except FileNotFoundError:
        print("File not found")

file_write("example.txt", "Hello World")
file_append("example.txt", " This is appended")
file_read("example.txt")
