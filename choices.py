import random
choices = {1:"Uma tempestade solar está chegando, você guarda seus equipamentos, ou não (risco de deterioração)", 2:"situation 2", 3:"situation 3", 4:"situation 4"}
conseqy = {1:"diminui energia", 2:"situation 2", 3:"situation 3", 4:"situation 4"}
conseqn = {1:"diminui a integridade dos equipamentos", 2:"situation 2", 3:"situation 3", 4:"situation 4"}
while True:
    probability = random.randint(1, 10)
    if probability == 1:
        choice_index = random.randint(1, 4)
        choice = choices[choice_index]
        answer = input(choice + " (yes/no): ")
        if answer == "yes":
            print("You chose yes.")
        elif answer == "no":
            print("You chose no.")