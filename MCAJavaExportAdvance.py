import os
import bpy

import mathutils
from math import radians
from math import pi



fullName = bpy.path.basename(bpy.context.blend_data.filepath)
name = os.path.splitext(fullName)[0]
sTextureWidth = str(256)
sTextureHeight = str(256)
package = "anonmine.beastmod"
outputPath = r'C:\test\Model' + name.title() + '.java'
outputLog = r'C:\test\log' + name + '.log'
ztrans= -12
Log = " "

sHeader = '''
package '''+package+'''.client.models;

import java.util.HashMap;

import net.minecraft.client.model.ModelBase;
import net.minecraft.entity.Entity;

import '''+package+'''.client.MCAClientLibrary.MCAModelRenderer;
import '''+package+'''.common.MCACommonLibrary.MCAVersionChecker;
import '''+package+'''.common.MCACommonLibrary.animation.AnimationHandler;
import '''+package+'''.common.MCACommonLibrary.math.Matrix4f;
import '''+package+'''.common.MCACommonLibrary.math.Quaternion;
import '''+package+'''.common.entities.mobs.Entity''' + name.title() + ''';
''' 

sModelBase = '''
public class Model''' + name.title() + ''' extends ModelBase {
	public final int MCA_MIN_REQUESTED_VERSION = 1;
	public HashMap<String, MCAModelRenderer> parts = new HashMap<String, MCAModelRenderer>();
'''
sPivotDefinition = ""
sBoxDefinition = ""

for obj in bpy.data.objects:
    nameObj = obj.name.split('.')[0]
    if (hasattr(obj,'["mcParentingPivot"]')):
        sPivotDefinition += "\n\tMCAModelRenderer " + nameObj+';'
for obj in bpy.data.objects:
    if (hasattr(obj,'["mcbox"]')):
        sBoxDefinition += "\n\tMCAModelRenderer " + obj.name+';'
        

sConstructor = '''
	public Model'''+name.title()+'''()
	{
		MCAVersionChecker.checkForLibraryVersion(getClass(), MCA_MIN_REQUESTED_VERSION);

		textureWidth = '''+sTextureWidth+''';
		textureHeight = '''+sTextureHeight+''';

'''

#CREATE PIVOT : 
for obj in bpy.data.objects:
    textureOffsetX = 0
    textureOffsetY = 0
    nameObj = obj.name.split('.')[0]
    if (hasattr(obj,'["mcParentingPivot"]')):
        #pivot are usefull only for children 
        if (bpy.data.objects[nameObj+'.emptyPivot'].children != () or bpy.data.objects[nameObj+'.emptyParentingPivot'].children != () ):
            
            
            objPivot = bpy.data.objects[nameObj+'.emptyPivot']
            objParent = obj.parent
            objParentPivot = None
            if (objParent == None):
                mat_rot = mathutils.Matrix.Rotation(radians(180.0), 4, 'Z') 
                mat_trans = mathutils.Matrix.Translation((0,0,ztrans))
                matrixTransform = mat_rot * mat_trans * obj.matrix_world
            else:
                objParentPivot = bpy.data.objects[objParent.name.split('.')[0]+'.emptyPivot']
                matrixTransform = (objParentPivot.matrix_world).inverted() * (objPivot.matrix_world )
                
            
            position = matrixTransform.to_translation()
            quat = (matrixTransform).to_quaternion()
			
            sPos = str(-round(position[0],ndigits = 1) ) + 'F,' +str(round(position[2],ndigits = 1) ) + 'F,' +str(round(position[1],ndigits = 1) ) +'F'
            squat = str(-round(quat[1],ndigits = 7) ) + 'F,' +str(round(quat[3],ndigits = 7) ) + 'F,' +str(round(quat[2],ndigits = 7) ) +'F,' +str(round(quat[0],ndigits = 7) ) +'F'
      
      
            sConstructor += "\n\t\t" + nameObj + " = " + 'new MCAModelRenderer(this, "'+ nameObj + '", '+ str(textureOffsetX) + ' , '+ str(textureOffsetY) + ');'
            sConstructor += "\n\t\t" + nameObj + ".setInitialRotationPoint (" + sPos + ");"
            sConstructor += "\n\t\t" + nameObj + ".setInitialRotationMatrix(new Matrix4f().set(new Quaternion(" + squat + ")).transpose());"
            
            Log += '\n\t\t' + nameObj + '(' + squat + ')' + '(' + sPos+ ')'
            #uncomment and modify if you want to see bones :
            #sConstructor += "\n\t\t" + nameObj + ".mirror = false;"
            #sConstructor += "\n\t\t" + nameObj + ".addBox (-5F,-5F,-5F,10,10,50);"
            #sConstructor += "\n\t\t" + nameObj + ".setTextureSize( "+sTextureWidth+" , "+sTextureHeight+" );"
            
            sConstructor += "\n\t\t" + "parts.put(" + nameObj + ".boxName," + nameObj+");"

            sConstructor += "\n\t\t"

#SET PARENTING PIVOT HIERARCHY
for obj in bpy.data.objects:
    nameObj = obj.name.split('.')[0]
    if (hasattr(obj,'["mcParentingPivot"]')):
        if (bpy.data.objects[nameObj+'.emptyPivot'].children != () or bpy.data.objects[nameObj+'.emptyParentingPivot'].children != () ):
            if (obj.parent != None):
                sConstructor += "\n\t\t" + obj.parent.name.split('.')[0] +".addChild("+nameObj+");"   

sConstructor += "\n\t\t"  

sConstructorBox = ''
#DO SAME FOR BLOCK
for obj in bpy.data.objects:
    textureOffsetX = 0 
    textureOffsetY = 0 
    mirrorTexture = False
    nameObj = obj.name.split('.')[0]
    if (hasattr(obj,'["mcbox"]')):
        if (hasattr(obj,'["texture_offset_x"]')):
            textureOffsetX = obj["texture_offset_x"] 
        if (hasattr(obj,'["texture_offset_y"]')):
            textureOffsetY = obj["texture_offset_y"] 
        if (hasattr(obj,'["mirror_texture"]')):
            mirrorTexture = bool(obj["mirror_texture"])
        
        if (obj.parent == None):
            mat_rot = mathutils.Matrix.Rotation(radians(180.0), 4, 'Z') 
            mat_trans = mathutils.Matrix.Translation((0,0,ztrans))
            matrixTransform = mat_rot * mat_trans * obj.matrix_world
        else:
            matrixTransform = obj.matrix_basis
        
        
        dim = obj.dimensions
        sOffset = str(-round(dim[0])/2)+'F,'+str(-round(dim[2])/2)+'F,'+str(-round(dim[1])/2) +'F'
        sDim = str(round(dim[0])) + ',' + str(round(dim[2])) + ',' + str(round(dim[1]))
        
        position = (matrixTransform).to_translation()
        sPos = str(-round(position[0],ndigits = 1) ) + 'F,' +str(round(position[2],ndigits = 1) ) + 'F,' +str(round(position[1],ndigits = 1) ) +'F'
  
        #fac = 180 / pi
        #quat = matrixTransform.to_quaternion()
        #matrix = quat.to_matrix()
        #mat_rot = mathutils.Matrix.Rotation(radians(0.0), 3, 'Y') 
        #mat_rot *= mathutils.Matrix.Rotation(radians(90.0), 3, 'X') 
        #mat_rot *= mathutils.Matrix.Rotation(radians(180.0), 3, 'Z') 
        #result = mat_rot * matrix
        #quat = result.to_quaternion()
        #squat = str(round(quat[1],ndigits = 7) ) + 'F,' +str(-round(quat[2],ndigits = 7) ) + 'F,' +str(-round(quat[3],ndigits = 7) ) +'F,' +str(round(quat[0],ndigits = 7) ) +'F'
     
     
        mat_rot = mathutils.Matrix.Rotation(radians(180.0), 4, 'Z') 
        quat = (matrixTransform * mat_rot).to_quaternion()
        squat = str(-round(quat[1],ndigits = 7) ) + 'F,' +str(round(quat[3],ndigits = 7) ) + 'F,' +str(round(quat[2],ndigits = 7) ) +'F,' +str(round(quat[0],ndigits = 7) ) +'F'
      
  
        sConstructorBox += "\n\t\t" + nameObj + " = " + 'new MCAModelRenderer(this, "'+ nameObj + '", '+ str(textureOffsetX) + ' , '+ str(textureOffsetY) + ');'
        sConstructorBox += "\n\t\t" + nameObj + ".mirror = " + str(mirrorTexture).lower() + ";"
        sConstructorBox += "\n\t\t" + nameObj + ".addBox (" + sOffset + ',' + sDim + ");"
        sConstructorBox += "\n\t\t" + nameObj + ".setInitialRotationPoint (" + sPos + ");"
        sConstructorBox += "\n\t\t" + nameObj + ".setInitialRotationMatrix(new Matrix4f().set(new Quaternion(" + squat + ")).transpose());"
        sConstructorBox += "\n\t\t" + nameObj + ".setTextureSize( "+sTextureWidth+" , "+sTextureHeight+" );"
        sConstructorBox += "\n\t\t" + "parts.put(" + nameObj + ".boxName," + nameObj+");"
        
        if (obj.parent != None):
            sConstructorBox += "\n\t\t" + obj.parent.name.split('.')[0] +".addChild("+nameObj+");"
        sConstructorBox += "\n\t\t"
        
sConstructor += sConstructorBox  
sConstructor += '''
    }
    '''
    
sRender = '''

	@Override
	public void render(Entity oldEntity, float time, float limbSwingDistance, float custom, float headYRot, float headXRot, float yTrans) 
	{
		Entity''' + name.title() + ''' entity = (Entity''' + name.title() + ''')oldEntity;

		//Render every non-child part
'''
sRenderBox =""

for obj in bpy.data.objects:  
    nameObj = obj.name.split('.')[0]
    if (hasattr(obj,'["mcParentingPivot"]') ):
        if (bpy.data.objects[nameObj+'.emptyPivot'].children != () or bpy.data.objects[nameObj+'.emptyParentingPivot'].children != () ):
            if (obj.parent == None):
                sRender += "\n\t\t" + nameObj + ".render(yTrans);"
    if (hasattr(obj,'["mcbox"]') ):
        if (obj.parent == None):
            sRenderBox += "\n\t\t" + nameObj + ".render(yTrans);"

sRender += sRenderBox
sRender += '''

		AnimationHandler.performAnimationInModel(parts, entity);
	}

	@Override
	public void setRotationAngles(float time, float limbSwingDistance, float custom, float headYRot, float headXRot, float yTrans, Entity oldEntity) {}

	public MCAModelRenderer getModelRendererFromName(String name)
	{
		return parts.get(name) != null ? parts.get(name) : null;
	}
'''
    
#sModelBase += sPivotDefinition + sConstructor + sRender 
sModelBase += sPivotDefinition + sBoxDefinition + sConstructor + sRender 
sModelBase +='''
}
'''

        
#print(sHeader + sModelBase)


### NOW WE LIKE TO WRITE OUT THE JAVA FILE

fileObject = open(outputPath, 'w+')
fileObject.write(sHeader + sModelBase)
fileObject.close()

fileObject = open(outputLog, 'w+')
fileObject.write(Log)
fileObject.close()