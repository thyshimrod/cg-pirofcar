import sys
import math
import time
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
        self.players=[]
        self.barrels = []
        self.mines = []
        self.ships=[]
        self.cannonBallExplosions=[]
        self.damage=[]
        self.cannonballs=[]

    def getScore(self):
        score = 0
        for p in self.players:
            for s in p.ships:
                #print ("HEALTH " + str(s.health),file=sys.stderr)
                if p.id == 1:
                    score==s.health + s.speed
                else:
                    score=s.health - s.speed
        return score

    def clone(self):
        cloneReferee = Referee()
        for p in self.players:
            cloneReferee.players.append(p.clone())
        for b in self.barrels:
            cloneReferee.barrels.append(b.clone())
        for m in self.mines:
            cloneReferee.mines.append(m.clone())
        for c in self.cannonballs:
            cloneReferee.cannonballs.append(c.clone())

        return cloneReferee


    def clamp(val,_min,_max):
        return max(_min,min(_max,val))

    def decrementRum(self):
        for p in self.players:
            for s in p.ships:
                s.damage(1)

    def updateInitialRum(self):
        for p in self.players:
            for s in p.ships:
                s.initialHealth = s.health

    def moveCannonballs(self):
        newCannon=[]
        for c in self.cannonballs:
            if c.remainingTurns>0:
                c.remainingTurns-=1
            if c.remainingTurns==0:
                self.cannonBallExplosions.append(c.position)
            else:
                newCannon.append(c)
        self.cannonballs=newCannon

    def applyActions(self):
        for s in self.ships:
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
                elif self.action=="Mine":
                    if ship.mineCooldown == 0:
                        target = s.stern().neighbor((s.orientation+3)%6)
                        if target.isInsideMap():
                            s.mineCooldown = Referee.COOLDOWN_MINE
                            mine = Mine(target.x,target.y)
                            self.mines.append(mine)
                elif self.action=="Fire":
                    distance=s.bow().distanceTo(s.target)
                    if s.target.isInsideMap() and distance <= Referee.FIRE_DISTANCE_MAX and s.cannonCooldown==0:
                        travelTime= (1 + s.bow().distanceTo(s.target)//3)
                        self.cannonballs.append(Cannonball(s.target.x,s.target.y,s.id,s.bow().x,s.bow().y,travelTime))
                        s.cannonCooldown = Referee.COOLDOWN_CANNON

    def checkCollisions(ship):
        bow = ship.bow()
        stern = ship.stern()
        center = ship.position

        newBarrel=[]
        for b in self.barrels:
            if b.position.equals(bow) or b.position.equals(stern) or b.position.equals(center):
                ship.heal(b.health)
            else:
                newBarrel.append(b)
        self.barrels = newBarrel

        newMines=[]
        for m in self.mines:
            mineDamage = mine.explode(self.ships,False)

            if mineDamage!=None:
                for md in mineDamage:
                    self.damage.append(md)
            else:
                newMines.append(m)
        self.mines=newMines

    def moveShips(self):
        for i in range(1,2):
            for s in self.ships:
                s.newPosition = s.position
                s.newBowCoordinate = s.bow()
                s.newSternCoordinate = s.stern()

                if i == s.speed:
                    newCoordinate = s.position.neighbor(s.orientation)
                    if newCoordinate.isInsideMap():
                        s.newPosition = newCoordinate
                        s.newBowCoordinate = newCoordinate.neighbor(s.orientation)
                        s.newSternCoordinate = newCoordinate.neighbor((s.orientation + 3)%6)
                    else:
                        s.speed=0


            collisions=[]
            collisionDetected = True
            while collisionDetected:
                collisionDetected=False
                for s in self.ships:
                    if s.newBowIntersect(self.ships):
                        collisions.append(s)
                for s in collisions:
                    s.newPosition = s.position
                    s.newBowCoordinate = s.bow()
                    s.newSternCoordinate = s.stern()
                    s.speed=0
                    collisionDetected = True

                collisions=[]

            for s in self.ships:
                s.position=s.newPosition
                self.checkCollisions(s)

    def rotateShip(self):
        for s in self.ships:
            s.newPosition = s.position
            s.newBowCoordinate = s.newBow()
            s.newSternCoordinate = s.newStern()

        collisionDetected = True
        collisions = []

        while collisionDetected:
            collisionDetected = False
            for s in self.ships:
                if s.newPositionsIntersect(self.ships):
                    collisions.append(s)

            for s in collisions:
                s.newOrientation = s.orientation
                s.newBowCoordinate = s.newBow()
                s.newSternCoordinate = s.newStern()
                s.speed=0
                collisionDetected=True

            collisions=[]

        for s in self.ships:
            s.orientation = s.newOrientation
            self.checkCollisions(s)

    def gameIsOver(self):
        for p in self.players:
            if len(p.shipsAlive) == 0 : return True

        return False

    def explodeShips(self):
        newCannon = []
        for position in self.cannonBallExplosions:
            toRemove=False
            for s in self.ships:
                if position.equals(s.bow()) or position.equals(s.stern()):
                      self.damage.append(Damage(position,Referee.LOW_DAMAGE,True))
                      s.damage(Referee.LOW_DAMAGE)
                      toRemove=True
                      break
                elif position.equals(s.position):
                    self.damage.append(Damage(position,Referee.HIGH_DAMAGE,True))
                    s.damage(Referee.HIGH_DAMAGE)
                    toRemove=True
                    break
            if toRemove==False:
                newCannon.append(position)
        self.cannonBallExplosions=newCannon

    def explodeMines(self):
        newCannon=[]
        for position in self.cannonBallExplosions:
            toRemove=False
            for mine in self.mines:
                if mine.position.equals(position):
                    mineDamage = mine.explode(self.ships,True)
                    for m in mineDamage:
                        self.damage.append(m)
                    toRemove = True
                    break
            if toRemove == False:
                newCannon.append(position)
        self.cannonBallExplosions=newCannon

    def explodeBarrels(self):
        newCannon=[]
        for c in self.cannonBallExplosions:
            newBarrel=[]
            toRemove=False
            for b in self.barrels:
                if b.position.equals(c):
                    self.damage.append(Damage(c,0,True))
                    toRemove=True
                else:
                    newBarrel.append(b)
            self.barrels=newBarrel
            if toRemove==False:
                newCannon.append(c)
        self.cannonBallExplosions=newCannon

    def updateGame(self):
        self.moveCannonballs()
        self.decrementRum()
        self.updateInitialRum()
        self.applyActions()
        self.moveShips()
        self.rotateShip()
        self.explodeShips()
        self.explodeMines()
        self.explodeBarrels()

        newShip = []
        for s in self.ships:
            if s.health <=0:
                reward = min(Referee.REWARD_RUM_BARREL_VALUE, s.initialHealth)
                if reward>0:
                    self.barrels.append(RumBarrel(s.position.x,s.position.y,reward))
                self.players.get(s.owner).shipsAlive.remove(s)
            else:
                newShip.append(s)
        self.ships=newShip

        for position in self.cannonBallExplosions:
            self.damage.append(Damage(position,0,False))

        #if self.gameIsOver()==True:
        #    print ("END REACHED",file=sys.stderr)






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
        return ((abs(self.x - dst.x) + abs(self.y-dst.y) + abs(self.z-dst.z))//2)



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
            newY = self.y + Coord.DIRECTIONS_ODD[orientation][1]
            newX = self.x + Coord.DIRECTIONS_ODD[orientation][0]
        else:
            newY = self.y + Coord.DIRECTIONS_EVEN[orientation][1]
            newX = self.x + Coord.DIRECTIONS_EVEN[orientation][0]

        return Coord(newX,newY)

    def isInsideMap(self):
        return ((self.x >= 0) and (self.x < Coord.MAP_WIDTH) and self.y>=0 and self.y < Coord.MAP_HEIGHT)

    def distanceTo(self,dst):
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

    def clone(self):
        return RumBarrel(self.position.x,self.position.y,self.health)

class Mine(Entity):
    def __init__(self,x,y):
        super().__init__("Mine",x,y)

    def clone(self):
        return Mine(self.position.x,self.position.y)


    def explode(self,ships,force):
        damage = []
        victim = None

        for s in ships:
            if self.position.equals(s.bow()) or self.position.equals(s.stern()) or self.position.equals(s.position):
                damage.append(Damage(self.position,Referee.MINE_DAMAGE,True))
                s.damage(Referee.MINE_DAMAGE)
                victim = s

        if force or victim!=None:
            if victim==None:
                damage.append(Damage(self.position,Referee.MINE_DAMAGE,True))
            for s in ships:
                if s!=victim:
                    impactPosition = None
                    if s.stern().distanceTo(position) <=1: impactPosition=s.stern()
                    if s.bow().distanceTo(position)<=1 : impactPosition=s.bow()
                    if s.position.distanceTo(position) <= 1: impactPosition = s.position

                    if impactPosition != None:
                        s.damage(Referee.NEAR_MINE_DAMAGE)
                        damage.append(Damage(impactPosition,Referee.NEAR_MINE_DAMAGE,True))

        return damage

class Cannonball(Entity):
    def __init__(self,row,col,ownerId,srcX,srcY,remainingTurns):
        self.ownerEntityId = ownerId
        self.srcX=srcX
        self.srcY=srcY
        self.initialRemainingTurns = self.remainingTurns = remainingTurns
        self.orientation=-1
        super().__init__("CannonBall",row,col)


    def defineOrientation(self,x,y):
        xx = self.position.x - x
        yy = self.position.y - y

        print ("defineOrientation " + str(xx) + "//" + str(yy),file=sys.stderr)
        if yy == 0:
            if xx<0: self.orientation = 3
            if xx>0: self.orientation = 0
        elif yy>0:
            if xx<0: self.orientation = 4
            if xx>0: self.orientation = 5
        elif yy<0:
            if xx<0: self.orientation = 2
            if xx>0: self.orientation = 1


    def clone(self):
        return Cannonball(self.position.x,self.position.y,self.ownerEntityId,0,0,self.remainingTurns)


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
        self.x=x
        self.y=y
        self.lastTurnShoot=0
        super().__init__("Ship",x,y)


    def clone(self):
        cloneShip = Ship(self.position.x,self.position.y,self.orientation,self.owner)
        cloneShip.speed = self.speed
        cloneShip.action = self.action
        cloneShip.initialHealth = self.initialHealth
        cloneShip.health = self.health
        cloneShip.id = self.id
        return cloneShip


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
                    return True
            return False
        else:
            return self.newBowCoordinate != None and (self.newBowCoordinate.equals(other.newBowCoordinate) or newBowCoordinate.equals(other.newPosition) or self.newBowCoordinate.equals(other.newSternCoordinate))

    def newPositionsIntersect(self,other):
        if type(other) is list:
            for o in other:
                if self != o and self.newPositionsIntersect(o):
                    return True
            return False
        else:
            sternCollision = self.newSternCoordinate != None and (self.newSternCoordinate.equals(other.newBowCoordinate) or self.newSternCoordinate.equals(other.newPosition) or self.newSternCoordinate.equals(other.newSternCoordinate))
            centerCollision = self.newPosition != None and (self.newPosition.equals(other.newBowCoordinate))

            return self.newBowIntersect(other) or sternCollision or centerCollision

    def damage(self,health):
        self.health-=health
        if self.health<=0: self.health=0

    def heal(self,health):
        self.health+=health
        if self.health>Referee.MAX_SHIP_HEALTH: self.health=Referee.MAX_SHIP_HEALTH

    def fire(self,x,y):
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

    def clone(self):
        clonePlayer = Player(self.id)
        for s in self.ships:
            cloneShip=s.clone()
            clonePlayer.ships.append(cloneShip)
        return clonePlayer

class Damage:
    def __init__(self,position,health,hit):
        self.position = position
        self.health = health
        self.hit = hit


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



def fireOn(tgt,dist):
    if True:
        temps = math.floor(1 + dist/3)
        tgtBow=tgt.bow()
        print("FIREON " + str(tgt.position.x) +"@" + str(tgt.position.y) + "/" + str(tgtBow.x) +"@" + str(tgtBow.y) + "/" + str(tgt.orientation) + "S" + str(tgt.speed),file=sys.stderr)

        xx=tgt.x
        yy=tgt.y
        factor=math.floor(tgt.speed*temps)
        if tgt.orientation==1 and xx>1 and yy<20:
            xx-=factor
            yy+=factor
        elif tgt.orientation==0 and xx<22:
            xx+=factor
        elif tgt.orientation==5 and xx<22 and yy<20:
            xx+=factor
            yy+=factor
        elif tgt.orientation==4 and xx>1 and yy<20:
            xx-=factor
            yy+=factor
        elif tgt.orientation==3 and xx>1:
            xx-=factor
        elif tgt.orientation==2 and xx>1 and yy>1:
            xx-=factor
            yy-=factor
        print ("FireON " + str(xx) + "//" + str(yy),file=sys.stderr)

    else:
        if tgt.speed==0:
            xx=tgt.x
            yy=tgt.y
        elif tgt.speed==1:
            bo=tgt.bow()
            xx=bo.x
            yy=bo.y
        else:
            bo=tgt.bow().neighbor(tgt.orientation)
            xx=bo.x
            yy=bo.y

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
    return target,minDistance



lastTurnShoot=0
lastTurnMine=0
actualTurn=0
Insult()
listOfShip=[]
listOfCannonBalls=[]
while True:
    map=[[0  for x in range(23)]  for x in range(20)]
    for i in range(20):
        for j in range(23):
            map[i][j]=0
    mainReferee = Referee()
    ships=[]
    cannonBalls=[]
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
            for s in listOfShip:
                if s.id == entity_id:
                    temp=s
                    break
            if temp==None:
                temp = Ship(x,y,arg_1,arg_4)

            temp.id = entity_id
            temp.health = arg_3
            temp.speed = arg_2
            temp.orientation = arg_1
            ships.append(temp)
            temp.x=x
            temp.y=y
            temp.position.x=x
            temp.position.y=y
        elif entity_type=="MINE":
            temp = Mine()
            temp.x=x
            temp.y=y
            Mine.listOfMines.append(temp)
        elif entity_type == "CANNONBALL":

            temp = Cannonball(x,y,arg_1,0,0,arg_2)
            temp.id=entity_id
            mainReferee.cannonballs.append(temp)


    listOfShip=ships
    i=0
    targetedShip=None
    for s in listOfShip:
        targetedShip=None
        if s.owner == 1 :
            insult = Insult.instance.getInsult()
            i+=1
            action=False
            for m in mainReferee.mines:
                bowpos = s.bow()
                if bowpos.position.equals(m.position):
                    action=True
                    print("PORT")
                    break
            for c in mainReferee.cannonballs:
                if  c.remainingTurns<=2:
                    if c.remainingTurns == 1:
                        sbowPos = s.bow()
                        if c.position.equals(sbowPos):
                            print("FASTER")
                            action=True
                            break
                    elif c.remainingTurns == 2:
                        sbowPos = s.bow().neighbor(s.orientation)
                        if c.position.equals(sbowPos):
                            print("PORT")
                            action=True
                            break

            if action==False and s.health > 30 and my_ship_count>1 :#and i< math.floor(my_ship_count/2):
                if targetedShip==None:
                    diMin = 9999
                    for ss in listOfShip:
                        if ss.owner == 0 and ss.health>0:
                            #d = calcDistance(s,ss)
                            d = s.position.distanceTo(ss.position)
                            if d < diMin:
                                targetedShip = ss
                if targetedShip!=None:
                    #distance = calcDistance(s,targetedShip)
                    distance = s.position.distanceTo(targetedShip.position)
                    print("distance " + str(distance),file=sys.stderr)
                    if distance <=7 and ((s.lastTurnShoot+2) < actualTurn):
                        xx,yy = fireOn(targetedShip,distance)
                        print("FIRE " + str(xx) + " " + str(yy)  + insult)
                        s.lastTurnShoot=actualTurn
                    elif distance <=2:
                        bobo=targetedShip.bow().neighbor(targetedShip.orientation)
                        if bobo.equals(s.stern()):
                            print("MINE")
                        else:
                            print("STARBOARD")
                    else:
                        t,dist = lessDistance(s)
                        if dist<=2:
                            print ("MOVE " + str(t.x) + " " + str(t.y)  + insult)
                        else:
                            shortTgt=None
                            for ss in listOfShip:
                                if ss.owner == 0 and ss.health>0:
                                    #d = calcDistance(s,ss)
                                    d = s.position.distanceTo(ss.position)
                                    if d < 6:
                                        shortTgt = ss
                                        break
                            if shortTgt!=None and ((s.lastTurnShoot+2) < actualTurn):
                                xx,yy = fireOn(shortTgt,distance)
                                print("FIRE " + str(xx) + " " + str(yy)  + insult)
                                s.lastTurnShoot=actualTurn
                            else:
                                print("MOVE " + str(targetedShip.x) + " " + str(targetedShip.y)  + insult)

            else:

                if (s.lastTurnShoot+1) < actualTurn:
                    for ss in listOfShip:
                        if ss.owner == 0 and ss.health>0:
                            #d = calcDistance(s,ss)
                            d = s.position.distanceTo(ss.position)
                            if d <= 6:
                                xx,yy = fireOn(ss,d)
                                print("FIRE " + str(xx) + " " + str(yy)  + insult)
                                action=True
                                s.lastTurnShoot = actualTurn
                                break
                if action==False:
                    t, dist = lessDistance(s)
                    if t!=None:
                        print ("MOVE " + str(t.x) + " " + str(t.y)  + insult)
                    else:
                        for ss in listOfShip:
                            if ss.owner==0:
                                print("MOVE " + str(ss.x) + " " + str(ss.y)  + insult)

        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr)

        # Any valid action, such as "WAIT" or "MOVE x y"
        #print("MOVE 11 10")
    actualTurn+=1
