import random   
dungeon = """
#######################################################
#....$$$...........Da....G.#.....$.m.G....#....W..P...#
##############.###########.#####.............#.....####
#..D..D...$$$#.###########....s#.......####...........#
#....#########.##..$$$...####..#..................#WW.#
#....#..WW.....######....#.###.#.........#.############
#..GG########.k.#.......#.D.................#...d....s#
#.............#.#.......#.W........G..........#.#######
###############.#................#.#.........##..GG..G#
#$$$.mm....D......################.#..........#.###G#.#
#d###############.#....W..W..W.....#..........#GG.G.#.#
#.#.............#.#...W....W.....#.##################m#
#.#.............#...W...W....W...#.........#...#...#.##
#.#....:........#....W...W..W..W.#.#######.#.#...#....#
#.#.............#W...W.W....W....#..#....#.#.########.#
#.#.............################.#..#.##.....#..D..G..#
#.....................#.#.#.#.......#.########.#..WD..#
################....#D.......D####........#....#D.W...#
#v$$$#..T..#...#....##############.######.#.###########
#$$$$d.T.T...#......#mm$...........#......#......$$$$k#
#######################################################
"""
hfood = {"a":"apple","m":"meat",}
level = []
for line in dungeon.splitlines():
    level.append(list(line))

def strike(attacker, defender):
    """attacking monster strikes vs. defending monster"""
    hitdice = random.random()
    evadedice = random.random()
    damage = random.randint(1, attacker.maxdamage)
    txt=""
    txt+= "{} attacks {}! ({} hp left)\n".format(attacker.name, defender.name, defender.hp)
    if hitdice > attacker.tohit:
        txt += "The attack fails completely"
        return txt
    if evadedice < defender.evade:
        txt += "But {} manages to evade the attack!".format(defender.name)
        return txt
    txt += "Ouch! {} makes {} damage to {}.\n".format(attacker.name, damage, defender.name)
    defender.hp -= damage
    if defender.hp <= 0:
        txt +="{} is dead, {} wins!".format(defender.name, attacker.name)
    return txt

def fight(attacker, defender):
    txt = "Strike!\n"
    txt += strike(attacker, defender)
    if defender.hp <= 0:
        return txt
    txt += "Counterstrike!\n"
    txt += strike(defender, attacker)
    return txt
    
class Item():
    number = 0
    storage = {}
    
    def __init__(self, char = "x", name = "pile of junk", x = 5, y = 5):
        self.char = char
        self.name = name
        self.x = x
        self.y = y
        self.number = Item.number
        Item.number += 1
        Item.storage[self.number] = self
        
class Potion(Item):
    
    def __init__(self, char = "p", name = "strange potion", x = 5, y = 5):
        Item.__init__(self, char, name, x, y)
        self.effect_hp = random.randint(-1, 5)
        self.effect_tohit = random.random() * 0.2 -0.05
        self.effect_evade = random.random() * 0.2 -0.05
        self.effect_hunger = random.randint(-30,5)
    
    def report(self):
        txt = "This is potion number {}\n".format(self.number)
        txt += "Effect on hitpoints: {}\n".format(self.effect_hp)
        txt += "Effect on tohit chance: {}\n".format(self.effect_tohit)
        txt += "Effect on evade chance: {}\n".format(self.effect_evade)
        txt += "Effect on hunger: {}\n".format(self.effect_hunger)
        return txt
        
class hp_Potion(Potion):
	def __init__(self):
		Item.__init__(self, char = "h", name = "healthy potion", x = 5, y = 5)
		self.effect_hp = random.randint(-1, 15)


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
        Monster.__init__(self, 1, 2, "@", "hero", 3000, 0.7, 0.3, 5)
        self.hunger = 0
        self.gold = 0
        self.poison = False
        self.key = 0
        
    def walk(self):
        pass
        
class Dragon(Monster):
    """giant boss, can only go left-right"""
    def __init__(self, posx, posy):
        Monster.__init__(self, posx, posy, "D", "Dragon", 50, 0.8, 0.1, 7)
    
    def walk(self):
        return random.choice((-1, 0, 1)), 0
        
class Goblin(Monster):
    """little monster that can never stand still"""
    def __init__(self, posx, posy):
        Monster.__init__(self, posx, posy, "G", "Goblin", 10, 0.4, 0.5, 3)
        
    def walk(self):
        return random.choice((-1, 1)), random.choice((-1, 1))
        
class Wolf(Monster):
    def __init__(self, posx, posy):
        Monster.__init__(self, posx, posy, "W", "Wolf", 8, 0.6, 0.6, 2)

class Devil(Monster):
    """giant boss"""
    def __init__(self, posx, posy):
        Monster.__init__(self, posx, posy, "T", "Devil", 50, 0.8, 0.3, 10)
    def walk(self):
        return random.choice((-2,-1,0,1,2)), random.choice((-2,-1,0,1,2))
        
class Ghost(Monster):
    """small ghost, high damage"""
    def __init__(self, posx, posy):
        Monster.__init__(self, posx, posy, "S", "Ghost", 3, 0.5, 0.5, 20)
    
        
#class Ghost

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
while hero.hp >0 and hero.hunger < 1000:
    if random.random() < 0.3:
        hero.hunger += 1
    #hero.hp += 1
    #if hero.poison:
    #    hero.hp -= 3

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
    command = input("$: {}; hunger {}; hp: {}; tohit: {}; evade: {}; maxd: {}; what now?".format(hero.gold, hero.hunger, hero.hp, hero.tohit, hero.evade, hero.maxdamage))
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
    elif command == "p":
        print("You created a new potion!")
        input(Potion().report())
    else:
        print("Press other key!")
    print("hero is moving")
    #---------wall check-----------
    if level[hero.y+dy][hero.x+dx] == "#":
        print("Ouch!")
        dx = 0
        dy = 0
    if level[hero.y+dy][hero.x+dx] == "d":
        if hero.key > 0:
            hero.key -= 1
            print("You used the key to open the door")
            level[hero.y][hero.x] = "."
        else:
            print("Ouch! Find a key (k)")
            dx = 0
            dy = 0
    # ------ monster check ------
    for monster in Monster.zoo.values():
        if monster.number == hero.number:
            continue
        if monster.x == hero.x + dx and monster.y == hero.y + dy:
            # ----- hero attacks monster ------
            dx = 0
            dy = 0
            input(fight(hero, monster))
            if monster.hp <= 0:
                #kill monster
                del Monster.zoo[monster.number]
                break
            if hero.hp <= 0:
                break
    if hero.hp <= 0:
        break    
    # ------ hero movement--------  
    hero.x += dx
    hero.y += dy
    print("monsters are moving")
    dx, dy = 0, 0
    # --- check monster movement ------ 
    for monster in Monster.zoo.values():
        if monster.number == hero.number:
            continue
        dx, dy = monster.walk()
        #------wall test for monsters------
        if level[monster.y + dy][monster.x + dx] == "#":
            dy = 0
            dx = 0
        if level[monster.y + dy][monster.x + dx] == "d":
            dy = 0
            dx = 0
        #-------test if walking into other monsters
        for monster2 in Monster.zoo.values():
            if monster2.number == hero.number:
                continue
            if monster2.number == monster.number:
                continue
            if monster.y + dy == monster2.y and monster.x +dx == monster2.x:
                dx = 0
                dy = 0
        #--------monster attacking hero-----------
        if (monster.y + dy == hero.y) and (monster.x + dx == hero.x):
            dx = 0
            dy = 0
            input(fight(monster, hero))
            if monster.hp <= 0:
                #del Monster.zoo[monster.number]
                #break
                continue
            if hero.hp <= 0:
                break
        monster.x += dx
        monster.y += dy
    # ----- kill off dead monsters ------
    if hero.hp <= 0:
        break
    monsternumbers = list(Monster.zoo.keys())
    for n in monsternumbers:
        if Monster.zoo[n].hp <= 0:
            del Monster.zoo[n]
    # ------- find stuff ---------     
    stuff = level[hero.y][hero.x]
    if stuff == "$":
        hero.gold += 1
        level[hero.y][hero.x] = "."
    elif stuff == "k":
        hero.key += 1
        level[hero.y][hero.x] = "."
    elif stuff == "a":
        hero.hunger -= 10
        level[hero.y][hero.x] = "."
    elif stuff == "m":
        hero.hunger -= 20
        level[hero.y][hero.x] = "."
  
