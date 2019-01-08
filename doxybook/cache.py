from doxybook.node import Node

class Cache:
    def __init__(self):
        self.cache = {}

    def add(self, refid: str, value: Node):
        self.cache[refid] = value

    def get(self, refid: str) -> Node:
        # For some reason, inside compounddef of a group, the id follows the following shorter format:
        # group__console_1ga0a2f84ed7838f07779ae24c5a9086d33 instead of the usual longer format:
        # group__console_ga0a2f84ed7838f07779ae24c5a9086d33_1ga0a2f84ed7838f07779ae24c5a9086d33
        # There might be another occurence similar to this that's not observed yet, so to make it generic
        # we make the cache get function check both of the cases
        # Here, we are going to convert them, so we can find the node inside the cache
        refid_tail = refid.split('_')[-1]
        if refid.count(refid_tail[1:]) == 1:
            refid_tail_index = refid.find(refid_tail)
            long_refid = refid[:refid_tail_index] + refid_tail[1:] + '_' + refid_tail
        else:
            long_refid = refid

        if refid in self.cache:
            return self.cache[refid]
        elif long_refid in self.cache:
            return self.cache[long_refid]
        else:
            raise IndexError('Refid: ' + refid + ' not found in cache!')