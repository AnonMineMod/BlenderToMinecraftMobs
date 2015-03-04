


import bpy
import math
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
    
    
    