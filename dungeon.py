import random

dungeon = """
#######################################################
#.WW.$$$..D.........a....G.#.....$.m.G....#....W..P...#
##############.###########.#$................#........#
#..D..D...$$$#.###########.............####...........#
#....#########.##..$$$...####.........................#
#....#..WW.....######....#.D.............#............#
#..GG#..........#.......#.............................#
#.............#.#.......#.W........G............#######
###############.#.............................#.......#
#$$$.mm....D..................................#.###.#.#
#.##############..............................#.....#.#
#................................####################.#
#.....................................................#
#................................#.#######............#
#................................#.......#..........#.#
#................................#.......#...########.#
#................................#...........#..D..G..#
#................................#........####.#..WD..#
#.............................####........#....#D.W...#
#...................##############........#.###########
#...................#mm$..................#......$$$$$#
#######################################################
"""
hfood = {"a":"apple","m":"meat",}
level = []
for line in dungeon.splitlines():
    level.append(list(line))

class Monster():
    number = 0
    zoo = {}
    chars = ""
    
    def __init__(self, posx = 0, posy = 0, char = "M", name = "Monster", hp = 20,
                 tohit = 0.6, evade = 0.2, maxdamage = 5):
        self.x = posx
        self.y = posy
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
        self.name, self.hp, self.tohit, self.evade, self.maxdamage)
        
    def walk(self):
        return random.choice((-1, 0, 1)), random.choice((-1, 0, 1))
        
class Hero(Monster):
    def __init__(self):
        Monster.__init__(self, 1, 2, "@", "hero", 20, 0.7, 0.3, 5)
        self.hunger = 0
        self.gold = 0
        self.poison = False
        
    def walk(self):
        pass
        
class Dragon(Monster):
    def __init__(self, posx, posy):
        Monster.__init__(self, posx, posy, "D", "Dragon", 50, 0.8, 0.1, 7)
        
class Goblin(Monster):
    def __init__(self, posx, posy):
        Monster.__init__(self, posx, posy, "G", "Goblin", 10, 0.4, 0.5, 3)
        
class Wolf(Monster):
    def __init__(self, posx, posy):
        Monster.__init__(self, posx, posy, "W", "Wolf", 8, 0.6, 0.6, 2)

#generate monsters

hero = Hero()
for y, line in enumerate(level):
    for x, char in enumerate(line):
        if char in "DGW":
            level[y][x] = "."
            if char == "D":
                Dragon(x,y)
            elif char == "G":
                Goblin(x,y)
            elif char == "W":
                Wolf(x,y)


#-------------------main loop--------------
while True:
    hero.hunger += 1
    hero.hp += 1
    if hero.poison:
        hero.hp -= 3

    for y, line in enumerate(level):
        for x, char in enumerate(line):
            #print(x, char)
            for monster in Monster.zoo.values():
                if monster.x == x and monster.y == y:
                    print(monster.char, end = "")
                    break
            else:
                print(level[y][x], end = "")
           
        print()
    command = input("$: {} hunger {} hp: {} what now?".format(hero.gold, hero.hunger, hero.hp))
    hero.hunger += 1
    dx = 0 
    dy = 0
    if command == "quit" or command == "exit":        
        break
    elif command == "a":
        dx = -1
       # hero.x -= 1
    elif command == "d":
        dx = 1
       # hero.x += 1
    elif command == "A":
        dx = -3
       # hero.x -= 3
    elif command == "D":
        dx = 3
       # hero.x += 3
    elif command == "w":
        dy = -1
    elif command == "s":
        dy = 1
    else:
        print("Press other key!")
    #---------wall check-----------
    if level[hero.y+dy][hero.x+dx] == "#":
        print("Ouch!")
        dx = 0
        dy = 0
    # ------ movement--------  
    hero.x += dx
    hero.y += dy
         
    stuff = level[hero.y][hero.x]
    if stuff == "$":
        hero.gold += 1
        level[hero.y][hero.x] = "."
    elif stuff == "a":
        hero.hunger -= 10
        level[hero.y][hero.x] = "."
    elif stuff == "m":
        hero.hunger -= 20
        level[hero.y][hero.x] = "."
    #check monsters
    for monster in Monster.zoo.values():
        if monster.number == hero.number:
            continue
        if monster.x == hero.x and monster.y == hero.y:
            print("epic fight against" + monster.report())
            print("Hero wins, monster is dead")
            #kill monster
            del Monster.zoo[monster.number]
            break
        dx, dy = monster.walk()
        if level[monster.y + dy][monster.x + dx] == "#":
            dy = 0
            dx = 0
        monster.x += dx
        monster.y += dy
