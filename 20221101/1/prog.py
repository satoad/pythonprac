class Omnibus:
    def __getattr__(self, item):
        if not item.startswith('_'):
