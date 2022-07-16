# 
# IMPORT SATURN LEV
# 

import os, sys
sys.path.append(os.path.dirname(__file__))

# modules
import kaitaistruct
from qslev import Qslev
from collections import defaultdict
from operator import add
import math
import numpy
import bpy
import bmesh
from mathutils import *

from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, CollectionProperty, BoolProperty, EnumProperty, FloatProperty

# bl_info
bl_info = {
	"name": "Sega Saturn Level (LEV) format",
	"author": "Jaycie Ewald, Rich Whitehouse",
	"version": (0, 0, 1),
	"blender": (3, 2, 0),
	"location": "File > Import",
	"description": "Import LEV",
	"warning": "",
	"doc_url": "",
	"support": "COMMUNITY",
	"category": "Import",
}

def register():
	bpy.utils.register_class(ImportLEV)
	bpy.types.TOPBAR_MT_file_import.append(menu_func)

def unregister():
	bpy.utils.unregister_class(ImportLEV)
	bpy.types.TOPBAR_MT_file_import.remove(menu_func)

if __name__ == "__main__":
	register()

class ImportLEV(bpy.types.Operator, ImportHelper):
	"""Load a Quake Sega Saturn Level (lev) File"""
	bl_idname = "import.lev"
	bl_label = "Import LEV"
	bl_options = {'UNDO'}

	filepath : StringProperty(name="File Path", description="File filepath used for importing the LEV file", maxlen=1024, default="", options={'HIDDEN'})
	files : CollectionProperty(type=bpy.types.OperatorFileListElement, options={'HIDDEN'})
	directory : StringProperty(maxlen=1024, default="", subtype='FILE_PATH', options={'HIDDEN'})
	filter_folder : BoolProperty(name="Filter Folders", description="", default=True, options={'HIDDEN'})
	filter_glob : StringProperty(default="*.lev", options={'HIDDEN'})

	bExtractTextures : BoolProperty(name="Extract Textures", default=False)
	bExtractEntities : BoolProperty(name="Extract Entities", default=False)
	bFixRotation : BoolProperty(name="Fix Rotation", default=True)
	bImportNodes : BoolProperty(name="Import Node Data", default=False)
	ImportScale : FloatProperty(name="Import Scale", default=0.25)

	def execute(self, context):
		load(context, self.filepath, self.bExtractTextures, self.bExtractEntities, self.ImportScale, self.bFixRotation, self.bImportNodes)
		return {'FINISHED'}

def menu_func(self, context):
	self.layout.operator(ImportLEV.bl_idname, text="Quake Sega Saturn Level (.lev)")

def load(context, filepath, bExtractTextures, bExtractEntities, ImportScale, bFixRotation, bImportNodes):
	print("Reading %s..." % filepath)

	name = bpy.path.basename(filepath)
	scene = bpy.context.scene

	lev = Qslev.from_file(filepath)

	print("Nodes: %i" % lev.header.nodecount)
	print("Planes: %i" % lev.header.planecount)
	print("Vertices: %i" % lev.header.vertcount)
	print("Quads: %i" % lev.header.quadcount)
	print("Entities: %i" % lev.header.entitycount)
	print("Tiles: %i" % lev.header.tileentrycount)

	lev_saturncolors = [
				[-16,-16,-16],	[-16,-15,-15],	[-15,-14,-14],
				[-14,-13,-13],	[-13,-12,-12],	[-12,-11,-11],
				[-11,-10,-10],	[-10,-9,-9],	[-9,-8,-8],
				[-8,-7,-7],		[-7,-6,-6],		[-6,-5,-5],
				[-5,-4,-4],		[-4,-3,-3],		[-3,-2,-2],
				[-2,-1,-1],		[-1,0,0],		[0,0,0]
	]

	lev_verts = []
	lev_vertcolorvalues = []
	lev_quads = []
	lev_quads_flags = []

	lev_tiles_verts = []
	lev_tiles_quads = []

	for lev.VertT in lev.verts:
		lev_verts.append([lev.VertT.position.x, lev.VertT.position.y, lev.VertT.position.z])
		lev_vertcolorvalues.append(lev.VertT.colorvalue)

	#for lev.QuadT in lev.quads:
		#lev_quads = range(lev.QuadT in lev.quads)
		#lev_quads.append([0, 0, 0, 0])
		#lev_quads.append([lev.QuadT.indices.x, lev.QuadT.indices.y, lev.QuadT.indices.z, lev.QuadT.indices.a])

	class NumpyFixToFloatConverter(object):
		def __init__(self, n_frac):
			self.n_frac = n_frac

		def __call__(self, values):
			return values / (2.0**self.n_frac)

	if (bImportNodes):
		for lev.NodeT in lev.nodes:
			node = lev.NodeT
			lev_node_verts = []
			lev_node_quads = []

			for x in range(node.lastplane - node.firstplane + 1):
				plane = lev.planes[node.firstplane + x]
				v0 = lev_verts[plane.vertices.x]
				v1 = lev_verts[plane.vertices.y]
				v2 = lev_verts[plane.vertices.z]
				v3 = lev_verts[plane.vertices.a]

				ofs = len(lev_node_verts)

				lev_node_verts.append(v0)
				lev_node_verts.append(v1)
				lev_node_verts.append(v2)
				lev_node_verts.append(v3)

				lev_node_quads.append([ofs, ofs + 1, ofs + 2, ofs + 3])

			mesh_node = bpy.data.meshes.new("Node")
			mesh_node.from_pydata(lev_node_verts, [], lev_node_quads)
			mesh_node.update()

			obj_node = bpy.data.objects.new("Node", mesh_node)
			obj_node.scale = [-ImportScale, ImportScale, ImportScale]
			if (bFixRotation):
				obj_node.rotation_euler = [math.radians(90), 0, 0]

			scene.collection.objects.link(obj_node)

	def add_empty(pos):
		empty = bpy.data.objects.new("empty", None)
		empty.location = pos
		empty.empty_display_size = 2
		empty.empty_display_type = "PLAIN_AXES"
		bpy.context.scene.collection.objects.link(empty)

	for lev.PlaneT in lev.planes:
		plane = lev.PlaneT
		if plane.tileindex < lev.header.tileentrycount:
			tile = lev.tiles[plane.tileindex]

			# thank u vfig
			def decode_vector(v):
				x0 = numpy.int16((v.x>>16)&0xFFFF)
				x1 = numpy.int16(v.x&0xFFFF)
				y0 = numpy.int16((v.y>>16)&0xFFFF)
				y1 = numpy.int16(v.y&0xFFFF)
				z0 = numpy.int16((v.z>>16)&0xFFFF)
				z1 = numpy.int16(v.z&0xFFFF)
				return Vector((float(x1), float(y1), float(z1)))

			for tileY in range(tile.height):
				for tileX in range(tile.width):
					base = decode_vector(tile.tilebasevec)
					horiz = decode_vector(tile.tilehorizvec)
					vert = decode_vector(tile.tilevertvec)

					tc0 = base + (vert * tileY) + (horiz * tileX)
					tc1 = tc0 + horiz
					tc2 = tc0 + horiz + vert
					tc3 = tc0 + vert

					points = tile.width + 1
					colorbase = (tileY * points) + tileX

					t0_color = tile.getcolordata[colorbase]
					t1_color = tile.getcolordata[colorbase + 1]
					t2_color = tile.getcolordata[colorbase + 1 + points]
					t3_color = tile.getcolordata[colorbase + points]

					ofs = len(lev_verts)

					lev_verts.append(tc0)
					lev_verts.append(tc1)
					lev_verts.append(tc2)
					lev_verts.append(tc3)
					lev_vertcolorvalues.append(t0_color)
					lev_vertcolorvalues.append(t1_color)
					lev_vertcolorvalues.append(t2_color)
					lev_vertcolorvalues.append(t3_color)
					lev_quads.append([ofs, ofs + 1, ofs + 2, ofs + 3])
					lev_quads_flags.append(plane.flags)

			#lev_quads.append([lev.PlaneT.vertices.x, lev.PlaneT.vertices.y, lev.PlaneT.vertices.z, lev.PlaneT.vertices.a])
		if plane.quadstartindex < lev.header.quadcount:
			for i in range(plane.quadendindex - plane.quadstartindex + 1):
				x = lev.quads[plane.quadstartindex + i].indices.x + plane.vertstartindex
				y = lev.quads[plane.quadstartindex + i].indices.y + plane.vertstartindex
				z = lev.quads[plane.quadstartindex + i].indices.z + plane.vertstartindex
				a = lev.quads[plane.quadstartindex + i].indices.a + plane.vertstartindex
				lev_quads.append([x, y, z, a])
				lev_quads_flags.append(plane.flags)

	mesh_quads = bpy.data.meshes.new(name)
	mesh_quads.from_pydata(lev_verts, [], lev_quads)
	mesh_quads.vertex_colors.new()
	mesh_quads.uv_layers.new()
	mesh_quads.update()

	mesh_tiles = bpy.data.meshes.new(name + " tiles")
	mesh_tiles.from_pydata(lev_tiles_verts, [], lev_tiles_quads)
	mesh_tiles.vertex_colors.new()
	mesh_tiles.uv_layers.new()
	mesh_tiles.update()

	# sort out vertex colors
	# add 31 to make them positive, and then divide by 31 to map them between 0 and 1
	# color = [31 + x for x in lev_saturncolors[10]]
	# color = [x / 31 for x in color]
	# color.extend([0])
	# print(color)

	vertex_map = defaultdict(list)

	# turns out we don't even need this, since just creating a blank UV layer maps all the quads the same as saturn hardware...
	#for face in mesh_quads.polygons:
	#	for vert_idx, loop_idx in zip(face.vertices, face.loop_indices):
	#		uv_coords = mesh_quads.uv_layers.active.data[loop_idx].uv
	#		print("face idx: %i, vert idx: %i, uvs: %f, %f" % (face.index, vert_idx, uv_coords.x, uv_coords.y))

	layer_flags = mesh_quads.polygon_layers_float.new(name="Source Plane Flags")
	layer_collisionflags = mesh_quads.polygon_layers_float.new(name="Source Plane Collision Flags")

	for poly in mesh_quads.polygons:
		layer_flags.data[poly.index].value = lev_quads_flags[poly.index]
		for vert_static_index, vert_loop_index in zip(poly.vertices, poly.loop_indices):
			vertex_map[vert_static_index].append(vert_loop_index)

	for vert_static_index, vert_loop_indexes in vertex_map.items():
		for vert_loop_index in vert_loop_indexes:
			color = [31 + x for x in lev_saturncolors[lev_vertcolorvalues[vert_static_index]]]
			color = [x / 31 for x in color] + [0]
			mesh_quads.vertex_colors.active.data[vert_loop_index].color = color

	obj_quads = bpy.data.objects.new(name, mesh_quads)
	obj_tiles = bpy.data.objects.new(name + " tiles", mesh_tiles)

	obj_quads.scale = [-ImportScale, ImportScale, ImportScale]
	obj_tiles.scale = [-ImportScale, ImportScale, ImportScale]

	if (bFixRotation):
		obj_quads.rotation_euler = [math.radians(90), 0, 0]
		obj_tiles.rotation_euler = [math.radians(90), 0, 0]

	scene.collection.objects.link(obj_quads)
	#scene.collection.objects.link(obj_tiles)

	# textures

	if (bExtractTextures):
		# this code SUCKS
		skypalettepixels = []

		for i in range(16):
			skypalettepixels.append(lev.skydata.skypalette[i].r * 0x1F // 0xFF)
			skypalettepixels.append(lev.skydata.skypalette[i].g * 0x1F // 0xFF)
			skypalettepixels.append(lev.skydata.skypalette[i].b * 0x1F // 0xFF)
			skypalettepixels.append(lev.skydata.skypalette[i].a)

		print(skypalettepixels)

		skypaletteimage = bpy.data.images.new("Sky Palette", alpha=False, width=8, height=2)
		skypaletteimage.pixels = skypalettepixels
		skypaletteimage.filepath_raw = filepath + ".skypalette.png"
		skypaletteimage.file_format = "PNG"
		skypaletteimage.update()
		skypaletteimage.save()

	# now done with the mesh, write out some entitiy data

	if (bExtractEntities):
		def match_entity(ent):
			match ent:
				case 146:
					return "func_mover"
				case _:
					return str(ent)

		entities_doc = open(filepath + ".ent",'w')

		for lev.EntityT in lev.entities:
			ent = lev.EntityT
			enttype = match_entity(ent.enttype)
			entloc = [ent.getentitydata.data[0], -ent.getentitydata.data[2], ent.getentitydata.data[1]]

			#print(str(enttype) + " position: " + str(entloc))

			empty_ent = bpy.data.objects.new(enttype, None)
			empty_ent.location = entloc
			empty_ent.empty_display_size = 2
			empty_ent.empty_display_type = "PLAIN_AXES"
			bpy.context.scene.collection.objects.link(empty_ent)

			entities_doc.write("{\n")
			entities_doc.write("\"classname\" \"%s\"\n" % enttype)
			for i in range(len(ent.getentitydata.data)):
				entities_doc.write("\"byte%i\" \"%s\"\n" % (i, ent.getentitydata.data[i]))
			entities_doc.write("}\n")