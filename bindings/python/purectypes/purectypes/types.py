from collections import namedtuple
Field = namedtuple("Field", ['offset','type_'])

class TyBase:
    _triple = None
    _size = 0
    _align = 0

    @property
    def size(self): return self._size

    @property
    def triple(self): return self._triple

    @property
    def align(self): return self._align

class StructTy(TyBase):
    def __init__(self, fields, name):
        self._fields = fields
        self._name = name

    @property
    def fields(self):
        return self._fields
    @property
    def name(self):
        return self._name

    def __repr__(self):
        return "%s: %s" % (self.name, repr(self.fields))

class BasicTy(TyBase):
    def __init__(self, format_):
        self._format = format_

    @property
    def format(self):
        return self._format

    def __repr__(self):
        return self.format

class PointerTy(TyBase):
    def __init__(self, pointee):
        self._pointee = pointee

    @property
    def pointee(self):
        return self._pointee

    def __repr__(self):
        return "%s*" % repr(self.pointee)

class ArrayTy(TyBase):
    _elt_type = None
    _elt_count = 0

    def __init__(self, elt_type, elt_count):
        self._elt_type = elt_type
        self._elt_count = elt_count

    @property
    def elt_type(self): return self._elt_type

    @property
    def elt_count(self): return self._elt_count

    def __repr__(self):
        return repr(self.elt_type)+"[%d]" % self.elt_count

class UnionTy(TyBase):
    def __init__(self, types):
        self._types = types

    @property
    def types(self): return self._types

class Visitor:
    def visit(self, Ty):
        name = type(Ty).__name__
        func = "visit_%s" % name
        func = getattr(self, func)
        return func(Ty)
