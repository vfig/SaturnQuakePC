# 
# IMPORT SATURN LEV
# 

import os, sys
sys.path.append(os.path.dirname(__file__))

# custom modules
import kaitaistruct
from lev_quake import LevQuake
from lev_powerslave import LevPowerslave
from lev_duke import LevDuke

# python modules
from collections import defaultdict
from operator import add
import math
from enum import Flag
import numpy

# blender python modules
import bpy
import bmesh
from mathutils import *
from bpy_extras.io_utils import *
from bpy.props import *

# bl_info
bl_info = {
	"name": "Sega Saturn SD Engine Level (.lev) format",
	"author": "Jaycie Ewald",
	"version": (0, 0, 1),
	"blender": (3, 2, 0),
	"location": "File > Import",
	"description": "Import .lev",
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

def menu_func(self, context):
	self.layout.operator(ImportLEV.bl_idname, text="Sega Saturn SD Engine Level (.lev)")

class ImportLEV(bpy.types.Operator, ImportHelper):
	"""Load a Sega Saturn SD Engine Level (.lev) File"""
	bl_idname = "import.lev"
	bl_label = "Import LEV"
	bl_options = {'UNDO'}

	# hidden properties
	filepath : StringProperty(name="File Path", description="File filepath used for importing the LEV file", maxlen=1024, default="", options={'HIDDEN'})
	files : CollectionProperty(type=bpy.types.OperatorFileListElement, options={'HIDDEN'})
	directory : StringProperty(maxlen=1024, default="", subtype='FILE_PATH', options={'HIDDEN'})
	filter_folder : BoolProperty(name="Filter Folders", description="", default=True, options={'HIDDEN'})
	filter_glob : StringProperty(default="*.lev;*.dat;", options={'HIDDEN'})

	level_formats = (
		("QUAKE", "Quake", "Sega Saturn SD Engine (Quake)"),
		("POWERSLAVE", "PowerSlave (Experimental)", "Sega Saturn SD Engine (PowerSlave)"),
		("DUKE3D", "Duke Nukem 3D (Experimental)", "Sega Saturn SD Engine (Duke Nukem 3D)"),
		("POWERSLAVEPSX", "PowerSlave PSX (Experimental)", "PlayStation SD Engine (PowerSlave)")
	)

	# user controllable properties
	bExtractTextures : BoolProperty(name="Extract Textures", default=True)
	bExtractPalettes : BoolProperty(name="Extract Texture Palettes", default=False)
	bExtractSkyTextures : BoolProperty(name="Extract Sky Textures", default=True)
	bExtractEntities : BoolProperty(name="Extract Entities", default=True)
	bFixRotation : BoolProperty(name="Fix Rotation", default=True)
	bImportNodes : BoolProperty(name="Import Node Data", default=False)
	bFlagPlanes : BoolProperty(name="Generated Flagged Planes", default=False)
	bGenerateMapFile : BoolProperty(name="Generate .map File", default=False)
	ImportScale : FloatProperty(name="Import Scale", default=1.0)
	LevelFormat : EnumProperty(name="Level Format", items=level_formats, default="QUAKE")

	# debug properties (removeme)
	debug_planes : BoolProperty(name="DEBUG: show planes with tiles", default=False)
	debug_plane_index : IntProperty(name="DEBUG: show only this specific plane index", default=-1)

	def execute(self, context):
		print("Reading %s..." % self.filepath)

		name = bpy.path.basename(self.filepath)
		scene = bpy.context.scene

		debug_mat_fix = Matrix.Identity(4)

		if self.bFixRotation:
			# Because the empties (and the planes as I am constructing them) do not
			# have their origin at zero, we cant just throw the same rotate-and-
			# flip-x approach to fixing the rotation as elsewhere. So instead for
			# those we use this matrix which does the same thing.
			debug_mat_fix[0] = [-1.0, 0.0, 0.0, 0.0]
			debug_mat_fix[1] = [ 0.0, 0.0,-1.0, 0.0]
			debug_mat_fix[2] = [ 0.0, 1.0, 0.0, 0.0]
			debug_mat_fix[3] = [ 0.0, 0.0, 0.0, 1.0]

		#
		# useful functions
		#

		def generate_vertex_colors(mesh, palette, values):
			vertex_map = defaultdict(list)

			for poly in mesh.polygons:
				for vert_static_index, vert_loop_index in zip(poly.vertices, poly.loop_indices):
					vertex_map[vert_static_index].append(vert_loop_index)

			for vert_static_index, vert_loop_indexes in vertex_map.items():
				for vert_loop_index in vert_loop_indexes:
					color = [31 + x for x in palette[values[vert_static_index]]]
					color = [x / 31 for x in color] + [0]
					mesh.vertex_colors.active.data[vert_loop_index].color = color

		def generate_vertex_brightness(mesh, values):
			vertex_map = defaultdict(list)

			for poly in mesh.polygons:
				for vert_static_index, vert_loop_index in zip(poly.vertices, poly.loop_indices):
					vertex_map[vert_static_index].append(vert_loop_index)

			for vert_static_index, vert_loop_indexes in vertex_map.items():
				for vert_loop_index in vert_loop_indexes:
					brightness = 16 - values[vert_static_index] / 16
					color = [brightness, brightness, brightness] + [0]
					mesh.vertex_colors.active.data[vert_loop_index].color = color

		def compute_palette(item, container):
			palette_entries = []

			for item in container:
				palette_entries.append([(item.r / 31), (item.g / 31), (item.b / 31), item.a])

			return palette_entries

		def compute_texture(item, imagesize):
			pixels = []

			for y in range(imagesize[1]):
				for x in range(imagesize[0]):
					pos = (y * imagesize[0]) + x
					pixel = item[pos]
					pixels.append(pixel[0])
					pixels.append(pixel[1])
					pixels.append(pixel[2])
					pixels.append(pixel[3])

			return pixels

		def compute_texture_paletted(container, imagesize, palette):
			pixels = []

			for y in range(imagesize[1]):
				for x in range(imagesize[0]):
					pos = (y * imagesize[0]) + x
					pixel = palette[container[pos]]
					pixels.append(pixel[0])
					pixels.append(pixel[1])
					pixels.append(pixel[2])
					pixels.append(pixel[3])

			return pixels

		def write_png(imagename, imagesize, a, pixel_struct):
			image = bpy.data.images.new(name=imagename, alpha=a, width=imagesize[0], height=imagesize[1])
			image.pixels = pixel_struct
			image.filepath_raw = self.filepath + "." + imagename + ".png"
			image.file_format = "PNG"
			image.update()
			image.save()

		def add_mesh(name, vertices, edges, polys):
			mesh = bpy.data.meshes.new(name)
			mesh.from_pydata(vertices, edges, polys)
			mesh.vertex_colors.new()
			mesh.uv_layers.new()
			mesh.update()

			return mesh

		def add_object(name, mesh):
			object = bpy.data.objects.new(name, mesh)

			return object

		def calc_object_rotation_scale(object):
			if self.bFixRotation:
				object.scale = [-self.ImportScale, self.ImportScale, self.ImportScale]
				object.rotation_euler = [math.radians(90), 0, 0]
			else:
				object.scale = [self.ImportScale, self.ImportScale, self.ImportScale]

		def link_object(object):
			scene.collection.objects.link(object)

		def write_material(name):
			mat = bpy.data.materials.new(name = name)
			mat.use_nodes = True
			bsdf = mat.node_tree.nodes["Principled BSDF"]
			texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
			texImage.image = bpy.data.images.load(self.filepath + f".texture.{tile_textureindex}.png")
			mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])

			return mat

		def match_entity(ent):
			match ent:
				# lights and light subtypes
				case 38: return "light" # static white
				case 92: return "light" # (style?)
				case 110: return "light" # heavy red pulse
				case 232: return "light" # flicker
				case 235: return "light" # (style?)
				case 253: return "light" # (style?)
				# ammo and items
				case 29: return "item_shells"
				case 88: return "item_armor1"
				# player
				case 13: return "info_player_start"
				# monsters
				case 243: return "monster_army"
				case 244: return "monster_dog"
				# miscellaneous
				case 113: return "light_flame_large_yellow"
				# poly objects
				case 146: return "misc_polymover"
				# default
				case _: return str(ent)

		#
		# defs
		#

		lev_saturncolors = [
					[-16,-16,-16],	[-16,-15,-15],	[-15,-14,-14],
					[-14,-13,-13],	[-13,-12,-12],	[-12,-11,-11],
					[-11,-10,-10],	[-10,-9,-9],	[-9,-8,-8],
					[-8,-7,-7],		[-7,-6,-6],		[-6,-5,-5],
					[-5,-4,-4],		[-4,-3,-3],		[-3,-2,-2],
					[-2,-1,-1],		[-1,0,0],		[0,0,0]
		]

		#
		# duke nukem 3d (experimental)
		#

		if self.LevelFormat == "DUKE3D":

			lev = LevDuke.from_file(self.filepath)

			#sector = lev.SectorT
			vertex = lev.VertexT
			plane = lev.PlaneT

			lev_verts = []
			lev_quads = []

			if self.bExtractSkyTextures:
				palette = compute_palette(lev.PaletteEntryT, lev.sky_data.palette)
				palette_pixels = compute_texture(palette, (16, 16))
				pixels = compute_texture_paletted(lev.sky_data.bitmap, (512, 256), palette)

				write_png("sky", (512, 256), True, pixels)
				write_png("skypalette", (16, 16), True, palette_pixels)

			for vertex in lev.vertices:
				lev_verts.append([vertex.coords[0], vertex.coords[1], vertex.coords[2]])

			for plane in lev.planes:
				lev_quads.append([plane.vertex_indices[0], plane.vertex_indices[1], plane.vertex_indices[2], plane.vertex_indices[3]])

			mesh_lev = add_mesh(name, lev_verts, [], [])
			obj_lev = add_object(name, mesh_lev)

			calc_object_rotation_scale(obj_lev)
			link_object(obj_lev)

		#
		# powerslave (experimental)
		#

		if self.LevelFormat == "POWERSLAVE":

			lev = LevPowerslave.from_file(self.filepath)

			lev_vertices = []
			lev_quads = []
			lev_vertex_colors = []

			vertex = lev.VertexT
			plane = lev.PlaneT

			if self.bExtractSkyTextures:
				skypalette = []
				skypixels = []

				skyimage = lev.skydata.skyimage

				for lev.PaletteentryT in lev.skydata.palette:
					entry = lev.PaletteentryT
					skypalette.append([(entry.r / 31), (entry.g / 31), (entry.b / 31), entry.a])

				for y in range(256): # sky texture height
					for x in range(512): # sky texture width
						pos = (y * 512) + x
						pixel = skypalette[skyimage[pos]]
						skypixels.append(pixel[0]) # red
						skypixels.append(pixel[1]) # green
						skypixels.append(pixel[2]) # blue
						skypixels.append(pixel[3]) # alpha

				output = bpy.data.images.new("Sky Texture", alpha=True, width=512, height=256)
				output.pixels = skypixels
				output.filepath_raw = self.filepath + ".sky.png"
				output.file_format = "PNG"
				output.update()
				output.save()

			for lev.VertexT in lev.vertices:
				vertex = lev.VertexT
				lev_verts.append([vertex.coords[0], vertex.coords[1], vertex.coords[2]])
				lev_vertex_colors.append(vertex.lightlevel)

			for plane in lev.planes:
				if plane.quadoffsets[0] > -1 and plane.quadoffsets[1] < (lev.header.quadcount + 1):
					for i in range(plane.quadoffsets[1] - plane.quadoffsets[0] + 1):
						quad = lev.quads[plane.quadoffsets[0] + i]
						x = quad.indices[0] + plane.vertexoffsets[0]
						y = quad.indices[1] + plane.vertexoffsets[0]
						z = quad.indices[2] + plane.vertexoffsets[0]
						a = quad.indices[3] + plane.vertexoffsets[0]
						lev_quads.append([x, y, z, a])

			for lev.SectorT in lev.sectors:
				sector = lev.SectorT
				if sector.planes[0] > -1 and sector.planes[1] < (lev.header.planecount + 1):
					for i in range(sector.planes[1] - sector.planes[0] + 1):
						plane = lev.planes[sector.planes[0] + i]
						x = plane.vertices[0]
						y = plane.vertices[1]
						z = plane.vertices[2]
						a = plane.vertices[3]
						lev_quads.append([x, y, z, a])

			mesh_lev = bpy.data.meshes.new(name)
			mesh_lev.from_pydata(lev_verts, [], lev_quads)
			mesh_lev.vertex_colors.new()
			mesh_lev.update()

			obj_lev = bpy.data.objects.new(name, mesh_lev)

			generate_vertex_colors(mesh_lev, lev_saturncolors, lev_vertcolors)

			if self.bFixRotation:
				obj_lev.scale = [-self.ImportScale, self.ImportScale, self.ImportScale]
				obj_lev.rotation_euler = [math.radians(90), 0, 0]
			else:
				obj_lev.scale = [self.ImportScale, self.ImportScale, self.ImportScale]

			scene.collection.objects.link(obj_lev)

		#
		# quake
		#

		if self.LevelFormat == "QUAKE":

			lev = LevQuake.from_file(self.filepath)

			lev_vertices = []
			lev_vertex_colors = []
			lev_quads = []
			lev_materials = []
			lev_entities = []

			vertex = lev.VertexT
			plane = lev.PlaneT
			node = lev.NodeT
			texture = lev.TextureT
			tile = lev.TileT
			palette_entry = lev.PaletteEntryT
			entity = lev.EntityT

			for vertex in lev.verts:
				lev_vertices.append([vertex.coords[0], vertex.coords[1], vertex.coords[2]])
				lev_vertex_colors.append(vertex.color_lookup)

			for plane in lev.planes:
				if plane.tile_index < lev.header.num_tile_entries:
					tile = lev.tiles[plane.tile_index]
					X = Vector(lev_vertices[plane.vertex_indices[0]])
					Y = Vector(lev_vertices[plane.vertex_indices[1]])
					Z = Vector(lev_vertices[plane.vertex_indices[2]])
					A = Vector(lev_vertices[plane.vertex_indices[3]])

					def convert_int16_16_vector(v):
						return Vector((round(v[0]/65536.0), round(v[1]/65536.0), round(v[2]/65536.0)))

					width = tile.width
					height = tile.height

					base = tile.base_vector
					horizontal = tile.horizontal_vector
					vertical = tile.vertical_vector

					for tileY in range(height):
						for tileX in range(width):
							vc0 = [
								base[0] + tileX * horizontal[0] + tileY * vertical[0],
								base[1] + tileX * horizontal[1] + tileY * vertical[1],
								base[2] + tileX * horizontal[2] + tileY * vertical[2]
							]
							vc1 = [
								vc0[0] + horizontal[0],
								vc0[1] + horizontal[1],
								vc0[2] + horizontal[2]
							]
							vc2 = [
								vc0[0] + horizontal[0] + vertical[0],
								vc0[1] + horizontal[1] + vertical[1],
								vc0[2] + horizontal[2] + vertical[2]
							]
							vc3 = [
								vc0[0] + vertical[0],
								vc0[1] + vertical[1],
								vc0[2] + vertical[2]
							]

							vc0 = convert_int16_16_vector(vc0)
							vc1 = convert_int16_16_vector(vc1)
							vc2 = convert_int16_16_vector(vc2)
							vc3 = convert_int16_16_vector(vc3)

							points = tile.width + 1
							color_base = (tileY * points) + tileX

							vc0_color = tile.get_color_data[color_base]
							vc1_color = tile.get_color_data[color_base + 1]
							vc2_color = tile.get_color_data[color_base + 1 + points]
							vc3_color = tile.get_color_data[color_base + points]

							ofs = len(lev_vertices)

							lev_vertices.append(vc0)
							lev_vertices.append(vc1)
							lev_vertices.append(vc2)
							lev_vertices.append(vc3)

							lev_vertex_colors.append(vc0_color)
							lev_vertex_colors.append(vc1_color)
							lev_vertex_colors.append(vc2_color)
							lev_vertex_colors.append(vc3_color)

							lev_quads.append([ofs, ofs + 1, ofs + 2, ofs + 3])
				
			for plane in lev.planes:
				if plane.quad_start_index < lev.header.num_quads:
					for i in range(plane.quad_end_index - plane.quad_start_index + 1):
						quad = lev.quads[plane.quad_start_index + i]
						x = quad.vertex_indices[0] + plane.vert_start_index
						y = quad.vertex_indices[1] + plane.vert_start_index
						z = quad.vertex_indices[2] + plane.vert_start_index
						a = quad.vertex_indices[3] + plane.vert_start_index
						lev_quads.append([x, y, z, a])

			mesh_lev = add_mesh(name, lev_vertices, [], lev_quads)

			generate_vertex_colors(mesh_lev, lev_saturncolors, lev_vertex_colors)

			obj_lev = add_object(name, mesh_lev)

			if self.bExtractTextures:
				for i, texture in enumerate(lev.texture_data.textures):
					if texture.type != 130: break

					palette = compute_palette(palette_entry, texture.palette)
					pixels = compute_texture_paletted(texture.bitmap, (64, 64), palette)
					write_png(f"texture.{i}", (64, 64), True, pixels)

					if self.bExtractPalettes:
						palette_pixels = compute_texture(palette, (16, 1))
						write_png(f"texture.{i}.palette", (16, 1), True, palette_pixels)

				numTiles = 0

				for plane in lev.planes:
					if plane.tile_index < lev.header.num_tile_entries:
						tile = lev.tiles[plane.tile_index]
						width = tile.width
						height = tile.height

						for tileY in range(height):
							for tileX in range(width):
								tile_index = (tileY * width) + tileX
								tile_textureindex = tile.get_tile_texture_data[(tile_index * 2) + 1]

								if tile_textureindex not in lev_materials:
									mat = write_material(name + f"-material-{tile_textureindex}")
									obj_lev.data.materials.append(mat)
									lev_materials.append(tile_textureindex)

								obj_lev.data.polygons[numTiles].material_index = lev_materials.index(tile_textureindex)
								numTiles += 1

				numQuads = 0

				for plane in lev.planes:
					if plane.quad_start_index < lev.header.num_quads:
						for i in range(plane.quad_end_index - plane.quad_start_index + 1):
							quad = lev.quads[plane.quad_start_index + i]

							if quad.texture_index not in lev_materials:
								mat = write_material(name + f"-material-{quad.texture_index}")
								obj_lev.data.materials.append(mat)
								lev_materials.append(quad.texture_index)

							obj_lev.data.polygons[numTiles + numQuads].material_index = lev_materials.index(quad.texture_index)
							numQuads += 1

			if self.bExtractEntities:

				if self.bGenerateMapFile:
					entities_doc = open(self.filepath + ".map",'w')

				for entNum, entity in enumerate(lev.entities):
					ent_type = f"Entity {entNum}: " + match_entity(entity.ent_type)

					if self.bFixRotation:
						entloc = [
							-entity.get_entity_data.origin.x * self.ImportScale,
							-entity.get_entity_data.origin.z * self.ImportScale,
							entity.get_entity_data.origin.y * self.ImportScale
						]
					else:
						entloc = [
							entity.get_entity_data.origin.x * self.ImportScale,
							entity.get_entity_data.origin.y * self.ImportScale,
							entity.get_entity_data.origin.z * self.ImportScale
						]

					empty_ent = bpy.data.objects.new(ent_type, None)
					empty_ent.location = entloc
					empty_ent["classname"] = match_entity(entity.ent_type)
					empty_ent.empty_display_size = 2
					empty_ent.empty_display_type = "PLAIN_AXES"
					link_object(empty_ent)

					if self.bGenerateMapFile:
						entities_doc.write("{\n")
						entities_doc.write(f"\"classname\" \"" + match_entity(entity.ent_type) + "\"\n")
						entities_doc.write(f"\"origin\" \"{entloc[0]} {entloc[1]} {entloc[2]}\"\n")
						entities_doc.write("}\n")

			calc_object_rotation_scale(obj_lev)
			link_object(obj_lev)

		return {'FINISHED'}