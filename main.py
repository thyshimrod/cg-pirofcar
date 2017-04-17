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
        self.matrix=[[0  for x in range(21)]  for y in range(23)]

class Ship:
    listOfShip=[]
    def __init__(self):
        self.x=0
        self.y=0
        self.stock=0
        self.owner=0
        self.matrix=[[0  for x in range(21)]  for y in range(23)]

    def checkBestCoordinate(self,factor):
        valMax=0
        x=y=-1
        if self.y>0:
            print(str(self.y) + "// " + str(self.matrix[x][y-1]),file=sys.stderr)
            if valMax<self.matrix[x][y-1]:
                valMax=self.matrix[x][y-1]
                x=self.x
                y=self.y-1
            if self.x>0:
                if valMax<self.matrix[x-1][y-1]:
                    valMax=self.matrix[x-1][y-1]
                    x=self.x-1
                    y=self.y-1
            if self.x<22:
                if valMax<self.matrix[x+1][y-1]:
                    valMax=self.matrix[x+1][y-1]
                    x=self.x+1
                    y=self.y-1
        if self.y<20:
            if valMax<self.matrix[x][y+1]:
                valMax=self.matrix[x][y+1]
                x=self.x
                y=self.y+1
            if self.x>0:
                if valMax<self.matrix[x-1][y+1]:
                    valMax=self.matrix[x-1][y+1]
                    x=self.x-1
                    y=self.y+1
            if self.x<22:
                if valMax<self.matrix[x+1][y-1]:
                    valMax=self.matrix[x+1][y+1]
                    x=self.x+1
                    y=self.y+1
        if self.x>0:
            if valMax<self.matrix[x-1][y]:
                valMax=self.matrix[x-1][y]
                x=self.x-1
                y=self.y
        if self.x<22:
            if valMax<self.matrix[x+1][y]:
                valMax=self.matrix[x+1][y]
                x=self.x+1
                y=self.y

        return x,y

class Mine:
    listOfMines=[]
    def __init__(self):
        self.x=0
        self.y=0
        self.matrix=[[0  for x in range(21)]  for y in range(23)]

# game loop
def fillMatrix(matrix,value,x,y,factor):
    #print("FilleMatrix" + str(x) + "//" + str(y) +"//" + str(value),file=sys.stderr)
    if matrix[x][y]<value:
        matrix[x][y]=value
    dec,value=math.modf(value*factor)
    value= int(value)
    #print("modf " + str(value),file=sys.stderr)
    if value>2:
        if (x-1>=0):
            fillMatrix(matrix,value,x-1,y,factor)
        if ((x+1)<23):
            fillMatrix(matrix,value,x+1,y,factor)
        if (x-1>=0) and (y-1>=0):
            fillMatrix(matrix,value,x-1,y-1,factor)
        if (x-1>=0) and (y+1<21):
            fillMatrix(matrix,value,x-1,y+1,factor)
        if  (y+1<21):
            fillMatrix(matrix,value,x,y+1,factor)
        if  (y-1>=0):
            fillMatrix(matrix,value,x,y-1,factor)
        if (x+1<23) and (y-1>=0):
            fillMatrix(matrix,value,x+1,y-1,factor)
        if ((x+1)<23) and (y+1<21):
            fillMatrix(matrix,value,x+1,y+1,factor)



def calcDistance(a,b):
    aa=a.x-b.x
    aa*=aa
    bb=a.y-b.y
    bb*=bb
    distance = math.sqrt(aa+bb)
    distance= abs(a.x-b.x) + abs(a.y-b.y)
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

def addMatrix(mat1,mat2,factor):
    for i in range(23):
        for j in range(21):
            mat1[i][j]+=factor*mat2[i][j]

    return mat1


lastTurnShoot=0
lastTurnMine=0
actualTurn=0

while True:
    targetedShip=None
    map=[[0  for x in range(23)]  for y in range(21)]
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
            #print("Barre",file=sys.stderr)
            fillMatrix(temp.matrix,100,x,y,0.3)
        elif entity_type =="SHIP":
            temp = Ship()
            temp.x = x
            temp.y = y
            temp.owner = arg_4
            temp.stock = arg_3
            Ship.listOfShip.append(temp)
            #fillMatrix(temp.matrix,100,x,y,0.6)
        elif entity_type=="MINE":
            temp = Mine()
            temp.x=x
            temp.y=y
            Mine.listOfMines.append(temp)
            #fillMatrix(temp.matrix,100,x,y,0.5)



    for s in Ship.listOfShip:
        if s.owner == 1 :
            for b in Barrel.listOfBarrels:
                s.matrix=addMatrix(s.matrix,b.matrix,1)
            x,y=s.checkBestCoordinate()
            print("MOVE " + str(x) + " " + str(y))
            print(s.matrix,file=sys.stderr)

    
