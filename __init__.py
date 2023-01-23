
import json
import string
from math import floor

import bpy
import mathutils
from numpy import poly
from . import getBlocks
from . import generateUVs
from . import exportColors
from . import bake
from . import addRemeshModifier
from . import selectSimilarColor

bl_info = {
    "name": "cubey addon",
    "author": "mary",
    "description": "",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Generic"
}


class GetBlocksOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "blocky.getblocks"  # best to put plugin name then obperator name #must be all lowercase
    bl_label = "cubey"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        return getBlocks.execute(self, context)


class AddRemeshModifier(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "blocky.addremeshmodifier"  # best to put plugin name then obperator name #must be all lowercase
    bl_label = "remeshadd"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        axis = context.scene.cubey_axis
        axis_num = -1
        if axis == "OP1":
            axis_num = 0
        elif axis == "OP2":
            axis_num = 1
        elif axis == "OP3":
            axis_num = 2
        return addRemeshModifier.execute(self, context, context.scene.cubey_size, axis_num, context.scene.cubey_joinselected)


class GenerateUVsOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "blocky.generateuvs"  # best to put plugin name then obperator name #must be all lowercase
    bl_label = "generateUVs"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        return generateUVs.execute(self, context)


class ExportColors(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "blocky.exportcolors"  # best to put plugin name then obperator name #must be all lowercase
    bl_label = "ExportColors"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        return exportColors.execute(self, context)


class Bake(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "blocky.bake"  # best to put plugin name then obperator name #must be all lowercase
    bl_label = "Bake"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        return bake.execute(self, context)


class SelectSimilarColor(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "blocky.selectsimilarcolor"  # best to put plugin name then obperator name #must be all lowercase
    bl_label = "SelectSimilarColor"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        return selectSimilarColor.execute(self, context)


bpy.types.Scene.cubey_size = bpy.props.IntProperty(name="cubey_size",
                                                   description="size of remesh",
                                                   min=4,
                                                   max=1000,
                                                   default=61)

bpy.types.Scene.cubey_axis = bpy.props.EnumProperty(name="cubey_axis",
                                                    description="axis that the remesh operator will constrain it's size to",
                                                    items=[
                                                        ('OP1', 'x', ''), ('OP2', 'y', ''), ('OP3', 'z', '')]
                                                    )

bpy.types.Scene.cubey_joinselected = bpy.props.BoolProperty(
    name="cubey_joinselected")


class CubeyPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Cubey"
    bl_idname = "OBJECT_PT_cubey"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Cubey"  # the tab name
    bl_context = "objectmode"

    def draw(self, context):  # the stuff in the panel
        layout = self.layout
        obj = context.object
        scene = context.scene

        row = layout.row()
        row.operator(GetBlocksOperator.bl_idname,
                     text="GERATEEE", icon="SPHERE")
        row = layout.row()
        row.operator(AddRemeshModifier.bl_idname,
                     text="add remesh", icon="SPHERE")
        row.prop(scene, "cubey_size")
        row.prop(scene, "cubey_axis")
        row.prop(scene, "cubey_joinselected")

        row = layout.row()
        row.operator(GenerateUVsOperator.bl_idname,
                     text="generateUVs", icon="SPHERE")

        row = layout.row()
        row.operator(ExportColors.bl_idname,
                     text="ExportColors", icon="SPHERE")

        row = layout.row()
        row.operator(Bake.bl_idname,
                     text="Bake", icon="SPHERE")

        row = layout.row()
        row.operator(SelectSimilarColor.bl_idname,
                     text="SelectSimilarColor", icon="SPHERE")

        # row.label(text="group".lower())
        # op = row.operator(GetBlocksOperator.bl_idname,
        #                   text="GERATEEE", icon="SPHERE")
        # op.group = "group"
        # op.action = 'SHOW'
        # op = row.operator(AddRemeshModifier.bl_idname,
        #                   text="add remesh", icon="SPHERE")
        # op.group = "group"
        # op.action = 'HIDE'

        # row.scale_y = 2.0


_classes = [GetBlocksOperator, AddRemeshModifier,
            CubeyPanel, GenerateUVsOperator, ExportColors, Bake, SelectSimilarColor]


def register():
    for cls in _classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in _classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
