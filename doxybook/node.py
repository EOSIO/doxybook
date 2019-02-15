from doxybook.kind import Kind
from doxybook.utils import mangle_name
from doxybook.config import config
from doxybook.refid import normalize_refid
import re

class Node:
    def __init__(self, name: str, refid: str, kind: str):
        if not isinstance(kind, Kind):
            raise TypeError('kind must be an instance of Kind Enum, got: ' + kind)

        self.name = name
        self.refid = refid
        self.kind = kind
        self.parent = None
        self.members = []
        self.url = None
        self.overloaded = False
        self.overload_num = 1
        self.overload_total = 1

    def get_full_name(self, include_namespace: bool = False) -> str:
        ret = self.name
        namespace_check = True
        if self.parent is not None and self.parent.kind == Kind.NAMESPACE and include_namespace == False:
            namespace_check = False
        if self.parent is not None and self.parent.kind != Kind.ROOT and namespace_check:
            ret = self.parent.get_full_name(include_namespace) + '::' + ret
        return ret

    def get_namespace(self) -> 'Node':
        if self.kind == Kind.ROOT:
            return None
        elif self.kind == Kind.NAMESPACE:
            return self
        else:
            return self.parent.get_namespace()

    def add_member(self, member: 'Node'):
        member.parent = self
        self.members.append(member)

    def find_member(self, name: str) -> 'Node':
        for child in self.members:
            if(child.name == name):
                return child

        return None

    def get_anchor_hash(self, prefix = None):
        if config.target == 'gitbook':
            return self.refid[-34:]

        if prefix is None:
            prefix = self.kind.value

        anchor = prefix + '-' + self.name if len(prefix) > 0 else self.name
        if self.overloaded:
            anchor = anchor + '-' + str(self.overload_num) + str(self.overload_total)

        # Reference to https://github.com/Flet/github-slugger/blob/master/index.js
        # Change anchor to github flavored anchor
        anchor = re.sub(r'[\u2000-\u206F\u2E00-\u2E7F\'!"#$%&()*+,./:;<=>?@[\]^`{|}~]', '', anchor)
        anchor = re.sub(r'\s', '-', anchor)
        anchor = anchor.lower()

        return anchor

    def get_kind_str(self):
        return self.kind.value

    def generate_url(self) -> str:
        normalized_refid = normalize_refid(self.refid)
        url = normalized_refid + '.md'
        if not self.kind.is_parent():
            url += '#' + self.get_anchor_hash()
        return url

    def finalize(self):
        self.url = self.generate_url()
