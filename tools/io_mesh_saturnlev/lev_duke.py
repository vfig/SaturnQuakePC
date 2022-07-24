# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class LevDuke(KaitaiStruct):
    """Duke Nukem 3D (Sega Saturn) Level Format (.lev)."""
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.sky_data = LevDuke.SkyDataT(self._io, self, self._root)
        self.unknown_01 = self._io.read_bytes(1280)
        self.unknown_02 = LevDuke.Unknown02T(self._io, self, self._root)
        self._raw_header = self._io.read_bytes(56)
        _io__raw_header = KaitaiStream(BytesIO(self._raw_header))
        self.header = LevDuke.HeaderT(_io__raw_header, self, self._root)
        self.sectors = []
        for i in range(self.header.num_sectors):
            self.sectors.append(self._io.read_bytes(28))

        self._raw_planes = []
        self.planes = []
        for i in range(self.header.num_planes):
            self._raw_planes.append(self._io.read_bytes(40))
            _io__raw_planes = KaitaiStream(BytesIO(self._raw_planes[i]))
            self.planes.append(LevDuke.PlaneT(_io__raw_planes, self, self._root))

        self._raw_vertices = []
        self.vertices = []
        for i in range(self.header.num_vertices):
            self._raw_vertices.append(self._io.read_bytes(8))
            _io__raw_vertices = KaitaiStream(BytesIO(self._raw_vertices[i]))
            self.vertices.append(LevDuke.VertexT(_io__raw_vertices, self, self._root))


    class Unknown02T(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_blocks = self._io.read_u4be()
            self.blocks = []
            for i in range(self.num_blocks):
                self.blocks.append(LevDuke.Unknown02BlockT(self._io, self, self._root))



    class VertexT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.coords = []
            for i in range(3):
                self.coords.append(self._io.read_u2be())



    class HeaderT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unknown_01 = self._io.read_u2be()
            self.unknown_02 = self._io.read_u2be()
            self.num_sectors = self._io.read_u4be()
            self.num_planes = self._io.read_u4be()
            self.num_vertices = self._io.read_u4be()
            self.data = self._io.read_bytes(40)


    class PaletteEntryT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.a = self._io.read_bits_int_be(1) != 0
            self.b = self._io.read_bits_int_be(5)
            self.g = self._io.read_bits_int_be(5)
            self.r = self._io.read_bits_int_be(5)


    class Unknown02BlockT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.len_data = self._io.read_u4be()
            self.data = self._io.read_bytes(self.len_data)


    class PlaneT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.vertex_indices = []
            for i in range(4):
                self.vertex_indices.append(self._io.read_u2be())



    class SkyDataT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.palette = []
            for i in range(256):
                self.palette.append(LevDuke.PaletteEntryT(self._io, self, self._root))

            self.width = self._io.read_s4be()
            self.height = self._io.read_s4be()
            self.bitmap = []
            for i in range((self.width * self.height)):
                self.bitmap.append(self._io.read_bits_int_be(8))




