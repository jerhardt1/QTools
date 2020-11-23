import bpy

class SuperIsolateToggle(bpy.types.Operator):
    bl_idname = "view3d.qisolatetoggle"
    bl_label = "Toggles Super Isolate"

    msg = ""

    def execute(self, context):
        self.toggle()
        self.report({'INFO'}, self.msg)
        return {'FINISHED'}

    def toggle(self):
        settings = bpy.context.scene.Qtools

        selection = []

        selection = bpy.context.selected_objects 

        if len(selection) == 0:
            for obj in bpy.context.scene.objects:
                if settings.isolateOnlyMeshes == True:
                    if obj.type == "MESH":
                        obj.hide_viewport = False
                else:
                    obj.hide_viewport = False

            self.msg = "Isolation off."

        else:

            for obj in bpy.context.scene.objects:
                if settings.isolateOnlyMeshes == True:
                    if obj.type == "MESH":
                        obj.hide_viewport = True
                        print(obj)
                else:
                    obj.hide_viewport = True

            for obj in selection:
                obj.hide_viewport = False

            self.msg = "Selection isolated."

        return





classes = (
    SuperIsolateToggle,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)