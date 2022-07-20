# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Powerslavelev(KaitaiStruct):
    """PowerSlave (Sega Saturn) Level Format (.lev).
    
    .. seealso::
       Source - https://github.com/ReyeMe/Saturn-Powerslave-map-viewer/blob/master/Powerslave.cs
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.skydata = Powerslavelev.SkydataT(self._io, self, self._root)
        self.unknown01 = self._io.read_bytes(1292)
        self.header = Powerslavelev.HeaderT(self._io, self, self._root)
        self.sectors = []
        for i in range(self.header.sectorcount):
            self.sectors.append(Powerslavelev.SectorT(self._io, self, self._root))

        self.planes = []
        for i in range(self.header.planecount):
            self.planes.append(Powerslavelev.PlaneT(self._io, self, self._root))

        self.vertices = []
        for i in range(self.header.vertexcount):
            self.vertices.append(Powerslavelev.VertexT(self._io, self, self._root))

        self.quads = []
        for i in range(self.header.quadcount):
            self.quads.append(Powerslavelev.QuadT(self._io, self, self._root))


    class SectorT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unknown01 = self._io.read_s2be()
            self.unknown02 = self._io.read_s2be()
            self.ceilingslope = self._io.read_s2be()
            self.floorslope = self._io.read_s2be()
            self.ceilingheight = self._io.read_s2be()
            self.floorheight = self._io.read_s2be()
            self.planes = []
            for i in range(2):
                self.planes.append(self._io.read_s2be())

            self.unknown03 = self._io.read_u2be()
            self.flags = self._io.read_u2be()
            self.unknown04 = self._io.read_s2be()
            self.unknown05 = self._io.read_s2be()


    class VertexT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.coords = []
            for i in range(3):
                self.coords.append(self._io.read_s2be())

            self.lightlevel = self._io.read_bits_int_be(8)
            self.unknown01 = self._io.read_bits_int_be(8)


    class HeaderT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.sectorcount = self._io.read_u4be()
            self.planecount = self._io.read_u4be()
            self.vertexcount = self._io.read_u4be()
            self.quadcount = self._io.read_u4be()
            self.unknown01 = self._io.read_u4be()
            self.unknown02 = self._io.read_u4be()
            self.unknown03 = self._io.read_u4be()
            self.unknown04 = self._io.read_u4be()
            self.unknown05 = self._io.read_u4be()
            self.unknown06 = self._io.read_u4be()
            self.unknown07 = self._io.read_u4be()
            self.unknown08 = self._io.read_u4be()
            self.unknown09 = self._io.read_u4be()
            self.unknown010 = self._io.read_u4be()


    class QuadT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.indices = []
            for i in range(4):
                self.indices.append(self._io.read_u2be())

            self.unknown01 = self._io.read_bits_int_be(8)
            self.unknown02 = self._io.read_bits_int_be(8)


    class SkydataT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.palette = []
            for i in range(256):
                self.palette.append(Powerslavelev.PaletteentryT(self._io, self, self._root))

            self.skyimage = []
            for i in range((512 * 256)):
                self.skyimage.append(self._io.read_bits_int_be(8))



    class PlaneT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.normal = []
            for i in range(3):
                self.normal.append(self._io.read_s4be())

            self.angle = self._io.read_s4be()
            self.unknown01 = self._io.read_s2be()
            self.unknown02 = self._io.read_s2be()
            self.flags = self._io.read_u2be()
            self.textureid = self._io.read_u2be()
            self.quadoffsets = []
            for i in range(2):
                self.quadoffsets.append(self._io.read_s2be())

            self.vertexoffsets = []
            for i in range(2):
                self.vertexoffsets.append(self._io.read_u2be())

            self.vertices = []
            for i in range(4):
                self.vertices.append(self._io.read_u2be())

            self.unknown03 = self._io.read_s2be()
            self.lookup = self._io.read_u2be()
            self.unknown04 = self._io.read_s2be()
            self.unknown05 = self._io.read_s2be()


    class PaletteentryT(KaitaiStruct):
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



