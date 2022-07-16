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
            self.entitypolylinks.append(self._io.read_bytes(18))

        self.entitypolylinkdata1 = []
        for i in range(self.header.entitypolylinkdata1count):
            self.entitypolylinkdata1.append(self._io.read_bytes(2))

        self.entitypolylinkdata2 = []
        for i in range(self.header.entitypolylinkdata2count):
            self.entitypolylinkdata2.append(self._io.read_bytes(4))

        self._raw_entitydata = self._io.read_bytes(self.header.entitydatasize)
        _io__raw_entitydata = KaitaiStream(BytesIO(self._raw_entitydata))
        self.entitydata = Qslev.Entitydata(_io__raw_entitydata, self, self._root)
        self.tiletexturedata = self._io.read_bytes(self.header.tiletexturedatasize)
        self._raw_tilecolordata = self._io.read_bytes(self.header.tilecolordatasize)
        _io__raw_tilecolordata = KaitaiStream(BytesIO(self._raw_tilecolordata))
        self.tilecolordata = Qslev.Tilecolordata(_io__raw_tilecolordata, self, self._root)
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



    class Tilecolordata(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.data = self._io.read_bytes(self._parent.header.tilecolordatasize)


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
                self.color.append(self._io.read_u2be())



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

            io = self._root.entitydata._io
            _pos = io.pos()
            io.seek(self.dataofs)
            _on = self.enttype
            if _on == 131:
                self._m_getentitydata = Qslev.Ent12(io, self, self._root)
            elif _on == 146:
                self._m_getentitydata = Qslev.Ent42(io, self, self._root)
            elif _on == 46:
                self._m_getentitydata = Qslev.Ent12(io, self, self._root)
            elif _on == 113:
                self._m_getentitydata = Qslev.Ent12(io, self, self._root)
            elif _on == 13:
                self._m_getentitydata = Qslev.Ent10(io, self, self._root)
            elif _on == 149:
                self._m_getentitydata = Qslev.Ent18(io, self, self._root)
            elif _on == 143:
                self._m_getentitydata = Qslev.Ent12(io, self, self._root)
            elif _on == 125:
                self._m_getentitydata = Qslev.Ent12(io, self, self._root)
            elif _on == 38:
                self._m_getentitydata = Qslev.Ent24(io, self, self._root)
            elif _on == 148:
                self._m_getentitydata = Qslev.Ent18(io, self, self._root)
            elif _on == 130:
                self._m_getentitydata = Qslev.Ent12(io, self, self._root)
            elif _on == 232:
                self._m_getentitydata = Qslev.Ent1656(io, self, self._root)
            elif _on == 164:
                self._m_getentitydata = Qslev.Ent10(io, self, self._root)
            elif _on == 28:
                self._m_getentitydata = Qslev.Ent12(io, self, self._root)
            elif _on == 74:
                self._m_getentitydata = Qslev.Ent12(io, self, self._root)
            elif _on == 147:
                self._m_getentitydata = Qslev.Ent12(io, self, self._root)
            elif _on == 92:
                self._m_getentitydata = Qslev.Ent6(io, self, self._root)
            elif _on == 111:
                self._m_getentitydata = Qslev.Ent12(io, self, self._root)
            elif _on == 128:
                self._m_getentitydata = Qslev.Ent12(io, self, self._root)
            elif _on == 254:
                self._m_getentitydata = Qslev.Ent12(io, self, self._root)
            elif _on == 154:
                self._m_getentitydata = Qslev.Ent18(io, self, self._root)
            else:
                self._m_getentitydata = Qslev.EntPlaceholder(io, self, self._root)
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
                self.palette.append(self._io.read_u2be())

            self.imagedata = []
            for i in range(2048):
                self.imagedata.append(self._io.read_u1())



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
                self.skypalette.append(Qslev.SkypaletteentryT(self._io, self, self._root))

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



    class SkypaletteentryT(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.r = self._io.read_bits_int_be(5)
            self.g = self._io.read_bits_int_be(5)
            self.b = self._io.read_bits_int_be(5)
            self.a = self._io.read_bits_int_be(1) != 0


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
            for i in range(58):
                self.textures.append(Qslev.TextureT(self._io, self, self._root))



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



