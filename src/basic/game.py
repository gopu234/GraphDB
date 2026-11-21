import random as rand
round = 0
total_round = 5
users = {"user1", "user2", "user3"}
score_board={"user1":0, "user2":0, "user3":0}

def generateRandomNumber():
    random_number=0
    try:
        random_number=rand.randint(1,9)
        print(f"random_number {random_number}")
    except Exception as e:
        print(e)
        random_number=7
    finally:
        return random_number

def verifyNumber(user_input,random_number):
    if user_input_int == 0:
        print("please enter a number between 1 and 9")
    else:
        if(user_input_int==random_number):                
            score_board[user]=score_board[user]+1
        else:
            print("wrong guess")


while(round < total_round):
    random_number = generateRandomNumber()    
    for user in users:
        user_input=input(f"{user} round:{round+1} guess a number: ")
        user_input_int=int(user_input)
        verifyNumber(user_input_int,random_number)
    round=round+1

print(f"Final score board: {score_board}")