import json
import string
from math import floor
import time
import bpy
import mathutils
from numpy import poly
import numpy as np
import math
import bmesh
import random
from . import blockyUtils as butils


def onlySelect(active_obj):
    for obj in bpy.data.objects:
        obj.select_set(False)
    active_obj.select_set(True)
    bpy.context.view_layer.objects.active = active_obj


def execute(self, context):
    active_obj = bpy.context.active_object

    bpy.context.view_layer.objects.active = active_obj
    active_obj.select_set(False)

    for obj in bpy.context.selected_objects:
        if obj.type != "MESH":
            obj.select_set(False)

    for obj in bpy.context.selected_objects:
        if obj.data.uv_layers.active:
            obj.data.uv_layers.active.name = 'MY UV'

    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked": False, "mode": 'TRANSLATION'}, TRANSFORM_OT_translate={"value": (0, 0, 0), "orient_axis_ortho": 'X', "orient_type": 'GLOBAL', "orient_matrix": ((0, 0, 0), (0, 0, 0), (0, 0, 0)), "orient_matrix_type": 'GLOBAL', "constraint_axis": (False, False, False), "mirror": False, "use_proportional_edit": False, "proportional_edit_falloff": 'SMOOTH', "proportional_size": 1,
                                  "use_proportional_connected": False, "use_proportional_projected": False, "snap": False, "snap_target": 'CLOSEST', "snap_point": (0, 0, 0), "snap_align": False, "snap_normal": (0, 0, 0), "gpencil_strokes": False, "cursor_transform": False, "texture_space": False, "remove_on_cancel": False, "view2d_edge_pan": False, "release_confirm": False, "use_accurate": False, "use_automerge_and_split": False})
    bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]

    bpy.ops.object.join()

    joined_obj = bpy.context.selected_objects[0]

    active_obj.select_set(True)
    bpy.context.view_layer.objects.active = active_obj
    bpy.ops.object.convert(target='MESH')

    if not bpy.context.object.data.uv_layers:
        self.report({"WARNING"}, "obj must have UVs")
        return {"CANCELLED"}

    otherObjects = bpy.context.selected_objects
    if len(otherObjects) < 2:
        self.report({"WARNING"}, "must be selecting 2 objects")
        return {"CANCELLED"}

    ref_obj = None
    if otherObjects[0] == active_obj:
        ref_obj = otherObjects[1]
    else:
        ref_obj = otherObjects[0]

    # create the cage obj
    cage_obj = active_obj.copy()
    cage_obj.data = active_obj.data.copy()
    cage_obj.name = "cage"
    context.collection.objects.link(cage_obj)

    # expand the cage
    onlySelect(cage_obj)
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.transform.shrink_fatten(value=0.03, use_even_offset=False, mirror=True, use_proportional_edit=False,
                                    proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    bpy.ops.object.editmode_toggle()

    mat = active_obj.material_slots[0].material
    image = None
    for n in mat.node_tree.nodes:
        if n.type == 'TEX_IMAGE':
            image = n.image

    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.render.bake.use_pass_direct = False
    bpy.context.scene.render.bake.use_pass_indirect = False
    bpy.context.scene.render.bake.use_selected_to_active = True
    bpy.context.scene.render.bake.use_cage = True
    bpy.context.scene.render.bake.cage_object = cage_obj
    bpy.context.scene.cycles.bake_type = 'DIFFUSE'

    bpy.ops.object.select_all(action='DESELECT')
    active_obj.select_set(True)
    ref_obj.select_set(True)
    bpy.context.view_layer.objects.active = active_obj

    bpy.ops.object.bake(type='DIFFUSE', use_selected_to_active=True, cage_object=cage_obj.name,
                        save_mode='INTERNAL',  use_cage=True, target='IMAGE_TEXTURES')

    onlySelect(cage_obj)
    bpy.ops.object.delete()

    onlySelect(joined_obj)
    bpy.ops.object.delete()

    return {'FINISHED'}
