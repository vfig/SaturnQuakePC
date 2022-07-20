meta:
  id: powerslavelev
  file-extension: lev
  endian: be
  bit-endian: be

doc: PowerSlave (Sega Saturn) Level Format (.lev)
doc-ref: https://github.com/ReyeMe/Saturn-Powerslave-map-viewer/blob/master/Powerslave.cs

seq:
  - id: skydata
    type: skydata_t
  - id: unknown01
    size: 1292
    # start at 0x2070C
  - id: header
    type: header_t
  - id: sectors
    type: sector_t
    repeat: expr
    repeat-expr: header.sectorcount
  - id: planes
    type: plane_t
    repeat: expr
    repeat-expr: header.planecount
  - id: vertices
    type: vertex_t
    repeat: expr
    repeat-expr: header.vertexcount
  - id: quads
    type: quad_t
    repeat: expr
    repeat-expr: header.quadcount

types:

  skydata_t:
    seq:
      - id: palette
        type: paletteentry_t
        repeat: expr
        repeat-expr: 256
      - id: skyimage
        type: b8
        repeat: expr
        repeat-expr: 512 * 256 # sky image size

  paletteentry_t:
    seq:
      - id: a
        type: b1
      - id: b
        type: b5
      - id: g
        type: b5
      - id: r
        type: b5

  header_t:
    seq:
      - id: sectorcount
        type: u4
      - id: planecount
        type: u4
      - id: vertexcount
        type: u4
      - id: quadcount
        type: u4
      - id: unknown01
        type: u4
      - id: unknown02
        type: u4
      - id: unknown03
        type: u4
      - id: unknown04
        type: u4
      - id: unknown05
        type: u4
      - id: unknown06
        type: u4
      - id: unknown07
        type: u4
      - id: unknown08
        type: u4
      - id: unknown09
        type: u4
      - id: unknown010
        type: u4

  sector_t:
    seq:
      - id: unknown01
        type: s2
      - id: unknown02
        type: s2
      - id: ceilingslope
        type: s2
      - id: floorslope
        type: s2
      - id: ceilingheight
        type: s2
      - id: floorheight
        type: s2
      - id: planes
        type: s2
        repeat: expr
        repeat-expr: 2
      - id: unknown03
        type: u2
      - id: flags
        type: u2
      - id: unknown04
        type: s2
      - id: unknown05
        type: s2

  plane_t:
    seq:
      - id: normal
        type: s4
        repeat: expr
        repeat-expr: 3
      - id: angle
        type: s4
      - id: unknown01
        type: s2
      - id: unknown02
        type: s2
      - id: flags
        type: u2
      - id: textureid
        type: u2
      - id: quadoffsets
        type: s2
        repeat: expr
        repeat-expr: 2
      - id: vertexoffsets
        type: u2
        repeat: expr
        repeat-expr: 2
      - id: vertices
        type: u2
        repeat: expr
        repeat-expr: 4
      - id: unknown03
        type: s2
      - id: lookup
        type: u2
      - id: unknown04
        type: s2
      - id: unknown05
        type: s2

  vertex_t:
    seq:
      - id: coords
        type: s2
        repeat: expr
        repeat-expr: 3
      - id: lightlevel
        type: b8
      - id: unknown01
        type: b8

  quad_t:
    seq:
      - id: indices
        type: u2
        repeat: expr
        repeat-expr: 4
      - id: unknown01
        type: b8
      - id: unknown02
        type: b8