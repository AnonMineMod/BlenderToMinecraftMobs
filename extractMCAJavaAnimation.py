
import bpy
import mathutils
import os
from collections import defaultdict
import operator
from math import radians
from math import pi


import time

extractActionName = 'roar'
scene = bpy.context.scene
fullName = bpy.path.basename(bpy.context.blend_data.filepath)
name = os.path.splitext(fullName)[0]
sTextureWidth = str(1024)
sTextureHeight = str(512)
package = "anonmine.beastmod"
outputPath = r'C:\test\Channel' + extractActionName.title() + '.java'
outputLog = r'C:\test\log'+ extractActionName.title()+'.log'

Log = " "



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



def extractKeyFrame(obj,frameName):

    Log = " "
    sFrameName = frameName
    nameObj = obj.name.split('.')[0]
    sExtractKeyFrame = ""
    if (hasattr(obj,'["mcParentingPivot"]')):
        #pivot are usefull only for children 
        if (bpy.data.objects[nameObj+'.emptyPivot'].children != () or bpy.data.objects[nameObj+'.emptyParentingPivot'].children != () ):
            
            
            objPivot = bpy.data.objects[nameObj+'.emptyPivot']
            objParent = obj.parent
            objParentPivot = None
            if (objParent == None):
                matrixTransform = obj.matrix_world
            else:
                objParentPivot = bpy.data.objects[objParent.name.split('.')[0]+'.emptyPivot']
                matrixTransform = (objParentPivot.matrix_world).inverted() * (objPivot.matrix_world )
                
            position = matrixTransform.to_translation()
            quat = (matrixTransform).to_quaternion()
            
            
            sPos = str(-round(position[0],ndigits = 1) ) + 'F,' +str(round(position[2],ndigits = 1) ) + 'F,' +str(round(position[1],ndigits = 1) ) +'F'
            squat = str(-round(quat[1],ndigits = 7) ) + 'F,' +str(round(quat[3],ndigits = 7) ) + 'F,' +str(round(quat[2],ndigits = 7) ) +'F,' +str(round(quat[0],ndigits = 7) ) +'F'
      
            sExtractKeyFrame += '\n\t\t' + sFrameName + '.modelRenderersRotations.put("' + nameObj + '", new Quaternion('+squat+'));'
            sExtractKeyFrame += '\n\t\t' + sFrameName + '.modelRenderersTranslations.put("' + nameObj + '", new Vector3f('+sPos+'));'

            Log += '\n\t\t' + nameObj + '(' + squat + ')' + '(' + sPos+ ')'
    return (sExtractKeyFrame,Log)




(bonesKeyFrames,keyFrames) = getKeyFrames(extractActionName)
layers = [True]*20
scene.layers = layers
sExtractChannel = '''
package '''+package+'''.common.animations.'''+name.lower()+''';

import '''+package+'''.common.mca.commonlibrary.animation.*;
import '''+package+'''.common.mca.commonlibrary.math.*;

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
    for obj in bpy.data.objects :
        if (obj.name.replace(".emptyParentingPivot", "") in frame[1] and obj.type == 'EMPTY'):
            sExtract, LogS = extractKeyFrame(obj,frameName)
            sExtractChannel += sExtract
            Log += LogS
    
    sExtractChannel += '\n\t\t' +'keyFrames.put('+str(frame[0])+','+ frameName +');'


sExtractChannel += '''

	}
}
'''

print(sExtractChannel)

fileObject = open(outputPath, 'w+')
fileObject.write(sExtractChannel)
fileObject.close()


fileObject = open(outputLog, 'w+')
fileObject.write(Log)
fileObject.close()