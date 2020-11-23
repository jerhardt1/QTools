import bpy



class QFixMaterials(bpy.types.Operator):
    bl_idname = "view3d.qfixmaterials"
    bl_label = "Remove dup. Materials"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return len(context.selected_objects) != 0 and obj.type == 'MESH'

    def execute(self,context):
        self.apply()
        return{'FINISHED'}
    

    def apply(self):
        context = bpy.context
        scene = context.scene
        mats = bpy.data.materials

        for obj in context.selected_objects: # selected context.scene.objects:
            # all objects have material_slots
            for slot in obj.material_slots:
                part = slot.name.rpartition('.')
                mat =  mats.get(part[0])
                if part[2].isnumeric() and mat is not None:
                    slot.material = mat

class QDeleteUnusedMaterials(bpy.types.Operator):
    bl_idname = "view3d.qfixunusedmaterials"
    bl_label = "Remove unused Materials"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return len(context.selected_objects) != 0 and obj.type == 'MESH'

    def execute(self,context):
        self.apply()
        return{'FINISHED'}

    def apply(self):
        context = bpy.context
        scene = context.scene
        selection = context.selected_objects

        for obj in selection:
            context.view_layer.objects.active = obj
            bpy.ops.object.material_slot_remove_unused()

class QDeleteUVChannel(bpy.types.Operator):
    bl_idname = "view3d.qdeleteuvchannel"
    bl_label = "Remove UV Channel"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return len(context.selected_objects) != 0 and obj.type == 'MESH'

    def execute(self,context):
        self.apply()
        return{'FINISHED'}

    def apply(self):
        context = bpy.context
        scene = context.scene
        settings = scene.Qtools

        obj = bpy.context.active_object

        print(obj.data)
        print(obj.data.uv_layers)

        print(obj.data.uv_layers.active_index)

        selection = context.selected_objects

        for obj in selection:
            context.view_layer.objects.active = obj
            for layer in obj.data.uv_layers:
                if(layer.name == settings.uvLayerName):
                    obj.data.uv_layers.remove(layer)
                    print('Deleted!')



class QAddUVChannel(bpy.types.Operator):
    bl_idname = "view3d.qadduvchannel"
    bl_label = "Add UV Channel"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return len(context.selected_objects) != 0 and obj.type == 'MESH'

    def execute(self,context):
        self.apply()
        return{'FINISHED'}

    def apply(self):
        context = bpy.context
        scene = context.scene
        settings = scene.Qtools

        selection = context.selected_objects

        for obj in selection:
            obj.data.uv_layers.new(name=settings.uvLayerName)
            print('Added!')

class QRenameUVChannel(bpy.types.Operator):
    bl_idname = "view3d.qrenameuvchannel"
    bl_label = "Add UV Channel"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return len(context.selected_objects) != 0 and obj.type == 'MESH'

    def execute(self,context):
        self.apply()
        return{'FINISHED'}

    def apply(self):
        context = bpy.context
        scene = context.scene
        settings = scene.Qtools

        selection = context.selected_objects

        for obj in selection:
            obj.data.uv_layers[0].name = settings.uvLayerName
            print('Renamed!')

class QSelectUVChannel(bpy.types.Operator):
    bl_idname = "view3d.qselectuvchannel"
    bl_label = "Select UV Channel"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return len(context.selected_objects) != 0 and obj.type == 'MESH'

    def execute(self,context):
        self.apply()
        return{'FINISHED'}

    def apply(self):
        context = bpy.context
        scene = context.scene
        settings = scene.Qtools

        selection = context.selected_objects

        for obj in selection:
            for layer in obj.data.uv_layers:
                if(layer.name == settings.uvLayerName):
                    obj.data.uv_layers.active = layer
                    print('Selected!')

class QPurge(bpy.types.Operator):
    bl_idname = "view3d.qpurge"
    bl_label = "Quick Purge Orphanage Data"


    def execute(self,context):
        bpy.ops.outliner.orphans_purge()
        self.report({'INFO'}, 'Cleaned up!')
        return{'FINISHED'}

        

        






classes = (
    QFixMaterials,
    QDeleteUnusedMaterials,
    QDeleteUVChannel,
    QAddUVChannel,
    QRenameUVChannel,
    QSelectUVChannel,
    QPurge,

)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)