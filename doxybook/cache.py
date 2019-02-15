from doxybook.node import Node
from doxybook.refid import normalize_refid

class Cache:
    def __init__(self):
        self.cache = {}

    def add(self, refid: str, value: Node):
        # Use normalized refid, check refid.py comments for reasoning
        normalized_refid = normalize_refid(refid)
        self.cache[normalized_refid] = value

    def get(self, refid: str) -> Node:
        # Use normalized refid, check refid.py comments for reasoning
        normalized_refid = normalize_refid(refid)
        if normalized_refid in self.cache:
            return self.cache[normalized_refid]
        else:
            raise IndexError('Refid: ' + refid + ' not found in cache!')