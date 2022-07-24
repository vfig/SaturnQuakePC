# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Qslev(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self._raw_skydata = self._io.read_bytes(131104)
        _io__raw_skydata = KaitaiStream(BytesIO(self._raw_skydata))
        self.skydata = Qslev.SkyheaderT(_io__raw_skydata, self, self._root)
        self.header = Qslev.HeaderT(self._io, self, self._root)
        self.nodes = []
        for i in range(self.header.nodecount):
            self.nodes.append(Qslev.NodeT(self._io, self, self._root))

        self.planes = []
        for i in range(self.header.planecount):
            self.planes.append(Qslev.PlaneT(self._io, self, self._root))

        self.tiles = []
        for i in range(self.header.tileentrycount):
            self.tiles.append(Qslev.TileT(self._io, self, self._root))

        self.verts = []
        for i in range(self.header.vertcount):
            self.verts.append(Qslev.VertT(self._io, self, self._root))

        self.quads = []
        for i in range(self.header.quadcount):
            self.quads.append(Qslev.QuadT(self._io, self, self._root))

        self.entities = []
        for i in range(self.header.entitycount):
            self.entities.append(Qslev.EntityT(i, self._io, self, self._root))

        self.entitypolylinks = []
        for i in range(self.header.entitypolylinkcount):
            self.entitypolylinks.append(Qslev.EntitypolylinkT(self._io, self, self._root))

        self._raw_entitypolylinkdata1 = self._io.read_bytes((self.header.entitypolylinkdata1count * 2))
        _io__raw_entitypolylinkdata1 = KaitaiStream(BytesIO(self._raw_entitypolylinkdata1))
        self.entitypolylinkdata1 = Qslev.Entitypolylinkdata1T(_io__raw_entitypolylinkdata1, self, self._root)
        self._raw_entitypolylinkdata2 = self._io.read_bytes((self.header.entitypolylinkdata2count * 4))
        _io__raw_entitypolylinkdata2 = KaitaiStream(BytesIO(self._raw_entitypolylinkdata2))
        self.entitypolylinkdata2 = Qslev.Entitypolylinkdata2T(_io__raw_entitypolylinkdata2, self, self._root)
        self._raw_entitydata = self._io.read_bytes(self.header.entitydatasize)
        _io__raw_entitydata = KaitaiStream(BytesIO(self._raw_entitydata))
        self.entitydata = Qslev.Entitydata(_io__raw_entitydata, self, self._root)
        self._raw_tiletexturedata = self._io.read_bytes(self.header.tiletexturedatasize)
        _io__raw_tiletexturedata = KaitaiStream(BytesIO(self._raw_tiletexturedata))
        self.tiletexturedata = Qslev.TiletexturedataT(_io__raw_tiletexturedata, self, self._root)
        self._raw_tilecolordata = self._io.read_bytes(self.header.tilecolordatasize)
        _io__raw_tilecolordata = KaitaiStream(BytesIO(self._raw_tilecolordata))
        self.tilecolordata = Qslev.TilecolordataT(_io__raw_tilecolordata, self, self._root)
        self.unknown = []
        for i in range(self.header.unknowncount):
            self.unknown.append(self._io.read_bytes(128))

        self.tabledata1 = Qslev.Tabledata1T(self._io, self, self._root)
        self.global_palette = Qslev.GlobalPaletteT(self._io, self, self._root)
        self.texturedata = Qslev.TexturedataT(self._io, self, self._root)

    class Ent12(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = []
            for i in range(12):
                self.data.append(self._io.read_s1())



    class GlobalPaletteT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.len_block = self._io.read_u4be()
            self.color = []
            for i in range(self.len_block // 2):
                self.color.append(Qslev.PaletteEntryT(self._io, self, self._root))



    class VertT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.position = Qslev.Vec3s2(self._io, self, self._root)
            self.colorvalue = self._io.read_u1()
            self.none = self._io.read_u1()


    class Vec3s4(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.x = self._io.read_s4be()
            self.y = self._io.read_s4be()
            self.z = self._io.read_s4be()


    class Vec2u2(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.x = self._io.read_u2be()
            self.y = self._io.read_u2be()


    class TiletexturedataT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = self._io.read_bytes(self._parent.header.tiletexturedatasize)


    class Entitypolylinkdata2SingleT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            if self._root.header.entitypolylinkdata2count != 0:
                self.data = []
                for i in range(4):
                    self.data.append(self._io.read_u1())




    class Ent42(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = []
            for i in range(42):
                self.data.append(self._io.read_s1())



    class Entitydata(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = self._io.read_bytes(self._parent.header.entitydatasize)


    class EntitypolylinkT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.lead = self._io.read_u2be()
            self.data1offset = Qslev.Vec2u2(self._io, self, self._root)
            self.data2offset = Qslev.Vec2u2(self._io, self, self._root)
            self.value4 = self._io.read_u2be()
            self.reserved = Qslev.Vec3u2(self._io, self, self._root)

        @property
        def getdata1(self):
            if hasattr(self, '_m_getdata1'):
                return self._m_getdata1

            io = self._root.entitypolylinkdata1._io
            _pos = io.pos()
            io.seek((self.data1offset.x * 2))
            self._m_getdata1 = []
            for i in range((((self.data1offset.y - self.data1offset.x) + 1) * 2)):
                self._m_getdata1.append(io.read_u1())

            io.seek(_pos)
            return getattr(self, '_m_getdata1', None)

        @property
        def getdata2(self):
            if hasattr(self, '_m_getdata2'):
                return self._m_getdata2

            io = self._root.entitypolylinkdata2._io
            _pos = io.pos()
            io.seek((self.data2offset.x * 4))
            self._m_getdata2 = []
            for i in range((((self.data2offset.y - self.data2offset.x) + 1) * 4)):
                self._m_getdata2.append(io.read_u1())

            io.seek(_pos)
            return getattr(self, '_m_getdata2', None)


    class EntPlaceholder(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = self._io.read_s1()


    class Vec6u2(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.a = self._io.read_u2be()
            self.b = self._io.read_u2be()
            self.c = self._io.read_u2be()
            self.x = self._io.read_u2be()
            self.y = self._io.read_u2be()
            self.z = self._io.read_u2be()


    class Entitypolylinkdata1T(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = []
            i = 0
            while not self._io.is_eof():
                self.data.append(self._io.read_u1())
                i += 1



    class EntityT(KaitaiStruct):
        def __init__(self, x, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.x = x
            self._read()

        def _read(self):
            self.enttype = self._io.read_u2be()
            self.dataofs = self._io.read_u2be()

        @property
        def getentitydata(self):
            if hasattr(self, '_m_getentitydata'):
                return self._m_getentitydata

            if self.dataofs < self._root.header.entitydatasize:
                io = self._root.entitydata._io
                _pos = io.pos()
                io.seek(self.dataofs)
                _on = self.enttype
                if _on == 146:
                    self._m_getentitydata = Qslev.EntityPolymoverT(io, self, self._root)
                else:
                    self._m_getentitydata = Qslev.EntityDatablockT(io, self, self._root)
                io.seek(_pos)

            return getattr(self, '_m_getentitydata', None)


    class Tabledata1block(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.len_block = self._io.read_s4be()
            self.attr2 = self._io.read_s4be()
            self.attr3 = self._io.read_s4be()
            self.attr4 = self._io.read_s4be()
            self.block = self._io.read_bytes(self.len_block)


    class Vec3u2(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.x = self._io.read_u2be()
            self.y = self._io.read_u2be()
            self.z = self._io.read_u2be()


    class Ent1614(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = []
            for i in range(1614):
                self.data.append(self._io.read_s1())



    class HeaderT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unknown1 = self._io.read_u4be()
            self.unknown2 = self._io.read_u4be()
            self.nodecount = self._io.read_u4be()
            self.planecount = self._io.read_u4be()
            self.vertcount = self._io.read_u4be()
            self.quadcount = self._io.read_u4be()
            self.tiletexturedatasize = self._io.read_u4be()
            self.tileentrycount = self._io.read_u4be()
            self.tilecolordatasize = self._io.read_u4be()
            self.entitycount = self._io.read_u4be()
            self.entitydatasize = self._io.read_u4be()
            self.entitypolylinkcount = self._io.read_u4be()
            self.entitypolylinkdata1count = self._io.read_u4be()
            self.entitypolylinkdata2count = self._io.read_u4be()
            self.unknowncount = self._io.read_u4be()


    class Ent6(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = []
            for i in range(6):
                self.data.append(self._io.read_s1())



    class Entitypolylinkdata2T(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = []
            i = 0
            while not self._io.is_eof():
                self.data.append(self._io.read_u1())
                i += 1



    class EntityPolymoverT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.polylink_id = self._io.read_s2be()
            self.data = []
            for i in range(20):
                self.data.append(self._io.read_s2be())



    class Ent24(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = []
            for i in range(24):
                self.data.append(self._io.read_s1())



    class QuadT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.indices = Qslev.Vec4u1(self._io, self, self._root)
            self.textureindex = self._io.read_u1()


    class TextureT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.flags = self._io.read_u1()
            self.type = self._io.read_u1()
            self.palette = []
            for i in range(16):
                self.palette.append(Qslev.PaletteEntryT(self._io, self, self._root))

            self.imagedata = []
            for i in range(4096):
                self.imagedata.append(self._io.read_bits_int_be(4))



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


    class EntityDatablockT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.lead = self._io.read_s2be()
            self.origin = Qslev.Vec3s2(self._io, self, self._root)


    class Tilesubvector(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.x = self._io.read_s4be()
            self.y = self._io.read_s4be()
            self.z = self._io.read_s4be()


    class Vec4u2(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.x = self._io.read_u2be()
            self.y = self._io.read_u2be()
            self.z = self._io.read_u2be()
            self.a = self._io.read_u2be()


    class Tabledata1prefixblock(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_values = self._io.read_u4be()
            self.values = []
            for i in range(self.num_values):
                self.values.append(self._io.read_s2be())



    class Ent10(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = []
            for i in range(10):
                self.data.append(self._io.read_s1())



    class SkyheaderT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.skypalette = []
            for i in range(16):
                self.skypalette.append(Qslev.PaletteEntryT(self._io, self, self._root))

            self.skyimagedata = []
            for i in range(64):
                self.skyimagedata.append(Qslev.SkyimageentryT(self._io, self, self._root))



    class EntNull(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            pass


    class Vec4u1(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.x = self._io.read_u1()
            self.y = self._io.read_u1()
            self.z = self._io.read_u1()
            self.a = self._io.read_u1()


    class Vec4s2(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.x = self._io.read_s2be()
            self.y = self._io.read_s2be()
            self.z = self._io.read_s2be()
            self.a = self._io.read_s2be()


    class Tabledata1T(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.prefixblock = Qslev.Tabledata1prefixblock(self._io, self, self._root)
            self.num_block = self._io.read_s4be()
            self.block = []
            for i in range(self.num_block):
                self.block.append(Qslev.Tabledata1block(self._io, self, self._root))



    class Ent18(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = []
            for i in range(18):
                self.data.append(self._io.read_s1())



    class TileT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.texturedataofs = self._io.read_u2be()
            self.width = self._io.read_u1()
            self.height = self._io.read_u1()
            self.colordataofs = self._io.read_u2be()
            self.unknown = self._io.read_u2be()
            self.tilehorizvec = Qslev.Vec3s4(self._io, self, self._root)
            self.tilevertvec = Qslev.Vec3s4(self._io, self, self._root)
            self.tilebasevec = Qslev.Vec3s4(self._io, self, self._root)

        @property
        def getcolordata(self):
            if hasattr(self, '_m_getcolordata'):
                return self._m_getcolordata

            io = self._root.tilecolordata._io
            _pos = io.pos()
            io.seek(self.colordataofs)
            self._m_getcolordata = []
            for i in range(((self.width + 1) * (self.height + 1))):
                self._m_getcolordata.append(io.read_u1())

            io.seek(_pos)
            return getattr(self, '_m_getcolordata', None)

        @property
        def gettiletexturedata(self):
            if hasattr(self, '_m_gettiletexturedata'):
                return self._m_gettiletexturedata

            io = self._root.tiletexturedata._io
            _pos = io.pos()
            io.seek(self.texturedataofs)
            self._m_gettiletexturedata = []
            for i in range(((self.height * self.width) * 2)):
                self._m_gettiletexturedata.append(io.read_u1())

            io.seek(_pos)
            return getattr(self, '_m_gettiletexturedata', None)


    class SkyimageentryT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.image = self._io.read_bytes(2048)


    class Ent1656(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = []
            for i in range(1656):
                self.data.append(self._io.read_s1())



    class Entitypolylinkdata1SingleT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            if self._root.header.entitypolylinkdata1count != 0:
                self.data = []
                for i in range(2):
                    self.data.append(self._io.read_u1())




    class NodeT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.resv = Qslev.Vec2u2(self._io, self, self._root)
            self.pos = Qslev.Vec3u2(self._io, self, self._root)
            self.distance = self._io.read_u2be()
            self.firstplane = self._io.read_u2be()
            self.lastplane = self._io.read_u2be()
            self.unknown = Qslev.Vec6u2(self._io, self, self._root)


    class PlaneT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.vertices = Qslev.Vec4u2(self._io, self, self._root)
            self.nodeindex = self._io.read_u2be()
            self.flags = self._io.read_u2be()
            self.collisionflags = self._io.read_u2be()
            self.tileindex = self._io.read_u2be()
            self.unknownindex = self._io.read_u2be()
            self.quadstartindex = self._io.read_u2be()
            self.quadendindex = self._io.read_u2be()
            self.vertstartindex = self._io.read_u2be()
            self.vertendindex = self._io.read_u2be()
            self.plane = Qslev.Vec4s2(self._io, self, self._root)
            self.angle = self._io.read_s2be()
            self.resv = Qslev.Vec2u2(self._io, self, self._root)


    class TexturedataT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.count = self._io.read_u4be()
            self.textures = []
            i = 0
            while True:
                _ = Qslev.TextureT(self._io, self, self._root)
                self.textures.append(_)
                if _.type != 130:
                    break
                i += 1


    class TilecolordataT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = self._io.read_bytes(self._parent.header.tilecolordatasize)


    class Vec3s2(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.x = self._io.read_s2be()
            self.y = self._io.read_s2be()
            self.z = self._io.read_s2be()



