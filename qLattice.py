import bpy
from mathutils import Vector

class QLattice(bpy.types.Operator):
    bl_idname = "view3d.qlattice"
    bl_label = "Quick Lattice"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return len(context.selected_objects) != 0 and obj.type == 'MESH'

    def execute(self, context):
        
        self.createLattice()
        self.report({'INFO'}, 'Lattice created!')
        return {'FINISHED'}

    def createLattice(self):
        obj = []
        obj = bpy.context.selected_objects 

        if len(obj) > 1:
            lattice_coords = self.calcLattice(obj)
            scale_value = lattice_coords[0]
            loc = lattice_coords[1]

            bpy.ops.object.add(type='LATTICE',enter_editmode=False, location=loc)
            latobj = bpy.context.active_object  
            bpy.context.object.data.interpolation_type_u = 'KEY_LINEAR'
            bpy.context.object.data.interpolation_type_v = 'KEY_LINEAR' 
            bpy.context.object.data.interpolation_type_w = 'KEY_LINEAR'    
            
            bpy.context.active_object.scale = scale_value
            
            for i in obj:
                mod = i.modifiers.new("Lattice", 'LATTICE')
                mod.object = latobj

        else:
            obj = bpy.context.active_object
            loc = self.calcLoc(obj)
            scale_value = obj.dimensions

            bpy.ops.object.add(type='LATTICE', enter_editmode=False, location=loc)
            latobj = bpy.context.active_object   
            bpy.context.object.data.interpolation_type_u = 'KEY_LINEAR' 
            bpy.context.object.data.interpolation_type_v = 'KEY_LINEAR'    
            bpy.context.object.data.interpolation_type_w = 'KEY_LINEAR'    

            bpy.context.active_object.scale = scale_value
            mod = obj.modifiers.new("Lattice", 'LATTICE')
            mod.object = latobj   
        return

    def calcLattice(self,obj):
        bbox = [] 

        # for every object: transform local bounding box to world and add all vectors into a new list
        for i in obj:
            coords = [(i.matrix_world @ v.co) for v in i.data.vertices]
            for v in coords:
                bbox.append(v)

        # get the smallest and biggest value for each axis out of the list
        max_values = self.getMaxValues(bbox)
        min_values = self.getMinValues(bbox)

        # calculate the length of the bbox by adding the absolute values of min and max
        final_bbox = self.subMinMax(min_values,max_values)
        location = self.addMinMax(min_values, max_values)

        return final_bbox, location


    def localToWorld(self, input_bbox, input_matrix):
        local_bbox = [Vector(v) for v in input_bbox]
        world_bbox = [input_matrix @ v for v in local_bbox]
        return world_bbox

    def subMinMax(self, min, max):    
        total = Vector(x - y for x,y in zip(max, min))
        return total

    def addMinMax(self, min, max):    
        total = Vector(x + y for x,y in zip(min, max))
        total *= 0.5
        return total

    def getMaxValues(self, input_list):
        ValuesX = []
        ValuesY = []
        ValuesZ = []

        # put x, y and z vectors in seperate lists
        for v in input_list:
            ValuesX.append((v[0]))
            ValuesY.append((v[1]))
            ValuesZ.append((v[2]))
        
        maxX = max(ValuesX)
        maxY = max(ValuesY)
        maxZ = max(ValuesZ)

        return maxX,maxY,maxZ
    
    def getMinValues(self, input_list):
        ValuesX = []
        ValuesY = []
        ValuesZ = []

        # put x, y and z vectors in seperate lists
        for v in input_list:
            ValuesX.append((v[0]))
            ValuesY.append((v[1]))
            ValuesZ.append((v[2]))
        
        minX = min(ValuesX)
        minY = min(ValuesY)
        minZ = min(ValuesZ)

        return minX,minY,minZ

    def calcLoc(self,obj):
        local_bbox_center = 0.125 * sum((Vector(b) for b in obj.bound_box), Vector())
        global_bbox_center = obj.matrix_world @ local_bbox_center
        return global_bbox_center


class QApplyLattice(bpy.types.Operator):
    bl_idname = "view3d.qapplylattice"
    bl_label = "Applies Lattice Modifier"

    def execute(self, context):
        
        self.applyLattice()
        self.report({'INFO'}, 'Lattice applied!')
        return {'FINISHED'}

    def applyLattice(self):
        obj = bpy.context.active_object
        for modifier in [m for m in obj.modifiers if m.type == 'LATTICE']:
            modobj = modifier.object
            bpy.ops.object.modifier_apply(modifier= modifier.name)
            bpy.context.active_object.select_set(state = False)
            bpy.data.objects[modobj.name].select_set(True)
            print(bpy.context.view_layer.objects.active)
            bpy.ops.object.delete()
            
        return

class QRemoveLattice(bpy.types.Operator):
    bl_idname = "view3d.qremovelattice"
    bl_label = "Removes Lattice Modifiers"

    def execute(self, context):
        self.removeLattice()
        self.report({'INFO'}, 'Lattice removed!')    
        return {'FINISHED'}

    def removeLattice(self):
        obj = bpy.context.active_object
        for modifier in [m for m in obj.modifiers if m.type == 'LATTICE']:
            modobj = modifier.object
            bpy.ops.object.modifier_remove(modifier= modifier.name)
            bpy.context.active_object.select_set(state = False)
            bpy.data.objects[modobj.name].select_set(True)
            bpy.ops.object.delete()
        return


classes = (
    QLattice,
    QApplyLattice,
    QRemoveLattice,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)