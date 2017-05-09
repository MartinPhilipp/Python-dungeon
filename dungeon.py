import random
level = "...$$$..................................."
hero = "@"
hero_x = 0
while True:
    line = list(level)
    for x, char in enumerate(line):
        #print(x, char)
        if x == hero_x:
            print(hero, end="")
        else:
            print(line[x], end="")
    print()
    command = input("was jetzt?")
    if command == "quit" or command == "exit":        
        break
    elif command == "a":
        herox -= 1
    elif command == "d":
        herox += 1
    elif command == "A":
        herox -= 3
    elif command == "D":
        herox += 3
    else:
        print("Drücke eine andere Taste")
