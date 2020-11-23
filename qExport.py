import os
import bpy
from bpy_extras.io_utils import ImportHelper, ExportHelper  

class QExport(bpy.types.Operator):
    bl_idname = "view3d.qexport"
    bl_label = "Quick Export"

    msg = "Exported to:"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return len(context.selected_objects) != 0 and obj.type == 'MESH'

    def execute(self, context):
        selection = bpy.context.selected_objects
        bpy.ops.object.select_all(action='DESELECT')
        for obj in selection:
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            settings = bpy.context.scene.Qtools
            if settings.exportAtOrigin == True:
                QTransform.toOrigin(self)
            if settings.exportApplyTransforms == True:
                QApplyTransform.apply(self)
        
            self.export()
            QRestoreTransform.restoreTransformation(self)
            bpy.ops.object.select_all(action='DESELECT')
        return {'FINISHED'}


    def export(self):
        obj = bpy.context.active_object
        meshname = '\\' + obj.name 
        filename = bpy.context.scene.Qtools.exportPath +  meshname + '.fbx'
        bpy.ops.export_scene.fbx(filepath= filename, use_selection=True)
        msg = 'Exported to: ' + filename
        self.report({'INFO'}, msg)
      

class WMFileSelector(bpy.types.Operator, ImportHelper, ExportHelper):
    bl_idname = "view3d.qexportfileselector"
    bl_label = "Select export folder"

    filter_glob = bpy.props.StringProperty(
        default="*.",
        options={'HIDDEN'},
        )

    def execute(self, context):
        #fdir = os.path.dirname(self.properties.filepath)
        fdir = self.properties.filepath
        context.scene.Qtools.exportPath = fdir
        print (fdir)
        return{'FINISHED'}


# q_transform

class QTransform(bpy.types.Operator):
    bl_idname = "view3d.qtransform"
    bl_label = "Quick Transform"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return len(context.selected_objects) != 0 and obj.type == 'MESH'

    

    def execute(self, context):
        self.toOrigin()

        return {'FINISHED'}


    def toOrigin(self):
        obj = bpy.context.active_object
        obj['PreviousLocation'] = obj.location

        obj.location = (0.0,0.0,0.0)

  

class QRestoreTransform(bpy.types.Operator):
    bl_idname = "view3d.qrestoretransform"
    bl_label = "Restores Transformation"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return len(context.selected_objects) != 0 and obj.type == 'MESH'

    def execute(self, context):
        self.restoreTransformation()
        return {'FINISHED'}

    def restoreTransformation(self):
        obj = bpy.context.active_object
        if not 'PreviousLocation' in obj:
            return
        else:
            obj.location = obj['PreviousLocation']
            return


class QApplyTransform(bpy.types.Operator):
    bl_idname = "view3d.qapplytransform"
    bl_label = "Quick Apply Transforms"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return len(context.selected_objects) != 0 and obj.type == 'MESH'

    def execute(self,context):
        self.apply()
        return{'FINISHED'}

    def apply(self):
        obj = bpy.context.active_object
        settings = bpy.context.scene.Qtools
        bpy.ops.object.transform_apply(location=settings.applyPosition, rotation=settings.applyRotation,scale=settings.applyScale)
        msg = 'Transforms applied!'
        self.report({'INFO'},msg)


classes = (
    QExport,
    WMFileSelector,
    QTransform,
    QRestoreTransform,
    QApplyTransform,
    #WM_ExportSettings,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


# bpy.ops.export_scene.fbx(filepath= filename, use_selection = es.use_selection, use_active_collection = es.use_active_collection, global_scale = es.global_scale, 
#                         apply_unit_scale = es.apply_unit_scale, apply_scale_options = es.apply_scale_options,
#                         bake_space_transform = es.bake_space_transform, use_mesh_modifiers = es.use_mesh_modifiers, mesh_smooth_type = es.mesh_smooth_type,
#                         use_subsurf = es.use_subsurf, use_mesh_edges = es.use_mesh_edges, use_tspace = es.use_tspace, use_custom_props = es.use_custom_props,
#                         add_leaf_bones = es.add_leaf_bones, primary_bone_axis = es.primary_bone_axis, secondary_bone_axis = es.secondary_bone_axis,
#                         use_armature_deform_only = es.use_armature_deform_only, armature_nodetype = es.armature_nodetype, bake_anim = es.bake_anim,
#                         bake_anim_use_all_bones = es.bake_anim_use_all_bones, bake_anim_use_nla_strips = es.bake_anim_use_nla_strips,
#                         bake_anim_use_all_actions = es.bake_anim_use_all_actions, bake_anim_force_startend_keying = es.bake_anim_force_startend_keying,
#                         bake_anim_step = es.bake_anim_step, bake_anim_simplify_factor = es.bake_anim_simplify_factor, axis_forward = es.axis_forward,
#                         axis_up = es.axis_up)

# class WM_ExportSettings(bpy.types.Operator, bpy.types.Panel):
#     """Export Settings"""
#     bl_label = "Export Settings"
#     bl_idname = "wm.exportsettings"


#     bp = bpy.props.BoolProperty
#     fp = bpy.props.FloatProperty
#     ep = bpy.props.EnumProperty

#     use_selection = bp(name = "Selected Objects", default= True)
#     use_active_collection = bp(name = "Active Collection", default = False)
#     #object_types = bpy.props.PointerProperty (type=bpy.types.ID, name="Object Types", tags = {'CAMERA','Light','ARMATURE','MESH'})
#     use_custom_props = bp (name= "Custom Properties", default = False)

#     global_scale = fp(name = "Scale", default = 1.0, min= 0.01, max=1000)
#     apply_scale_options = ep (items=[('FBX_SCALE_NONE', "All Local", ""), ('FBX_SCALE_UNITS', "FBX Unity Scale",""), ('FBX_SCALE_CUSTOM',"FBX Custom Scale",""), ('FBX_SCALE_ALL',"FBX All","")], name = "Apply Scalings", default = 'FBX_SCALE_NONE' )
#     axis_forward = ep(items=[('X',"X Forward",""),('Y',"Y Forward",""),('Z',"Z Forward",""),('-X',"-X Forward",""),('-Y',"-Y Forward",""),('-Z',"-Z Forward","")], name = "Forward", default = "-Z")
#     axis_up = ep(items=[('X',"X Up",""),('Y',"Y Up",""),('Z',"Z Up",""),('-X',"-X Up",""),('-Y',"-Y Up",""),('-Z',"-Z Up","")], name = "Up", default = "Y")
#     apply_unit_scale = bp (name = "Apply Unit", default = False)
#     bake_space_transform = bp (name= "!EXPERIMENTAL! Apply Transform", default = False)
#     mesh_smooth_type = ep (items=[('OFF', "Normals Only",""),('FACE',"Face",""),('EDGE',"Edge","")], name="Smoothing", default='OFF')
#     use_subsurf = bp (name = "Export Subdivision Surface", default= False)
#     use_mesh_modifiers = bp (name = "Apply Modifers", default = True)
#     use_mesh_edges = bp (name = "Loose Edges", default=False)
#     use_tspace = bp (name= "Tangent Space", default = False)
#     primary_bone_axis = ep (items=[('X',"X Axis",""),('Y',"Y Axis",""),('Z',"Z Axis",""),('-X',"-X Axis",""),('-Y',"-Y Axis",""),('-Z',"-Z Axis","")], name="Primary Bone Axis", default='Y')
#     secondary_bone_axis = ep (items=[('X',"X Axis",""),('Y',"Y Axis",""),('Z',"Z Axis",""),('-X',"-X Axis",""),('-Y',"-Y Axis",""),('-Z',"-Z Axis","")], name="Secondary Bone Axis", default='X')
#     armature_nodetype = ep (items=[('NULL',"Null",""),('LIMBNODE',"LimbNode",""),('ROOT',"Root","")], name="Armature FBX Node Type", default= 'NULL')
#     use_armature_deform_only = bp(name= "Only Deform Bones", default=False)
#     add_leaf_bones = bp (name= "Add Leaf Bones", default = False)
#     bake_anim = bp (name= "Baked Animation", default=True)
#     bake_anim_use_all_bones = bp (name= "Key All Bones", default = True)
#     bake_anim_use_nla_strips = bp (name= "NLA Strips", default = True)
#     bake_anim_use_all_actions = bp (name= "All Actions", default = True)
#     bake_anim_force_startend_keying = bp (name= "Force Start/End Keying", default = True)
#     bake_anim_step = fp (name= "Sampling Rate", default = 1.0, min= 0.01, max= 10.0)
#     bake_anim_simplify_factor = fp (name= "Simplify", default = 1.0, min= 0.0, max= 10.0)



#     def execute(self, context):
#         settings = bpy.context.scene.Qtools

#         settings.use_selection = self.use_selection
#         settings.use_active_collection = self.use_active_collection
#         #object_types
#         settings.use_custom_props = self.use_custom_props
#         settings.global_scale = self.global_scale
#         settings.apply_scale_options = self.apply_scale_options
#         settings.axis_forward = self.axis_forward
#         settings.axis_up = self.axis_up
#         settings.apply_unit_scale = self.apply_unit_scale
#         settings.bake_space_transform = self.bake_space_transform
#         settings.mesh_smooth_type = self.mesh_smooth_type
#         settings.use_subsurf = self.use_subsurf
#         settings.use_mesh_modifiers = self.use_mesh_modifiers
#         settings.use_mesh_edges = self.use_mesh_edges
#         settings.use_tspace = self.use_tspace
#         settings.primary_bone_axis = self.primary_bone_axis
#         settings.secondary_bone_axis = self.secondary_bone_axis
#         settings.armature_nodetype = self.armature_nodetype
#         settings.use_armature_deform_only = self.use_armature_deform_only
#         settings.add_leaf_bones = self.add_leaf_bones
#         settings.bake_anim = self.bake_anim
#         settings.bake_anim_use_all_bones = self.bake_anim_use_all_bones
#         settings.bake_anim_use_nla_strips = self.bake_anim_use_nla_strips
#         settings.bake_anim_use_all_actions = self.bake_anim_use_all_actions
#         settings.bake_anim_force_startend_keying = self.bake_anim_force_startend_keying
#         settings.bake_anim_step = self.bake_anim_step
#         settings.bake_anim_simplify_factor = self.bake_anim_simplify_factor
#         return {'FINISHED'}

#     def draw(self, context):
#         settings = bpy.context.scene.Qtools

#         layout = self.layout
#         #scn = context.scene

#         col = layout.column()
#         col.prop(self, "use_selection")
#         col.prop(self, "use_active_collection")
#         col.prop(self, "use_custom_props")
#         row = layout.row()
#         row.label(text="Global Scale")
#         row.prop(self, "global_scale", text="Global Scale")
#         col.prop(self, "axis_forward")
#         col.prop(self, "axis_up")
#         col.prop(self, "apply_unit_scale")
#         col.prop(self, "bake_space_transform")
#         col.prop(self, "mesh_smooth_type")
#         col.prop(self, "use_subsurf")
#         col.prop(self, "use_mesh_modifiers")
#         col.prop(self, "use_mesh_edges")
#         col.prop(self, "use_tspace")
#         col.prop(self, "primary_bone_axis")
#         col.prop(self, "secondary_bone_axis")
#         col.prop(self, "armature_nodetype")
#         col.prop(self, "use_armature_deform_only")
#         col.prop(self, "add_leaf_bones")
#         col.prop(self, "bake_anim")
#         col.prop(self, "bake_anim_use_all_bones")
#         col.prop(self, "bake_anim_use_nla_strips")
#         col.prop(self, "bake_anim_use_all_actions")
#         col.prop(self, "bake_anim_force_startend_keying")
#         col.prop(self, "bake_anim_step")
#         col.prop(self, "bake_anim_simplify_factor")


#     def invoke(self, context, event):
#         wm = context.window_manager

#         return wm.invoke_props_dialog(self)