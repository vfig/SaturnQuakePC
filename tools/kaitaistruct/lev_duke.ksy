meta:
  id: lev_duke
  file-extension: lev
  endian: be
  bit-endian: be

doc: Duke Nukem 3D (Sega Saturn) Level Format (.lev)
#doc-ref:

seq:
  - id: sky_data
    type: sky_data_t
  - id: unknown_01
    size: 1280
  - id: unknown_02
    type: unknown_02_t
  - id: header
    type: header_t
  - id: sectors
    type: sector_t
    repeat: expr
    repeat-expr: header.num_sectors
  - id: planes
    type: plane_t
    repeat: expr
    repeat-expr: header.num_planes
  - id: unknown
    type: unknown_t
    repeat: expr
    repeat-expr: header.num_unknown
  - id: vertices
    type: vertex_t
    repeat: expr
    repeat-expr: header.num_vertices

types:

  sky_data_t:
    seq:
      - id: palette
        type: palette_entry_t
        repeat: expr
        repeat-expr: 256
      - id: width
        type: s4
      - id: height
        type: s4
      - id: bitmap
        type: b8
        repeat: expr
        repeat-expr: width * height

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

  unknown_02_t:
    seq:
      - id: num_blocks
        type: u4
      - id: blocks
        type: unknown_02_block_t
        repeat: expr
        repeat-expr: num_blocks

  unknown_02_block_t:
    seq:
      - id: len_data
        type: u4
      - id: data
        size: len_data

  header_t:
    seq:
      - id: unknown_01
        type: u4
      - id: num_sectors
        type: u4
      - id: num_planes
        type: u4
      - id: num_vertices
        type: u4
      - id: unknown_03
        type: u4
      - id: unknown_04
        type: u4
      - id: num_unknown
        type: u4
      - id: remaining_data
        size: 28

  sector_t:
    seq:
      - id: data
        size: 28

  plane_t:
    seq:
      - id: vertex_indices
        type: u2
        repeat: expr
        repeat-expr: 4
      - id: remaining_data
        size: 32

  unknown_t:
    seq:
      - id: data
        size: 44

  vertex_t:
    seq:
      - id: coords
        type: u2
        repeat: expr
        repeat-expr: 3
      - id: color_lookup
        type: u1
      - id: filler
        type: u1
