
import bpy
import mathutils
import os
from collections import defaultdict
import operator
from math import radians
from math import pi


import time

extractActionName = 'run'
scene = bpy.context.scene
fullName = bpy.path.basename(bpy.context.blend_data.filepath)
name = os.path.splitext(fullName)[0]
sTextureWidth = str(1024)
sTextureHeight = str(512)
package = "anonmine.beastmod"
outputPath = r'C:\Users\Guillaume\Documents\Blender\godzilla\\Channel' + extractActionName.title() + '.java'





def getKeyFrames(actionName):

    scene = bpy.context.scene

    action =  bpy.data.actions[actionName]

    keyframes = set([])
    bones = defaultdict(set)


    for fcu in action.fcurves:
        keys = set([])
        boneName = fcu.data_path.split('"')[1]
        
        for kf in fcu.keyframe_points:
            time = int(kf.co[0]) - scene.frame_start #mca start always at 0
            
            if (time >= scene.frame_start and time <= scene.frame_end):
                keyframes.add(time)
                bones[(time)].add(boneName)            

    sortedBonesKeyFrames = (sorted(bones.items(), key=operator.itemgetter(0)))
    sortedKeyFrames = (sorted(keyframes))
    
    return(sortedBonesKeyFrames,sortedKeyFrames)



def extractKeyFrame(boneName,frameName):

    sFrameName = frameName
    pivot = bpy.data.objects[boneName+".emptyPivot"]
    parentingPivot = bpy.data.objects[boneName+".emptyParentingPivot"]
    parentingPivotParent = parentingPivot.parent
    pivotParent = None
    if (parentingPivotParent != None):
        pivotParent = bpy.data.objects[parentingPivotParent.name.split(".")[0] + ".emptyPivot"]
    
    #sExtractKeyFrame = "\n\t\tKeyFrame "+sFrameName+" = new KeyFrame();"
    sExtractKeyFrame = ''
    
    if (hasattr(pivot,'["mcRotationPoint"]')):
        #pivot are usefull only for children 
        if (pivot.children != () or parentingPivot.children != () ):
            if (pivotParent == None):
                mat_rot = mathutils.Matrix.Rotation(radians(180.0), 4, 'Z') 
                matrixTransform = mat_rot * pivot.matrix_world
            else:
                matrixTransform = pivotParent.matrix_world.inverted() * pivot.matrix_world
                
            position = matrixTransform.to_translation()
            
            sPos = str(-round(position[0],ndigits = 1) ) + 'F,' +str(round(position[2],ndigits = 1) ) + 'F,' +str(round(position[1],ndigits = 1) ) +'F'
       
            quat = (matrixTransform).to_quaternion()
            squat = str(-round(quat[1],ndigits = 7) ) + 'F,' +str(round(quat[3],ndigits = 7) ) + 'F,' +str(round(quat[2],ndigits = 7) ) +'F,' +str(round(quat[0],ndigits = 7) ) +'F'
      
            sExtractKeyFrame += '\n\t\t' + sFrameName + '.modelRenderersRotations.put("' + boneName + '", new Quaternion('+squat+'));'
            sExtractKeyFrame += '\n\t\t' + sFrameName + '.modelRenderersTranslations.put("' + boneName + '", new Vector3f('+sPos+'));'


    return sExtractKeyFrame




(bonesKeyFrames,keyFrames) = getKeyFrames(extractActionName)
layers = [True]*20
scene.layers = layers
sExtractChannel = '''
package '''+package+'''.common.animations.'''+name.title()+''';

import '''+package+'''.common.MCACommonLibrary.animation.*;
import '''+package+'''.common.MCACommonLibrary.math.*;

public class Channel'''+extractActionName.title()+''' extends Channel {
	public Channel'''+extractActionName.title()+'''(String _name, float _fps, int _totalFrames, byte _mode) {
		super(_name, _fps, _totalFrames, _mode);
	}

	@Override
	protected void initializeAllFrames() {
'''


for frame in bonesKeyFrames:
    scene.frame_set(frame[0])
    
    frameName = 'frame'+str(frame[0])
    sExtractChannel += '\n\t\t' +'KeyFrame frame'+str(frame[0])+' = new KeyFrame();'
    #time.sleep(0.5)
    for boneName in frame[1]:
        sExtractChannel += extractKeyFrame(boneName,frameName)
    
    sExtractChannel += '\n\t\t' +'keyFrames.put('+str(frame[0])+','+ frameName +');'


sExtractChannel += '''

	}
}
'''

print(sExtractChannel)

fileObject = open(outputPath, 'w+')
fileObject.write(sExtractChannel)
fileObject.close()