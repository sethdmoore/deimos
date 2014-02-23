class _OpenHolder(object):
    def __init__(self, **properties):
        self.__dict__.update(properties)
        self._properties = properties.keys()
    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)
    def keys(self):
        return self._properties

class CGroups(_OpenHolder):
    "Holder for a container's cgroups hierarchy."
    def __init__(self, **cgroups_path_mapping):
        properties = {}
        for k, v in cgroups_path_mapping.items():
            properties[k] = construct(v, k)
        _OpenHolder.__init__(self, **properties)

class CGroup(object):
    "A generic CGroup, allowing lookup of CGroup values as Python attributes."
    def __init__(self, path, name):
        self.path = path
        self.name = name
        self._cache = {}
    def __getattr__(self, key):
        path = self.path + "/" + self.name + "." + key
        with open(path) as h:
            data = h.read()
        return data
    def stat_data(self):
        return StatFile(self.stat)

def construct(path, name=None):
    "Selects an appropriate CGroup subclass for the given CGroup path."
    name = name if name else path.split("/")[-2]
    classes = { "memory"  : Memory,
                "cpu"     : CPU,
                "cpuacct" : CPUAcct }
    constructor = classes.get(name, CGroup)
    return constructor(path, name)

class Memory(CGroup):
    def rss(self):
        return int(self.stat_data().rss)
    def limit(self):
        return int(self.limit_in_bytes)

class CPU(CGroup):
    def limit(self):
        return float(self.shares) / 1024
        # The scale factor must be the same as for the Docker module. This
        # scale factor is the same as the Docker tools use by default. When a
        # task is started without any explicit CPU limit, the limit that shows
        # up in CGroups is 1024.

class CPUAcct(CGroup):
    def user_time(self):
        "Total user time for container in seconds."
        return float(self.stat_data().user) / 100
    def system_time(self):
        "Total system time for container in seconds."
        return float(self.stat_data().system) / 100

class StatFile(_OpenHolder):
    def __init__(self, data):
        kvs = [ line.strip().split(" ") for line in data.strip().split("\n") ]
        res = {}
        for kvs in kvs:
            if len(kvs) != 2: continue  # Silently skip lines that aren't pairs
            k, v = kvs
            res[k] = v
        _OpenHolder.__init__(self, **res)
