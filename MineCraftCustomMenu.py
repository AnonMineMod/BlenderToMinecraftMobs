
import bpy 
import mathutils
from mathutils import Vector


def createMeshFromData(name, origin, verts, faces):
    # Create mesh and object
    me = bpy.data.meshes.new(name+'Mesh')
    # Create mesh from given verts, faces.
    me.from_pydata(verts, [], faces)
    # Update mesh with new data
    me.update()    
    return me

def convertToMcBox(object):
    scn = bpy.context.scene
    dim = object.dimensions.copy()
    mWorld = object.matrix_world
    mcbox = True
    mirrorTexture = False
    textureOffsetX = 0
    textureOffsetY = 0
    if ( hasattr(object,('["mirror_texture"]'))):
        mirrorTexture = object["mirror_texture"]
    if ( hasattr(object,('["texture_offset_x"]'))):
        textureOffsetX = object["texture_offset_x"]
    if ( hasattr(object,('["texture_offset_y"]'))):
        textureOffsetY = object["texture_offset_y"]
    
    
    # faces are : 
    #           [0] Left
    #           [1] Front
    #           [2] Right
    #           [3] Back
    #           [4] Top
    #           [5] Bot
    verts = ((-0.5,-0.5,-0.5),(-0.5,0.5,-0.5),(0.5,0.5,-0.5),(0.5,-0.5,-0.5),(-0.5,-0.5,0.5),(-0.5,0.5,0.5),(0.5,0.5,0.5),(0.5,-0.5,0.5))
    faces = ((1,0,4,5),(0,3,7,4),(3,2,6,7),(2,1,5,6),(4,7,6,5),(1,2,3,0))
    name = 'mc'+object.name
    
    oldMesh = object.data    
    object.data = createMeshFromData(name,(0,0,0),verts,faces)
    del oldMesh
    
    #scn.objects.active = object
    #bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
   
    object.matrix_world = mWorld
    
    object.dimensions = dim
    
    object["mcbox"] = mcbox
    object["mirror_texture"] = mirrorTexture
    object["texture_offset_x"] = textureOffsetX
    object["texture_offset_y"] = textureOffsetY
    
    

#copy the object by symmetry

def duplicateMirrorObject(scene, name, copyobj):
 
    # Create new mesh
    mesh = bpy.data.meshes.new(name)
     
    # Create new object associated with the mesh
    ob_new = bpy.data.objects.new(name, mesh)
     
    # Copy data box from the old object into the new object
    ob_new.data = copyobj.data.copy()
    ob_new.scale = copyobj.scale
    ob_new.rotation_euler  = (copyobj.rotation_euler[0],-copyobj.rotation_euler[1],-copyobj.rotation_euler[2])
    ob_new.location = (-copyobj.location[0],copyobj.location[1],copyobj.location[2])
     
    # Link new object to the given scene and select it
    scene.objects.link(ob_new)
    ob_new.select = True
     
    return ob_new

#round the size of objects
def roundSize(object):
 
    object.scale = (abs(object.scale[0]),abs(object.scale[1]),abs(object.scale[2]))
    object.dimensions = (round(object.dimensions[0]),round(object.dimensions[1]),round(object.dimensions[2]))
     
    return object

      
    #copy box mirror
class OBJECT_OT_MirrorBox(bpy.types.Operator):
    bl_idname = "button.mirror_box"
    bl_label = "Mirror Shape"

    def execute(self, context):
        print("test2")
        for obj in bpy.context.selected_objects:
            if (obj.type == "MESH"):
                if (obj.name.endswith("_L")):
                    new_obj = duplicateMirrorObject(context.scene,obj.name[:-2]+"_R",obj)
                else:
                    if (obj.name.endswith("_R")):
                        new_obj = duplicateMirrorObject(context.scene,obj.name[:-2]+"_L",obj)
                    else:
                        new_obj = duplicateMirrorObject(context.scene,obj.name+"mirror",obj)
                new_obj["mirror_texture"] = True
        return{'FINISHED'}  
    
    #Define the element as a MineCraft Box
class OBJECT_OT_DefineAsBox(bpy.types.Operator):
    bl_idname = "button.define_as_box"
    bl_label = "Define As Box"
 
    def execute(self, context):
        for obj in bpy.context.selected_objects:
            if (obj.type == "MESH"):
                obj.name  = obj.name.replace('.','_')
                convertToMcBox(obj)
        return{'FINISHED'}    
    #Define the Element as Not a MineCraft Box
class OBJECT_OT_NotABox(bpy.types.Operator):
    bl_idname = "button.not_a_box"
    bl_label = "Not A Box"
 
    def execute(self, context):
        for obj in bpy.context.selected_objects:
            if (obj.type == "MESH"):
                if (hasattr(obj,'["mcbox"]')):
                    del obj["mcbox"]
        return{'FINISHED'}   
    
 
        
class OBJECT_OT_RoundSize(bpy.types.Operator):
    bl_idname = "button.round_size"
    bl_label = "Round Size"
 
    def execute(self, context):
        for obj in bpy.context.selected_objects:
            if (obj.type == "MESH"):
                roundSize(obj)
        return{'FINISHED'}    
    

class MineCraftEditorPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "MineCraft Custom Panel "
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"

    
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("button.mirror_box")
        row = layout.row()
        split = row.split()
        col = split.column()
        col.operator("button.define_as_box")
        col = split.column()
        col.operator("button.not_a_box")
        row = layout.row()
        row.operator("button.round_size")



def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_class(MineCraftEditorPanel)


if __name__ == "__main__":
    register()
    
    
    