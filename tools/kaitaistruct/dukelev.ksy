meta:
  id: dukelev
  file-extension: lev
  endian: be
  bit-endian: be

doc: Duke Nukem 3D (Sega Saturn) Level Format (.lev)
#doc-ref:

seq:
  - id: skydata
    type: skydata_t
  - id: header
    type: header_t

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
        repeat-expr: 256 * 512 # sky image size

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