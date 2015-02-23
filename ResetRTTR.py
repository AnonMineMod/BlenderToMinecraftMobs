

import bpy
import mathutils
from collections import defaultdict

def clearRelativParenting(ArmatureName):
    
    arm = bpy.data.objects[ArmatureName]
    
    matrixWorld = defaultdict(mathutils.Matrix)
    
    for bone in arm.data.bones:
        if bone.use_relative_parent :
            
            for obj in bpy.data.objects: 
                if obj.parent_bone == bone.name:
                    
                    matrixWorld[obj.name] = obj.matrix_world
                
            bone.use_relative_parent = False
            
            for obj in bpy.data.objects: 
                if obj.parent_bone == bone.name:
                    
                    obj.matrix_world = matrixWorld[obj.name]

def setEmptyBone(ArmatureName):
    
    clearRelativParenting(ArmatureName)
    
    scene = bpy.context.scene
    arm = bpy.data.objects[ArmatureName]

    layers = 20*[False]
    layers[11] = True

    for bone in arm.data.bones:
            
        vBone = (0,-bone.length,0)
        
        
        emptyName = bone.name + '.emptyPivot'
        
        if (not emptyName in bpy.data.objects) :
            
            empty = bpy.data.objects.new(emptyName, None)
            scene.objects.link(empty)
            scene.update()
        else:
            empty = bpy.data.objects[emptyName]
            
            
        empty.layers = layers
        empty.parent = arm
        empty.parent_type = 'BONE'
        empty.parent_bone = bone.name
        
        empty['mcRotationPoint'] = True
        
        empty.location = vBone
        scene.update()
        
        for obj in bpy.data.objects: 
            if obj.type == 'MESH' and obj.parent_bone == bone.name:
                
                print (obj.name + " " + bone.name)
                
                boneLengthTr  = mathutils.Matrix.Translation((0,bone.length,0))
                matrixObj = boneLengthTr * obj.matrix_parent_inverse * obj.matrix_basis
                             
                obj.parent = empty
                obj.parent_bone = ''
                obj.parent_type = 'OBJECT'
                obj.matrix_basis = matrixObj
                
                #obj.location = matrixObj.to_translation()
                #obj.rotation_euler = matrixObj.to_quaternion()
                
    scene.update()

    
    
    layers[11] = False
    layers[12] = True
    
    #create Parenting Empties :
    for bone in arm.data.bones:
        
        emptyName = bone.name +'.emptyParentingPivot'
        
        if (not emptyName in bpy.data.objects) :
            
            empty = bpy.data.objects.new(emptyName, None)
            scene.objects.link(empty)
            scene.update()
        else:
            empty = bpy.data.objects[emptyName]
            
        empty.layers = layers
        empty['mcParentingPivot'] = True
        
    for bone in arm.data.bones:
        
        matrixTransform = bone.matrix_local    
        
        emptyName = bone.name +'.emptyParentingPivot'
        empty = bpy.data.objects[emptyName]    
        
        parentBone = bone.parent
        if (parentBone != None):
            emptyParentName =  parentBone.name + '.emptyParentingPivot' 
            emptyParent = bpy.data.objects[ emptyParentName ]
            matrixTransform = parentBone.matrix_local.inverted() * matrixTransform
            
            empty.parent = emptyParent
            empty.parent_bone = ''
            empty.parent_type = 'OBJECT'
        else :
            matrixTransform = arm.matrix_world * matrixTransform
            
        empty.matrix_basis = matrixTransform


                    
                    
setEmptyBone("Armature") 