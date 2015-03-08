import pygame
import sys
import random

def calculateSize(obj):
    foo = False
    
def addSpaceSpot():
    foo = False


        
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
        return "("+str(self.x)+","+str(self.y)+","+str(self.width)+","+str(self.height)+")"
    def __repr__(self):
        return self.__str__()
    
class SpaceList:
    def __init__(self):
        self.list = []
    def getSmallestSpaceFor(self,rect):
        areamax = sys.maxsize
        posx = 0
        posy = 0
        for s in self.list:
            if (s.checkPlace(rect) and areamax>s.calculateArea()):
                areamax = s.calculateArea()
                posx = s.x
                posy = s.y
        return (posx,posy)
                
    def append(self,space):
        toAdd = True
        listToRemove = []
        listToAdd = []
        for s in self.list:
            if (space.include(s)):
                listToRemove.append(s)
            if (s.include(space)):
                toAdd = False
            c = s.combine(space)
            if c is not None:
                if not (s in listToRemove):
                    listToRemove.append(s)
                listToAdd.append(c)
                toAdd = False
        if(toAdd):
            self.list.append(space)
        else :
            for s in listToRemove:
                self.list.remove(s)
            for s in listToAdd:
                self.list.append(s)
    def getList(self):
        return self.list
    def appendList(self,aList):
        for s in aList.getList():
            self.append(s)
            
    def removeRect(self,rect):
        listToRemove = []
        listToAdd = []
        for s in self.list:
            if (s.overlap(rect)):
                listToRemove.append(s)
                listToAdd.append(s.freeSpacesDivision(rect))
        for s in listToRemove:
            self.list.remove(s)
            print("remove")
            print(s)
        for slist in listToAdd:
            print("add")
            self.appendList(slist)
    def draw(self,p,screen):
        for s in self.list:
            s.draw(p,screen)
    
            
class cubeRect(Space):
    def __init__(self,maxX,maxY):
        w = random.randint(0,40)
        h = random.randint(0,40)
        d = random.randint(0,40)
        self.depth = d
        self.width = w + w + d+d
        self.height = d+h
        
        self.x = random.randint(0,maxX)
        self.y = random.randint(0,maxY)
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    

    def getFreeSpace(self):
        return (Space(self.x,self.y,self.depth,self.depth),Space(self.x+self.depth+2*self.width,self.y,self.depth,self.depth))
    def draw(self,p,screen):
        p.draw.rect(screen, self.color, (self.x,self.y,self.width,self.height), 0)
    def overlap(self,rect):
        if (super(cubeRect, self).overlap(rect)):
            space1,space2 = self.getFreeSpace()

            if (space1.include(rect) or space2.include(rect)):
                print("specialOverlap False")
                print(space1)
                print(space2)
                print(rect)
                return False
            else:
                print("specialOverlap True")
                print(space1)
                print(space2)
                print(rect)
                return True
        return False
    

import pygame
import sys


pygame.init()
sizeX = 680
sizeY = 480

screen = pygame.display.set_mode((sizeX,sizeY))
screen.fill((50,50,50))
pygame.display.update()

spaceList = SpaceList()
spaceList.append( Space(0,0,sizeX,sizeY) )

rectList =[]

while (True):
    add = True
    # check for quit events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit();
        else :
            if event.type == pygame.KEYDOWN:
                keys=pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    if (add):
                        rect = cubeRect(sizeX,sizeY)
                        rectList.append(rect)
                        posx,posy = spaceList.getSmallestSpaceFor(rect)
                        rect.x = posx
                        rect.y = posy
                        spaceList.removeRect(rect)
                        space1,space2 = rect.getFreeSpace()
                        spaceList.append(space1)
                        spaceList.append(space2)
                        print(rect)
                    add = False
            else :
                add = True
                
                
        
    
    # draw the updated picture
    screen.fill((255,255,255))
    
    spaceList.draw(pygame,screen)
    for r in rectList:
        for r2 in rectList:
            if r.overlap(r2) and r is not r2:
                pygame.quit()
                print("fail")
                print(r)
                print(r2)
                
        r.draw(pygame,screen)
    
    # update the screen
    pygame.display.update()



    
