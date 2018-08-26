from enum import Enum
import pydffi
from purectypes.types import BasicTy,ArrayTy,StructTy,PointerTy,Field,EnumTy,UnionTy,FunctionTy,VoidTy

class GenPureCType:
    def __init__(self):
        self._types = {}
        self._anon_id = 0
        self._triple = pydffi.native_triple()

    def __call__(self, Ty):
        if isinstance(Ty, pydffi.QualType):
            return self(Ty.type)
        ret = self._types.get(Ty, None)
        if not ret is None:
            return ret

        name = None
        if Ty is None:
            # void
            ret = VoidTy()
            self._types[None] = ret
            return ret
        if isinstance(Ty, pydffi.BasicType):
            ret = BasicTy(Ty.portable_format)
            print(Ty,Ty.kind,str(Ty.kind))
            name = str(Ty.kind).split(".")[1] + "Ty"
        elif isinstance(Ty, pydffi.StructType):
            name = Ty.name
            fields = {}
            for f in Ty.fields:
                fields[f.name] = Field(offset=f.offset, type_=self(f.type))
            ret = StructTy(fields)
        elif isinstance(Ty, pydffi.ArrayType):
            ret = ArrayTy(self(Ty.elementType()), len(Ty()))
        elif isinstance(Ty, pydffi.PointerType):
            ret = PointerTy(self(Ty.pointee()), Ty.portable_format)
        elif isinstance(Ty, pydffi.EnumType):
            name = "_enum_%d" % self._anon_id
            self._anon_id += 1
            ret = EnumTy(pydffi.portable_format(Ty), Enum(name, dict(Ty)))
        elif isinstance(Ty, pydffi.UnionType):
            types = {t.name: self(t.type) for t in Ty}
            ret = UnionTy(types)
        elif isinstance(Ty, pydffi.FunctionType):
            ret = FunctionTy(self(Ty.returnType), tuple(self(a) for a in Ty.params), Ty.varArgs)
        else:
            raise ValueError("unsupported type %s" % repr(Ty))
        ret._triple = self._triple
        ret._size = Ty.size
        ret._align = Ty.align
        ret._name = name
        self._types[Ty] = ret
        return ret
