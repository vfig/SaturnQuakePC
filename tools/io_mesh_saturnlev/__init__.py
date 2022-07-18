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
from bpy.props import StringProperty, CollectionProperty, BoolProperty, EnumProperty, FloatProperty, IntProperty

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
	bExtractSkyTextures : BoolProperty(name="Extract Sky Textures", default=False)
	bExtractEntities : BoolProperty(name="Extract Entities", default=False)
	bFixRotation : BoolProperty(name="Fix Rotation", default=True)
	bImportNodes : BoolProperty(name="Import Node Data", default=False)
	ImportScale : FloatProperty(name="Import Scale", default=0.25)

	debug_planes : BoolProperty(name="DEBUG: show planes with tiles", default=False)
	debug_plane_index : IntProperty(name="DEBUG: show only this specific plane index", default=-1)

	def execute(self, context):
		load(context, self.filepath, self.bExtractTextures, self.bExtractEntities, self.ImportScale, self.bFixRotation, self.bImportNodes, self.debug_planes, self.debug_plane_index, self.bExtractSkyTextures)
		return {'FINISHED'}

def menu_func(self, context):
	self.layout.operator(ImportLEV.bl_idname, text="Quake Sega Saturn Level (.lev)")

def load(context, filepath, bExtractTextures, bExtractEntities, ImportScale, bFixRotation, bImportNodes, debug_planes, debug_plane_index, bExtractSkyTextures):
	print("Reading %s..." % filepath)

	name = bpy.path.basename(filepath)
	scene = bpy.context.scene

	debug_mat_fix = Matrix.Identity(4)
	if bFixRotation:
		# Because the empties (and the planes as I am constructing them) do not
		# have their origin at zero, we cant just throw the same rotate-and-
		# flip-x approach to fixing the rotation as elsewhere. So instead for
		# those we use this matrix which does the same thing.
		debug_mat_fix[0] = [-1.0, 0.0, 0.0, 0.0]
		debug_mat_fix[1] = [ 0.0, 0.0,-1.0, 0.0]
		debug_mat_fix[2] = [ 0.0, 1.0, 0.0, 0.0]
		debug_mat_fix[3] = [ 0.0, 0.0, 0.0, 1.0]

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
	lev_materials = []

	for lev.VertT in lev.verts:
		lev_verts.append([lev.VertT.position.x, lev.VertT.position.y, lev.VertT.position.z])
		lev_vertcolorvalues.append(lev.VertT.colorvalue)

	#for lev.QuadT in lev.quads:
		#lev_quads = range(lev.QuadT in lev.quads)
		#lev_quads.append([0, 0, 0, 0])
		#lev_quads.append([lev.QuadT.indices.x, lev.QuadT.indices.y, lev.QuadT.indices.z, lev.QuadT.indices.a])

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
			if (bFixRotation):
				obj_node.scale = [-ImportScale, ImportScale, ImportScale]
				obj_node.rotation_euler = [math.radians(90), 0, 0]
			else:
				obj_node.scale = [ImportScale, ImportScale, ImportScale]

			scene.collection.objects.link(obj_node)

	def debug_add_empty(pos, name):
		empty = bpy.data.objects.new(name, None)
		empty.location = debug_mat_fix@Vector(pos)
		empty.empty_display_size = 2
		empty.empty_display_type = "PLAIN_AXES"
		empty.show_name = True
		scene.collection.objects.link(empty)

	def debug_add_plane_mesh(verts, name):
		verts = [debug_mat_fix@Vector(v) for v in verts]
		total = Vector((0.0,0.0,0.0))
		for v in verts:
			total += v
		center = total/len(verts)
		for i,v in enumerate(verts):
			verts[i] = v-center
		mesh = bpy.data.meshes.new(name)
		mesh.from_pydata(verts, [], [(0,1,2,3)])
		mesh.update()
		obj = bpy.data.objects.new(name, mesh)
		obj.show_name = True
		obj.location = center
		obj.display_type = 'WIRE'
		scene.collection.objects.link(obj)

	# thank you vfig
	for plane_index, lev.PlaneT in enumerate(lev.planes):
		plane = lev.PlaneT
		if plane.tileindex < lev.header.tileentrycount:
			tile = lev.tiles[plane.tileindex]
			X = Vector(lev_verts[plane.vertices.x])
			Y = Vector(lev_verts[plane.vertices.y])
			Z = Vector(lev_verts[plane.vertices.z])
			A = Vector(lev_verts[plane.vertices.a])

			if plane_index == debug_plane_index:
				debug_add_empty(X, "X")
				debug_add_empty(Y, "Y")
				debug_add_empty(Z, "Z")
				debug_add_empty(A, "A")
			elif debug_plane_index >= 0:
				continue

			def convert_int16_16_vector(v):
				return Vector((
					round(v[0]/65536.0),
					round(v[1]/65536.0),
					round(v[2]/65536.0)
					))

			width = tile.width
			height = tile.height

			for tileY in range(height):
				for tileX in range(width):
					tc0i = [
						tile.tilebasevec.x + tileX*tile.tilehorizvec.x + tileY*tile.tilevertvec.x,
						tile.tilebasevec.y + tileX*tile.tilehorizvec.y + tileY*tile.tilevertvec.y,
						tile.tilebasevec.z + tileX*tile.tilehorizvec.z + tileY*tile.tilevertvec.z,
						]
					tc1i = [
						tc0i[0] + tile.tilehorizvec.x,
						tc0i[1] + tile.tilehorizvec.y,
						tc0i[2] + tile.tilehorizvec.z,
						]
					tc2i = [
						tc0i[0] + tile.tilehorizvec.x + tile.tilevertvec.x,
						tc0i[1] + tile.tilehorizvec.y + tile.tilevertvec.y,
						tc0i[2] + tile.tilehorizvec.z + tile.tilevertvec.z,
						]
					tc3i = [
						tc0i[0] + tile.tilevertvec.x,
						tc0i[1] + tile.tilevertvec.y,
						tc0i[2] + tile.tilevertvec.z,
						]
					tc0 = convert_int16_16_vector(tc0i)
					tc1 = convert_int16_16_vector(tc1i)
					tc2 = convert_int16_16_vector(tc2i)
					tc3 = convert_int16_16_vector(tc3i)

					if plane_index==debug_plane_index and tileX==0 and tileY==0:
						print(f"tc0: {tc0i} ; {tc0}")
						print(f"tc1: {tc1i} ; {tc1}")
						print(f"tc2: {tc2i} ; {tc2}")
						print(f"tc3: {tc3i} ; {tc3}")
						debug_add_empty(tc0, "origin")
						debug_add_empty(tc1, "U")
						debug_add_empty(tc3, "V")

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
			if debug_planes:
				debug_add_plane_mesh([lev_verts[plane.vertices.x],lev_verts[plane.vertices.y],lev_verts[plane.vertices.z],lev_verts[plane.vertices.a]], f"Plane:{plane_index}, tile:{plane.tileindex}")
			#lev_quads.append([lev.PlaneT.vertices.x, lev.PlaneT.vertices.y, lev.PlaneT.vertices.z, lev.PlaneT.vertices.a])
		
	for lev.PlaneT in lev.planes:
		plane = lev.PlaneT
		if plane.quadstartindex < lev.header.quadcount:
			for i in range(plane.quadendindex - plane.quadstartindex + 1):
				quad = lev.quads[plane.quadstartindex + i]
				x = quad.indices.x + plane.vertstartindex
				y = quad.indices.y + plane.vertstartindex
				z = quad.indices.z + plane.vertstartindex
				a = quad.indices.a + plane.vertstartindex
				lev_quads.append([x, y, z, a])
				lev_quads_flags.append(plane.flags)

	mesh_quads = bpy.data.meshes.new(name)
	mesh_quads.from_pydata(lev_verts, [], lev_quads)
	mesh_quads.vertex_colors.new()
	mesh_quads.uv_layers.new()
	mesh_quads.update()

	vertex_map = defaultdict(list)

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

	if (bExtractTextures):
		for i, lev.TextureT in enumerate(lev.texturedata.textures):
			tex = lev.TextureT
			if tex.type != 130: break
			tex_pixels = []
			tex_palette = [
						[0, 0, 0, 0],	[0, 0, 0, 0],	[0, 0, 0, 0], [0, 0, 0, 0],
						[0, 0, 0, 0],	[0, 0, 0, 0],	[0, 0, 0, 0], [0, 0, 0, 0],
						[0, 0, 0, 0],	[0, 0, 0, 0],	[0, 0, 0, 0], [0, 0, 0, 0],
						[0, 0, 0, 0],	[0, 0, 0, 0],	[0, 0, 0, 0], [0, 0, 0, 0]
			]

			for x, lev.PaletteEntryT in enumerate(tex.palette):
				entry = lev.PaletteEntryT
				tex_palette[x] = [(entry.r / 31), (entry.g / 31), (entry.b / 31), entry.a]

			for y in range(4096):
				tex_pixels.append(tex_palette[tex.imagedata[y]][0])
				tex_pixels.append(tex_palette[tex.imagedata[y]][1])
				tex_pixels.append(tex_palette[tex.imagedata[y]][2])
				tex_pixels.append(tex_palette[tex.imagedata[y]][3])

			texture = bpy.data.images.new("Texture", alpha=True, width=64, height=64)
			texture.pixels = tex_pixels
			texture.filepath_raw = filepath + f".texture.{i}.png"
			texture.file_format = "PNG"
			texture.update()
			texture.save()

		numTiles = 0

		shaderfile = open(filepath + ".shader", "w")

		for lev.PlaneT in lev.planes:
			plane = lev.PlaneT

			if plane.tileindex < lev.header.tileentrycount:
				tile = lev.tiles[plane.tileindex]
				width = tile.width
				height = tile.height

				for tileY in range(height):
					for tileX in range(width):
						tile_index = (tileY * width) + tileX
						tile_textureindex = tile.gettiletexturedata[(tile_index * 2) + 1]
						if tile_textureindex not in lev_materials:
							mat = bpy.data.materials.new(name = name + f"-material-{tile_textureindex}")
							mat.use_nodes = True
							bsdf = mat.node_tree.nodes["Principled BSDF"]
							texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
							texImage.image = bpy.data.images.load(filepath + f".texture.{tile_textureindex}.png")
							mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])
							obj_quads.data.materials.append(mat)
							lev_materials.append(tile_textureindex)

							shaderfile.write(mat.name)
							shaderfile.write(" { program saturn_level diffusemap textures/levels/" + name + "/")
							shaderfile.write(name + f".texture.{tile_textureindex}.png")
							shaderfile.write(" cull disable }\n")


						obj_quads.data.polygons[numTiles].material_index = lev_materials.index(tile_textureindex)
						numTiles += 1

		numQuads = 0

		for lev.PlaneT in lev.planes:
			plane = lev.PlaneT
			if plane.quadstartindex < lev.header.quadcount:
				for i in range(plane.quadendindex - plane.quadstartindex + 1):
					quad = lev.quads[plane.quadstartindex + i]
					if quad.textureindex not in lev_materials:
						mat = bpy.data.materials.new(name = name + f"-material-{quad.textureindex}")
						mat.use_nodes = True
						bsdf = mat.node_tree.nodes["Principled BSDF"]
						texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
						texImage.image = bpy.data.images.load(filepath + f".texture.{quad.textureindex}.png")
						mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])
						obj_quads.data.materials.append(mat)
						lev_materials.append(quad.textureindex)

						shaderfile.write(mat.name)
						shaderfile.write(" { program saturn_level diffusemap textures/levels/" + name + "/")
						shaderfile.write(name + f".texture.{quad.textureindex}.png")
						shaderfile.write(" cull disable }\n")

					obj_quads.data.polygons[numTiles + numQuads].material_index = lev_materials.index(quad.textureindex)
					numQuads += 1

	if (bExtractSkyTextures):
		skypalette = [
					[0, 0, 0, 0],	[0, 0, 0, 0],	[0, 0, 0, 0], [0, 0, 0, 0],
					[0, 0, 0, 0],	[0, 0, 0, 0],	[0, 0, 0, 0], [0, 0, 0, 0],
					[0, 0, 0, 0],	[0, 0, 0, 0],	[0, 0, 0, 0], [0, 0, 0, 0],
					[0, 0, 0, 0],	[0, 0, 0, 0],	[0, 0, 0, 0], [0, 0, 0, 0]
		]

		for i, lev.PaletteEntryT in enumerate(lev.skydata.skypalette):
			entry = lev.PaletteEntryT
			skypalette[i] = [(entry.r / 31), (entry.g / 31), (entry.b / 31), entry.a]

		for x, lev.SkyimageT in enumerate(lev.skydata.skyimagedata):
			image = lev.SkyimageT

			pixels = []

			for i in range(4096):
				pixels.append(skypalette[image.pixels[i]][0])
				pixels.append(skypalette[image.pixels[i]][1])
				pixels.append(skypalette[image.pixels[i]][2])
				pixels.append(skypalette[image.pixels[i]][3])

			skyimage = bpy.data.images.new("Sky Image", alpha=True, width=64, height=64)
			skyimage.pixels = pixels
			skyimage.filepath_raw = filepath + f".sky.{x}.png"
			skyimage.file_format = "PNG"
			skyimage.update()
			skyimage.save()

		#skypaletteimage = bpy.data.images.new("Sky Palette", alpha=False, width=8, height=2)
		#skypaletteimage.pixels = skypalettepixels
		#skypaletteimage.filepath_raw = filepath + ".skypalette.png"
		#skypaletteimage.file_format = "PNG"
		#skypaletteimage.update()
		#skypaletteimage.save()

	# now done with the mesh, write out some entitiy data

	if (bExtractEntities):
		def match_entity(ent):
			match ent:
				# lights and light subtypes
				case 38: # static white light
					return "light"
				case 92: # ?
					return "light"
				case 110: # heavy red pulse
					return "light"
				case 232: # flicker
					return "light"
				case 235: # ?
					return "light"
				case 253: # ?
					return "light"
				# ammo and items
				case 29:
					return "item_shells"
				case 88:
					return "item_armor1"
				# player
				case 13:
					return "info_player_start"
				# monsters
				case 243:
					return "monster_army"
				case 244:
					return "monster_dog"
				# miscellaneous
				case 113:
					return "light_flame_large_yellow"
				# poly objects
				case 146:
					return "func_door"
				case _:
					return str(ent)

		entities_doc = open(filepath + ".ent",'w')

		entities = []

		for lev.EntityT in lev.entities:
			ent = lev.EntityT
			enttype = "Entity " + match_entity(ent.enttype)
			if (bFixRotation):
				entloc = [-ent.getentitydata.origin.x * ImportScale, -ent.getentitydata.origin.z * ImportScale, ent.getentitydata.origin.y * ImportScale]
			else:
				entloc = [ent.getentitydata.origin.x * ImportScale, ent.getentitydata.origin.y * ImportScale, ent.getentitydata.origin.z * ImportScale]

			entloc_original = [ent.getentitydata.origin.x * ImportScale, ent.getentitydata.origin.y * ImportScale, ent.getentitydata.origin.z * ImportScale]

			empty_ent = bpy.data.objects.new(enttype, None)
			empty_ent.location = entloc
			empty_ent["original_origin"] = f"{entloc_original[0]} {entloc_original[1]} {entloc_original[2]}"
			empty_ent["classname"] = match_entity(ent.enttype)
			empty_ent.empty_display_size = 2
			empty_ent.empty_display_type = "PLAIN_AXES"
			scene.collection.objects.link(empty_ent)
			entities_doc.write("{\n")
			entities_doc.write(f"\"classname\" \"" + match_entity(ent.enttype) + "\"\n")
			entities_doc.write(f"\"origin\" \"{entloc[0]} {entloc[1]} {entloc[2]}\"\n")
			entities_doc.write("}\n")

			#empty_ent.parent = obj_quads

	if (bFixRotation):
		obj_quads.scale = [-ImportScale, ImportScale, ImportScale]
		obj_quads.rotation_euler = [math.radians(90), 0, 0]
	else:
		obj_quads.scale = [ImportScale, ImportScale, ImportScale]

	scene.collection.objects.link(obj_quads)