round = 0
total_round = 5
while(round < total_round):
    user_input=input("guess a number: ")
    print(user_input)
    if int(user_input) == 0:
        print("please enter a number between 1 and 9")
    else:
        pass
        round=round+1