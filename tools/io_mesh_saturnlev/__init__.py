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

	bExtractTextures : BoolProperty(name="Extract Textures", default=True)
	bExtractEntities : BoolProperty(name="Extract Entities", default=False)
	ImportScale : FloatProperty(name="Import Scale", default=0.25)

	def execute(self, context):
		load(context, self.filepath, self.bExtractTextures, self.bExtractEntities, self.ImportScale)
		return {'FINISHED'}

def menu_func(self, context):
	self.layout.operator(ImportLEV.bl_idname, text="Quake Sega Saturn Level (.lev)")

def load(context, filepath, bExtractTextures, bExtractEntities, ImportScale):
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
				[-16,-16,-16], [-16,-15,-15], [-15,-14,-14],
				[-14,-13,-13], [-13,-12,-12], [-12,-11,-11],
				[-11,-10,-10], [-10,-9,-9],   [-9,-8,-8],
				[-8,-7,-7],	[-7,-6,-6],	[-6,-5,-5],
				[-5,-4,-4],	[-4,-3,-3],	[-3,-2,-2],
				[-2,-1,-1],	[-1,0,0],	  [0,0,0]
	]

	lev_verts = []
	lev_vertcolorvalues = []
	lev_quads = []

	lev_tile_verts = []
	lev_tile_quads = []

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

	for lev.PlaneT in lev.planes:
		plane = lev.PlaneT
		if plane.tileindex < lev.header.tileentrycount:
			tile = lev.tiles[plane.tileindex]
			for tileY in range(tile.height):
				for tileX in range(tile.width):
					magic = 1<<16
					tile_base_vec = [tile.tilebasevec.x / magic, tile.tilebasevec.y / magic, tile.tilebasevec.z / magic]
					tile_horiz_vec = [tile.tilehorizvec.x / magic, tile.tilehorizvec.y / magic, tile.tilehorizvec.z / magic]
					tile_vert_vec = [tile.tilevertvec.x / magic, tile.tilevertvec.y / magic, tile.tilevertvec.z / magic]
					tilecorner0 = [
						tile_base_vec[0] + (tile_vert_vec[0] * tileY) + (tile_horiz_vec[0] * tileX),
						tile_base_vec[1] + (tile_vert_vec[1] * tileY) + (tile_horiz_vec[1] * tileX),
						tile_base_vec[2] + (tile_vert_vec[2] * tileY) + (tile_horiz_vec[2] * tileX),
					]
					tilecorner1 = [
						tilecorner0[0] + tile_horiz_vec[0],
						tilecorner0[1] + tile_horiz_vec[1],
						tilecorner0[2] + tile_horiz_vec[2],
                    ]
					tilecorner2 = [
						tilecorner0[0] + tile_horiz_vec[0] + tile_vert_vec[0],
						tilecorner0[1] + tile_horiz_vec[1] + tile_vert_vec[2],
						tilecorner0[2] + tile_horiz_vec[2] + tile_vert_vec[2],
					]
					tilecorner3 = [
						tilecorner0[0] + tile_vert_vec[0],
						tilecorner0[1] + tile_vert_vec[1],
						tilecorner0[2] + tile_vert_vec[2],
					]

					lev_tile_verts.append((tilecorner0[0], tilecorner0[1], tilecorner0[2]))
					lev_tile_verts.append((tilecorner1[0], tilecorner1[1], tilecorner1[2]))
					lev_tile_verts.append((tilecorner2[0], tilecorner2[1], tilecorner2[2]))
					lev_tile_verts.append((tilecorner3[0], tilecorner3[1], tilecorner3[2]))
			lev_quads.append([lev.PlaneT.vertices.x, lev.PlaneT.vertices.y, lev.PlaneT.vertices.z, lev.PlaneT.vertices.a])
		elif plane.quadstartindex < lev.header.quadcount:
			for i in range(plane.quadendindex - plane.quadstartindex + 1):
				x = lev.quads[plane.quadstartindex + i].indices.x + plane.vertstartindex
				y = lev.quads[plane.quadstartindex + i].indices.y + plane.vertstartindex
				z = lev.quads[plane.quadstartindex + i].indices.z + plane.vertstartindex
				a = lev.quads[plane.quadstartindex + i].indices.a + plane.vertstartindex
				lev_quads.append([x, y, z, a])

	mesh_quads = bpy.data.meshes.new(name + " quads")
	mesh_quads.from_pydata(lev_verts, [], lev_quads)
	mesh_quads.vertex_colors.new()
	mesh_quads.update()

	#mesh_tiles = bpy.data.meshes.new(name + " tiles")
	#mesh_tiles.from_pydata(lev_tile_verts, [], [])
	#mesh_tiles.vertex_colors.new()
	#mesh_tiles.update()

	# sort out vertex colors
	# add 31 to make them positive, and then divide by 31 to map them between 0 and 1
	# color = [31 + x for x in lev_saturncolors[10]]
	# color = [x / 31 for x in color]
	# color.extend([0])
	# print(color)

	vertex_map = defaultdict(list)

	for poly in mesh_quads.polygons:
		for vert_static_index, vert_loop_index in zip(poly.vertices, poly.loop_indices):
			vertex_map[vert_static_index].append(vert_loop_index)

	for vert_static_index, vert_loop_indexes in vertex_map.items():
		for vert_loop_index in vert_loop_indexes:
			color = [31 + x for x in lev_saturncolors[lev_vertcolorvalues[vert_static_index]]]
			color = [x / 31 for x in color] + [0]
			mesh_quads.vertex_colors.active.data[vert_loop_index].color = color

	obj_quads = bpy.data.objects.new(name + " quads", mesh_quads)
	#obj_tiles = bpy.data.objects.new(name + " tiles", mesh_tiles)

	obj_quads.scale = [ImportScale, ImportScale, ImportScale]
	obj_quads.rotation_euler = [math.radians(90), 0, 0]
	#obj_tiles.scale = [ImportScale, ImportScale, ImportScale]
	#obj_tiles.rotation_euler = [math.radians(90), 0, 0]

	scene.collection.objects.link(obj_quads)
	#scene.collection.objects.link(obj_tiles)

	# textures

	if (bExtractTextures):
		# this code SUCKS
		skypalettepixels = (
			(lev.skydata.skypalette[0].r * 255 + 15) / 31, (lev.skydata.skypalette[0].g * 255 + 15) / 31, (lev.skydata.skypalette[0].b * 255 + 15) / 31, 255,
			(lev.skydata.skypalette[1].r * 255 + 15) / 31, (lev.skydata.skypalette[1].g * 255 + 15) / 31, (lev.skydata.skypalette[1].b * 255 + 15) / 31, 255,
			(lev.skydata.skypalette[2].r * 255 + 15) / 31, (lev.skydata.skypalette[2].g * 255 + 15) / 31, (lev.skydata.skypalette[2].b * 255 + 15) / 31, 255,
			(lev.skydata.skypalette[3].r * 255 + 15) / 31, (lev.skydata.skypalette[3].g * 255 + 15) / 31, (lev.skydata.skypalette[3].b * 255 + 15) / 31, 255,
			(lev.skydata.skypalette[4].r * 255 + 15) / 31, (lev.skydata.skypalette[4].g * 255 + 15) / 31, (lev.skydata.skypalette[4].b * 255 + 15) / 31, 255,
			(lev.skydata.skypalette[5].r * 255 + 15) / 31, (lev.skydata.skypalette[5].g * 255 + 15) / 31, (lev.skydata.skypalette[5].b * 255 + 15) / 31, 255,
			(lev.skydata.skypalette[6].r * 255 + 15) / 31, (lev.skydata.skypalette[6].g * 255 + 15) / 31, (lev.skydata.skypalette[6].b * 255 + 15) / 31, 255,
			(lev.skydata.skypalette[7].r * 255 + 15) / 31, (lev.skydata.skypalette[7].g * 255 + 15) / 31, (lev.skydata.skypalette[7].b * 255 + 15) / 31, 255,
		)

		print(skypalettepixels)

		skypaletteimage = bpy.data.images.new("Sky Palette", alpha=True, width=8, height=2)
		skypaletteimage.pixels = skypalettepixels
		skypaletteimage.alpha_mode = "STRAIGHT"
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