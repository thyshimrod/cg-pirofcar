import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
class Barrel:
    listOfBarrels=[]
    def __init__(self):
        self.x=0
        self.y=0
        self.targeted=False

class Ship:
    listOfShip=[]
    def __init__(self):
        self.x=0
        self.y=0
        self.owner=0

class Mine:
    listOfMines=[]
    def __init__(self):
        self.x=0
        self.y=0

# game loop

def calcDistance(a,b):
    aa=a.x-b.x
    aa*=aa
    bb=a.y-b.y
    bb*=bb
    distance = math.sqrt(aa+bb)
    return distance

def lessDistance(ship):
    minDistance=9999
    target=None
    for b in Barrel.listOfBarrels:
        d = calcDistance(b,ship)
        if d < minDistance and b.targeted == False:
            minDistance = d
            target = b

    if target!=None:
        target.targeted=True
    return target
lastTurnShoot=0
lastTurnMine=0
actualTurn=0
while True:
    map=[[0  for x in range(23)]  for x in range(20)]
    for i in range(20):
        for j in range(23):
            map[i][j]=0

    Barrel.listOfBarrels=[]
    Ship.listOfShip = []
    my_ship_count = int(input())  # the number of remaining ships
    entity_count = int(input())  # the number of entities (e.g. ships, mines or cannonballs)
    for i in range(entity_count):
        entity_id, entity_type, x, y, arg_1, arg_2, arg_3, arg_4 = input().split()
        entity_id = int(entity_id)
        x = int(x)
        y = int(y)
        arg_1 = int(arg_1)
        arg_2 = int(arg_2)
        arg_3 = int(arg_3)
        arg_4 = int(arg_4)
        if entity_type == "BARREL":
            temp = Barrel()
            temp.x=x
            temp.y=y
            Barrel.listOfBarrels.append(temp)
        elif entity_type =="SHIP":
            temp = Ship()
            temp.x = x
            temp.y = y
            temp.owner = arg_4
            Ship.listOfShip.append(temp)
        elif entity_type=="MINE":
            temp = Mine()
            temp.x=x
            temp.y=y
            Mine.listOfMines.append(temp)



    for s in Ship.listOfShip:
        if s.owner == 1:
            action=False
            #if 1==1:
            #if (actualTurn-2)>lastTurnShoot:

            if (actualTurn-1)>lastTurnShoot:
                for ss in Ship.listOfShip:
                    if ss.owner == 0:
                        d = calcDistance(s,ss)
                        if d <= 10:
                            print("FIRE " + str(ss.x) + " " + str(ss.y))
                            action=True
                            lastTurnShoot = actualTurn
                            break

            if action==False:
                if (actualTurn-6)>lastTurnMine:
                    print("MINE")
                    lastTurnMine=actualTurn
                    action=True
            if action==False:
                t = lessDistance(s)
                if t!=None:
                    print ("MOVE " + str(t.x) + " " + str(t.y))
                else:
                    for ss in Ship.listOfShip:
                        if ss.owner==0:
                            print("MOVE " + str(ss.x) + " " + str(ss.y))
                    #print("WAIT")

        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr)

        # Any valid action, such as "WAIT" or "MOVE x y"
        #print("MOVE 11 10")
    actualTurn+=1
