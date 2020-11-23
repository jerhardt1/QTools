import bpy
from mathutils import Vector, Quaternion

class QDuplicate(bpy.types.Operator):
    bl_idname = "view3d.qduplicate"
    bl_label = "Quick Duplicate"

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) != 0

    def execute(self, context):
        if not 'qdupval' in bpy.context.active_object:
            self.report({'ERROR'}, 'Please press prepare before duplicating!')
            return {'FINISHED'}
        else:
            content = bpy.context.active_object['qdupval']
            val = (Vector(content[0]), Quaternion(content[1]), Vector(content[2]))
            self.smartDuplicate(val)
            self.report({'INFO'}, 'Transformation successful!')
            return {'FINISHED'}

    def smartDuplicate(self, initTransform):
        obj = bpy.context.active_object   
        Transform = self.getTransforms(obj)
        if not 'qtdupval' in bpy.context.active_object: 
            # Calculate transformation values using the saved inital values
            qtdupval = self.calcTransforms(initTransform, Transform)
            obj['qtdupval'] = qtdupval
            bpy.ops.object.duplicate()
            obj = bpy.context.active_object
            obj.location += Vector(qtdupval[0])
            self.performRotation(obj, qtdupval) # Rotation
            obj.scale = Vector(x * y for x,y in zip(obj.scale, Vector(qtdupval[2]))) # Scale    
        else:
            qtdupval = obj['qtdupval']
            bpy.ops.object.duplicate()
            obj = bpy.context.active_object
            obj.location += Vector(qtdupval[0])
            self.performRotation(obj, qtdupval) # Rotation
            obj.scale = Vector(x * y for x,y in zip(obj.scale, Vector(qtdupval[2])))  # Scale

    def performRotation(self, obj, tinput): # Rotation
            Transform = self.getTransforms(obj)
            bpy.context.active_object.rotation_mode = 'QUATERNION'
            rotation = Transform[1] @ Quaternion(tinput[1])
            bpy.context.active_object.rotation_quaternion = rotation
            bpy.context.active_object.rotation_mode = 'XYZ'

    def getTransforms(self, obj):
        translation = obj.location
        bpy.context.active_object.rotation_mode = 'QUATERNION'
        rotation = obj.rotation_quaternion
        bpy.context.active_object.rotation_mode = 'XYZ'
        scale = obj.scale
        return (translation, rotation, scale)

    def calcTransforms(self, initVals, val):
        translation = val[0] - initVals[0]
        rotation =   initVals[1] @ (val[1] * -1)
        sval = val[2]
        sival = initVals[2]
        sval = Vector(x / y for x,y in zip(sval, sival))
        scale = sval
        return (translation, rotation, scale) # Translation/Vector, Rotation/Quaternion, Scale/Vector
     

class QSaveTransform(bpy.types.Operator):
    bl_idname = "view3d.qsavetransform"
    bl_label = "Save Transform"

    initTransform = ()

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) != 0

    def execute(self, context):
        self.saveTransforms()
        self.report({'INFO'}, 'Prepared!')
        return {'FINISHED'}

    def saveTransforms(self):
        self.initTransform = self.getTransforms(bpy.context.active_object)
        bpy.context.object['qdupval'] = self.initTransform
        if 'qtdupval' in bpy.context.active_object:
            del bpy.context.object['qtdupval']
        return self.initTransform

    def getTransforms(self, obj):
        translation = obj.location
        rotation = obj.rotation_quaternion
        scale = obj.scale
        return (translation, rotation, scale)

classes = (
    QDuplicate,
    QSaveTransform
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)




