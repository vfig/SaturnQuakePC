# 
# IMPORT SATURN LEV
# 

import os, sys
sys.path.append(os.path.dirname(__file__))

# custom modules
import kaitaistruct
from qslev import Qslev
from powerslavelev import Powerslavelev
from dukelev import Dukelev

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
	filter_glob : StringProperty(default="*.lev", options={'HIDDEN'})

	level_formats = (
		("QUAKE", "Quake", "Sega Saturn SD Engine (Quake)"),
		("POWERSLAVE", "PowerSlave (Experimental)", "Sega Saturn SD Engine (PowerSlave)"),
		("DUKE3D", "Duke Nukem 3D (Experimental)", "Sega Saturn SD Engine (Duke Nukem 3D)")
	)

	# user controllable properties
	bExtractTextures : BoolProperty(name="Extract Textures", default=True)
	bExtractSkyTextures : BoolProperty(name="Extract Sky Textures", default=True)
	bExtractEntities : BoolProperty(name="Extract Entities", default=True)
	bFixRotation : BoolProperty(name="Fix Rotation", default=True)
	bImportNodes : BoolProperty(name="Import Node Data", default=False)
	bFlagPlanes : BoolProperty(name="Generated Flagged Planes", default=False)
	bGenerateMapFile : BoolProperty(name="Generate .map File", default=False)
	ImportScale : FloatProperty(name="Import Scale", default=1.0)
	LevelFormat : EnumProperty(name="Level Format", items=level_formats, default="DUKE3D")

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

		def compute_palette(item, container, bForceTransparency):
			palette_entries = []

			for i, item in enumerate(container):
				if bForceTransparency and i == 255:
					palette_entries.append([(item.r / 31), (item.g / 31), (item.b / 31), False])
				else:
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

			lev = Dukelev.from_file(self.filepath)

			if self.bExtractSkyTextures:
				palette = compute_palette(lev.PaletteentryT, lev.skydata.palette, True)
				palette_pixels = compute_texture(palette, (16, 16))
				pixels = compute_texture_paletted(lev.skydata.skyimage, (512, 256), palette)

				write_png("sky", (512, 256), True, pixels)
				write_png("skypalette", (16, 16), True, palette_pixels)

		#
		# powerslave (experimental)
		#

		if self.LevelFormat == "POWERSLAVE":

			lev = Powerslavelev.from_file(self.filepath)

			print("Sectors: %i" % lev.header.sectorcount)
			print("Planes: %i" % lev.header.planecount)
			print("Vertices: %i" % lev.header.vertexcount)
			print("Quads: %i" % lev.header.quadcount)

			lev_verts = []
			lev_quads = []
			lev_vertcolors = []

			if self.bExtractSkyTextures:
				palette = compute_palette(lev.PaletteentryT, lev.skydata.palette, True)
				palette_pixels = compute_texture(palette, (16, 16))
				pixels = compute_texture_paletted(lev.skydata.skyimage, (512, 256), palette)

				write_png("sky", (512, 256), True, pixels)
				write_png("skypalette", (16, 16), True, palette_pixels)

			for lev.VertexT in lev.vertices:
				vertex = lev.VertexT
				lev_verts.append([vertex.coords[0], vertex.coords[1], vertex.coords[2]])
				lev_vertcolors.append(vertex.lightlevel)

			for lev.PlaneT in lev.planes:
				plane = lev.PlaneT
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

			if (self.bFixRotation):
				obj_lev.scale = [-self.ImportScale, self.ImportScale, self.ImportScale]
				obj_lev.rotation_euler = [math.radians(90), 0, 0]
			else:
				obj_lev.scale = [self.ImportScale, self.ImportScale, self.ImportScale]

			scene.collection.objects.link(obj_lev)

		#
		# quake
		#

		if self.LevelFormat == "QUAKE":

			lev = Qslev.from_file(self.filepath)

			print("Nodes: %i" % lev.header.nodecount)
			print("Planes: %i" % lev.header.planecount)
			print("Vertices: %i" % lev.header.vertcount)
			print("Quads: %i" % lev.header.quadcount)
			print("Entities: %i" % lev.header.entitycount)
			print("Tiles: %i" % lev.header.tileentrycount)

			class lev_planeflags(Flag):
				LAVA = 1
				UN2 = 2
				UN3 = 4
				TOUCHABLE = 8
				UN4 = 16
				UN5 = 32
				UN6 = 64
				UN7 = 128
				VISIBLE = 256
				LIQUID = 512
				UN8 = 1024
				UN9 = 2048
				UN10 = 4096
				SLIME = 8192

				# LAVA surface = 384 = 256 + 128 + 1
				# LAVA volume = 641 = 512 + 128 + 1
				# WATER volume = 512 = 512
				# SLIME volume = 8704 = 8192 + 512

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

			if (self.bImportNodes):
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
					if (self.bFixRotation):
						obj_node.scale = [-self.ImportScale, self.ImportScale, self.ImportScale]
						obj_node.rotation_euler = [math.radians(90), 0, 0]
					else:
						obj_node.scale = [self.ImportScale, self.ImportScale, self.ImportScale]

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

			if (self.bFlagPlanes):
				for plane_index, lev.PlaneT in enumerate(lev.planes):
					plane = lev.PlaneT

					if plane.tileindex < lev.header.tileentrycount or plane.quadstartindex < lev.header.quadcount:
						lev_flaggedplane_verts = []
						lev_flaggedplane_quads = []

						lev_flaggedplane_verts.append([-lev_verts[plane.vertices.x][0] * self.ImportScale, -lev_verts[plane.vertices.x][2] * self.ImportScale, lev_verts[plane.vertices.x][1] * ImportScale])
						lev_flaggedplane_verts.append([-lev_verts[plane.vertices.y][0] * self.ImportScale, -lev_verts[plane.vertices.y][2] * self.ImportScale, lev_verts[plane.vertices.y][1] * ImportScale])
						lev_flaggedplane_verts.append([-lev_verts[plane.vertices.z][0] * self.ImportScale, -lev_verts[plane.vertices.z][2] * self.ImportScale, lev_verts[plane.vertices.z][1] * ImportScale])
						lev_flaggedplane_verts.append([-lev_verts[plane.vertices.a][0] * self.ImportScale, -lev_verts[plane.vertices.a][2] * self.ImportScale, lev_verts[plane.vertices.a][1] * ImportScale])

						lev_flaggedplane_quads.append([0, 1, 2, 3])

						mesh_flaggedplane = bpy.data.meshes.new(f"Flagged Plane {plane_index}")
						mesh_flaggedplane.from_pydata(lev_flaggedplane_verts, [], lev_flaggedplane_quads)
						mesh_flaggedplane.update()

						obj_flaggedplane = bpy.data.objects.new(f"Flagged Plane {plane_index}", mesh_flaggedplane)
						obj_flaggedplane["flags"] = plane.flags
						obj_flaggedplane["collisionflags"] = plane.collisionflags
						scene.collection.objects.link(obj_flaggedplane)

				return

			# thank you vfig
			for plane_index, lev.PlaneT in enumerate(lev.planes):
				plane = lev.PlaneT
				if plane.tileindex < lev.header.tileentrycount:
					tile = lev.tiles[plane.tileindex]
					X = Vector(lev_verts[plane.vertices.x])
					Y = Vector(lev_verts[plane.vertices.y])
					Z = Vector(lev_verts[plane.vertices.z])
					A = Vector(lev_verts[plane.vertices.a])

					if plane_index == self.debug_plane_index:
						debug_add_empty(X, "X")
						debug_add_empty(Y, "Y")
						debug_add_empty(Z, "Z")
						debug_add_empty(A, "A")
					elif self.debug_plane_index >= 0:
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

							if plane_index==self.debug_plane_index and tileX==0 and tileY==0:
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
					if self.debug_planes:
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

			layer_flags = mesh_quads.polygon_layers_float.new(name="Source Plane Flags")
			layer_collisionflags = mesh_quads.polygon_layers_float.new(name="Source Plane Collision Flags")

			generate_vertex_colors(mesh_quads, lev_saturncolors, lev_vertcolorvalues)

			obj_quads = bpy.data.objects.new(name, mesh_quads)

			if (self.bExtractTextures):
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
					texture.filepath_raw = self.filepath + f".texture.{i}.png"
					texture.file_format = "PNG"
					texture.update()
					texture.save()

				numTiles = 0

				shaderfile = open(self.filepath + ".shader", "w")

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
									texImage.image = bpy.data.images.load(self.filepath + f".texture.{tile_textureindex}.png")
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
								texImage.image = bpy.data.images.load(self.filepath + f".texture.{quad.textureindex}.png")
								mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])
								obj_quads.data.materials.append(mat)
								lev_materials.append(quad.textureindex)

								shaderfile.write(mat.name)
								shaderfile.write(" { program saturn_level diffusemap textures/levels/" + name + "/")
								shaderfile.write(name + f".texture.{quad.textureindex}.png")
								shaderfile.write(" cull disable }\n")

							obj_quads.data.polygons[numTiles + numQuads].material_index = lev_materials.index(quad.textureindex)
							numQuads += 1

			#if self.bExtractSkyTextures:
				#skypalette = [
				#			[0, 0, 0, 0],	[0, 0, 0, 0],	[0, 0, 0, 0], [0, 0, 0, 0],
				#			[0, 0, 0, 0],	[0, 0, 0, 0],	[0, 0, 0, 0], [0, 0, 0, 0],
				#			[0, 0, 0, 0],	[0, 0, 0, 0],	[0, 0, 0, 0], [0, 0, 0, 0],
				#			[0, 0, 0, 0],	[0, 0, 0, 0],	[0, 0, 0, 0], [0, 0, 0, 0]
				#]

				#for i, lev.PaletteEntryT in enumerate(lev.skydata.skypalette):
					#entry = lev.PaletteEntryT
					#skypalette[i] = [(entry.r / 31), (entry.g / 31), (entry.b / 31), entry.a]

				#for x, lev.SkyimageT in enumerate(lev.skydata.skyimagedata):
					#image = lev.SkyimageT

					#pixels = []

					#for i in range(4096):
					#	pixels.append(skypalette[image.pixels[i]][0])
					#	pixels.append(skypalette[image.pixels[i]][1])
					#	pixels.append(skypalette[image.pixels[i]][2])
					#	pixels.append(skypalette[image.pixels[i]][3])

					#skyimage = bpy.data.images.new("Sky Image", alpha=True, width=64, height=64)
					#skyimage.pixels = pixels
					#skyimage.filepath_raw = self.filepath + f".sky.{x}.png"
					#skyimage.file_format = "PNG"
					#skyimage.update()
					#skyimage.save()

				#skypaletteimage = bpy.data.images.new("Sky Palette", alpha=False, width=8, height=2)
				#skypaletteimage.pixels = skypalettepixels
				#skypaletteimage.filepath_raw = filepath + ".skypalette.png"
				#skypaletteimage.file_format = "PNG"
				#skypaletteimage.update()
				#skypaletteimage.save()

			# now done with the mesh, write out some entitiy data

			if (self.bExtractEntities):
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

				entities_doc = open(self.filepath + ".ent",'w')

				entities = []

				l = 0

				# entity polylinks
				for entNum, lev.EntityT in enumerate(lev.entities):
					ent = lev.EntityT
					if ent.enttype == 146:
						polylink_id = ent.getentitydata.polylink_id
						link = lev.entitypolylinks[polylink_id]
						print(f"{l} - entity number {entNum}: link {polylink_id}")
						print("-----------")
						print(link.getdata1)
						print(link.getdata2)
						print("----------------------")
						l += 1

				for entNum, lev.EntityT in enumerate(lev.entities):
					ent = lev.EntityT
					enttype = f"Entity {entNum}: " + match_entity(ent.enttype)
					if (self.bFixRotation):
						entloc = [-ent.getentitydata.origin.x * self.ImportScale, -ent.getentitydata.origin.z * self.ImportScale, ent.getentitydata.origin.y * self.ImportScale]
					else:
						entloc = [ent.getentitydata.origin.x * self.ImportScale, ent.getentitydata.origin.y * self.ImportScale, ent.getentitydata.origin.z * self.ImportScale]

					entloc_original = [ent.getentitydata.origin.x, ent.getentitydata.origin.y, ent.getentitydata.origin.z]

					#if match_entity(ent.enttype)[0:8] == "monster_" or match_entity(ent.enttype)[0:5] == "item_":
					#	entloc[2] += 64

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

			if (self.bFixRotation):
				obj_quads.scale = [-self.ImportScale, self.ImportScale, self.ImportScale]
				obj_quads.rotation_euler = [math.radians(90), 0, 0]
			else:
				obj_quads.scale = [self.ImportScale, self.ImportScale, self.ImportScale]

			scene.collection.objects.link(obj_quads)

			if (self.bGenerateMapFile):
				mapfile = open(self.filepath + ".map", "w")
				mapfile.write("// Game: Quake\n")
				mapfile.write("// Format: Standard\n")
				mapfile.write("// entity 0\n")
				mapfile.write("{\n")
				mapfile.write(f"\"classname\" \"worldspawn\"\n")

				brushNum = 0

				for i, lev.PlaneT in enumerate(lev.planes):
					plane = lev.PlaneT

					normal = Vector([plane.plane.x / 16384, plane.plane.y / 16384, plane.plane.z / 16384])
					distance = plane.plane.a
					mod = -normal * distance

					def write_brush(verts_start, num):
						verts_end = [verts_start[2] + mod, verts_start[1] + mod, verts_start[0] + mod, verts_start[3] + mod]
						verts_1 = [verts_end[0], verts_end[3], verts_start[3], verts_start[2]]
						verts_2 = [verts_end[2], verts_start[0], verts_start[3], verts_end[3]]
						verts_3 = [verts_start[2], verts_start[1], verts_end[1], verts_end[0]]
						verts_4 = [verts_end[1], verts_start[1], verts_start[0], verts_end[2]]
						mapfile.write(f"// brush {num}\n")
						mapfile.write("{\n")
						mapfile.write(f"( {verts_1[0][0]} {verts_1[0][1]} {verts_1[0][2]} ) ( {verts_1[1][0]} {verts_1[1][1]} {verts_1[1][2]} ) ( {verts_1[2][0]} {verts_1[2][1]} {verts_1[2][2]} ) hintskip 0 0 0 1 1\n")
						mapfile.write(f"( {verts_2[0][0]} {verts_2[0][1]} {verts_2[0][2]} ) ( {verts_2[1][0]} {verts_2[1][1]} {verts_2[1][2]} ) ( {verts_2[2][0]} {verts_2[2][1]} {verts_2[2][2]} ) hintskip 0 0 0 1 1\n")
						mapfile.write(f"( {verts_end[0][0]} {verts_end[0][1]} {verts_end[0][2]} ) ( {verts_end[1][0]} {verts_end[1][1]} {verts_end[1][2]} ) ( {verts_end[2][0]} {verts_end[2][1]} {verts_end[2][2]} ) trigger 0 0 0 1 1\n")
						mapfile.write(f"( {verts_start[0][0]} {verts_start[0][1]} {verts_start[0][2]} ) ( {verts_start[1][0]} {verts_start[1][1]} {verts_start[1][2]} ) ( {verts_start[2][0]} {verts_start[2][1]} {verts_start[2][2]} ) skip 0 0 0 1 1\n")
						mapfile.write(f"( {verts_3[0][0]} {verts_3[0][1]} {verts_3[0][2]} ) ( {verts_3[1][0]} {verts_3[1][1]} {verts_3[1][2]} ) ( {verts_3[2][0]} {verts_3[2][1]} {verts_3[2][2]} ) hintskip 0 0 0 1 1\n")
						mapfile.write(f"( {verts_4[0][0]} {verts_4[0][1]} {verts_4[0][2]} ) ( {verts_4[1][0]} {verts_4[1][1]} {verts_4[1][2]} ) ( {verts_4[2][0]} {verts_4[2][1]} {verts_4[2][2]} ) hintskip 0 0 0 1 1\n")
						mapfile.write("}\n")

					if plane.tileindex < lev.header.tileentrycount:
						write_brush([Vector(lev_verts[plane.vertices.a]), Vector(lev_verts[plane.vertices.z]), Vector(lev_verts[plane.vertices.y]), Vector(lev_verts[plane.vertices.x])], brushNum)
						brushNum += 1
					#if plane.quadstartindex < lev.header.quadcount:
					#	write_brush([Vector(lev_verts[plane.vertices.a]), Vector(lev_verts[plane.vertices.z]), Vector(lev_verts[plane.vertices.y]), Vector(lev_verts[plane.vertices.x])], brushNum)
					#	brushNum += 1
						#for i in range(plane.quadendindex - plane.quadstartindex + 1):
						#	quad = lev.quads[plane.quadstartindex + i]
						#	quadx = quad.indices.x + plane.vertstartindex
						#	quady = quad.indices.y + plane.vertstartindex
						#	quadz = quad.indices.z + plane.vertstartindex
						#	quada = quad.indices.a + plane.vertstartindex
						#	write_brush([Vector(lev_verts[quadx]), Vector(lev_verts[quady]), Vector(lev_verts[quadz]), Vector(lev_verts[quada])], brushNum)
						#	brushNum += 1

				mapfile.write("}\n")

		return {'FINISHED'}

def menu_func(self, context):
	self.layout.operator(ImportLEV.bl_idname, text="Sega Saturn SD Engine Level (.lev)")