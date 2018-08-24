from pkg_resources import iter_entry_points
from collections import namedtuple

_gens = {ep.name[1:]: ep.load() for ep in iter_entry_points("purectypes.generators")}
generators = namedtuple("generators", list(_gens.keys()))(**_gens)
