import random
dungeon = "...$$$..................................."
hero = "@"
hero_x = 0
hero_gold = 0

level = list(dungeon)



while True:
    for x, char in enumerate(level):
        #print(x, char)
        if x == hero_x:
            print(hero, end="")
        else:
            print(level[x], end="")
    print()
    command = input("$: {} was jetzt?".format(hero_gold))
    if command == "quit" or command == "exit":        
        break
    elif command == "a":
        hero_x -= 1
    elif command == "d":
        hero_x += 1
    elif command == "A":
        hero_x -= 3
    elif command == "D":
        hero_x += 3
    else:
        print("Drücke eine andere Taste")
    stuff = level[hero_x]
    if stuff == "$":
        hero_gold += 1
        level[hero_x] = "."
