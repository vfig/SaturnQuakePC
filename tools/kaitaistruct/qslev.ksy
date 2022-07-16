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
    size: 18
    repeat: expr
    repeat-expr: header.entitypolylinkcount
  - id: entitypolylinkdata1
    size: 2
    repeat: expr
    repeat-expr: header.entitypolylinkdata1count
  - id: entitypolylinkdata2
    size: 4
    repeat: expr
    repeat-expr: header.entitypolylinkdata2count
  - id: entitydata
    type: entitydata
    size: header.entitydatasize
  - id: tiletexturedata
    size: header.tiletexturedatasize
  - id: tilecolordata
    type: tilecolordata
    size: header.tilecolordatasize
  - id: unknown
    size: 128
    repeat: expr
    repeat-expr: header.unknowncount
  - id: tabledata1
    type: tabledata1_t
  - id: palette
    size: 1028

types:
  # 131104 bytes
  skyheader_t:
    seq:
      - id: skypalette
        type: skypaletteentry_t
        repeat: expr
        repeat-expr: 16
      - id: skyimagedata
        type: skyimageentry_t
        repeat: expr
        repeat-expr: 64

  skypaletteentry_t:
    seq:
      - id: r
        type: b5
      - id: g
        type: b5
      - id: b
        type: b5
      - id: a
        type: b1

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

  tilesubvector:
    seq:
      - id: x
        type: s4be
      - id: y
        type: s4be
      - id: z
        type: s4be

  tilecolordata:
    seq:
      - id: data
        size: _parent.header.tilecolordatasize

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
        # type: s1
        # repeat: expr
        # repeat-expr: _parent.entities[x + 1].dataofs - dataofs
        type:
            switch-on: enttype
            cases:
              0x2E: ent_12
              0x1C: ent_12
              0x71: ent_12
              0x4A: ent_12
              0x9A: ent_18
              0x94: ent_18
              0x95: ent_18
              0x92: ent_42
              0x26: ent_24
              0xFE: ent_12
              0xE8: ent_1656
              0xA4: ent_10
              0x93: ent_12
              0xD: ent_10
              0x6F: ent_12
              0x5C: ent_6
              0x8F: ent_12
              0x82: ent_12
              0x7D: ent_12
              0x80: ent_12
              0x83: ent_12
              _: ent_placeholder

  entitydata:
    seq:
      - id: data
        size: _parent.header.entitydatasize

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

  ent_placeholder:
    seq:
      - id: data
        type: s1

  ent_null: {}

  tabledata1_t:
    seq:
      - id: num_block
        type: s4
      - id: block
        type: tabledata1block
        repeat: expr
        repeat-expr: num_block

  tabledata1block:
    seq:
      - id: attr1
        type: s4
      - id: attr2
        type: s4
      - id: attr3
        type: s4
      - id: attr4
        type: s4

  textures:
    seq:
      - id: flags
        type: u2
      - id: type
        type: u2
      - id: palette
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: imagedata
        type: u2
        repeat: expr
        repeat-expr: 2048

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