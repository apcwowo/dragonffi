from enum import Enum
from purectypes.types import Visitor,StructTy,Field,EnumTy

class Dumper(Visitor):
    def __init__(self):
        self._types = {}
        self._names = set()
        self._output = list()
        self._needed_types = set()

    def visit(self, ty):
        ret = self._types.get(ty, None)
        if not ret is None:
            return ret
        expr = super(Dumper, self).visit(ty)
        expr = "%s(%s,%s)" % (type(ty).__name__,expr,self.base_args(ty))
        name = ty.name
        if name is None:
            name = "_anon"
        name_org = name
        i = 0
        while name in self._names:
            name = name_org + "_%d" % i
            i += 1
        self._names.add(name)
        self._output.append((name, expr))
        self._types[ty] = name
        self._needed_types.add(type(ty))
        if isinstance(ty, StructTy):
            self._needed_types.add(Field)
        if isinstance(ty, EnumTy):
            self._needed_types.add(Enum)
        return name

    @staticmethod
    def base_args(ty):
        return 'triple="%s",size=%d,align=%d' % (ty.triple,ty.size,ty.align)

    def visit_BasicTy(self, ty):
        return 'format_="%s"' % ty.format
    def visit_ArrayTy(self, ty):
        return 'elt_type=%s,elt_count=%d' % (self.visit(ty.elt_type),ty.elt_count)
    def visit_StructTy(self, ty):
        fields = ",".join('"%s": %s' % (fname, "Field(offset=%d,type_=%s)" % (field.offset, self.visit(field.type_))) for fname,field in ty.fields.items())
        return 'fields={%s},name="%s"' % (fields,ty.name)
    def visit_PointerTy(self, ty):
        return 'pointee=%s,ptr_format="%s"' % (self.visit(ty.pointee), ty.ptr_format)
    def visit_EnumTy(self, ty):
        return 'format_="%s",enum=Enum("%s", {%s})' % (ty.format, ty.name, ",".join('"%s": %d' % (v.name,v.value) for v in ty.enum))
    def visit_UnionTy(self, ty):
        return 'types={%s}' % ','.join('"%s": %s' % (name, self.visit(attrty)) for name,attrty in ty.types.items())
    def visit_FunctionTy(self, ty):
        return 'ret=%s,args=(%s,),varargs=%s' % (self.visit(ty.ret), ",".join(self.visit(a) for a in ty.args), str(ty.varargs))

    def __str__(self):
        ret = "from collections import namedtuple\n"
        try:
            self._needed_types.remove(Enum)
            ret += "from enum import Enum\n"
        except KeyError: pass
        ret += "from purectypes.types import %s\n" % ",".join(ty.__name__ for ty in self._needed_types)
        ret += "\n".join("%s = %s" % (name,expr) for name,expr in self._output)
        return ret

def dump(ty, data):
    return Dumper().visit(ty)
