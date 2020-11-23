bl_info = {
    "name" : "Quick Tools",
    "author" : "Johann Erhardt",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 1, 0),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

if "bpy" in locals():
    import importlib
    importlib.reload(UI)
    importlib.reload(qDuplicate)
    importlib.reload(qLattice)
    importlib.reload(qExport)
    importlib.reload(qIsolate)
    importlib.reload(qFix)



else:
    print("Importing .py files.")
    import bpy
    from . import UI
    from . import qDuplicate
    from . import qLattice
    from . import qExport
    from . import qIsolate
    from . import qFix

class QToolsProperties(bpy.types.PropertyGroup):
    exportPath = bpy.props.StringProperty()
    applyPosition = bpy.props.BoolProperty()
    applyRotation = bpy.props.BoolProperty()
    applyScale = bpy.props.BoolProperty()
    exportAtOrigin = bpy.props.BoolProperty()
    exportApplyTransforms = bpy.props.BoolProperty()
    isolateOnlyMeshes = bpy.props.BoolProperty()
    uvLayerName = bpy.props.StringProperty(default="UVMap")



def register():
    bpy.utils.register_class(QToolsProperties)
    bpy.types.Scene.Qtools = bpy.props.PointerProperty(type=QToolsProperties)
    UI.register()
    qDuplicate.register()
    qLattice.register()
    qExport.register()
    qIsolate.register()
    qFix.register()


def unregister():
    bpy.utils.unregister_class(QToolsProperties)
    UI.unregister()
    qDuplicate.unregister()
    qLattice.unregister()
    qExport.unregister()
    qIsolate.unregister()
    qFix.unregister()


if __name__ == '__main__':
    register()