			if (self.bGenerateMapFile):
				mapfile = open(self.filepath + ".map", "w")
				mapfile.write("// Game: Quake\n")
				mapfile.write("// Format: Standard\n")
				mapfile.write("// entity 0\n")
				mapfile.write("{\n")
				mapfile.write(f"\"classname\" \"worldspawn\"\n")

				brushNum = 0

				for i, plane in enumerate(lev.planes):
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
