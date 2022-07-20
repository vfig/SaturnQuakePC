# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Dukelev(KaitaiStruct):
    """Duke Nukem 3D (Sega Saturn) Level Format (.lev)."""
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.skydata = Dukelev.SkydataT(self._io, self, self._root)
        self.header = Dukelev.HeaderT(self._io, self, self._root)

    class SkydataT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.palette = []
            for i in range(256):
                self.palette.append(Dukelev.PaletteentryT(self._io, self, self._root))

            self.skyimage = []
            for i in range((256 * 512)):
                self.skyimage.append(self._io.read_bits_int_be(8))



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



