import random

dungeon = "...$$$..D......a....M........m...........P....."
hero = "@"
hero_x = 0
hero_gold = 0
hero_hunger = 0
hero_hp = 100
hero_poison = False
food = {"a":"apple","m":"meat",}
level = list(dungeon)

while True:
    hero_hunger += 1
    hero_hp += 1
    if hero_poison == True:
        hero_hp -= 3
    for x, char in enumerate(level):
        #print(x, char)
        if x == hero_x:
            print(hero, end="")
        else:
            print(level[x], end="")
    print()
    command = input("$: {} hunger {} hp: {} what now?".format(hero_gold, hero_hunger, hero_hp))
    hero_hunger += 1
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
        print("Press other key!")
    stuff = level[hero_x]
    if stuff == "$":
        hero_gold += 1
        level[hero_x] = "."
    elif stuff == "a":
        hero_hunger -= 10
        level[hero_x] = "."
    elif stuff == "m":
        hero_hunger -= 20
        level[hero_x] = "."
    elif stuff == "M":
        hero_hp -= 40
        level[hero_x] = "."
    elif stuff == "D":
        hero_hp -= 50
        level[hero_x] = "."
    elif stuff == "P":
        hero_poison = True
        level[hero_x] = "."
