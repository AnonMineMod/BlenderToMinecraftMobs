

import bpy
import sys
import random

def closestPower2(value):
    return pow(2,ceil(log(value,2)))

def flipName(inString):
    ns=len(inString)
    endingsL=['L','l','Left','left']
    endingsR=['R','r','Right','right']
    indexlist=[1,0];
    endings=[endingsL,endingsR]
    preendings=['.','_','-']

    hitIndex=[]
    for i in range(0,2):
        for j in range(len(endings[i])):
            e=endings[i][j]
            if len(e)<=(ns-1):
                if e==inString[ns-len(e):ns]:
                    for pe in preendings:
                        if inString[ns-len(e)-1]==pe:
                            firstPart=inString[0:ns-len(e)-1]
                            outString=firstPart+pe+endings[indexlist[i]][j]
                            return outString
    if (inString.find("mirror")):
        return inString.replace("mirror","")
    else:
        return inString + "mirror"


        
class Space:
    # posx,posy = upper left corner position and also the lower posx and posy
    def __init__(self, posx, posy, width, height):
        self.x = posx
        self.y = posy
        self.height = height
        self.width = width
        
    def overlap(self,s):
        if ( (self.x + self.width) > s.x and self.x < (s.x + s.width) and (self.y + self.height) > s.y and self.y < (s.y + s.height) ):
            return True
        return False

    def include(self,s):
        if (self.x <= s.x and (self.x + self.width) >= (s.x + s.width) and self.y <= s.y and (self.y + self.height) >= (s.y + s.height)):
            return True
        return False
    def combine(self,s):
        if ((self.x == s.x) and (self.width == s.width) and (self.y + self.height) >= s.y and self.y <= (s.y + s.height) ):
            posy =  min(self.y,s.y)
            height = max(self.y+self.height,s.y+s.height) - posy
            return Space(s.x,posy,s.width,height )
        if ((self.y == s.y) and (self.height == s.height) and (self.x + self.width) >= s.x and self.x <= (s.x + s.width) ):
            posx =  min(self.x,s.x)
            width = max(self.x+self.width,s.x+s.width) - posx
            return Space(posx,s.y,width,s.height )
        return None
    def freeSpacesDivision(self,s):
        spaces = SpaceList()
        if (not self.overlap(s)):
            spaces.append(self)
            return spaces 
        else:
            left = 0
            top = 0
            right = 0
            bot = 0
            if (self.x < s.x):
                left = s.x - self.x
            if ((self.x + self.width) > (s.x + s.width)):
                right = (self.x + self.width) - (s.x + s.width)
                
            if (self.y < s.y):
                top = s.y - self.y
            if ((self.y + self.height) > (s.y + s.height)):
                bot = (self.y + self.height) - (s.y + s.height)

            if (bot!= 0):
                spaces.append(Space(self.x,s.y+s.height,self.width,bot))
            if (top!= 0):
                spaces.append(Space(self.x,self.y,self.width,top))
            if (right!= 0):
                spaces.append(Space(s.x + s.width,self.y,right,self.height))
            if (left!= 0):
                spaces.append(Space(self.x,self.y,left,self.height))

        return spaces
    def calculateArea(self):
        return self.width*self.height
    def checkPlace(self,rect):
        return (self.width >= rect.width and self.height >= rect.height)
    def draw(self,p,screen):
        p.draw.rect(screen, (255,0,0) , (self.x,self.y,self.width,self.height), 1)
    def __str__(self):
        s = "("+str(self.x)+","+str(self.y)+","+str(self.width)+","+str(self.height)+")"
        return s
    def __repr__(self):
        return self.__str__()
    
class SpaceList:
    def __init__(self):
        self.list = []
        self.rectList = []
    def clearUnuseableSpace(self,interspace=1):
        listToRemove = []
        for s in self.list:
            if (s.height <= interspace or s.width <= interspace):
                listToRemove.append(s)
            else:
                for s2 in self.list:
                    if not s is s2:
                        if s.include(s2):
                            if (s.calculateArea() == s2.calculateArea()):
                                if (not s in listToRemove and not s2 in listToRemove):
                                    listToRemove.append(s2)
                            elif (not s2 in listToRemove):
                                listToRemove.append(s2)
        for s in listToRemove:
            self.list.remove(s)
    def getFullSpaceSize(self):
        sizeX = 0
        sizeY = 0
        for r in self.rectList:
            if (r.x+r.width > sizeX):
                sizeX = r.x+r.width
            if (r.y+r.height > sizeY):
                sizeY = r.y+r.height
        return sizeX,sizeY
    def printListSizes(self):
        print("space size" + str(len(self.list)))
        print("rect size" + str(len(self.rectList)))
    def getSmallestSpaceFor(self,rect):
        areamax = sys.maxsize
        posx = 0
        posy = 0
        for s in self.list:
            area = s.calculateArea()
            if (s.checkPlace(rect) and areamax>area):
                rect.x = s.x
                rect.y = s.y
                for s2 in self.list:
                    if (s2.overlap(rect)):
                        area2 = s2.calculateArea()
                        if (area2>area):
                            area = area2
                if (areamax>area):
                    areamax = area
                    posx = s.x
                    posy = s.y
        return (posx,posy)
    
    def getBestGreedyDistanceSpaceFor(self,rect):
        maxPos = sys.maxsize
        posx = 0
        posy = 0
        for s in self.list:
            mpos = max(s.x+rect.width,s.y+rect.height)
            #print(str(s.x+rect.width) +" " +str(s.y+rect.height)+" "+str(mpos))
            if (s.checkPlace(rect) and maxPos > mpos):
                maxPos = mpos
                posx = s.x
                posy = s.y
        return (posx,posy)
        
    def append(self,space):
        self.appendSafe(space)
                
    def getList(self):
        return self.list
    
    def appendList(self,aList):
        for s in aList.getList():
            self.append(s)
            
    def appendSafe(self,space):
        toAdd = True
        listToRemove = []
        for r in self.rectList:
            if r.overlap(space):
                toAdd = False
        if (toAdd):
            for s in self.list:
                if (space.include(s)):
                    listToRemove.append(s)
                elif(s.include(space)):
                    toAdd = False
        if (toAdd):
            self.list.append(space)
                
    def removeCubeRect(self,rect):
        #self.rectList.append(rect)
        listToRemove = []
        listToAdd = []

        rect1,rect2 = rect.getFullSpace()
        self.rectList.append(rect1)
        for s in self.list:
            if (s.overlap(rect1)):
                listToRemove.append(s)
                listToAdd.append(s.freeSpacesDivision(rect1))
        for s in listToRemove:
            self.list.remove(s)
        for slist in listToAdd:
            #print("ADDING SPACES1")
            #for r in slist.getList():
            #    print(r)
            self.appendList(slist)

        self.rectList.append(rect2)
        listToRemove = []
        listToAdd = []
        
        for s in self.list:
            if (s.overlap(rect2)):
                listToRemove.append(s)
                listToAdd.append(s.freeSpacesDivision(rect2))
        for s in listToRemove:
            #print("Removing SPACES2")
            self.list.remove(s)
        for slist in listToAdd:
            #print("ADDING SPACES2")
            self.appendList(slist)
            
    def removeRect(self,rect):
        self.rectList.append(rect)
        listToRemove = []
        listToAdd = []
        
        for s in self.list:
            if (s.overlap(rect)):
                listToRemove.append(s)
                listToAdd.append(s.freeSpacesDivision(rect))
        for s in listToRemove:
            self.list.remove(s)
        for slist in listToAdd:
            self.appendList(slist)
            
    def draw(self,p,screen):
        for s in self.list:
            s.draw(p,screen)
#        for r in self.rectList:
#            r.draw(p,screen)
    
            
class cubeRect(Space):
    def __init__(self,maxX,maxY,interspace = 2):
        self.objList = []
        
        w = random.randint(0,40)
        h = random.randint(0,40)
        d = random.randint(0,40)
        self.depth = d
        self.width = w + w + d+d + interspace * 2
        self.height = d+h + interspace * 2
        self.interspace = interspace
        
        self.x = random.randint(0,maxX)
        self.y = random.randint(0,maxY)
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        
    def __init__(self,obj,interspace = 2):
        self.objList = []
        self.objList.append(obj)
        
        w = obj.dimensions[0]
        h = obj.dimensions[2]
        d = obj.dimensions[1]
        
        self.depth = d
        self.width = w + w + d+d + interspace * 2
        self.height = d+h + interspace * 2
        self.interspace = interspace
        
        self.x = 0
        self.y = 0

        if (hasattr(obj,'["texture_offset_x"]')):
            self.x = obj["texture_offset_x"]
        if (hasattr(obj,'["texture_offset_y"]')):
            self.y = obj["texture_offset_y"] 
        
        self.color = None
    
    def addObj(self,obj):
        self.objList.append(obj)
    def getObjList(self):
        return self.objList
    def getFreeSpace(self):
        return (Space(self.x,self.y,self.depth,self.depth),Space(self.x-self.depth+self.width,self.y,self.depth,self.depth))
    def getFullSpace(self):
        return (Space(self.x+self.depth,self.y,self.width-self.depth*2,self.depth),Space(self.x,self.y+self.depth,self.width,self.height-self.depth))
    def draw(self,p,screen):
        p.draw.rect(screen, self.color, (self.x+self.depth + self.interspace,self.y+self.interspace,self.width-self.depth*2-self.interspace,self.depth),0)
        p.draw.rect(screen, self.color, (self.x+self.interspace,self.y+self.depth+self.interspace,self.width-self.interspace,self.height-self.depth-self.interspace), 0)
    def overlap(self,rect):
        if (super(cubeRect, self).overlap(rect)):
            rect1,rect2 = self.getFullSpace()
            if (rect.overlap(rect1) or rect.overlap(rect2)):
                return True
            else:
                return False
        return False
    def __str__(self):
        s = "("+str(self.x)+","+str(self.y)+","+str(self.width)+","+str(self.height)+")"
        for obj in self.objList:
            s += "\n\t"+obj.name
        return s






try:
    img = bpy.data.images['TextureAtlas']
except:
    raise NameError("No texture atlas")

sizeX = img.size[0]
sizeY = img.size[1]

rectDict = {}

for obj in bpy.data.objects:
    if (obj.type == "MESH"):
        if (hasattr(obj,'["mcbox"]')):
            flippedName = flipName(obj.name)
            if (flippedName in rectDict):
                rectDict[flippedName].addObj(obj)
            else:
                rectDict[obj.name] = cubeRect(obj)

    
spaceList = SpaceList()
spaceList.append( Space(0,0,sizeX,sizeY) )    
rectList = []    
            
for key in rectDict:
    rect = rectDict[key]
    print(rect)
    posx,posy = spaceList.getBestGreedyDistanceSpaceFor(rect)
    rect.x = posx
    rect.y = posy
    spaceList.removeCubeRect(rect)
    rectList.append(rect)
    spaceList.clearUnuseableSpace()
    
    for r in rectList:
        for r2 in rectList:
            if r.overlap(r2) and r is not r2:
                print("not enough place in texture")
                print(r)
                print(r2)
    
for key in rectDict:
    rect = rectDict[key]
    for obj in rect.getObjList():
        obj["texture_offset_x"] = rect.x
        obj["texture_offset_y"] = rect.y
            

#
#
#pygame.init()
#sizeX = 680
#sizeY = 480
#
#screen = pygame.display.set_mode((sizeX,sizeY))
#screen.fill((50,50,50))
#pygame.display.update()
#

#
#rectList =[]
#
#while (True):
#    add = True
#    # check for quit events
#    for event in pygame.event.get():
#        if event.type == pygame.QUIT:
#            pygame.quit(); sys.exit();
#        
#        else :
#            if event.type == pygame.KEYDOWN:
#                keys=pygame.key.get_pressed()
#                
#                if keys[pygame.K_RIGHT]:
#                    spaceList.printListSizes()
#                    spaceList.clearUnuseableSpace()
#                    width,height = spaceList.getFullSpaceSize()
#                    spaceList.printListSizes()
#                    
#                    print("Space :" + str(width) + " " + str(height))
#                if keys[pygame.K_LEFT]:
#                    if (add):
#                        rect = cubeRect(sizeX,sizeY)
#                        rectList.append(rect)
#                        posx,posy = spaceList.getBestGreedyDistanceSpaceFor(rect)
#                        rect.x = posx
#                        rect.y = posy
#                        spaceList.removeCubeRect(rect)
#                        #space1,space2 = rect.getFreeSpace()
#                        #spaceList.append(space1)
#                        #spaceList.append(space2)
#                        print(rect)
#                        
#                        for r in rectList:
#                            for r2 in rectList:
#                                if r.overlap(r2) and r is not r2:
#                                    
#                                    screen.fill((255,255,255))
#                                    r.draw(pygame,screen)
#                                    r2.draw(pygame,screen)
#                                    spaceList.draw(pygame,screen)
#                                    pygame.display.update()
#                                    
#                                    pygame.time.wait(5000)
#                                    print("fail")
#                                    print(r)
#                                    print(r2)
#                                    pygame.quit()
#                                    sys.exit();
#                    add = False
#            else :
#                add = True
#                
#                
#    '''   
#    rect = cubeRect(sizeX,sizeY)
#    rectList.append(rect)
#    posx,posy = spaceList.getBestGreedyDistanceSpaceFor(rect)
#    rect.x = posx
#    rect.y = posy
#    spaceList.removeRect(rect)'''
##    space1,space2 = rect.getFreeSpace()
##    print("append space")
##    print (space1)
##    print (space2)
##    spaceList.append(space1)
##    spaceList.append(space2)
#    
#    # draw the updated picture
#    screen.fill((255,255,255))
#    
#    for r in rectList:
#        r.draw(pygame,screen)
#    spaceList.draw(pygame,screen)
#    
#    # update the screen
#    pygame.display.update()



    
