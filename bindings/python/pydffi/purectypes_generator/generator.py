import pydffi
from purectypes.types import BasicTy,ArrayTy,StructTy,PointerTy

class GenPureCType:
    def __init__(self):
        self._types = {}
        self._anon_id = 0

    def __call__(self, Ty):
        if isinstance(Ty, pydffi.QualType):
            return self(Ty.type)
        ret = self._types.get(Ty, None)
        if not ret is None:
            return ret

        if isinstance(Ty, pydffi.BasicType):
            ret = BasicTy(Ty.portable_format)
        elif isinstance(Ty, pydffi.StructType):
            name = Ty.name
            if name is None:
                name = "pydffi_anon_%d" % anon_id
                self._anon_id += 1
            fields = {}
            for f in Ty.fields:
                fields[f.name] = Field(offset=f.offset, type_=self(f.type))
            ret = StructTy(fields, name)
        elif isinstance(Ty, pydffi.ArrayType):
            ret = ArrayTy(self(Ty.elementType()), len(Ty()))
        elif isinstance(Ty, pydffi.PointerType):
            ret = PointerTy(self(Ty.pointee()))
        else:
            print(Ty)
            fds
        ret._triple = "todo"
        ret._size = Ty.size
        ret._align = Ty.align
        self._types[Ty] = ret
        return ret
