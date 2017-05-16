import random

dungeon = "..WW.$$$..D.........a....G.......$.m.G........W..P....."
hfood = {"a":"apple","m":"meat",}
level = list(dungeon)

class Monster():
    number = 0
    zoo = {}
    chars = ""
    
    def __init__(self, posx=0, char = "M", name = "Monster", hp = 20,
                 tohit = 0.6, evade = 0.2, maxdamage = 5):
        self.x = posx
        self.char = char
        self.name = name
        self.hp = hp
        self.tohit = tohit
        self.evade = evade
        self.maxdamage = maxdamage
        self.number = Monster.number
        Monster.number += 1
        Monster.zoo[self.number] = self
        if self.char not in Monster.chars:
            Monster.chars += self.char
    
    def report(self):
        return "{} hp: {} ; tohit: {} ; evade {} ; maxdamage: {}".format(
        self.name, self.hp, self.tohit, self.evade, self.damage)
        
class Hero(Monster):
    def __init__(self):
        Monster.__init__(self, 0, "@", "hero", 20, 0.7, 0.3, 5)
        self.hunger = 0
        self.gold = 0
        self.poison = False
        
class Dragon(Monster):
    def __init__(self, posx):
        Monster.__init__(self, posx, "D", "Dragon", 50, 0.8, 0.1, 7)
        
class Goblin(Monster):
    def __init__(self, posx):
        Monster.__init__(self, posx, "G", "Goblin", 10, 0.4, 0.5, 3)
        
class Wolf(Monster):
    def __init__(self, posx):
        Monster.__init__(self, posx, "W", "Wolf", 8, 0.6, 0.6, 2)

#generate monsters

hero = Hero() #hero alwys start at_position 0

for x, char in enumerate(level):
    if char in "DGW":
        level[x] = "."
        if char == "D":
            Dragon(x)
        elif char == "G":
            Goblin(x)
        elif char == "W":
            Wolf(x)


#-------------------main loop--------------
while True:
    hero.hunger += 1
    hero.hp += 1
    if hero.poison:
        hero.hp -= 3
    for x, char in enumerate(level):
        #print(x, char)
        for monster in Monster.zoo.values():
            if monster.x == x:
                print(monster.char, end = "")
                break
        else:
            print(level[x], end = "")
       
    print()
    command = input("$: {} hunger {} hp: {} what now?".format(hero.gold, hero.hunger, hero.hp))
    hero.hunger += 1
    if command == "quit" or command == "exit":        
        break
    elif command == "a":
        hero.x -= 1
    elif command == "d":
        hero.x += 1
    elif command == "A":
        hero.x -= 3
    elif command == "D":
        hero.x += 3
    else:
        print("Press other key!")
    stuff = level[hero.x]
    if stuff == "$":
        hero.gold += 1
        level[hero.x] = "."
    elif stuff == "a":
        hero.hunger -= 10
        level[hero.x] = "."
    elif stuff == "m":
        hero.hunger -= 20
        level[hero.x] = "."
    #check monsters
    for monster in Monster.zoo.values():
        if monster.number == hero.number:
            continue
        if monster.x == hero.x:
            print("epic fight against" + monster.report())
            print("Hero wins, monster is dead")
            #kill monster
            del Monster.zoo[monster.number]
            break
