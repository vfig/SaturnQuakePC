meta:
  id: qslev
  file-extension: lev
  endian: be
  bit-endian: be

seq:
  - id: skydata
    size: 131104
    type: skyheader_t
  - id: header
    type: header_t
  - id: nodes
    type: node_t
    repeat: expr
    repeat-expr: header.nodecount
  - id: planes
    type: plane_t
    repeat: expr
    repeat-expr: header.planecount
  - id: tiles
    type: tile_t
    repeat: expr
    repeat-expr: header.tileentrycount
  - id: verts
    type: vert_t
    repeat: expr
    repeat-expr: header.vertcount
  - id: quads
    type: quad_t
    repeat: expr
    repeat-expr: header.quadcount
  - id: entities
    type: entity_t(_index)
    repeat: expr
    repeat-expr: header.entitycount
  - id: entitypolylinks
    type: entitypolylink_t
    repeat: expr
    repeat-expr: header.entitypolylinkcount
  - id: entitypolylinkdata1
    type: entitypolylinkdata1_t
    size: header.entitypolylinkdata1count * 2
  - id: entitypolylinkdata2
    type: entitypolylinkdata2_t
    size: header.entitypolylinkdata2count * 4
  - id: entitydata
    type: entitydata
    size: header.entitydatasize
  - id: tiletexturedata
    type: tiletexturedata_t
    size: header.tiletexturedatasize
  - id: tilecolordata
    type: tilecolordata_t
    size: header.tilecolordatasize
  - id: unknown
    size: 128
    repeat: expr
    repeat-expr: header.unknowncount
  - id: tabledata1
    type: tabledata1_t
  - id: global_palette
    type: global_palette_t
  - id: texturedata
    type: texturedata_t

types:
  # 131104 bytes
  skyheader_t:
    seq:
      - id: skypalette
        type: palette_entry_t
        repeat: expr
        repeat-expr: 16
      - id: skyimagedata
        type: skyimageentry_t
        repeat: expr
        repeat-expr: 64

  palette_entry_t:
    seq:
      - id: a
        type: b1
      - id: b
        type: b5
      - id: g
        type: b5
      - id: r
        type: b5

  skyimageentry_t:
    seq:
      - id: image
        size: 2048

  # 60 bytes
  header_t:
    seq:
      - id: unknown1
        type: u4
        doc: Unknown purpose, usually always 0.
      - id: unknown2
        type: u4
        doc: Unknown purpose, might represent a bank or collective size
      - id: nodecount
        type: u4
        doc: Number of nodes. 28 bytes each.
      - id: planecount
        type: u4
        doc: Number of planes. 40 bytes each.
      - id: vertcount
        type: u4
        doc: Number of vertices. 8 bytes each.
      - id: quadcount
        type: u4
        doc: Number of quads. 5 bytes each.
      - id: tiletexturedatasize
        type: u4
      - id: tileentrycount
        type: u4
        doc: Number of tiles. 44 bytes each.
      - id: tilecolordatasize
        type: u4
      - id: entitycount
        type: u4
        doc: Number of entities. 4 bytes each.
      - id: entitydatasize
        type: u4
        doc: Size of entity data.
      - id: entitypolylinkcount
        type: u4
        doc: Unverified - 18 bytes each.
      - id: entitypolylinkdata1count
        type: u4
        doc: 2 bytes each.
      - id: entitypolylinkdata2count
        type: u4
        doc: 4 bytes each.
      - id: unknowncount
        type: u4
        doc: Unknown purpose. 16 bytes each.

  # 28 bytes each
  node_t:
    seq:
      - id: resv
        type: vec2u2
      - id: pos
        type: vec3u2
      - id: distance
        type: u2
      - id: firstplane
        type: u2
      - id: lastplane
        type: u2
      - id: unknown
        type: vec6u2

  # 40 bytes each
  plane_t:
    seq:
      - id: vertices
        type: vec4u2
      - id: nodeindex
        type: u2
      - id: flags
        type: u2
      - id: collisionflags
        type: u2
      - id: tileindex
        type: u2
      - id: unknownindex
        type: u2
      - id: quadstartindex
        type: u2
      - id: quadendindex
        type: u2
      - id: vertstartindex
        type: u2
      - id: vertendindex
        type: u2
      - id: plane
        type: vec4s2
      - id: angle
        type: s2
      - id: resv
        type: vec2u2

  # 44 bytes each
  tile_t:
    seq:
      - id: texturedataofs
        type: u2
      - id: width
        type: u1
      - id: height
        type: u1
      - id: colordataofs
        type: u2
      - id: unknown
        type: u2
      - id: tilehorizvec
        type: vec3s4
      - id: tilevertvec
        type: vec3s4
      - id: tilebasevec
        type: vec3s4
    instances:
      getcolordata:
        io: _root.tilecolordata._io
        pos: colordataofs
        type: u1
        repeat: expr
        repeat-expr: (width + 1) * (height + 1)
      gettiletexturedata:
        io: _root.tiletexturedata._io
        pos: texturedataofs
        type: u1
        repeat: expr
        repeat-expr: (height * width) * 2

  tilesubvector:
    seq:
      - id: x
        type: s4be
      - id: y
        type: s4be
      - id: z
        type: s4be

  tilecolordata_t:
    seq:
      - id: data
        size: _parent.header.tilecolordatasize

  tiletexturedata_t:
    seq:
      - id: data
        size: _parent.header.tiletexturedatasize

  # 8 bytes each
  vert_t:
    seq:
      - id: position
        type: vec3s2
      - id: colorvalue
        type: u1
      - id: none
        type: u1

  # 5 bytes each
  quad_t:
    seq:
      - id: indices
        type: vec4u1
      - id: textureindex
        type: u1

  # 4 bytes each
  entity_t:
    params:
      - id: x
        type: s4
    seq:
      - id: enttype
        type: u2
      - id: dataofs
        type: u2
    instances:
      getentitydata:
        io: _root.entitydata._io
        pos: dataofs
        #size: _parent.entities[x + 1].dataofs - dataofs
        type:
            switch-on: enttype
            cases:
              0x92: entity_polymover_t # poly mover
              _: entity_datablock_t

  entity_datablock_t:
    seq:
      - id: lead
        type: s2
      - id: origin
        type: vec3s2

  entity_polymover_t:
    seq:
      - id: polylink_id
        type: s2
      - id: origin
        type: vec3s2
      - id: data
        type: s2
        repeat: expr
        repeat-expr: 17

  entitydata:
    seq:
      - id: data
        size: _parent.header.entitydatasize

  entitypolylinkdata1_t:
    seq:
      - id: data
        type: u1
        repeat: eos

  entitypolylinkdata2_t:
    seq:
      - id: data
        type: u1
        repeat: eos

  entitypolylinkdata1_single_t:
    seq:
      - id: data
        type: u1
        repeat: expr
        repeat-expr: 2
        if: _root.header.entitypolylinkdata1count != 0

  entitypolylinkdata2_single_t:
    seq:
      - id: data
        type: u1
        repeat: expr
        repeat-expr: 4
        if: _root.header.entitypolylinkdata2count != 0

  # mapped entity size declations

  ent_6:
    seq:
      - id: data
        type: s1
        repeat: expr
        repeat-expr: 6

  ent_10:
    seq:
      - id: data
        type: s1
        repeat: expr
        repeat-expr: 10

  ent_12:
    seq:
      - id: data
        type: s1
        repeat: expr
        repeat-expr: 12

  ent_18:
    seq:
      - id: data
        type: s1
        repeat: expr
        repeat-expr: 18

  ent_24:
    seq:
      - id: data
        type: s1
        repeat: expr
        repeat-expr: 24

  ent_42:
    seq:
      - id: data
        type: s1
        repeat: expr
        repeat-expr: 42

  ent_1656:
    seq:
      - id: data
        type: s1
        repeat: expr
        repeat-expr: 1656

  ent_1614:
    seq:
      - id: data
        type: s1
        repeat: expr
        repeat-expr: 1614

  ent_placeholder:
    seq:
      - id: data
        type: s1

  ent_null: {}

  # 18 bytes each
  entitypolylink_t:
    seq:
      - id: lead
        type: u2
      - id: data1offset
        type: vec2u2
      - id: data2offset
        type: vec2u2
      - id: value4
        type: u2
      - id: reserved
        type: vec3u2
    instances:
      getdata1:
        io: _root.entitypolylinkdata1._io
        pos: data1offset.x * 2
        type: entitypolylinkdata1_single_t
        repeat: expr
        repeat-expr: data1offset.y - data1offset.x + 1
      getdata2:
        io: _root.entitypolylinkdata2._io
        pos: data2offset.x * 4
        type: entitypolylinkdata2_single_t
        repeat: expr
        repeat-expr: data2offset.y - data2offset.x + 1

  tabledata1_t:
    seq:
      - id: prefixblock
        type: tabledata1prefixblock
      - id: num_block
        type: s4
      - id: block
        type: tabledata1block
        repeat: expr
        repeat-expr: num_block

  tabledata1prefixblock:
    seq:
      - id: num_values
        type: u4
      - id: values
        type: s2
        repeat: expr
        repeat-expr: num_values

  tabledata1block:
    seq:
      - id: len_block
        type: s4
      - id: attr2
        type: s4
      - id: attr3
        type: s4
      - id: attr4
        type: s4
      - id: block
        size: len_block

  global_palette_t:
    seq:
      - id: len_block
        type: u4
      - id: color
        type: palette_entry_t
        repeat: expr
        repeat-expr: len_block/2

  texturedata_t:
    seq:
      - id: count
        type: u4
      - id: textures
        type: texture_t
        repeat: until
        repeat-until: _.type != 130
        #repeat: expr
        #repeat-expr: 58 # this is wrong!
        # TITLE.LEV has 58 textures but the raw 'count' is 0x52 (82)
        # E1L1.LEV has 120 textures but the raw 'count' is 0x93 (147)
        # i dont know how to automatically determine number of textures yet!

  texture_t:
    seq:
      - id: flags
        type: u1
      - id: type
        type: u1
      - id: palette
        type: palette_entry_t
        repeat: expr
        repeat-expr: 16
      - id: imagedata
        type: b4
        repeat: expr
        repeat-expr: 4096

# vector types

  vec2u2:
    seq:
      - id: x
        type: u2
      - id: y
        type: u2

  vec3u2:
    seq:
      - id: x
        type: u2
      - id: y
        type: u2
      - id: z
        type: u2

  vec4u2:
    seq:
      - id: x
        type: u2
      - id: y
        type: u2
      - id: z
        type: u2
      - id: a
        type: u2

  vec4u1:
    seq:
      - id: x
        type: u1
      - id: y
        type: u1
      - id: z
        type: u1
      - id: a
        type: u1

  vec6u2:
    seq:
      - id: a
        type: u2
      - id: b
        type: u2
      - id: c
        type: u2
      - id: x
        type: u2
      - id: y
        type: u2
      - id: z
        type: u2

  vec4s2:
    seq:
      - id: x
        type: s2
      - id: y
        type: s2
      - id: z
        type: s2
      - id: a
        type: s2

  vec3s4:
    seq:
      - id: x
        type: s4
      - id: y
        type: s4
      - id: z
        type: s4

  vec3s2:
    seq:
      - id: x
        type: s2
      - id: y
        type: s2
      - id: z
        type: s2