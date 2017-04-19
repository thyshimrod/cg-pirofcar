import sys
import math
from random import randint

class Insult:
    listOfInsult=[]
    instance = None
    def __init__(self):
        Insult.listOfInsult.append(" We’ll hang ye by the gibbet")
        Insult.listOfInsult.append(" I’ll plunder yer coffer")
        Insult.listOfInsult.append(" I’ll reduce yer ship to rubble")
        Insult.listOfInsult.append(" A black spot upon thee")
        Insult.listOfInsult.append(" Yer doom be at hand")
        Insult.listOfInsult.append(" Hands off me booty")
        Insult.listOfInsult.append(" Swim with the fishes")
        Insult.listOfInsult.append(" We’ll dance the hornpipe over yer grave")
        Insult.listOfInsult.append(" Prepare for yer doom")
        Insult.listOfInsult.append(" Enough with yer bilge")
        Insult.listOfInsult.append(" Dead men tell no tales")
        Insult.listOfInsult.append(" Surrender or die")
        Insult.listOfInsult.append(" Walk the plank")
        Insult.instance = self

    def getInsult(self):
        val = randint(0,1)
        if val ==1 :
            val = randint(0,len(Insult.listOfInsult)-1)
            return Insult.listOfInsult[val]
        else:
            return ""

######################################################################
########################## REFEREE ###################################
######################################################################
class Referee:
    MAP_WIDTH = 23
    MAP_HEIGHT = 21
    COOLDOWN_CANNON = 2
    COOLDOWN_MINE = 5
    INITIAL_SHIP_HEALTH = 100
    MAX_SHIP_HEALTH = 100
    MAX_SHIP_SPEED = 2
    MIN_SHIPS = 1
    MAX_SHIPS = 3
    MIN_MINES = 5
    MAX_MINES = 10
    MIN_RUM_BARRELS = 10
    MAX_RUM_BARRELS = 26
    MIN_RUM_BARREL_VALUE = 10
    MAX_RUM_BARREL_VALUE = 20
    REWARD_RUM_BARREL_VALUE = 30
    MINE_VISIBILITY_RANGE = 5
    FIRE_DISTANCE_MAX = 10
    LOW_DAMAGE = 25
    HIGH_DAMAGE = 50
    MINE_DAMAGE = 25
    NEAR_MINE_DAMAGE = 10
    CANNONS_ENABLED = True
    MINES_ENABLED = True

    def __init__(self):
        self.player=None
        self.IA=None
        self.barrels = []
        self.mines = []
        self.ships=[]

    def clamp(val,_min,_max):
        return max(_min,min(_max,val))

    def decrementRum(self):
        for s in self.player.ships:
            s.damage(1)
        for s in self.IA.ships:
            s.damage(1)

    def updateInitialRum(self):
        for s in self.player.ships:
            s.initialHealth = s.health
        for s in self.IA.ships:
            s.initialHealth = s.health

    def applyActions(self):
        for s in ships:
            if s.mineCooldown > 0 : s.mineCooldown-=1
            if s.cannonCooldown > 0 : s.cannonCooldown-=1

            s.newOrientation = s.orientation

            if self.action!="" and self.action!=None:
                if self.action=="Faster":
                    if s.speed < Referee.MAX_SHIP_SPEED: s.speed+=1
                elif self.action == "Slower":
                    if s.speed > 0: s.speed-=1
                elif self.action=="Port": s.orientation = (s.orientation +1)%6
                elif self.action=="Starboard": s.orientation = (s.orientation +5)%6




####################### COORD ########################################
class CubeCoordinate:
    directions = [ [ 1, -1, 0 ], [ +1, 0, -1 ], [ 0, +1, -1 ], [ -1, +1, 0 ], [ -1, 0, +1 ], [ 0, -1, +1 ] ]
    def __init__(self,xp,yp,zp):
        self.x = xp
        self.y = yp
        self.z = zp

    def toOffsetCoordinate(self):
        newX = self.x + (self.z - (self.z & 1)) // 2
        newY = self.z

        return Coord(newX,newZ)

    def neighbor(self,orientation):
        nx = self.x + directions[orientation[0]]
        ny = self.y + directions[orientation[1]]
        nz = self.z + directions[orientation[2]]

        return CubeCoordinate(nx,ny,nz)

    def distanceTo(self,dst):
        return ((abs(x - dst.x) + abs(y-dst.y) + abs(z-dst.z))//2)



####################### COORD ########################################
class Coord:
    DIRECTIONS_EVEN = [ [ 1, 0 ], [ 0, -1 ], [ -1, -1 ], [ -1, 0 ], [ -1, 1 ], [ 0, 1 ] ]
    DIRECTIONS_ODD = [ [ 1, 0 ], [ 1, -1 ], [ 0, -1 ], [ -1, 0 ], [ 0, 1 ], [ 1, 1 ] ]

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def setCoord(self,other):
        self.x = other.x
        self.y = other.y

    def equals(self,other):
        return self.y == other.y and self.x == other.x

    def angle(tgt):
        dy  = (tgt.y - self.y) * math.sqrt(3)/2
        dx = tgt.x - self.x + ((self.y-tgt.y) & 1) * 0.5
        angle = -math.atan2(dy,dx) * 3 / math.pi
        if angle < 0:
            angle+=6
        elif angle >= 6:
            angle-=6

        return angle

    def toCubeCoordinate(self):
        xp = self.x - (self.y - (self.y & 1)) /2
        zp = self.y
        yp = -(xp+zp)
        return CubeCoordinate(xp,yp,zp)

    def neighbor(self,orientation):
        if self.y%2 ==1 :
            newY = self.y + DIRECTIONS_ODD[orientation][1]
            newX = self.x + DIRECTIONS_ODD[orientation][0]
        else:
            newY = self.y + DIRECTIONS_EVEN[orientation][1]
            newX = self.x + DIRECTIONS_EVEN[orientation][0]

        return Coord(newX,newY)

    def isInsideMap(self):
        return ((self.x >= 0) and (self.x < Coord.MAP_WIDTH) and self.y>=0 and self.y < Coord.MAP_HEIGHT)

    def distanceTo(dst):
        return self.toCubeCoordinate().distanceTo(dst.toCubeCoordinate())

########################### Entity #####################################

class Entity:
    def __init__(self,_type,x,y):
        self.id=0
        self.type=_type
        self.position=Coord(x,y)

class RumBarrel( Entity):
    def __init__(self,x,y,health):
        self.health=health
        super().__init__("Barrel",x,y)

class Ship(Entity):
    def __init__(self,x,y,orientation,owner):
        self.orientation=orientation
        self.newPosition=None
        self.newOrientation=None
        self.newBowCoordinate=None
        self.owner=owner
        self.speed=0
        self.action=""
        self.target = None
        self.initialHealth=0
        self.health=Referee.INITIAL_SHIP_HEALTH
        super().__init__("Ship",x,y)

    def moveTo(self,x,y):
        currentPosition = self.position
        targetPosition = Coord(x,y)

        if currentPosition.equals(targetPosition):
            self.action="Slower"
            return

        if self.speed == 2:
            self.action="Slower"
        elif self.speed == 1:
            currentPosition = currentPosition.neighbor(self.orientation)
            if(currentPosition.isInsideMap()):
                self.action="Slower"
            if currentPosition.equals(targetPosition):
                self.action=""

            targetAngle = currentPosition.angle(targetPosition)
            angleStraight = min(abs(self.orientation-targetAngle),6-abs(self.orientation-targetAngle))
            anglePort = min(abs(self.orientation+1-targetAngle),abs(self.orientation-5-targetAngle))
            angleStarboard = min(abs(self.orientation+5 - targetAngle),abs(self.orientation-1-targetAngle))

            centerAngle = currentPosition.angle(Coord(23//2,21//2))
            anglePortCenter = min(abs(self.orientation+1 - centerAngle),abs(self.orientation-5 - centerAngle))
            angleStarboardCenter = min(abs(self.orientation+5-centerAngle),abs(self.orientation-1-centerAngle))

            if currentPosition.distanceTo(targetPosition) == 1 and angleStraight > 1.5:
                self.action = "Slower"
            else:
                distanceMin=-1
                nextPosition = currentPosition.neighbor((self.orientation+1)%6)
                if nextPosition.isInsideMap():
                    distance = nextPosition.distanceTo(targetPosition)
                    if distanceMin == -1 or distance < distanceMin or distance == distanceMin and anglePort < (angleStraight-0.5):
                        distanceMin = distance
                        self.action = "Port"

                nextPosition = currentPosition.neighbor((self.orientation+5)%6)
                if nextPosition.isInsideMap():
                    distance = nextPosition.distanceTo(targetPosition)
                    if distanceMin==-1 or distance < distanceMin or (distance == distanceMin and angleStarboard< (anglePort-0.5) and self.action == "Port") or (distance == distanceMin and angleStarboard < (angleStraight-0.5) and self.action=="") or (distance == distanceMin and self.action == "Port" and angleStarboard == anglePort and angleStarboardCenter < anglePortCenter) or (distance == distanceMin and self.action == "Port" and angleStarboard == anglePort and angleStarboardCenter == anglePortCenter and (self.orientation ==1 or self.orientation == 4)):
                        distanceMin = distanceMin
                        self.action = "Starboard"
        elif speed == 0:
            targetAngle = currentPosition.angle(targetPosition)
            angleStraight = min(abs(self.orientation-targetAngle),6-abs(self.orientation-targetAngle))
            anglePort = min(abs(self.orientation+1-targetAngle),abs(self.orientation-5-targetAngle))
            angleStarboard = min(abs(self.orientation+5 - targetAngle),abs(self.orientation-1-targetAngle))
            centerAngle=currentPosition.angle(Coord(23//2,21//2))
            anglePortCenter = min(abs(self.orientation+1 - centerAngle),abs(self.orientation-5 - centerAngle))
            angleStarboardCenter = min(abs(self.orientation+5-centerAngle),abs(self.orientation-1-centerAngle))

            forwardPosition = currentPosition.neighbor(self.orientation)

            self.action=""

            if anglePort <= angleStarboard:
                self.action = "Port"
            if angleStarboard<anglePort or angleStarboard == anglePort and angleStarboardCenter<anglePortCenter or angleStarboard == anglePort and angleStarboardCenter == anglePortCenter and (orientation==1 or orientation==4):
                self.action = "Starboard"
            if forwardPosition.isInsideMap() and angleStraight <= anglePort and angleStraight <= angleStarboard:
                self.action = "Faster"

    def faster(self):
        self.action="Faster"
    def slower(self):
        self.action="Slower"
    def port(self):
        self.action="Port"
    def starboard(self):
        self.action="Starboard"
    def placeMine(self):
        self.action="Mine"

    def stern(self):
        return self.position.neighbor((self.orientation+3)%6)

    def bow(self):
        return self.position.neighbor(self.orientation)

    def newStern(self):
        return self.position.neighbor((self.newOrientation+3)%6)

    def newBow(self):
        return self.position.neighbor(self.newOrientation)

    def at(self,coord):
        stern = stern()
        bow = bow()
        return stern != None and stern.equals(coord) or bow != None or self.position.equals(coord)

    def newBowIntersect(self,other):
        if type(other) is list:
            for s in other:
                if self != s and self.newBowIntersect(s):
                    return true
            return false
        else:
            return self.newBowCoordinate != None and (self.newBowCoordinate.equals(other.newBowCoordinate) or newBowCoordinate.equals(other.newPosition) or self.newBowCoordinate.equals(other.newSternCoordinate))

    def newPositionsIntersect(self,other):
        if type(other) is list:
            for o in other:
                if self != o and self.newPositionsIntersect(o):
                    return true
            return false
        else:
            sternCollision = self.newSternCoordinate != None and (self.newSternCoordinate.equals(other.newBowCoordinate) or self.newSternCoordinate.equals(other.newPosition) or self.newSternCoordinate.equals(other.newSternCoordinate))
            centerCollision = self.newPosition != None and (self.newPosition.equals(other.newBowCoordinate))

            return self.newBowIntersect(other) or sternCollision or centerCollision

    def damage(health):
        self.health-=health
        if self.health<=0: self.health=0

    def heal(health):
        self.health+=health
        if self.health>Referee.MAX_SHIP_HEALTH: self.health=Referee.MAX_SHIP_HEALTH

    def fire(x,y):
        target = Coord(x,y)
        self.target = target
        self.action = "Fire"

########################    PLAYER   #################################
class Player:
    def __init__(self,id):
        self.id = id
        self.ships = []
        self.shipsAlive = []

    def setDead(self):
        for s in self.ships:
            s.health=0

    def getScore(self):
        score=0
        for s in self.ships:
            score+=ship.health
        return score

######################################################################
######################################################################
######################################################################
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
class Barrel:
    listOfBarrels=[]
    def __init__(self):
        self.x=0
        self.y=0
        self.targeted=False

class ShipA:
    listOfShip=[]
    def __init__(self):
        self.stock=0
        self.owner=0
        self.orientation=0
        self.speed=0
        self.lastTurnShoot=0
        self.id=0

    def fireOn(self,tgt):
        xx=tgt.x
        yy=tgt.y
        if tgt.orientation==1 and xx>1 and yy<20:
            xx-=tgt.speed
            yy+=tgt.speed
        elif tgt.orientation==0 and xx<22:
            xx+=tgt.speed
        elif tgt.orientation==5 and xx<22 and yy<20:
            xx+=tgt.speed
            yy+=tgt.speed
        elif tgt.orientation==4 and xx>1 and yy<20:
            xx-=tgt.speed
            yy+=tgt.speed
        elif tgt.orientation==3 and xx>1:
            xx-=tgt.speed
        elif tgt.orientation==2 and xx>1 and yy>1:
            xx-=tgt.speed
            yy-=tgt.speed

        return xx,yy


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
Insult()

while True:
    map=[[0  for x in range(23)]  for x in range(20)]
    for i in range(20):
        for j in range(23):
            map[i][j]=0

    Barrel.listOfBarrels=[]
    #Ship.listOfShip = []
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
            temp=None
            for s in ShipA.listOfShip:
                if s.id == entity_id:
                    temp=s
                    break

            if temp==None:
                temp = ShipA()
                ShipA.listOfShip.append(temp)
            else:
                print("FOUND SHIP",file=sys.stderr)

            temp.id = entity_id
            temp.x = x
            temp.stock = arg_3
            temp.y = y
            temp.owner = arg_4
            temp.orientation = arg_1
            temp.speed = arg_2
        elif entity_type=="MINE":
            temp = Mine()
            temp.x=x
            temp.y=y
            Mine.listOfMines.append(temp)
    i=0
    targetedShip=None
    for s in ShipA.listOfShip:
        targetedShip=None
        if s.owner == 1 :
            insult = Insult.instance.getInsult()
            i+=1
            if s.stock > 40 and my_ship_count>1 :#and i< math.floor(my_ship_count/2):
                if targetedShip==None:
                    diMin = 9999
                    for ss in ShipA.listOfShip:
                        if ss.owner == 0 and ss.stock>0:
                            d = calcDistance(s,ss)
                            if d < diMin:
                                targetedShip = ss
                if targetedShip!=None:
                    distance = calcDistance(s,targetedShip)
                    if distance <=6 and ((s.lastTurnShoot+2) < actualTurn):
                        xx,yy = s.fireOn(targetedShip)
                        print("FIRE " + str(xx) + " " + str(yy)  + insult)
                        s.lastTurnShoot=actualTurn
                    elif distance <=2:
                        t = lessDistance(s)
                        if t!=None:
                            print ("MOVE " + str(t.x) + " " + str(t.y)  + insult)
                        else:
                            print("MOVE " + str(targetedShip.x) + " " + str(targetedShip.y)  + insult)
                    else:
                        print("MOVE " + str(targetedShip.x) + " " + str(targetedShip.y)  + insult)
            else:
                action=False
                print ("#######" + str(s.lastTurnShoot),file=sys.stderr)
                if (s.lastTurnShoot+1) < actualTurn:
                    for ss in ShipA.listOfShip:
                        if ss.owner == 0 and ss.stock>0:
                            d = calcDistance(s,ss)
                            if d <= 6:
                                xx,yy = s.fireOn(ss)
                                print("FIRE " + str(xx) + " " + str(yy)  + insult)
                                action=True
                                s.lastTurnShoot = actualTurn
                                break
                if action==False:
                    t = lessDistance(s)
                    if t!=None:
                        print ("MOVE " + str(t.x) + " " + str(t.y)  + insult)
                    else:
                        for ss in ShipA.listOfShip:
                            if ss.owner==0:
                                print("MOVE " + str(ss.x) + " " + str(ss.y)  + insult)

        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr)

        # Any valid action, such as "WAIT" or "MOVE x y"
        #print("MOVE 11 10")
    actualTurn+=1
