


import bpy
import math
import sys
from math import floor

texMatName = 'TexMat'


def setTexture(obj):

    try:
        img = bpy.data.images['TextureAtlas']
    except:
        raise NameError("No texture atlas")
    # Create image texture from image
    bTex = bpy.data.textures.new('ColorTex', type = 'IMAGE')
    bTex.image = img

    if (not 'TexMat' in bpy.data.materials):
        # Create material
        mat = bpy.data.materials.new(texMatName)
     
        # Add texture slot 
        mtex = mat.texture_slots.add()
        mtex.texture = bTex
        mtex.texture_coords = 'UV'
        mtex.use_map_color_diffuse = True 
        mtex.diffuse_color_factor = 1.0
        mtex.blend_type = 'MIX'
        
    else:
        
        mat = bpy.data.materials[texMatName]

    me = obj.data
    me.materials.append(mat)
 
    return



def setIndividualsUvs(object_cube):
    
    try:
        img = bpy.data.images['TextureAtlas']
        textureWidth = img.size[0]
        textureHeight = img.size[1]
     
    except:
        raise NameError("No texture atlas")
        
        
    if (hasattr(object_cube,'["texture_offset_x"]')):
        texture_offset_x = object_cube["texture_offset_x"]
    else:
        texture_offset_x = 0
        object_cube["texture_offset_x"] = 0
        
    if (hasattr(object_cube,'["texture_offset_y"]')):
        texture_offset_y = object_cube["texture_offset_y"]
    else:
        texture_offset_y = 0
        object_cube["texture_offset_y"] = 0
    
    if (hasattr(object_cube,'["mirror_texture"]')):
        mirror_texture = object_cube["mirror_texture"]
    else:
        mirror_texture = False
        object_cube["mirror_texture"] = False
        
        
        
     
    me = object_cube.data
    if (len(me.uv_textures) == 0):
        me.uv_textures.new("mctexture")
    
    uv_layer = me.uv_layers.active.data

    dimensions = object_cube.dimensions

    for poly in me.polygons:
        print("Polygon index: %d, length: %d" % (poly.index, poly.loop_total))

        # range is used here to show how the polygons reference loops,
        # for convenience 'poly.loop_indices' can be used instead.
        for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
            print("    Vertex: %d" % me.loops[loop_index].vertex_index)
            #print("    UV: %r" % uv_layer[loop_index].uv[0])
            print ("    loop: %r" % loop_index) 
            
            
    # this shit help : [i.index for i in bpy.context.active_object.data.vertices if i.select] 


    width = dimensions[0]
    height = dimensions[2]
    depth = dimensions[1]
    
    

    for poly in me.polygons:
        print ("%d,%d,%d,%d" % (poly.vertices[0],poly.vertices[1],poly.vertices[2],poly.vertices[3]))
        
        if ( set(poly.vertices).issubset([0,1,2,3]) ):
            bot_face = poly.loop_start
        if ( set(poly.vertices).issubset([0,1,4,5]) ):
            left_face = poly.loop_start
        if ( set(poly.vertices).issubset([1,2,5,6]) ):
            back_face = poly.loop_start
        if ( set(poly.vertices).issubset([2,3,7,6]) ):
            right_face = poly.loop_start
        if ( set(poly.vertices).issubset([0,3,4,7]) ):
            front_face = poly.loop_start
        if ( set(poly.vertices).issubset([4,5,6,7]) ):
            top_face = poly.loop_start

    if (not mirror_texture):
        
        #LEFTFACE  (4): 
        print(str(left_face) + ', ' + str(bot_face) + ', ' +  str(back_face) + ', ' +  str(right_face) + ', ' +  str(front_face) + ', ' +  str(top_face))
        # vertice 1 
        uv_layer[left_face+0].uv[0] = 0
        uv_layer[left_face+0].uv[1] = - depth - height
        
        # vertice 0 :front bottom ouest
        uv_layer[left_face+1].uv[0] = depth 
        uv_layer[left_face+1].uv[1] = - depth - height

        # vertice 4 : front top ouest
        uv_layer[left_face+2].uv[0] = depth 
        uv_layer[left_face+2].uv[1] = - depth

        # vertice 5 
        uv_layer[left_face+3].uv[0] = 0
        uv_layer[left_face+3].uv[1] = - depth 
        

        #FRONTFACE (3): 

        # vertice 0
        uv_layer[front_face+0].uv[0] = depth 
        uv_layer[front_face+0].uv[1] = - depth - height

        # vertice 3
        uv_layer[front_face+1].uv[0] = depth+ width
        uv_layer[front_face+1].uv[1] = - depth - height

        # vertice 7
        uv_layer[front_face+2].uv[0] = depth+ width
        uv_layer[front_face+2].uv[1] = - depth

        # vertice 4
        uv_layer[front_face+3].uv[0] = depth
        uv_layer[front_face+3].uv[1] = - depth

        #BACKFACE (5) : 

        # vertice 2
        uv_layer[back_face+0].uv[0] = 2*depth + width
        uv_layer[back_face+0].uv[1] = - depth - height

        # vertice 1
        uv_layer[back_face+1].uv[0] = 2*depth + 2*width 
        uv_layer[back_face+1].uv[1] = - depth - height

        # vertice 5
        uv_layer[back_face+2].uv[0] = 2*depth + 2*width
        uv_layer[back_face+2].uv[1] = - depth

        # vertice 6
        uv_layer[back_face+3].uv[0] = 2*depth + width
        uv_layer[back_face+3].uv[1] = - depth 


        #RIGHTFACE  (3): 

        # vertice 3
        uv_layer[right_face+0].uv[0] = depth + width
        uv_layer[right_face+0].uv[1] = - depth - height
        
        # vertice 2 
        uv_layer[right_face+1].uv[0] = 2*depth + width
        uv_layer[right_face+1].uv[1] = - depth - height

        # vertice 6 
        uv_layer[right_face+2].uv[0] = 2*depth + width
        uv_layer[right_face+2].uv[1] = - depth

        # vertice 7 
        uv_layer[right_face+3].uv[0] = depth + width
        uv_layer[right_face+3].uv[1] = - depth 

        
       
        #BOTFACE  (0): 

        # vertice 1 :
        uv_layer[bot_face+0].uv[0] = depth + width
        uv_layer[bot_face+0].uv[1] =  - depth

        # vertice 2 
        uv_layer[bot_face+1].uv[0] = depth + 2 * width
        uv_layer[bot_face+1].uv[1] = - depth 

        # vertice 3 
        uv_layer[bot_face+2].uv[0] = depth + 2 * width
        uv_layer[bot_face+2].uv[1] = 0
        
        # vertice 0 :
        uv_layer[bot_face+3].uv[0] = depth + width
        uv_layer[bot_face+3].uv[1] = 0

        #TOPFACE  (1): 
        # vertice 4 
        uv_layer[top_face].uv[0] = depth
        uv_layer[top_face].uv[1] = - depth

        # vertice 7 
        uv_layer[top_face+1].uv[0] = depth + width
        uv_layer[top_face+1].uv[1] = - depth

        # vertice 6 
        uv_layer[top_face+2].uv[0] = depth + width
        uv_layer[top_face+2].uv[1] = 0

        # vertice 5
        uv_layer[top_face+3].uv[0] = depth
        uv_layer[top_face+3].uv[1] = 0
        
        
        
    #####################################
    #####################################
    #       Mirrored texture            #
    #####################################
    #####################################
    
    else:
        
        #right_face  (4): 
        
        # vertice  1 right_face
        uv_layer[right_face+0].uv[0] = depth 
        uv_layer[right_face+0].uv[1] = - depth - height
        
        # vertice 0 :
        uv_layer[right_face+1].uv[0] = 0 
        uv_layer[right_face+1].uv[1] = - depth - height

        # vertice 4 :
        uv_layer[right_face+2].uv[0] = 0
        uv_layer[right_face+2].uv[1] = - depth

        # vertice 5 
        uv_layer[right_face+3].uv[0] = depth 
        uv_layer[right_face+3].uv[1] = - depth 
        

        #FRONTFACE (3): 

        # vertice 0
        uv_layer[front_face+0].uv[0] = depth + width
        uv_layer[front_face+0].uv[1] = - depth - height

        # vertice 3
        uv_layer[front_face+1].uv[0] = depth
        uv_layer[front_face+1].uv[1] = - depth - height

        # vertice 7
        uv_layer[front_face+2].uv[0] = depth
        uv_layer[front_face+2].uv[1] = - depth

        # vertice 4
        uv_layer[front_face+3].uv[0] = depth + width
        uv_layer[front_face+3].uv[1] = - depth

        #BACKFACE (5) : 

        # vertice 2
        uv_layer[back_face+0].uv[0] = 2*depth + 2*width
        uv_layer[back_face+0].uv[1] = - depth - height

        # vertice 1
        uv_layer[back_face+1].uv[0] = 2*depth + width 
        uv_layer[back_face+1].uv[1] = - depth - height

        # vertice 5
        uv_layer[back_face+2].uv[0] = 2*depth + width
        uv_layer[back_face+2].uv[1] = - depth

        # vertice 6
        uv_layer[back_face+3].uv[0] = 2*depth + 2*width
        uv_layer[back_face+3].uv[1] = - depth 


        #left_face  (3): 

        # vertice 3
        uv_layer[left_face+0].uv[0] = 2*depth + width
        uv_layer[left_face+0].uv[1] = - depth - height
        
        # vertice 2 
        uv_layer[left_face+1].uv[0] = depth + width
        uv_layer[left_face+1].uv[1] = - depth - height

        # vertice 6 
        uv_layer[left_face+2].uv[0] = depth + width
        uv_layer[left_face+2].uv[1] = - depth

        # vertice 7 
        uv_layer[left_face+3].uv[0] = 2*depth + width
        uv_layer[left_face+3].uv[1] = - depth 

        
       
        #BOTFACE  (0): 

        # vertice 1 :
        uv_layer[bot_face+0].uv[0] = depth + 2 * width
        uv_layer[bot_face+0].uv[1] =  - depth

        # vertice 2 
        uv_layer[bot_face+1].uv[0] = depth + width
        uv_layer[bot_face+1].uv[1] = - depth 

        # vertice 3 
        uv_layer[bot_face+2].uv[0] = depth + width
        uv_layer[bot_face+2].uv[1] = 0
        
        # vertice 0 :
        uv_layer[bot_face+3].uv[0] = depth + 2 * width
        uv_layer[bot_face+3].uv[1] = 0

        #TOPFACE  (1): 
        # vertice 4 
        uv_layer[top_face].uv[0] = depth + width
        uv_layer[top_face].uv[1] = - depth

        # vertice 7 
        uv_layer[top_face+1].uv[0] = depth 
        uv_layer[top_face+1].uv[1] = - depth

        # vertice 6 
        uv_layer[top_face+2].uv[0] = depth 
        uv_layer[top_face+2].uv[1] = 0

        # vertice 5
        uv_layer[top_face+3].uv[0] = depth + width
        uv_layer[top_face+3].uv[1] = 0
        
        

        
    for uvs in uv_layer:
        uvs.uv[0] = uvs.uv[0]/textureWidth + texture_offset_x/textureWidth
        uvs.uv[1] = uvs.uv[1]/textureHeight + 1 - texture_offset_y/textureHeight




def createTexture():
    
    try:
        image = bpy.data.images['TextureAtlas']
    except:
        raise NameError("No texture atlas")
        
    texWidth = image.size[0]
    texHeight = image.size[1]
    
    pixels = [0.0] * (4 * texWidth * texHeight)
        
    for obj in bpy.data.objects:
        if (hasattr(obj,'["mcbox"]')):
            
            width = int(round(obj.dimensions[0]))
            height = int(round(obj.dimensions[2]))
            depth = int(round(obj.dimensions[1]))          
            
            texOffsetX = int(round(obj['texture_offset_x']))
            texOffsetY = int(round(obj['texture_offset_y']))
            
            initY = texHeight - texOffsetY - height - depth
            a = 1.0
            for i in range ( height ) :
                initX = texOffsetX
                for j in range (depth):
                    r = 0.5
                    pixels[((initY + i )* texWidth + j+initX )*4 + 0] = r
                    pixels[((initY + i )* texWidth + j+initX )*4 + 3] = a
                initX += depth
                for j in range (width):
                    b = 0.5
                    pixels[((initY + i )* texWidth + j+initX )*4 + 2] = b
                    pixels[((initY + i )* texWidth + j+initX )*4 + 3] = a
                initX += width
                for j in range (depth):
                    r = 1
                    pixels[((initY + i )* texWidth + j+initX )*4 + 0] = r
                    pixels[((initY + i )* texWidth + j+initX )*4 + 3] = a
                initX += depth
                for j in range (width):
                    b = 1
                    pixels[((initY + i )* texWidth + j+initX )*4 + 2] = b
                    pixels[((initY + i )* texWidth + j+initX )*4 + 3] = a
            initY += height
            for i in range ( depth ) :
                initX = texOffsetX + depth
                for j in range (width):
                    g = 0.5
                    pixels[((initY + i )* texWidth + j+initX )*4 + 1] = g
                    pixels[((initY + i )* texWidth + j+initX )*4 + 3] = a
                initX += width
                for j in range (width):
                    g = 1
                    pixels[((initY + i )* texWidth + j+initX )*4 + 1] = g
                    pixels[((initY + i )* texWidth + j+initX )*4 + 3] = a
                
                
                
                
                
    image.pixels = pixels
            
            
    
def roundTextureOffset():
    
    image = bpy.data.images['TextureAtlas']
    texWidth = image.size[0]
    texHeight = image.size[1]
    
    for obj in bpy.data.objects:
        if (hasattr(obj,'["mcbox"]') and obj.type == "MESH"):
            for data in obj.data.uv_layers.active.data:
                data.uv[0] = round(data.uv[0]*texWidth)/texWidth
                data.uv[1] = round(data.uv[1]*texHeight)/texHeight
            setIndividualsUvs(obj)  
    
        if (hasattr(obj,'["texture_offset_x"]')):
            obj["texture_offset_x"] = round(obj["texture_offset_x"])
        if (hasattr(obj,'["texture_offset_y"]')):
            obj["texture_offset_y"] = round(obj["texture_offset_y"])          
                

def getMinUv(data):
    minUV = (data[0].uv[0],data[0].uv[1])
    
    for uvData in data :
        
        if (minUV[0] > uvData.uv[0]):
            minUV = (uvData.uv[0],minUV[1])
        if (minUV[1] < uvData.uv[1]):
            minUV = (minUV[0],uvData.uv[1])
    return minUV
    
def setTextureOffsetIdProp():
    image = bpy.data.images['TextureAtlas']
    texWidth = image.size[0]
    texHeight = image.size[1]
    
    for obj in bpy.data.objects:
        if (hasattr(obj,'["mcbox"]') and obj.type == "MESH"):
            
            width = obj.dimensions[0]
            height = obj.dimensions[2]
            depth = obj.dimensions[1]
            
            
            minUV = getMinUv(obj.data.uv_layers.active.data)
            
            textureOffsetX = minUV[0] * texWidth 
            textureOffsetY = - minUV[1] * texHeight + texHeight * 1
            
            print(minUV[1])

            if (hasattr(obj,'["texture_offset_x"]')):
                obj["texture_offset_x"] = textureOffsetX
            if (hasattr(obj,'["texture_offset_y"]')):
                obj["texture_offset_y"] = textureOffsetY


#########################################
##         packing algorithm
#########################################

def closestPower2(value):
    if (value == 0):
        return value
    return pow(2,math.ceil(math.log(value,2)))   

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
        self.boundaryx = 0
        self.boundaryy = 0
    def clear(self):
        self.list = []
        self.rectList = []
        self.boundaryx = 0
        self.boundaryy = 0
    #NOT USED ANYMORE : 
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
                
        return boundaryx,boundaryy
    def printListSizes(self):
        print("space size" + str(len(self.list)))
        print("rect size" + str(len(self.rectList)))

    def getBestGreedySpace(self,rect):
        subList = self.getMinMaxPow2Size(rect)
        space = self.getMinMaxDistanceFor(rect,subList)
        return (space.x,space.y)
            
    def getMinMaxPow2Size(self,rect):
        spaceList = SpaceList()
        maxAir = sys.maxsize
        
        for s in self.list:
            
            maxx = max(closestPower2(s.x+rect.width) , closestPower2(self.boundaryx) )
            maxy = max(closestPower2(s.y+rect.height) , closestPower2(self.boundaryy) )
            
            mAir = maxx * maxy
            
            if (s.checkPlace(rect)):
                if (maxAir == mAir):
                    spaceList.append(s)
                elif(maxAir > mAir):
                    maxAir = mAir
                    spaceList.clear()
                    spaceList.append(s)
                
        return spaceList
        
    def getMinMaxDistanceFor(self,rect,spaceList):
        maxPos = sys.maxsize
        space = None
        for s in spaceList.getList():
            mpos = max(s.x+rect.width,s.y+rect.height)
            if (s.checkPlace(rect) and maxPos > mpos):
                maxPos = mpos
                space = s
        return space
        
    def getMinMaxAirFor(self,rect,spaceList):
        posx = 0
        posy = 0
        airmax = sys.maxsize
        air = 0
        space = None
        for s in spaceList.getList():
            air = s.calculateAir()
            if (s.checkPlace(rect) and airmax>air):
                rect.x = s.x
                rect.y = s.y
                #take the biggest
                for s2 in self.list:
                    if (rect.overlap(s2)):
                        air2 = s2.calculateAir()
                        if (air2 > air):
                            air = air2
                if (airmax>air):
                    air = airmax
                    space = s
        return space  
        
    def append(self,space):
        self.appendSafe(space)
                
    def getList(self):
        return self.list
    
    def appendList(self,aList):
        for s in aList.getList():
            self.append(s)
            
    def appendSafe(self,space,interspace =0):
        toAdd = True
        listToRemove = []
        if (space.height <= 2+interspace or space.width <= 4+interspace):
            toAdd=False
        if (toAdd):
            for r in self.rectList:
                if r.overlap(space):
                    toAdd = False
        if (toAdd):
            for s in self.list:
                if (space.include(s)):
                    listToRemove.append(s)
                elif(s.include(space)):
                    toAdd = False
                else:
                    comb = space.combine(s)
                    if ( not comb is None):
                        space = comb
                        listToRemove.append(s)
        if (toAdd):
            self.list.append(space)
        for s in listToRemove:
            self.list.remove(s)
                
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
            
        if (self.boundaryx < rect2.x + rect2.width):
            self.boundaryx = rect2.x+rect2.width
        if (self.boundaryy < rect2.y + rect2.height):
            self.boundaryy = rect2.y+rect2.height
            
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


def autoPacking():
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
        posx,posy = spaceList.getBestGreedySpace(rect)
        rect.x = posx
        rect.y = posy
        spaceList.removeCubeRect(rect)
        rectList.append(rect)
        #spaceList.clearUnuseableSpace()
        
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
        


#########################################

#########################################



class OBJECt_OT_AutoPack(bpy.types.Operator):
    bl_idname = "button.autopack"
    bl_label = "auto pack uv"
     
    def execute(self, context):
        autoPacking()
        return{'FINISHED'}   
                
class OBJECt_OT_SetUvIdProp(bpy.types.Operator):
    bl_idname = "button.setuvidprop"
    bl_label = "Set UV ID Properties"
     
    def execute(self, context):
        setTextureOffsetIdProp()
        roundTextureOffset()
        return{'FINISHED'}   


class OBJECt_OT_SetUvMap(bpy.types.Operator):
    bl_idname = "button.setuvmap"
    bl_label = "Set UV MAP"
     
    def execute(self, context):
        for obj in bpy.context.selected_objects:
            if (obj.type == "MESH"):
                if (hasattr(obj,'["mcbox"]')):
                    setIndividualsUvs(obj)
        return{'FINISHED'}   
    

class OBJECt_OT_ResetTexture(bpy.types.Operator):
    bl_idname = "button.resettexture"
    bl_label = "Reset Texture"
     
    def execute(self, context):
        createTexture()   
        return{'FINISHED'}   
    
    

class MineCraftUVPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "MineCraft Custom UV "
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("button.setuvmap")
        row = layout.row()
        row.operator("button.resettexture")
        row = layout.row()
        row.operator("button.setuvidprop")
        row = layout.row()
        row.operator("button.autopack")
    
    
    
'''
for obj in bpy.context.selected_objects:
    if (obj.type == "MESH"):
        if (hasattr(obj,'["mcbox"]')):
            setTexture(obj)'''
            
            
            
def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_class(MineCraftUVPanel)


if __name__ == "__main__":
    register()
    
    
    