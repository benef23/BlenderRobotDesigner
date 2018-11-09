# #####
# This file is part of the RobotDesigner of the Neurorobotics subproject (SP10)
# in the Human Brain Project (HBP).
# It has been forked from the RobotEditor (https://gitlab.com/h2t/roboteditor)
# developed at the Karlsruhe Institute of Technology in the
# High Performance Humanoid Technologies Laboratory (H2T).
# #####

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# #####
#
# Copyright (c) 2018, Technical University Munich
#
#
# ######

# Blender imports
import bpy

# RobotDesigner imports
from .model import check_armature

from ..properties.globals import global_properties
from ..operators import modules

from .helpers import create_segment_selector


def draw(layout, context):
    """
    Draws the user interface for importing modules.

    :param layout: Current GUI element (e.g., collapsible box, row, etc.)
    :param context: Blender context
    """
    if not check_armature(layout, context):
        return

    import_box = layout.box()
    row0 = import_box.row()

    ######### Create sub-box where user can import one of a few gripper and robot arm files (SDF + meshes) #########
    # Sub-box 1 contains buttons to import grippers
    row0.label("Import modular robot parts to scene")
    sub_box_1 = import_box.box()
    sub_box_1.label('Import gripper')
    row1 = sub_box_1.row(align=True)
    row2 = sub_box_1.row(align=True)
    modules.ImportGripper1.place_button(row1)
    modules.ImportGripper2.place_button(row1)
    modules.ImportGripper3.place_button(row2)
    modules.ImportGripper4.place_button(row2)

    # Sub-box 2 contains buttons to import arms
    # TODO create buttons to import arm modules
    sub_box_2 = import_box.box()
    sub_box_2.label('Import arm')
    row1 = sub_box_2.row(align=True)
    modules.ImportArm1.place_button(row1)
    modules.ImportArm2.place_button(row1)

    #######################################################

    ######### Create box with merge functionality #########
    merge_box = layout.box()
    merge_box.label("Add module to robot")
    merge_box_row1 = merge_box.row(align=True)
    merge_col1 = merge_box_row1.column(align=True)
    merge_col2 = merge_box_row1.column(align=True)
    merge_box_row2 = merge_box.row(align=True)
    merge_col3 = merge_box_row2.column(align=True)
    merge_col4 = merge_box_row2.column(align=True)
    merge_box_row3 = merge_box.row(align=True)

    merge_col1.label("Select module to assign to robot '" + global_properties.model_name.get(context.scene) + "'")
    moduleMenuText = ""

    # Only show addable modules that can be selected in module selector menu
    if (bpy.context.active_object.name != global_properties.new_module_name.get(context.scene)):
        moduleMenuText = global_properties.new_module_name.get(context.scene)
    modules.ModuleMenu.putMenu(merge_col2, context, text=moduleMenuText)

    merge_col3.label("Select parent bone of '" + global_properties.model_name.get(context.scene) + "'")
    create_segment_selector(merge_col4, context)

    modules.MergeModuleToRobot.place_button(merge_box_row3)

    #######################################################

    # TODO Implement functionality to detach modules
