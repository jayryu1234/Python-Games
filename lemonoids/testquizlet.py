dic = {1:'intrepid', 2:'virtuous', 3: 'faculty', 4: 'eminence', 5: 'evanescent', 6: 'furtive', 7: 'grotesque', 8:'wend', 9:'grieve', 10: 'tarry', 11:'heave', 12:'anatomy',13:'rapped',14:'exultation',15:'potent',16:'audacious',17:'reproach',18:'sacred',19:'pathos',20:'martyr'}
import random
choice = None
running = True
next = 0
while True:
    score = 0
    option = int(input(f"what style of test do you want now? 1. randomx20, or 2. in order\n"))
    for i in range(20):
        if option == 1:
            choice = random.randint(1, 20)
        elif option == 2:
            choice = i+1
        solution = dic[choice]
        print_this = print(choice)
        value = input("please enter da solution (youll get it wrong haah ah ah)\n")
        if value == solution:
            print("you got it correct!")
            score += 1
        else:
            print(f"womp womp da answer was {solution} and the number is {choice}")
            #might add definition he he boi

        if i == 20:
            print(score)
            global brh
            brh = input("do you want to try again? 1 = yes, 2= no\n")
            if brh == 1:
                break
            if brh == 2:
                break
    if brh == 2:
        break
