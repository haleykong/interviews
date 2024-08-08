class HierarchicalDict(dict):
    """Dictionary that supports accessing members as attributes"""
    def __init__(self, data):
        super().__init__({key: (HierarchicalDict(value) if isinstance(value, dict) else
                              value) for key, value in data.items()})
   
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as e:
            raise AttributeError(str(e))
           
    def __setattr__(self, name, value):
        if name not in self:
            raise AttributeError('Cannot add new member')
        elif isinstance(self[name], HierarchicalDict):
            raise AttributeError(f"Cannot assign to child dictionary '{name}'")
        else:
            self[name] = value
            

    def _print(self, level=0):
        printstr = ''
        for k, v in self.items():
            if isinstance(v, dict):
                printstr += '\n' + ' ' * level * 2 + f'- {k}'
                printstr += v._print(level=level+1)
            else:
                printstr += '\n' + ' ' * level * 2 + f'- {k}: {str(v)}'
        return printstr
               
    def __repr__(self):
        repstr = '-' * 79 + '\nConfiguration Summary\n'
        repstr +=  self._print()
        return repstr
           

a = {'b': 2, 'c': {'e': 3, 'f': 4}}

config = HierarchicalDict(a)


import yaml

with open('base.yml', 'r') as file:
    data = yaml.safe_load(file)

print(data)
           
config2 = HierarchicalDict(data)

