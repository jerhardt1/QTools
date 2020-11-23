import bpy

class QTOOLS_PT_Duplicate(bpy.types.Panel):
    bl_idname = "QTOOLS_PT_duplicate"
    bl_label = "Quick Duplicate"
    bl_category = "QTools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"


    def draw(self, context):
        layout = self.layout

        info = layout.row()
        info.label(text="Press Prepare before duplicating.")
        row = layout.row()
        row.operator("view3d.qsavetransform", text ="Prepare")
        row.operator("view3d.qduplicate", text ="Duplicate", icon="DUPLICATE")

class QTOOLS_PT_Lattice(bpy.types.Panel):
    bl_idname = "QTOOLS_PT_lattice"
    bl_label = "Quick Lattice"
    bl_category = "QTools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"


    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("view3d.qlattice", text ="Quick Lattice", icon='MOD_LATTICE')
        row = layout.row()
        row.operator("view3d.qapplylattice", text="Apply")
        row.operator("view3d.qremovelattice", text="Remove")


class QTOOLS_PT_qexport(bpy.types.Panel):
    bl_idname = "QTOOLS_PT_qexport"
    bl_label = "Quick Export"
    bl_category = "QTools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"


    def draw(self, context):
        layout = self.layout
        scn = context.scene
        

        # ui
        box = layout.box()
        col = box.column()
        row = col.row(align=True)
        
        # transforms
        row.operator("view3d.qtransform", text ="Move to Origin")
        row.operator("view3d.qrestoretransform", text = "Restore")
        col.operator("view3d.qapplytransform", text="Apply Transforms")

        col.prop(scn.Qtools, 'applyPosition', text='Position')
        col.prop(scn.Qtools, 'applyRotation', text='Rotation')
        col.prop(scn.Qtools, 'applyScale', text='Scale')

        # export

        row = layout.row()
        row2 = row.row()
        row2.prop(scn.Qtools, 'exportPath', text='')
        row2.enabled = False
        row.operator("view3d.qexportfileselector", icon="FILE_FOLDER", text="")

        # row = layout.row()
        # row.operator("wm.exportsettings", text="Settings")

        row = layout.row()
        row.prop(scn.Qtools, 'exportAtOrigin', text='At Origin')
        col = layout.column()
        col.prop(scn.Qtools, 'exportApplyTransforms', text='Apply Transforms')

        row = layout.row()
        row.operator("view3d.qexport", text = "Quick Export", icon="EXPORT")

class QTOOLS_PT_quickIsolate(bpy.types.Panel):
    bl_idname = "QTOOLS_PT_qisolate"
    bl_label = "Quick Isolate"
    bl_category = "QTools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        row = layout.row()
        row.operator("view3d.qisolatetoggle", text = "Toggle Quick Isolate", icon="HIDE_OFF")

        col = layout.column()
        col.prop(scn.Qtools, 'isolateOnlyMeshes', text = "Only Meshes")

class QTOOLS_PT_qFix(bpy.types.Panel):
    bl_idname = "QTOOLS_PT_qfix"
    bl_label = "Quick Fix"
    bl_category = "QTools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        layout.label(text="Materials:")
        box = layout.box()
        row = box.row()
        row.operator("view3d.qfixmaterials", text = "Fix duplicates", icon="MATERIAL_DATA")
        row = box.row()
        row.operator("view3d.qfixunusedmaterials", text = "Remove unused Materials", icon="TRASH")
        layout.label(text="UV Channels:")
        box = layout.box()
        row = box.row()
        row.operator("view3d.qadduvchannel", text = "Add", icon="ADD")
        row.operator("view3d.qselectuvchannel", text= "Select", icon="RESTRICT_SELECT_OFF")
        row = box.row()
        row.operator("view3d.qrenameuvchannel", text= "Rename main UV Channel", icon="UV_DATA")
        row = box.row()
        row.operator("view3d.qdeleteuvchannel", text = "Remove UV Channel", icon="TRASH")
        row = box.row()
        row.prop(scn.Qtools, 'uvLayerName', text='Name')
        row = layout.row()
        row.operator("view3d.qpurge", text = "Clean up project", icon="BRUSH_DATA")








classes = (
    QTOOLS_PT_Duplicate,
    QTOOLS_PT_Lattice,
    QTOOLS_PT_qexport,
    QTOOLS_PT_quickIsolate,
    QTOOLS_PT_qFix,

)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)